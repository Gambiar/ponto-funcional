"""Interpretação e validação de registros (funções puras).

Conceitos de programação funcional usados aqui:
- pattern matching estrutural (match/case) sobre dicts e dataclasses;
- funções de primeira classe: regras são funções guardadas numa lista;
- funções de ordem superior: fábricas de regras e de validadores (closures);
- funções anônimas (lambda) e processamento de coleções (map, filter, next).
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime

from .modelos import Aceito, Registro, Rejeitado, Resultado

# Uma regra recebe um registro e devolve o motivo da rejeição ou None.
Regra = Callable[[Registro], str | None]


def interpretar(payload: object) -> Registro | None:
    """Converte o JSON recebido em Registro; None se o formato for inválido."""
    match payload:
        case {
            "id_evento": str(id_evento),
            "servidor": int(servidor),
            "tipo": str(tipo),
            "instante": str(texto),
            "dispositivo": str(dispositivo),
        } if not isinstance(servidor, bool):
            instante = _ler_instante(texto)
            if instante is None:
                return None
            return Registro(id_evento, servidor, tipo, instante, dispositivo)
        case _:
            return None


def _ler_instante(texto: str) -> datetime | None:
    try:
        return datetime.fromisoformat(texto)
    except ValueError:
        return None


# ---------------------------------------------------------------- regras

def regra_tipo(registro: Registro) -> str | None:
    match registro:
        case Registro(tipo="entrada" | "saida"):
            return None
        case _:
            return "tipo_invalido"


def regra_servidor(cadastrados: frozenset[int]) -> Regra:
    """Fábrica de regra: captura o cadastro numa closure."""
    return lambda r: None if r.servidor in cadastrados else "servidor_inexistente"


def regra_jornada(inicio: int = 6, fim: int = 24) -> Regra:
    """Registros só são aceitos entre `inicio` e `fim` horas."""

    def verificar(registro: Registro) -> str | None:
        match registro.instante.hour:
            case h if inicio <= h < fim:
                return None
            case _:
                return "fora_da_jornada"

    return verificar


def regras_padrao(cadastrados: frozenset[int]) -> list[Regra]:
    """Ordem importa: a primeira regra violada define o motivo."""
    return [regra_tipo, regra_servidor(cadastrados), regra_jornada()]


def criar_validador(regras: Sequence[Regra]) -> Callable[[Registro], Resultado]:
    """Compõe uma lista de regras num único validador."""

    def validar(registro: Registro) -> Resultado:
        motivos = map(lambda regra: regra(registro), regras)
        primeiro = next(filter(None, motivos), None)  # avaliação preguiçosa
        match primeiro:
            case None:
                return Aceito(registro)
            case str(motivo):
                return Rejeitado(registro, motivo)

    return validar
