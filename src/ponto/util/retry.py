"""Decoradores (funções de ordem superior) para resiliência da gravação."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

Assincrona = Callable[P, Awaitable[R]]


class FalhaSimulada(ConnectionError):
    """Indisponibilidade artificial do banco, usada no experimento de falha."""


def com_retry(
    tentativas: int,
    base: float = 0.2,
    maximo: float = 5.0,
    excecoes: tuple[type[BaseException], ...] = (ConnectionError, OSError),
    ao_falhar: Callable[[int, BaseException], None] = lambda n, e: None,
) -> Callable[[Assincrona], Assincrona]:
    """Repete a função com backoff exponencial: base, 2*base, 4*base... até `maximo`.

    Recebe uma função e devolve outra função: o comportamento de retry fica
    separado da lógica de gravação e pode ser ligado ou desligado.
    """

    def decorador(func: Assincrona) -> Assincrona:
        @wraps(func)
        async def envolvida(*args, **kwargs):
            for n in range(1, tentativas + 1):
                try:
                    return await func(*args, **kwargs)
                except excecoes as erro:
                    if n == tentativas:
                        raise
                    ao_falhar(n, erro)
                    await asyncio.sleep(min(maximo, base * 2 ** (n - 1)))

        return envolvida

    return decorador


def com_falha_simulada(falha_ate: Callable[[], float]) -> Callable[[Assincrona], Assincrona]:
    """Faz a função falhar enquanto o relógio estiver antes de `falha_ate()`."""

    def decorador(func: Assincrona) -> Assincrona:
        @wraps(func)
        async def envolvida(*args, **kwargs):
            if time.monotonic() < falha_ate():
                await asyncio.sleep(0.05)  # simula o tempo até a conexão falhar
                raise FalhaSimulada("banco indisponível (falha simulada)")
            return await func(*args, **kwargs)

        return envolvida

    return decorador
