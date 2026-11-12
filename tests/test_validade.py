"""C13: degraus invalidados (API caiu, fila não drenou, gerador atrasou) aparecem nos resultados."""
import pandas as pd

from ponto.analise.comparar import figura_validade, motivo_principal, tabela_validade
from ponto.analise.graficos import medidos
from ponto.carga.experimento import Cenario, degrau_com_falha, descrever_incidente, limite


def test_descrever_incidente():
    assert descrever_incidente(True, True, True) == ""
    assert descrever_incidente(False, False, False) == "api_reiniciou; fila_nao_drenou; gerador_atrasou"
    assert descrever_incidente(True, True, True, "X") == "falha_execucao: X"


def test_degrau_com_falha_e_invalido_e_encerra_o_limite():
    falho = degrau_com_falha(Cenario("lote_200"), 2000, ConnectionError("api fora\nlinha 2"))
    assert not falho["degrau_valido"] and "falha_execucao: ConnectionError" in falho["incidente"]
    assert "\n" not in falho["incidente"]
    ok = dict(taxa_alvo=1000, sem_erros=True, degrau_valido=True)
    assert limite([ok, falho], "sem_erros") == 1000


def test_tabela_validade_conta_motivos_e_lista_degraus():
    df = pd.DataFrame([
        dict(impl="elixir", rep="rep_1", cenario="lote_200", taxa_alvo=1000, degrau_valido=True,
             incidente="", perdidos_servidor=0),
        dict(impl="elixir", rep="rep_1", cenario="lote_200", taxa_alvo=2000, degrau_valido=False,
             incidente="api_reiniciou; fila_nao_drenou", perdidos_servidor=200),
    ])
    texto = tabela_validade(df)
    assert "| elixir | 2 | 1 | 1 | 1 | 0 | 0 | 200 |" in texto
    assert "| elixir | rep_1 | lote_200 | 2000 | api_reiniciou; fila_nao_drenou |" in texto


def test_medidos_descarta_degrau_interrompido():
    df = pd.DataFrame({"incidente": ["", "gerador_atrasou", "falha_execucao: X"]})
    assert len(medidos(df)) == 2


def test_motivo_principal_e_figura(tmp_path):
    assert motivo_principal("") == "valido"
    assert motivo_principal("fila_nao_drenou; gerador_atrasou") == "fila_nao_drenou"
    assert motivo_principal("api_reiniciou; falha_execucao: X") == "falha_execucao"
    df = pd.DataFrame([dict(impl="elixir", incidente=i, degrau_valido=not i) for i in ["", "gerador_atrasou"]])
    figura_validade(df, tmp_path)
    assert (tmp_path / "validade.png").stat().st_size > 0
