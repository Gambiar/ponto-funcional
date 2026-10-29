"""Persistência em lote no PostgreSQL.

O repositório só executa SQL; as decisões ficam nas funções puras do núcleo.
"""
from __future__ import annotations

from collections.abc import Sequence

import asyncpg

from ..nucleo.lotes import aceitos_por_tipo, ordenar, resolver_desfechos, separar_saidas
from ..nucleo.modelos import Desfecho, Registro, Resultado

ESQUEMA = """
CREATE TABLE IF NOT EXISTS servidores (
    id INTEGER PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS pontos (
    id_evento   UUID PRIMARY KEY,
    servidor    INTEGER NOT NULL,
    tipo        TEXT NOT NULL,
    dia         DATE NOT NULL,
    instante    TIMESTAMP NOT NULL,
    dispositivo TEXT NOT NULL,
    UNIQUE (servidor, tipo, dia)          -- idempotência
);
CREATE TABLE IF NOT EXISTS eventos (
    id_evento   UUID PRIMARY KEY,           -- um desfecho por evento
    servidor    INTEGER NOT NULL,
    tipo        TEXT NOT NULL,
    instante    TIMESTAMP NOT NULL,
    desfecho    TEXT NOT NULL,
    motivo      TEXT,
    processado_em TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);
"""

_INSERIR_PONTOS = """
INSERT INTO pontos (id_evento, servidor, tipo, dia, instante, dispositivo)
SELECT * FROM unnest($1::uuid[], $2::int[], $3::text[], $4::date[], $5::timestamp[], $6::text[])
ON CONFLICT DO NOTHING
RETURNING id_evento::text
"""

_ENTRADAS_EXISTENTES = """
SELECT p.servidor, p.dia FROM pontos p
JOIN unnest($1::int[], $2::date[]) AS q(servidor, dia) USING (servidor, dia)
WHERE p.tipo = 'entrada'
"""

_INSERIR_EVENTOS = """
INSERT INTO eventos (id_evento, servidor, tipo, instante, desfecho, motivo)
SELECT * FROM unnest($1::uuid[], $2::int[], $3::text[], $4::timestamp[], $5::text[], $6::text[])
ON CONFLICT (id_evento) DO NOTHING
"""


def _colunas_pontos(regs: Sequence[Registro]):
    return (
        [r.id_evento for r in regs],
        [r.servidor for r in regs],
        [r.tipo for r in regs],
        [r.dia for r in regs],
        [r.instante for r in regs],
        [r.dispositivo for r in regs],
    )


async def criar_esquema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(ESQUEMA)


async def reiniciar(pool: asyncpg.Pool, n_servidores: int) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute("TRUNCATE pontos, eventos, servidores")
        await conn.execute("INSERT INTO servidores SELECT generate_series(1, $1)", n_servidores)


async def carregar_cadastro(pool: asyncpg.Pool) -> frozenset[int]:
    async with pool.acquire() as conn:
        return frozenset(r["id"] for r in await conn.fetch("SELECT id FROM servidores"))


async def gravar_lote(pool: asyncpg.Pool, resultados: Sequence[Resultado]) -> list[Desfecho]:
    """Grava um lote numa única transação e devolve o desfecho de cada registro."""
    lote = ordenar(resultados)
    entradas = aceitos_por_tipo(lote, "entrada")
    saidas = aceitos_por_tipo(lote, "saida")

    async with pool.acquire() as conn, conn.transaction():
        inseridos = set()
        if entradas:
            inseridos |= {r[0] for r in await conn.fetch(_INSERIR_PONTOS, *_colunas_pontos(entradas))}
        sem_entrada: list[Registro] = []
        if saidas:
            existentes = await conn.fetch(
                _ENTRADAS_EXISTENTES, [r.servidor for r in saidas], [r.dia for r in saidas]
            )
            validas, sem_entrada = separar_saidas(saidas, frozenset((e["servidor"], e["dia"]) for e in existentes))
            if validas:
                inseridos |= {r[0] for r in await conn.fetch(_INSERIR_PONTOS, *_colunas_pontos(validas))}

        desfechos = resolver_desfechos(lote, inseridos, (r.id_evento for r in sem_entrada))
        regs = [r.registro for r in lote]
        await conn.execute(
            _INSERIR_EVENTOS,
            [r.id_evento for r in regs],
            [r.servidor for r in regs],
            [r.tipo for r in regs],
            [r.instante for r in regs],
            [d.desfecho for d in desfechos],
            [d.motivo for d in desfechos],
        )
    return desfechos
