"""Operações puras sobre lotes de registros.

A casca (repositório) chama estas funções antes e depois de falar com o banco;
toda a decisão de negócio fica aqui, testável sem banco.
"""
from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date
from itertools import groupby
from typing import TypeVar

from .modelos import (
    DESCARTADO,
    GRAVADO,
    REJEITADO,
    Aceito,
    Desfecho,
    Registro,
    Rejeitado,
    Resultado,
)

T = TypeVar("T")


# ------------------------------------------------------------ recursão

def particionar(itens: Sequence[T], tamanho: int) -> list[Sequence[T]]:
    """Divide uma sequência em blocos de no máximo `tamanho` itens.

    Recursão por divisão e conquista: a profundidade é log2(n / tamanho),
    então não esbarra no limite de recursão do Python (~1000 chamadas).
    """
    if tamanho < 1:
        raise ValueError("tamanho deve ser >= 1")
    match len(itens):
        case 0:
            return []
        case n if n <= tamanho:
            return [itens]
        case n:
            # corta num múltiplo de `tamanho` para manter os blocos cheios
            meio = ((n // tamanho + 1) // 2) * tamanho
            return particionar(itens[:meio], tamanho) + particionar(itens[meio:], tamanho)


def bissectar(lote: Sequence[T]) -> tuple[Sequence[T], Sequence[T]]:
    """Divide um lote ao meio (usado na recursão de isolamento de falhas)."""
    meio = len(lote) // 2
    return lote[:meio], lote[meio:]


# --------------------------------------------------- preparação do lote

def ordenar(resultados: Iterable[Resultado]) -> list[Resultado]:
    """Ordena pelo instante: em duplicatas, o registro mais antigo vence."""
    return sorted(resultados, key=lambda r: (r.registro.instante, r.registro.id_evento))


def aceitos_por_tipo(resultados: Iterable[Resultado], tipo: str) -> list[Registro]:
    return [r.registro for r in resultados if isinstance(r, Aceito) and r.registro.tipo == tipo]


def separar_saidas(
    saidas: Iterable[Registro], entradas_existentes: frozenset[tuple[int, date]]
) -> tuple[list[Registro], list[Registro]]:
    """Saídas com entrada correspondente seguem; as demais são rejeitadas."""
    tem_entrada = lambda r: (r.servidor, r.dia) in entradas_existentes  # noqa: E731
    lista = list(saidas)
    return [r for r in lista if tem_entrada(r)], [r for r in lista if not tem_entrada(r)]


# ------------------------------------------------------ desfecho final

def desfecho(resultado: Resultado, inseridos: frozenset[str], sem_entrada: frozenset[str]) -> Desfecho:
    """Decide o desfecho de um registro depois da tentativa de inserção."""
    match resultado:
        case Rejeitado(registro=r, motivo=motivo):
            return Desfecho(r.id_evento, REJEITADO, motivo)
        case Aceito(registro=r) if r.id_evento in sem_entrada:
            return Desfecho(r.id_evento, REJEITADO, "saida_sem_entrada")
        case Aceito(registro=r) if r.id_evento in inseridos:
            return Desfecho(r.id_evento, GRAVADO)
        case Aceito(registro=r):
            return Desfecho(r.id_evento, DESCARTADO, "duplicado")


def resolver_desfechos(
    resultados: Iterable[Resultado], inseridos: Iterable[str], sem_entrada: Iterable[str]
) -> list[Desfecho]:
    ins, sem = frozenset(inseridos), frozenset(sem_entrada)
    return [desfecho(r, ins, sem) for r in resultados]


# ------------------------------------------------------------ resumo

def contar_por_rotulo(desfechos: Iterable[Desfecho]) -> dict[str, int]:
    """Agrupa desfechos por rótulo (ex.: 'rejeitado:tipo_invalido')."""
    rotulos = sorted(d.rotulo for d in desfechos)
    return {rotulo: sum(1 for _ in grupo) for rotulo, grupo in groupby(rotulos)}
