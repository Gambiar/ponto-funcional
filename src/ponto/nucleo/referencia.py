"""Oráculo: implementação de referência, sequencial e independente do sistema.

Dado um conjunto de registros em ordem cronológica, calcula o desfecho que
um sistema perfeito (sem concorrência, sem falhas) produziria.

Usos:
1. o gerador confere que o gabarito construído coincide com o oráculo;
2. a reconciliação recalcula o esperado considerando só os registros que a
   API aceitou, separando erros de carga (recusa, timeout) de erros de
   integridade (desfecho errado, perda silenciosa).

Como servidores diferentes não interferem entre si, os registros são
agrupados por servidor e cada grupo é dobrado (reduce) com estado imutável.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import date
from functools import reduce
from itertools import groupby
from typing import NamedTuple

from .modelos import DESCARTADO, GRAVADO, REJEITADO, Desfecho, Registro
from .validacao import Regra


class Estado(NamedTuple):
    chaves: frozenset[tuple[int, str, date]]  # chaves já gravadas
    desfechos: tuple[Desfecho, ...]


def _passo(regras: list[Regra]) -> Callable[[Estado, Registro], Estado]:
    def aplicar(estado: Estado, r: Registro) -> Estado:
        motivo = next(filter(None, (regra(r) for regra in regras)), None)
        entrada = (r.servidor, "entrada", r.dia)
        match (motivo, r.tipo):
            case (str(m), _):
                novo = Desfecho(r.id_evento, REJEITADO, m)
            case (None, "saida") if entrada not in estado.chaves:
                novo = Desfecho(r.id_evento, REJEITADO, "saida_sem_entrada")
            case (None, _) if r.chave in estado.chaves:
                novo = Desfecho(r.id_evento, DESCARTADO, "duplicado")
            case _:
                return Estado(estado.chaves | {r.chave}, estado.desfechos + (Desfecho(r.id_evento, GRAVADO),))
        return Estado(estado.chaves, estado.desfechos + (novo,))

    return aplicar


def desfechos_esperados(registros: Iterable[Registro], regras: list[Regra]) -> dict[str, Desfecho]:
    ordem = sorted(registros, key=lambda r: (r.servidor, r.instante, r.id_evento))
    passo = _passo(regras)
    por_servidor = (
        reduce(passo, grupo, Estado(frozenset(), ())).desfechos
        for _, grupo in groupby(ordem, key=lambda r: r.servidor)
    )
    return {d.id_evento: d for grupo in por_servidor for d in grupo}
