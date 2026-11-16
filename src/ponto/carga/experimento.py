"""Experimento automatizado: rampa de carga + reconciliação + mapeamento de erros.

Para cada taxa (req/s) da rampa:
  1. gera uma base sintética nova, com gabarito;
  2. reinicia o banco e configura a API (modo, lote, retry);
  3. dispara a base na taxa escolhida (opcionalmente injetando falha);
  4. espera a fila esvaziar;
  5. lê o banco e reconcilia cada registro com o gabarito.

Saídas em resultados/<cenario>/:
  resumo.csv           uma linha por taxa (o que vai para o artigo)
  envios_<taxa>.csv    cada requisição: horário, latência, status
  erros_<taxa>.csv     cada registro que não terminou "correto", com categoria
  config.json          parâmetros do cenário

Exemplos:
  python -m ponto.carga.experimento --cenario lote_200 --modo lote --lote 200 --taxas 100,500,1000,2000
  python -m ponto.carga.experimento --suite padrao
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import time
from dataclasses import asdict, dataclass, field, replace
from itertools import takewhile
from pathlib import Path
from statistics import quantiles

import aiohttp
import asyncpg

from ..dados.gerador import gerar
from ..dados.reconciliacao import COMPONENTE, SUCESSO, reconciliar, resumir
from ..nucleo.modelos import Desfecho
from ..nucleo.validacao import regras_padrao
from .rampa import disparar

API = os.getenv("API_URL", "http://localhost:8000")
PERFIL_CPU = os.getenv("PERFIL_CPU", "livre")  # perfil de núcleos do compose (C15)
PROCESSOS = int(os.getenv("GERADOR_PROCESSOS", "1"))  # processos do gerador de carga (C12)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto")
ESPERA_REPETIR_S = 60  # > TIME_WAIT do Linux (60 s): as portas do degrau anterior voltam (C16)


@dataclass(frozen=True)
class Cenario:
    nome: str
    modo: str = "lote"
    lote: int = 200
    espera_ms: int = 100
    tentativas: int = 8
    # 1250, 1750 e 2500 (C17): o baseline satura entre 1000 e 1500 e o lote passou de 2000 mas
    # não de 3000 no experimento 1; com degraus de 500, diferenças entre implementações sumiam
    taxas: tuple[int, ...] = (100, 250, 500, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 6000)
    duracao: int = 20            # segundos de carga por degrau
    anomalias: float = 0.05
    seed: int = 42
    timeout: float = 5.0
    falha_em: float | None = None  # segundo do degrau em que o banco "cai"
    falha_seg: float = 10.0
    falha_tipo: str = "simulada"   # "simulada" (dentro da API) ou "real" (no Postgres, C17)
    parar_apos: int = 2          # para a rampa após N degraus seguidos com erro
    tolerancia: float = 1e-4     # taxa máxima de erro de integridade aceita no limite (C5)
    atraso_max_ms: float = 20.0  # acima disso o gerador não cumpriu a agenda: degrau inválido (C3)
    extra: dict = field(default_factory=dict)


# Cenários do artigo. Ajuste as taxas conforme a máquina.
# Falhas: com 8 tentativas o backoff acumula 16,2 s, então a queda de 10 s é coberta
# por construção; variar a duração mostra onde o retry deixa de bastar (C8).
SUITE_PADRAO = [
    Cenario("baseline", modo="baseline"),
    Cenario("lote_50", lote=50),
    Cenario("lote_200", lote=200),
    Cenario("lote_1000", lote=1000),
    Cenario("falha_com_retry", taxas=(500,), duracao=30, falha_em=5),
    Cenario("falha_sem_retry", taxas=(500,), duracao=30, falha_em=5, tentativas=1),
    Cenario("falha_com_retry_20s", taxas=(500,), duracao=45, falha_em=5, falha_seg=20.0),
    Cenario("falha_com_retry_30s", taxas=(500,), duracao=55, falha_em=5, falha_seg=30.0),
    # grupo de comparação: no baseline o cliente recebe 503 e sabe que deve reenviar (C7)
    Cenario("falha_baseline_com_retry", modo="baseline", taxas=(500,), duracao=30, falha_em=5),
    Cenario("falha_baseline_sem_retry", modo="baseline", taxas=(500,), duracao=30, falha_em=5, tentativas=1),
    # queda real (C17): o Postgres encerra as conexões da API e recusa novas por 10 s; valida a
    # falha simulada contra erros de verdade do driver (transação cortada, pool quebrado)
    Cenario("falha_real_com_retry", taxas=(500,), duracao=30, falha_em=5, falha_tipo="real"),
    Cenario("falha_real_sem_retry", taxas=(500,), duracao=30, falha_em=5, tentativas=1, falha_tipo="real"),
    Cenario("falha_real_baseline_sem_retry", modo="baseline", taxas=(500,), duracao=30, falha_em=5,
            tentativas=1, falha_tipo="real"),
]


def percentil(valores: list[float], p: int) -> float:
    if len(valores) < 2:
        return valores[0] if valores else 0.0
    return quantiles(valores, n=100, method="inclusive")[p - 1]


async def _admin(sessao, metodo, caminho, **kw):
    async with sessao.request(metodo, f"{API}{caminho}", **kw) as r:
        r.raise_for_status()
        return await r.json()


async def _esperar_fila(sessao, limite=300.0) -> tuple[dict, bool]:
    """Espera a API ficar ociosa. Devolve (estado, drenou); drenou=False se o
    limite estourou, e o degrau não pode ser usado (a fila ainda gravava)."""
    inicio = time.monotonic()
    while time.monotonic() - inicio < limite:
        estado = await _admin(sessao, "GET", "/admin/estado")
        if estado["ocioso"]:
            return estado, True
        await asyncio.sleep(0.5)
    estado = await _admin(sessao, "GET", "/admin/estado")
    return estado, bool(estado["ocioso"])


def _url_manutencao(url: str) -> tuple[str, str]:
    """(URL do banco `postgres`, nome do banco do experimento): a queda é comandada de fora dele."""
    base, _, nome = url.rpartition("/")
    return f"{base}/postgres", nome.split("?")[0]


async def abrir_banco() -> None:
    """Garante que o banco aceita conexões (uma queda real interrompida não pode vazar)."""
    url, nome = _url_manutencao(DATABASE_URL)
    conn = await asyncpg.connect(url)
    try:
        await conn.execute(f'ALTER DATABASE "{nome}" ALLOW_CONNECTIONS true')
    finally:
        await conn.close()


async def queda_real(segundos: float) -> None:
    """Queda real do banco por `segundos` (C17), sem precisar do Docker: recusa conexões novas
    (SQLSTATE 55000) e encerra as existentes (57P01, transações em curso abortadas). Volta
    sozinho no fim, mesmo se a tarefa for cancelada."""
    url, nome = _url_manutencao(DATABASE_URL)
    conn = await asyncpg.connect(url)
    try:
        await conn.execute(f'ALTER DATABASE "{nome}" ALLOW_CONNECTIONS false')
        await conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                           "WHERE datname = $1 AND pid <> pg_backend_pid()", nome)
        await asyncio.sleep(segundos)
    finally:
        await conn.execute(f'ALTER DATABASE "{nome}" ALLOW_CONNECTIONS true')
        await conn.close()


async def _ler_banco() -> dict[str, Desfecho]:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        linhas = await conn.fetch("SELECT id_evento::text, desfecho, motivo FROM eventos")
    finally:
        await conn.close()
    return {r["id_evento"]: Desfecho(r["id_evento"], r["desfecho"], r["motivo"]) for r in linhas}


def _escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    if not linhas:
        caminho.write_text("")
        return
    with caminho.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)


async def rodar_degrau(c: Cenario, taxa: int, pasta: Path) -> dict:
    n_servidores = max(50, int(taxa * c.duracao / 2.05))  # ~2,05 registros por servidor
    base = gerar(n_servidores, c.anomalias, seed=c.seed + taxa)
    registros = base.registros

    # force_close: sem keep-alive, a conexão de administração nunca fica velha
    if c.falha_tipo == "real":
        await abrir_banco()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as sessao:
        await _admin(sessao, "POST", "/admin/config", json={
            "modo": c.modo, "tamanho_lote": c.lote, "espera_ms": c.espera_ms, "tentativas": c.tentativas})
        # requisições atrasadas do degrau anterior não podem cair no banco novo
        _, drenou_antes = await _esperar_fila(sessao)
        # se não drenou, gravações antigas podem cair no banco novo: o degrau fica inválido
        await _admin(sessao, "POST", "/admin/reset", json={"servidores": n_servidores})
        # identifica o processo da API: se mudar até o fim, ela reiniciou no meio do degrau
        instancia_inicio = (await _admin(sessao, "GET", "/admin/estado")).get("instancia")

        eventos = {}
        if c.falha_em is not None and c.falha_tipo == "real":
            eventos[c.falha_em] = lambda: queda_real(c.falha_seg)
        elif c.falha_em is not None:
            eventos[c.falha_em] = lambda: _admin(sessao, "POST", "/admin/falha", params={"segundos": c.falha_seg})

        inicio = time.monotonic()
        envios = await disparar(registros, taxa, f"{API}/registros", c.timeout, eventos, processos=PROCESSOS)
        duracao_envio = time.monotonic() - inicio
        estado, drenou_depois = await _esperar_fila(sessao)
        drenou = drenou_antes and drenou_depois
        duracao_total = time.monotonic() - inicio

    banco = await _ler_banco()
    avaliacoes = reconciliar(registros, base.gabarito, envios, banco, regras_padrao(frozenset(range(1, n_servidores + 1))))

    lat_ok = [e.latencia for e in envios if e.status in SUCESSO]
    lat_todas = [e.latencia for e in envios]  # inclui timeouts e erros (C4)
    atrasos = [e.t_envio - e.t_agendado for e in envios]
    # taxa de ENVIO: até o último envio, sem esperar respostas (C2)
    ultimo_envio = max((e.t_envio for e in envios), default=0.0)
    atraso_p99 = round(percentil(atrasos, 99) * 1000, 1)
    contagens = resumir(avaliacoes)
    gerador_ok = atraso_p99 <= c.atraso_max_ms
    saturou = api_saturou(gerador_ok, contagens["erros_de_carga"], contagens["registros"])
    sem_reinicio = estado.get("instancia") == instancia_inicio
    resumo = {
        "cenario": c.nome,
        "seed": c.seed,
        "taxa_alvo": taxa,
        "processos_gerador": PROCESSOS,
        "perfil_cpu": PERFIL_CPU,
        "taxa_obtida": round(len(envios) / ultimo_envio, 1) if ultimo_envio else 0.0,
        "atraso_gerador_p99_ms": atraso_p99,
        "gerador_valido": gerador_ok,
        # o gerador atrasou porque a API já tinha saturado: degrau válido e reprovado (C17)
        "api_saturou": saturou,
        # o degrau só vale se a fila drenou e a API não reiniciou (perderia fila, contadores e config)
        "drenou": drenou,
        "api_sem_reinicio": sem_reinicio,
        "degrau_valido": (gerador_ok or saturou) and drenou and sem_reinicio,
        "incidente": descrever_incidente(gerador_ok or saturou, drenou, sem_reinicio),
        "duracao_envio_s": round(duracao_envio, 1),
        "duracao_ate_drenar_s": round(duracao_total, 1),
        "lat_p50_ms": round(percentil(lat_ok, 50) * 1000, 1),
        "lat_p95_ms": round(percentil(lat_ok, 95) * 1000, 1),
        "lat_p99_ms": round(percentil(lat_ok, 99) * 1000, 1),
        "lat_p99_todas_ms": round(percentil(lat_todas, 99) * 1000, 1),
        "lote_medio": estado["lote_medio"],
        "retries": estado["retries"],
        "perdidos_servidor": estado["registros_perdidos"],
        **contagens,
        **avaliar_degrau(contagens, c.tolerancia),
    }

    _escrever_csv(pasta / f"envios_{taxa}.csv", [asdict(e) for e in envios])
    _escrever_csv(pasta / f"erros_{taxa}.csv", [
        {**asdict(a), "componente": COMPONENTE.get(a.categoria, "?")}
        for a in avaliacoes if a.categoria != "correto"
    ])
    return resumo


SATURACAO_MIN = 0.01  # fração de erros de carga que caracteriza a API já saturada (C17)


def api_saturou(gerador_ok: bool, erros_de_carga: int, registros: int) -> bool:
    """O gerador atrasou, mas a API já recusava ou deixava sem resposta pelo menos 1% dos
    registros: o atraso é consequência da saturação (milhares de conexões presas), não a causa.

    O degrau conta como reprovado, não como inválido: se a API falhou com a carga que de fato
    recebeu (menor ou igual à pedida), falharia também com a pedida. Sem isso, o degrau em que
    a API satura aparecia como "gerador atrasou" na tabela de validade (C17)."""
    return not gerador_ok and registros > 0 and erros_de_carga / registros >= SATURACAO_MIN


def descrever_incidente(gerador_ok: bool, drenou: bool, sem_reinicio: bool, falha: str = "") -> str:
    """Motivos que invalidam o degrau, separados por ';' (vazio = degrau válido). Vão para o
    resumo e para a tabela de validade dos resultados finais (C13)."""
    motivos = [m for m, ruim in (("api_reiniciou", not sem_reinicio), ("fila_nao_drenou", not drenou),
                                 ("gerador_atrasou", not gerador_ok)) if ruim]
    if falha:
        motivos.append(f"falha_execucao: {falha}")
    return "; ".join(motivos)


async def _esperar_api(limite: float = 180.0) -> bool:
    """Depois de uma falha, espera a API voltar (restart: on-failure) antes do próximo degrau."""
    inicio = time.monotonic()
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3)) as sessao:
        while time.monotonic() - inicio < limite:
            try:
                async with sessao.get(f"{API}/saude") as r:
                    if r.status == 200:
                        return True
            except (aiohttp.ClientError, TimeoutError):
                pass
            await asyncio.sleep(2)
    return False


def degrau_com_falha(c: Cenario, taxa: int, erro: BaseException) -> dict:
    """Linha do resumo para um degrau que não chegou ao fim (API caiu, banco fora, etc.).
    Fica registrado como inválido em vez de derrubar a suíte inteira."""
    falha = f"{type(erro).__name__}: {erro}"[:200].replace("\n", " ")
    return {
        "cenario": c.nome, "seed": c.seed, "taxa_alvo": taxa, "processos_gerador": PROCESSOS,
        "gerador_valido": False, "drenou": False, "api_sem_reinicio": False, "degrau_valido": False,
        "incidente": descrever_incidente(True, True, True, falha),
        "ok_carga": False, "ok_integridade": False, "sem_erros": False,
    }


def _imprimir(r: dict) -> None:
    if "lat_p99_ms" not in r:
        print(f"  [INV] {r['taxa_alvo']:>5} req/s | {r['incidente']}", flush=True)
        return
    erros = {k[2:]: v for k, v in r.items() if k.startswith("n_")}
    marca = "OK " if r["sem_erros"] else "ERR"
    print(f"  [{marca}] {r['taxa_alvo']:>5} req/s (obtido {r['taxa_obtida']:>7}) | "
          f"p99 {r['lat_p99_ms']:>8} ms | disp {r['disponibilidade']:.4f} | "
          f"integr {r['integridade']:.4f} | {erros or 'sem erros'}", flush=True)


def avaliar_degrau(contagens: dict, tolerancia: float) -> dict[str, bool]:
    """Separa os critérios (C5): carga (nada recusado/perdido no caminho) e
    integridade (erros estruturais zero e taxa total dentro da tolerância)."""
    return {
        "ok_carga": contagens["erros_de_carga"] == 0,
        "ok_integridade": contagens["erros_de_integridade_sem_ordem"] == 0
        and contagens["taxa_erro_integridade"] <= tolerancia,
    }


def limite(resumos: list[dict], criterio: str = "sem_erros") -> int | None:
    """Maior taxa antes do primeiro degrau que falha no critério.
    Degraus em que o gerador não cumpriu a agenda encerram a contagem (C3)."""
    ordenados = sorted(resumos, key=lambda r: r["taxa_alvo"])
    ok = list(takewhile(lambda r: r.get("degrau_valido", r.get("gerador_valido", True)) and r[criterio], ordenados))
    return ok[-1]["taxa_alvo"] if ok else None


def limite_sem_erros(resumos: list[dict]) -> int | None:
    return limite(resumos, "sem_erros")


async def rodar_cenario(c: Cenario, raiz: Path) -> list[dict]:
    pasta = raiz / c.nome
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "config.json").write_text(json.dumps(asdict(c), indent=2, ensure_ascii=False))
    print(f"\n== {c.nome} ({c.modo}, lote={c.lote}, espera={c.espera_ms} ms, tentativas={c.tentativas})")

    resumos, falhas_seguidas = [], 0
    for taxa in c.taxas:
        api_ok = True
        for tentativa in (1, 2):
            try:
                r = await rodar_degrau(c, taxa, pasta)
                break
            except Exception as erro:  # API caiu, banco fora, portas esgotadas...
                r = degrau_com_falha(c, taxa, erro)
                api_ok = await _esperar_api()
                if not api_ok or tentativa == 2:
                    break
                # deixa as conexões do degrau anterior saírem de TIME_WAIT e repete uma vez:
                # sem isso, um degrau saturado abortava os primeiros degraus do cenário
                # seguinte e a repetição inteira contava como limite 0 (C16)
                print(f"  [INV] {taxa:>5} req/s | {r['incidente']} (repetindo em {ESPERA_REPETIR_S} s)", flush=True)
                await asyncio.sleep(ESPERA_REPETIR_S)
        if not api_ok:
            resumos.append(r)
            _imprimir(r)
            print("  API não voltou em 180 s: cenário interrompido")
            break
        resumos.append(r)
        _imprimir(r)
        passou = r["ok_carga"] and r["ok_integridade"] and r["degrau_valido"]
        falhas_seguidas = 0 if passou else falhas_seguidas + 1
        if c.falha_em is None and falhas_seguidas >= c.parar_apos:
            print("  rampa interrompida: limite ultrapassado")
            break

    # colunas n_* variam entre degraus: une todas
    colunas = list(dict.fromkeys(k for r in resumos for k in r))
    _escrever_csv(pasta / "resumo.csv", [{k: r.get(k, 0) for k in colunas} for r in resumos])
    for criterio in ("sem_erros", "ok_carga", "ok_integridade"):
        print(f"  limite ({criterio}): {limite(resumos, criterio)} req/s")
    for r in resumos:
        if r.get("incidente"):
            print(f"  atenção: degrau {r['taxa_alvo']} req/s inválido ({r['incidente']})")
    return resumos


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--suite", choices=["padrao"], help="roda todos os cenários do artigo")
    p.add_argument("--cenario", default="manual")
    p.add_argument("--modo", choices=["lote", "baseline"], default="lote")
    p.add_argument("--lote", type=int, default=200)
    p.add_argument("--espera", type=int, default=100, help="espera máxima do lote (ms)")
    p.add_argument("--tentativas", type=int, default=8)
    p.add_argument("--taxas", default="100,250,500,1000,1500,2000,3000")
    p.add_argument("--duracao", type=int, default=20)
    p.add_argument("--anomalias", type=float, default=0.05)
    p.add_argument("--falha-em", type=float, default=None)
    p.add_argument("--falha-seg", type=float, default=10.0)
    p.add_argument("--escala", type=float, default=1.0,
                   help="multiplica as taxas da suíte (ex.: 0.5 em máquinas modestas)")
    p.add_argument("--saida", type=Path, default=Path("resultados"))
    p.add_argument("--repeticoes", type=int, default=1,
                   help="repete tudo com sementes diferentes, em <saida>/rep_<k> (C9)")
    p.add_argument("--rep", type=int, default=None,
                   help="roda só a repetição K (semente de rep_K) direto em --saida; "
                        "permite intercalar implementações entre repetições (C14)")
    p.add_argument("--duracao-suite", type=int, default=None,
                   help="sobrescreve a duração dos degraus de rampa da suíte (ex.: 60)")
    p.add_argument("--tolerancia", type=float, default=1e-4)
    p.add_argument("--atraso-max", type=float, default=20.0, help="atraso p99 máximo do gerador (ms)")
    p.add_argument("--processos", type=int, default=None,
                   help="processos do gerador de carga (padrão: $GERADOR_PROCESSOS ou 1)")
    a = p.parse_args()

    if a.suite:
        cenarios = [replace(c, taxas=tuple(max(1, int(t * a.escala)) for t in c.taxas)) for c in SUITE_PADRAO]
        if a.duracao_suite:
            cenarios = [replace(c, duracao=a.duracao_suite) if c.falha_em is None else c for c in cenarios]
    else:
        cenarios = [Cenario(
            a.cenario, a.modo, a.lote, a.espera, a.tentativas,
            tuple(int(t) for t in a.taxas.split(",")), a.duracao, a.anomalias,
            falha_em=a.falha_em, falha_seg=a.falha_seg,
        )]
    cenarios = [replace(c, tolerancia=a.tolerancia, atraso_max_ms=a.atraso_max) for c in cenarios]
    if a.processos:
        global PROCESSOS
        PROCESSOS = a.processos

    def rodadas():
        if a.rep is not None:
            yield a.saida, [replace(c, seed=c.seed + 1000 * a.rep) for c in cenarios]
            return
        if a.repeticoes == 1:
            yield a.saida, cenarios
            return
        for k in range(1, a.repeticoes + 1):
            yield a.saida / f"rep_{k}", [replace(c, seed=c.seed + 1000 * k) for c in cenarios]

    async def tudo():
        for saida, lista in rodadas():
            print(f"\n######## {saida}")
            for c in lista:
                await rodar_cenario(c, saida)

    asyncio.run(tudo())


if __name__ == "__main__":
    main()
