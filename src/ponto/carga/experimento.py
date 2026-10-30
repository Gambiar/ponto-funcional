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
PROCESSOS = int(os.getenv("GERADOR_PROCESSOS", "1"))  # processos do gerador de carga (C12)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto")


@dataclass(frozen=True)
class Cenario:
    nome: str
    modo: str = "lote"
    lote: int = 200
    espera_ms: int = 100
    tentativas: int = 8
    taxas: tuple[int, ...] = (100, 250, 500, 1000, 1500, 2000, 3000, 4000, 6000)
    duracao: int = 20            # segundos de carga por degrau
    anomalias: float = 0.05
    seed: int = 42
    timeout: float = 5.0
    falha_em: float | None = None  # segundo do degrau em que o banco "cai"
    falha_seg: float = 10.0
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
]


def percentil(valores: list[float], p: int) -> float:
    if len(valores) < 2:
        return valores[0] if valores else 0.0
    return quantiles(valores, n=100, method="inclusive")[p - 1]


async def _admin(sessao, metodo, caminho, **kw):
    async with sessao.request(metodo, f"{API}{caminho}", **kw) as r:
        r.raise_for_status()
        return await r.json()


async def _esperar_fila(sessao, limite=300.0) -> dict:
    inicio = time.monotonic()
    while time.monotonic() - inicio < limite:
        estado = await _admin(sessao, "GET", "/admin/estado")
        if estado["ocioso"]:
            return estado
        await asyncio.sleep(0.5)
    return await _admin(sessao, "GET", "/admin/estado")


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
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as sessao:
        await _admin(sessao, "POST", "/admin/config", json={
            "modo": c.modo, "tamanho_lote": c.lote, "espera_ms": c.espera_ms, "tentativas": c.tentativas})
        # requisições atrasadas do degrau anterior não podem cair no banco novo
        await _esperar_fila(sessao)
        await _admin(sessao, "POST", "/admin/reset", json={"servidores": n_servidores})

        eventos = {}
        if c.falha_em is not None:
            eventos[c.falha_em] = lambda: _admin(sessao, "POST", "/admin/falha", params={"segundos": c.falha_seg})

        inicio = time.monotonic()
        envios = await disparar(registros, taxa, f"{API}/registros", c.timeout, eventos, processos=PROCESSOS)
        duracao_envio = time.monotonic() - inicio
        estado = await _esperar_fila(sessao)
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
    resumo = {
        "cenario": c.nome,
        "seed": c.seed,
        "taxa_alvo": taxa,
        "processos_gerador": PROCESSOS,
        "taxa_obtida": round(len(envios) / ultimo_envio, 1) if ultimo_envio else 0.0,
        "atraso_gerador_p99_ms": atraso_p99,
        "gerador_valido": atraso_p99 <= c.atraso_max_ms,
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


def _imprimir(r: dict) -> None:
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
    ok = list(takewhile(lambda r: r.get("gerador_valido", True) and r[criterio], ordenados))
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
        r = await rodar_degrau(c, taxa, pasta)
        resumos.append(r)
        _imprimir(r)
        passou = r["ok_carga"] and r["ok_integridade"] and r["gerador_valido"]
        falhas_seguidas = 0 if passou else falhas_seguidas + 1
        if c.falha_em is None and falhas_seguidas >= c.parar_apos:
            print("  rampa interrompida: limite ultrapassado")
            break

    # colunas n_* variam entre degraus: une todas
    colunas = list(dict.fromkeys(k for r in resumos for k in r))
    _escrever_csv(pasta / "resumo.csv", [{k: r.get(k, 0) for k in colunas} for r in resumos])
    for criterio in ("sem_erros", "ok_carga", "ok_integridade"):
        print(f"  limite ({criterio}): {limite(resumos, criterio)} req/s")
    if not all(r["gerador_valido"] for r in resumos):
        print(f"  atenção: gerador atrasou mais de {c.atraso_max_ms} ms em algum degrau (degrau inválido)")
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
