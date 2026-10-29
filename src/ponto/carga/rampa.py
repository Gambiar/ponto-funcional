"""Disparo de carga em malha aberta (open loop).

Cada registro tem um horário agendado (i / taxa). O envio acontece no horário
mesmo que respostas anteriores ainda não tenham chegado; assim a lentidão do
servidor aparece como latência e erro, em vez de reduzir a carga em silêncio
(o problema conhecido como "coordinated omission").
"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable, Sequence

import aiohttp

from ..dados.gerador import para_json
from ..dados.reconciliacao import Envio
from ..nucleo.lotes import particionar
from ..nucleo.modelos import Registro


async def _enviar(sessao: aiohttp.ClientSession, url: str, r: Registro, t0: float, agendado: float) -> Envio:
    inicio = time.monotonic()
    status: int | str
    erro = ""
    try:
        async with sessao.post(url, json=para_json(r)) as resp:
            status = resp.status
            if status >= 400:
                try:
                    erro = (await resp.json()).get("erro", "")
                except (aiohttp.ContentTypeError, ValueError):
                    erro = ""
            else:
                await resp.read()
    except TimeoutError:
        status = "timeout"
    except aiohttp.ClientError:
        status = "conexao"
    fim = time.monotonic()
    return Envio(r.id_evento, agendado, inicio - t0, fim - inicio, status, erro)


async def disparar(
    registros: Sequence[Registro],
    taxa: float,
    url: str,
    timeout: float = 5.0,
    eventos: dict[float, Callable[[], Awaitable[object]]] | None = None,
) -> list[Envio]:
    """Envia `registros` a `taxa` req/s. `eventos` mapeia segundo -> corrotina
    a disparar naquele instante (ex.: injetar falha)."""
    conector = aiohttp.TCPConnector(limit=0, force_close=False)
    tempo = aiohttp.ClientTimeout(total=timeout)
    pendentes = dict(sorted((eventos or {}).items()))
    async with aiohttp.ClientSession(connector=conector, timeout=tempo) as sessao:
        t0 = time.monotonic()
        tarefas: list[asyncio.Task] = []
        # um bloco por segundo de carga; dentro do bloco, espaçamento uniforme
        por_segundo = max(1, round(taxa))
        for segundo, bloco in enumerate(particionar(registros, por_segundo)):
            for j, r in enumerate(bloco):
                agendado = segundo + j / por_segundo
                for instante in [t for t in pendentes if t <= agendado]:
                    tarefas.append(asyncio.create_task(pendentes.pop(instante)()))
                espera = t0 + agendado - time.monotonic()
                if espera > 0:
                    await asyncio.sleep(espera)
                tarefas.append(asyncio.create_task(_enviar(sessao, url, r, t0, agendado)))
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)
    return [x for x in resultados if isinstance(x, Envio)]
