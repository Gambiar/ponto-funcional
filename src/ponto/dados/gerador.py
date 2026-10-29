"""Gerador de base sintética com gabarito.

Cada registro gerado sai acompanhado do desfecho esperado. Nenhum dado real
é usado: servidores são IDs sequenciais.

Uso:
    python -m ponto.dados.gerador --servidores 40000 --anomalias 0.05 --seed 42 --saida dados/
"""
from __future__ import annotations

import argparse
import csv
import random
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from ..nucleo.modelos import DESCARTADO, GRAVADO, REJEITADO, Desfecho, Registro

DIA_PADRAO = date(2026, 11, 3)
TURNOS = (7, 13, 18)  # horas de início de turno; picos de registro


@dataclass(frozen=True, slots=True)
class Caso:
    registro: Registro
    esperado: Desfecho
    anomalia: str  # rótulo da anomalia que originou o caso ("normal" se nenhuma)


@dataclass(frozen=True, slots=True)
class Base:
    casos: tuple[Caso, ...]
    n_servidores: int

    @property
    def registros(self) -> list[Registro]:
        return [c.registro for c in self.casos]

    @property
    def gabarito(self) -> dict[str, Desfecho]:
        return {c.registro.id_evento: c.esperado for c in self.casos}


# ------------------------------------------------------------ auxiliares

def _id(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def _registro(rng, servidor, tipo, instante) -> Registro:
    return Registro(_id(rng), servidor, tipo, instante, f"rep-{servidor % 2000:04d}")


def _caso(registro, desfecho, motivo=None, anomalia="normal") -> Caso:
    return Caso(registro, Desfecho(registro.id_evento, desfecho, motivo), anomalia)


def _jornada(rng, servidor, dia) -> tuple[Registro, Registro]:
    inicio = datetime.combine(dia, datetime.min.time()) + timedelta(hours=rng.choice(TURNOS))
    entrada = inicio + timedelta(minutes=rng.gauss(0, 4))
    saida = entrada + timedelta(hours=4, minutes=rng.gauss(0, 5))
    return _registro(rng, servidor, "entrada", entrada), _registro(rng, servidor, "saida", saida)


# ------------------------------------------------------------ anomalias
# Cada anomalia é uma função (rng, entrada, saida, n_servidores) -> casos.
# Funções guardadas num dicionário: funções de primeira classe.

Anomalia = Callable[[random.Random, Registro, Registro, int], list[Caso]]


def _normal(rng, e, s, n):
    return [_caso(e, GRAVADO), _caso(s, GRAVADO)]


def _duplicado(rng, e, s, n):
    copia = _registro(rng, e.servidor, "entrada", e.instante + timedelta(seconds=rng.uniform(1, 50)))
    return _normal(rng, e, s, n) + [_caso(copia, DESCARTADO, "duplicado", "duplicado")]


def _tipo_invalido(rng, e, s, n):
    extra = _registro(rng, e.servidor, rng.choice(["intervalo", "ENTRADA", ""]), e.instante + timedelta(minutes=30))
    return _normal(rng, e, s, n) + [_caso(extra, REJEITADO, "tipo_invalido", "tipo_invalido")]


def _fora_jornada(rng, e, s, n):
    madrugada = datetime.combine(e.dia, datetime.min.time()) + timedelta(minutes=rng.uniform(0, 359))
    extra = _registro(rng, e.servidor, "entrada", madrugada)
    return _normal(rng, e, s, n) + [_caso(extra, REJEITADO, "fora_da_jornada", "fora_da_jornada")]


def _servidor_inexistente(rng, e, s, n):
    extra = _registro(rng, n + rng.randint(1, 10_000), "entrada", e.instante)
    return _normal(rng, e, s, n) + [_caso(extra, REJEITADO, "servidor_inexistente", "servidor_inexistente")]


def _saida_sem_entrada(rng, e, s, n):
    return [_caso(s, REJEITADO, "saida_sem_entrada", "saida_sem_entrada")]  # entrada omitida


ANOMALIAS: dict[str, Anomalia] = {
    "duplicado": _duplicado,
    "tipo_invalido": _tipo_invalido,
    "fora_da_jornada": _fora_jornada,
    "servidor_inexistente": _servidor_inexistente,
    "saida_sem_entrada": _saida_sem_entrada,
}


# --------------------------------------------------------------- gerador

def gerar(n_servidores: int, taxa_anomalia: float = 0.05, seed: int = 42, dia: date = DIA_PADRAO) -> Base:
    rng = random.Random(seed)
    nomes = sorted(ANOMALIAS)

    def casos_do_servidor(servidor: int) -> list[Caso]:
        entrada, saida = _jornada(rng, servidor, dia)
        anomalia = ANOMALIAS[rng.choice(nomes)] if rng.random() < taxa_anomalia else _normal
        return anomalia(rng, entrada, saida, n_servidores)

    casos = [c for sid in range(1, n_servidores + 1) for c in casos_do_servidor(sid)]
    ordenados = sorted(casos, key=lambda c: (c.registro.instante, c.registro.id_evento))
    return Base(tuple(ordenados), n_servidores)


def para_json(r: Registro) -> dict:
    return {
        "id_evento": r.id_evento,
        "servidor": r.servidor,
        "tipo": r.tipo,
        "instante": r.instante.isoformat(),
        "dispositivo": r.dispositivo,
    }


def salvar(base: Base, pasta: Path) -> tuple[Path, Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    arq_reg, arq_gab = pasta / "registros.csv", pasta / "gabarito.csv"
    with arq_reg.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id_evento", "servidor", "tipo", "instante", "dispositivo"])
        w.writeheader()
        w.writerows(map(para_json, base.registros))
    with arq_gab.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id_evento", "desfecho", "motivo", "anomalia"])
        w.writerows((c.registro.id_evento, c.esperado.desfecho, c.esperado.motivo or "", c.anomalia) for c in base.casos)
    return arq_reg, arq_gab


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--servidores", type=int, default=40_000)
    p.add_argument("--anomalias", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--saida", type=Path, default=Path("dados"))
    a = p.parse_args()
    base = gerar(a.servidores, a.anomalias, a.seed)
    reg, gab = salvar(base, a.saida)
    print(f"{len(base.casos)} registros para {a.servidores} servidores -> {reg}, {gab}")


if __name__ == "__main__":
    main()
