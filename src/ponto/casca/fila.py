"""Fila com back-pressure e consumidor que grava em lotes."""
from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field

from ..nucleo.lotes import bissectar
from ..nucleo.modelos import Resultado

log = logging.getLogger("ponto.fila")

Gravador = Callable[[Sequence[Resultado]], Awaitable[object]]


class ErroDeDados(Exception):
    """Erro causado pelo conteúdo do lote (não adianta repetir)."""


async def gravar_isolando_falhas(
    gravar: Gravador,
    lote: Sequence[Resultado],
    ao_descartar: Callable[[Resultado, BaseException], None],
) -> None:
    """Se o lote tem um registro corrompido, divide ao meio recursivamente até
    isolá-lo, gravando todo o resto. Profundidade máxima: log2(tamanho do lote).
    """
    try:
        await gravar(lote)
    except ErroDeDados as erro:
        match lote:
            case [unico]:
                ao_descartar(unico, erro)
            case _:
                esquerda, direita = bissectar(lote)
                await gravar_isolando_falhas(gravar, esquerda, ao_descartar)
                await gravar_isolando_falhas(gravar, direita, ao_descartar)


@dataclass
class Contadores:
    enfileirados: int = 0
    recusados: int = 0
    lotes: int = 0
    registros_gravados_em_lote: int = 0
    registros_perdidos: int = 0
    registros_corrompidos: int = 0
    tamanhos_de_lote: list[int] = field(default_factory=list)


class ProcessadorDeLotes:
    """Junta até `tamanho()` registros ou espera até `espera_ms()` e grava."""

    def __init__(
        self,
        gravar: Callable[[], Gravador],
        tamanho: Callable[[], int],
        espera_ms: Callable[[], int],
        capacidade: int,
        consumidores: int = 1,
    ) -> None:
        # parâmetros recebidos como funções: a configuração pode mudar em execução
        self._gravar, self._tamanho, self._espera = gravar, tamanho, espera_ms
        self.fila: asyncio.Queue[Resultado] = asyncio.Queue(maxsize=capacidade)
        self.consumidores = consumidores
        self.em_processamento = 0
        self.pendentes = 0  # enfileirados ainda não gravados (inclui o lote em coleta)
        self.contadores = Contadores()
        self._tarefas: list[asyncio.Task] = []

    def enfileirar(self, item: Resultado) -> bool:
        try:
            self.fila.put_nowait(item)
        except asyncio.QueueFull:
            self.contadores.recusados += 1
            return False
        self.contadores.enfileirados += 1
        self.pendentes += 1
        return True

    async def _coletar(self) -> list[Resultado]:
        lote = [await self.fila.get()]
        limite = time.monotonic() + self._espera() / 1000
        while len(lote) < self._tamanho():
            try:
                lote.append(self.fila.get_nowait())
                continue
            except asyncio.QueueEmpty:
                pass
            restante = limite - time.monotonic()
            if restante <= 0:
                break
            try:
                lote.append(await asyncio.wait_for(self.fila.get(), restante))
            except TimeoutError:
                break
        return lote

    def _descartar(self, item: Resultado, erro: BaseException) -> None:
        self.contadores.registros_corrompidos += 1
        log.warning("registro %s descartado: %s", item.registro.id_evento, erro)

    async def _consumir(self) -> None:
        while True:
            lote = await self._coletar()
            self.em_processamento += len(lote)
            try:
                await gravar_isolando_falhas(self._gravar(), lote, self._descartar)
                self.contadores.lotes += 1
                self.contadores.registros_gravados_em_lote += len(lote)
                self.contadores.tamanhos_de_lote.append(len(lote))
            except Exception as erro:  # retries esgotados: o lote se perde
                self.contadores.registros_perdidos += len(lote)
                log.error("lote de %d registros perdido: %r", len(lote), erro)
            finally:
                self.em_processamento -= len(lote)
                self.pendentes -= len(lote)
                for _ in lote:
                    self.fila.task_done()

    def iniciar(self) -> None:
        self._tarefas = [asyncio.create_task(self._consumir()) for _ in range(self.consumidores)]

    async def parar(self) -> None:
        for t in self._tarefas:
            t.cancel()
        await asyncio.gather(*self._tarefas, return_exceptions=True)

    @property
    def ocioso(self) -> bool:
        return self.pendentes == 0
