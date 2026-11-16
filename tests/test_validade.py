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


def test_repeticao_sem_degrau_valido_fica_fora_da_mediana():
    """C16: repetição abortada pelo ambiente não conta como limite 0; reprovada de fato, sim (B5)."""
    from ponto.analise.comparar import celula

    def rep(nome, valido, passou):
        return [dict(rep=nome, taxa_alvo=t, degrau_valido=valido, ok_carga=passou) for t in (100, 250)]

    g = pd.DataFrame(rep("rep_1", True, True) + rep("rep_2", True, True) + rep("rep_3", False, False))
    assert celula(g, "ok_carga") == "250 [250–250] (n=2)"
    g = pd.DataFrame(rep("rep_1", True, True) + rep("rep_2", True, False))
    assert celula(g, "ok_carga") == "125 [0–250] (n=2)"
    assert celula(pd.DataFrame(rep("rep_1", False, False)), "ok_carga") == "sem degrau válido"
    # só o primeiro degrau abortado: o limite abaixo dele é desconhecido, não 0
    abortado = rep("rep_2", True, True)
    abortado[0].update(degrau_valido=False, ok_carga=False)
    g = pd.DataFrame(rep("rep_1", True, True) + abortado)
    assert celula(g, "ok_carga") == "250"


def _degrau(pasta, taxa, atrasos, incidente, drenou=True):
    """Escreve envios_<taxa>.csv com um atraso por registro (1 registro a cada 0,01 s)."""
    pasta.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"t_agendado": [i * 0.01 for i in range(len(atrasos))],
                  "t_envio": [i * 0.01 + a for i, a in enumerate(atrasos)],
                  "latencia": [0.001 + a for a in atrasos],
                  "status": [202] * len(atrasos)}).to_csv(pasta / f"envios_{taxa}.csv", index=False)
    return dict(taxa_alvo=taxa, ok_carga=True, degrau_valido=not incidente, gerador_valido="gerador" not in incidente,
                drenou=drenou, api_sem_reinicio=True, incidente=incidente, atraso_gerador_p99_ms=0.0)


def test_reanalise_da_largada_revalida_so_o_surto_inicial(tmp_path):
    """C16: surto atrasado só nos 2 s iniciais revalida o degrau; atraso no meio, não; e os
    outros motivos de invalidade continuam valendo."""
    from ponto.analise.comparar import carregar, exportar, revalidar, tabela_revalidacao

    pasta = tmp_path / "elixir" / "rep_1" / "lote_200"
    surto = [0.5] * 100 + [0.001] * 400            # atrasado só no 1º segundo
    meio = [0.001] * 300 + [0.5] * 50 + [0.001] * 150  # atrasado no meio
    linhas = [_degrau(pasta, 1000, surto, "gerador_atrasou"),
              _degrau(pasta, 1500, meio, "gerador_atrasou"),
              _degrau(pasta, 2000, surto, "fila_nao_drenou; gerador_atrasou", drenou=False)]
    pd.DataFrame(linhas).to_csv(pasta / "resumo.csv", index=False)

    d = revalidar(carregar(tmp_path), 2.0)
    assert d.degrau_valido.tolist() == [True, False, False]
    assert d.incidente.tolist() == ["", "gerador_atrasou", "fila_nao_drenou"]
    assert "| elixir | 3 | 0 | 1 | 1 |" in tabela_revalidacao(d, 2.0)

    # arquivo compacto: guarda o medido + a coluna, e a reanálise sai igual sem os envios
    exportar(d, tmp_path / "arquivo")
    salvo = pd.read_csv(tmp_path / "arquivo" / "elixir" / "rep_1" / "lote_200" / "resumo.csv")
    assert not salvo.degrau_valido.any() and "atraso_p99_apos_largada_ms" in salvo
    assert salvo.lat_p99_apos_largada_ms.iloc[0] == 2.0  # o surto ficou fora da latência também
    assert revalidar(carregar(tmp_path / "arquivo"), 2.0).degrau_valido.tolist() == [True, False, False]
    assert "api_saturou" not in salvo  # só existia na reanálise

    # resultado novo, com api_saturou medido: a exportação guarda o valor medido
    pd.DataFrame([{**l, "api_saturou": False} for l in linhas]).to_csv(pasta / "resumo.csv", index=False)
    exportar(revalidar(carregar(tmp_path), 2.0), tmp_path / "novo")
    novo = pd.read_csv(tmp_path / "novo" / "elixir" / "rep_1" / "lote_200" / "resumo.csv")
    assert novo.api_saturou.tolist() == [False, False, False]


def test_mann_whitney_exato():
    from ponto.analise.comparar import mann_whitney
    assert abs(mann_whitney([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) - 2 / 252) < 1e-12
    assert mann_whitney([1, 2, 3], [4, 5, 6]) == 0.1          # 3×3: nunca abaixo de 0,1
    assert mann_whitney([5, 5, 5], [5, 5, 5]) == 1.0          # empates totais
    assert abs(mann_whitney([1, 2, 3, 4, 6], [5, 7, 8, 9, 10]) - 4 / 252) < 1e-12


def test_api_saturada_e_reprovada_nao_invalida():
    """C17: gerador atrasou porque a API saturou (≥ 1% de erros de carga) -> degrau válido e reprovado."""
    from ponto.carga.experimento import api_saturou
    assert api_saturou(False, 100, 1000)
    assert not api_saturou(False, 5, 1000)      # poucos erros: o atraso pode ser do gerador
    assert not api_saturou(True, 500, 1000)     # gerador em dia: nada a reclassificar
    assert not api_saturou(False, 0, 0)


def test_tabela_latencia_so_com_degraus_validos_e_aprovados():
    from ponto.analise.comparar import tabela_latencia
    linhas = [dict(impl=i, rep=f"rep_{k}", cenario="lote_200", taxa_alvo=1000, degrau_valido=True, ok_carga=True,
                   lat_p99_ms=base + k) for i, base in (("python_imperativo", 10), ("python_funcional", 20), ("elixir", 1))
              for k in range(1, 6)]
    linhas.append(dict(impl="elixir", rep="rep_9", cenario="lote_200", taxa_alvo=1000, degrau_valido=False,
                       ok_carga=True, lat_p99_ms=9999))
    texto = tabela_latencia(pd.DataFrame(linhas))
    assert "| lote_200 | 1000 | 13.0 [11.0–15.0] | 23.0 [21.0–25.0] | 4.0 [2.0–6.0] | **0.008** | **0.008** |" in texto
    assert "9999" not in texto
