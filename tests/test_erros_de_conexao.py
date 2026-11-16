"""C17: as três APIs tratam os mesmos erros do banco como falha de conexão (com retry/503).

Com a falha simulada isso não aparecia: as três lançam a mesma exceção artificial. Numa
queda real, o erro vem do driver, e uma diferença aqui viraria diferença de resultado.
A lista é a mesma de `Ponto.Retry.conexao?/1` (testada em elixir/test/casca_test.exs)."""
import asyncpg
import pytest

from ponto.casca.api import ERROS_DE_CONEXAO as FUNCIONAL
from ponto_imperativo.api import ERROS_DE_CONEXAO as IMPERATIVO

SQLSTATE_DE_CONEXAO = ["08000", "08003", "08006", "53300", "57P01", "57P02", "57P03", "55000"]
SQLSTATE_DE_DADOS = ["22P02", "23505", "42P01"]


def _classe(sqlstate: str) -> type:
    return asyncpg.exceptions.PostgresError.get_message_class_for_sqlstate(sqlstate)


@pytest.mark.parametrize("erros", [FUNCIONAL, IMPERATIVO], ids=["funcional", "imperativo"])
def test_mesmos_sqlstate_contam_como_conexao(erros):
    assert [s for s in SQLSTATE_DE_CONEXAO if not issubclass(_classe(s), erros)] == []
    assert [s for s in SQLSTATE_DE_DADOS if issubclass(_classe(s), erros)] == []


def test_conexao_fechada_pelo_servidor_conta_como_conexao():
    assert issubclass(asyncpg.ConnectionDoesNotExistError, FUNCIONAL)
    assert set(FUNCIONAL) == set(IMPERATIVO)
