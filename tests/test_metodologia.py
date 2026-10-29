"""Testes das correções metodológicas (docs/metodologia.md)."""
from ponto.carga.experimento import avaliar_degrau, limite
from ponto.dados.reconciliacao import Avaliacao, resumir


def degrau(taxa, sem_erros=True, ok_carga=True, ok_integridade=True, gerador_valido=True):
    return dict(taxa_alvo=taxa, sem_erros=sem_erros, ok_carga=ok_carga,
                ok_integridade=ok_integridade, gerador_valido=gerador_valido)


def test_limite_para_no_primeiro_degrau_que_falha():
    rs = [degrau(100), degrau(500), degrau(1000, sem_erros=False), degrau(1500)]
    assert limite(rs, "sem_erros") == 500


def test_limite_ignora_degraus_com_gerador_invalido():
    """C3: se o gerador não cumpriu a agenda, o degrau não mede a API."""
    rs = [degrau(1000), degrau(2000, gerador_valido=False), degrau(3000)]
    assert limite(rs, "ok_carga") == 1000


def test_criterios_separados():
    """C5: um degrau pode passar em carga e falhar em integridade."""
    rs = [degrau(100), degrau(500, ok_integridade=False)]
    assert limite(rs, "ok_carga") == 500 and limite(rs, "ok_integridade") == 100


def a(cat):
    return Avaliacao("x", cat, "", "", "")


def test_ordem_invertida_dentro_da_tolerancia_nao_reprova_integridade():
    r = resumir([a("correto")] * 99_999 + [a("divergente:ordem_invertida")])
    assert r["erros_de_integridade_sem_ordem"] == 0
    assert avaliar_degrau(r, 1e-4) == {"ok_carga": True, "ok_integridade": True}
    assert r["sem_erros"] is False  # o critério estrito continua disponível


def test_perda_silenciosa_sempre_reprova_integridade():
    r = resumir([a("correto")] * 99_999 + [a("perda_silenciosa")])
    assert avaliar_degrau(r, 1e-4)["ok_integridade"] is False


def test_processado_sem_confirmacao_e_erro_de_carga():
    """C1: o cliente viu erro; do ponto de vista dele a requisição não foi aceita."""
    r = resumir([a("correto"), a("processado_sem_confirmacao")])
    assert r["erros_de_carga"] == 1 and r["disponibilidade"] == 0.5 and r["integridade"] == 1.0
