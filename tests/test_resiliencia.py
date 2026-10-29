"""Testes da recursão de isolamento de falhas e do retry, sem banco."""
import asyncio

import pytest

from ponto.casca.fila import ErroDeDados, gravar_isolando_falhas
from ponto.util.retry import com_retry


def rodar(coro):
    return asyncio.run(coro)


def test_bissecao_isola_registro_corrompido():
    gravados, descartados = [], []

    async def gravar(lote):
        if "X" in lote:
            raise ErroDeDados("corrompido")
        gravados.extend(lote)

    lote = list("abcdefgXhijklmn")
    rodar(gravar_isolando_falhas(gravar, lote, lambda item, erro: descartados.append(item)))
    assert descartados == ["X"]
    assert sorted(gravados) == sorted(set(lote) - {"X"})


def test_retry_recupera_apos_falhas_temporarias():
    chamadas = []

    @com_retry(tentativas=4, base=0.001)
    async def instavel():
        chamadas.append(1)
        if len(chamadas) < 3:
            raise ConnectionError
        return "ok"

    assert rodar(instavel()) == "ok"
    assert len(chamadas) == 3


def test_retry_desiste_e_propaga():
    @com_retry(tentativas=2, base=0.001)
    async def sempre_falha():
        raise ConnectionError("fora do ar")

    with pytest.raises(ConnectionError):
        rodar(sempre_falha())


def test_retry_nao_repete_erro_de_dados():
    chamadas = []

    @com_retry(tentativas=5, base=0.001)
    async def dado_ruim():
        chamadas.append(1)
        raise ErroDeDados("x")

    with pytest.raises(ErroDeDados):
        rodar(dado_ruim())
    assert len(chamadas) == 1
