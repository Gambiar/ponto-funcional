"""Tipos imutáveis que circulam pelo pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

TIPOS_VALIDOS = frozenset({"entrada", "saida"})

# Desfechos possíveis de um registro
GRAVADO = "gravado"        # entrou na tabela de pontos
DESCARTADO = "descartado"  # duplicata (mesmo servidor, tipo e dia)
REJEITADO = "rejeitado"    # violou uma regra de negócio


@dataclass(frozen=True, slots=True)
class Registro:
    id_evento: str
    servidor: int
    tipo: str
    instante: datetime
    dispositivo: str

    @property
    def dia(self) -> date:
        return self.instante.date()

    @property
    def chave(self) -> tuple[int, str, date]:
        """Chave de idempotência: um registro de cada tipo por servidor e dia."""
        return (self.servidor, self.tipo, self.dia)


@dataclass(frozen=True, slots=True)
class Aceito:
    registro: Registro


@dataclass(frozen=True, slots=True)
class Rejeitado:
    registro: Registro
    motivo: str


Resultado = Aceito | Rejeitado


@dataclass(frozen=True, slots=True)
class Desfecho:
    id_evento: str
    desfecho: str
    motivo: str | None = None

    @property
    def rotulo(self) -> str:
        return self.desfecho if self.motivo is None else f"{self.desfecho}:{self.motivo}"
