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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto")


@dataclass(frozen=True)
class Cenario:
    nome: str
    modo: str = "lote"
    lote: int = 200
    espera_ms: int = 100
    tentativas: int = 8
    taxas: tuple[int, ...] = (100, 250, 500, 1000, 1500, 2000, 3000)
    duracao: int = 20            # segundos de carga por degrau
    anomalias: float = 0.05
    seed: int = 42
    timeout: float = 5.0
    falha_em: float | None = None  # segundo do degrau em que o banco "cai"
    falha_seg: float = 10.0
    parar_apos: int = 2          # para a rampa após N degraus seguidos com erro
    extra: dict = field(default_factory=dict)


# Cenários do artigo. Ajuste as taxas conforme a máquina.
SUITE_PADRAO = [
    Cenario("baseline", modo="baseline"),
    Cenario("lote_50", lote=50),
    Cenario("lote_200", lote=200),
    Cenario("lote_1000", lote=1000),
    Cenario("falha_com_retry", taxas=(500,), duracao=30, falha_em=5),
    Cenario("falha_sem_retry", taxas=(500,), duracao=30, falha_em=5, tentativas=1),
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
        envios = await disparar(registros, taxa, f"{API}/registros", c.timeout, eventos)
        duracao_envio = time.monotonic() - inicio
        estado = await _esperar_fila(sessao)
        duracao_total = time.monotonic() - inicio

    banco = await _ler_banco()
    avaliacoes = reconciliar(registros, base.gabarito, envios, banco, regras_padrao(frozenset(range(1, n_servidores + 1))))

    lat_ok = [e.latencia for e in envios if e.status in SUCESSO]
    atrasos = [e.t_envio - e.t_agendado for e in envios]
    resumo = {
        "cenario": c.nome,
        "taxa_alvo": taxa,
        "taxa_obtida": round(len(envios) / duracao_envio, 1),
        "atraso_gerador_p99_ms": round(percentil(atrasos, 99) * 1000, 1),
        "duracao_ate_drenar_s": round(duracao_total, 1),
        "lat_p50_ms": round(percentil(lat_ok, 50) * 1000, 1),
        "lat_p95_ms": round(percentil(lat_ok, 95) * 1000, 1),
        "lat_p99_ms": round(percentil(lat_ok, 99) * 1000, 1),
        "lote_medio": estado["lote_medio"],
        "retries": estado["retries"],
        "perdidos_servidor": estado["registros_perdidos"],
        **resumir(avaliacoes),
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


def limite_sem_erros(resumos: list[dict]) -> int | None:
    """Maior taxa antes do primeiro degrau com erro."""
    ok = list(takewhile(lambda r: r["sem_erros"], sorted(resumos, key=lambda r: r["taxa_alvo"])))
    return ok[-1]["taxa_alvo"] if ok else None


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
        falhas_seguidas = 0 if r["sem_erros"] else falhas_seguidas + 1
        if c.falha_em is None and falhas_seguidas >= c.parar_apos:
            print("  rampa interrompida: limite ultrapassado")
            break

    # colunas n_* variam entre degraus: une todas
    colunas = list(dict.fromkeys(k for r in resumos for k in r))
    _escrever_csv(pasta / "resumo.csv", [{k: r.get(k, 0) for k in colunas} for r in resumos])
    limite = limite_sem_erros(resumos)
    print(f"  limite sem erros: {limite} req/s" if limite else "  nenhum degrau sem erros")
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
    a = p.parse_args()

    if a.suite:
        cenarios = [replace(c, taxas=tuple(max(1, int(t * a.escala)) for t in c.taxas)) for c in SUITE_PADRAO]
    else:
        cenarios = [Cenario(
            a.cenario, a.modo, a.lote, a.espera, a.tentativas,
            tuple(int(t) for t in a.taxas.split(",")), a.duracao, a.anomalias,
            falha_em=a.falha_em, falha_seg=a.falha_seg,
        )]

    async def tudo():
        for c in cenarios:
            await rodar_cenario(c, a.saida)

    asyncio.run(tudo())


if __name__ == "__main__":
    main()
