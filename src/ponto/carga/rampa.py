"""Disparo de carga em malha aberta (open loop), opcionalmente em vários processos.

Cada registro tem um horário agendado (i / taxa). O envio acontece no horário
mesmo que respostas anteriores ainda não tenham chegado; assim a lentidão do
servidor aparece como latência e erro, em vez de reduzir a carga em silêncio
(o problema conhecido como "coordinated omission").

Um único processo Python satura por volta de 1500–2000 req/s (C3). Com
`processos > 1`, a agenda é calculada uma vez no processo principal e repartida
entre processos trabalhadores que compartilham o mesmo instante zero (o relógio
monotônico é do sistema, comum a todos os processos). A repartição é por
servidor: os registros de um mesmo servidor saem sempre do mesmo processo, como
viriam do mesmo relógio de ponto, e a ordem entre eles é preservada (C12).
"""
from __future__ import annotations

import asyncio
import multiprocessing
import time
from collections.abc import Awaitable, Callable, Sequence
from concurrent.futures import ProcessPoolExecutor

import aiohttp

from ..dados.gerador import para_json
from ..dados.reconciliacao import Envio
from ..nucleo.modelos import Registro

Agenda = list[tuple[Registro, float]]  # (registro, segundos desde o instante zero)


# ------------------------------------------------------------ funções puras

def agendar(registros: Sequence[Registro], taxa: float) -> Agenda:
    """Espaçamento uniforme: o registro i sai em i / taxa segundos."""
    return [(r, i / taxa) for i, r in enumerate(registros)]


def repartir(agenda: Agenda, partes: int) -> list[Agenda]:
    """Divide a agenda por servidor, mantendo a ordem dentro de cada parte."""
    return [[(r, t) for r, t in agenda if r.servidor % partes == k] for k in range(partes)]


# ------------------------------------------------------------ envio

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


async def _cumprir_agenda(
    agenda: Agenda,
    url: str,
    timeout: float,
    t0: float,
    eventos: dict[float, Callable[[], Awaitable[object]]] | None = None,
) -> list[Envio]:
    conector = aiohttp.TCPConnector(limit=0, force_close=False)
    tempo = aiohttp.ClientTimeout(total=timeout)
    pendentes = dict(sorted((eventos or {}).items()))
    async with aiohttp.ClientSession(connector=conector, timeout=tempo) as sessao:
        tarefas: list[asyncio.Task] = []
        for r, agendado in agenda:
            for instante in [t for t in pendentes if t <= agendado]:
                tarefas.append(asyncio.create_task(pendentes.pop(instante)()))
            espera = t0 + agendado - time.monotonic()
            if espera > 0:
                await asyncio.sleep(espera)
            tarefas.append(asyncio.create_task(_enviar(sessao, url, r, t0, agendado)))
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)
    return [x for x in resultados if isinstance(x, Envio)]


def _trabalhador(agenda: Agenda, url: str, timeout: float, t0: float) -> list[Envio]:
    """Executado em outro processo: um laço de eventos próprio para a sua parte."""
    return asyncio.run(_cumprir_agenda(agenda, url, timeout, t0))


def _aquecer() -> int:
    """Força a criação do processo e a importação do aiohttp antes do instante zero."""
    return multiprocessing.current_process().pid


async def _executar_eventos(eventos: dict[float, Callable[[], Awaitable[object]]], t0: float) -> None:
    for instante, acao in sorted(eventos.items()):
        espera = t0 + instante - time.monotonic()
        if espera > 0:
            await asyncio.sleep(espera)
        await acao()


async def disparar(
    registros: Sequence[Registro],
    taxa: float,
    url: str,
    timeout: float = 5.0,
    eventos: dict[float, Callable[[], Awaitable[object]]] | None = None,
    processos: int = 1,
) -> list[Envio]:
    """Envia `registros` a `taxa` req/s. `eventos` mapeia segundo -> corrotina
    a disparar naquele instante (ex.: injetar falha)."""
    agenda = agendar(registros, taxa)
    if processos <= 1:
        return await _cumprir_agenda(agenda, url, timeout, time.monotonic(), eventos)

    partes = repartir(agenda, processos)
    laco = asyncio.get_running_loop()
    contexto = multiprocessing.get_context("spawn")  # processo limpo, sem herdar o laço de eventos
    with ProcessPoolExecutor(max_workers=processos, mp_context=contexto) as pool:
        await asyncio.gather(*[laco.run_in_executor(pool, _aquecer) for _ in range(processos)])
        t0 = time.monotonic() + 0.5  # todos começam juntos, já aquecidos
        tarefas = [laco.run_in_executor(pool, _trabalhador, parte, url, timeout, t0) for parte in partes]
        if eventos:
            tarefas.append(_executar_eventos(eventos, t0))
        resultados = await asyncio.gather(*tarefas)
    return [e for lista in resultados if isinstance(lista, list) for e in lista]
