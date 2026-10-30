"""Calibração do gerador de carga (C3).

Mede até que taxa o gerador consegue cumprir a agenda contra um servidor
"eco" que responde 202 sem fazer nada. Acima dessa taxa, qualquer limite
medido na API é limite do gerador, não do sistema.

Uso:
    python -m ponto.carga.calibrar --servir --processos 4    # sobe o eco (porta 8001)
    python -m ponto.carga.calibrar --processos 4 --taxas 1000,2000,4000,6000,8000
"""
from __future__ import annotations

import argparse
import asyncio
import multiprocessing
import os
from statistics import quantiles

from aiohttp import web

from ..dados.gerador import gerar
from .rampa import disparar

ECO = os.getenv("ECO_URL", "http://localhost:8001")


async def _eco(_request: web.Request) -> web.Response:
    return web.json_response({"situacao": "eco"}, status=202)


def _servir_um(porta: int, compartilhar: bool) -> None:
    app = web.Application()
    app.router.add_post("/registros", _eco)
    app.router.add_get("/saude", _eco)
    web.run_app(app, port=porta, access_log=None, reuse_port=compartilhar, print=None)


def servir(porta: int = 8001, processos: int = 1) -> None:
    """Com processos > 1, vários processos escutam a mesma porta (SO_REUSEPORT, só Linux):
    o eco não pode ser o gargalo da calibração."""
    if processos <= 1:
        _servir_um(porta, False)
        return
    filhos = [multiprocessing.Process(target=_servir_um, args=(porta, True)) for _ in range(processos)]
    for f in filhos:
        f.start()
    for f in filhos:
        f.join()


def p99(valores: list[float]) -> float:
    return quantiles(valores, n=100, method="inclusive")[98] if len(valores) > 1 else 0.0


async def calibrar(taxas: list[int], duracao: int, processos: int) -> None:
    print(f"gerador com {processos} processo(s)")
    print(f"{'taxa':>6} {'enviado/s':>10} {'atraso_p99_ms':>14} {'lat_p99_ms':>11} {'falhas':>7}")
    for taxa in taxas:
        registros = gerar(max(50, int(taxa * duracao / 2.05)), seed=taxa).registros[: taxa * duracao]
        envios = await disparar(registros, taxa, f"{ECO}/registros", timeout=5.0, processos=processos)
        ultimo = max(e.t_envio for e in envios)
        atraso = p99([e.t_envio - e.t_agendado for e in envios]) * 1000
        lat = p99([e.latencia for e in envios]) * 1000
        falhas = sum(e.status != 202 for e in envios)
        print(f"{taxa:>6} {len(envios) / ultimo:>10.1f} {atraso:>14.1f} {lat:>11.1f} {falhas:>7}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--servir", action="store_true")
    p.add_argument("--taxas", default="500,1000,2000,3000,4000,6000,8000")
    p.add_argument("--duracao", type=int, default=15)
    p.add_argument("--processos", type=int, default=int(os.getenv("GERADOR_PROCESSOS", "1")))
    a = p.parse_args()
    if a.servir:
        servir(processos=a.processos)
    else:
        asyncio.run(calibrar([int(t) for t in a.taxas.split(",")], a.duracao, a.processos))


if __name__ == "__main__":
    main()
