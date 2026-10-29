from datetime import datetime

from ponto.dados.reconciliacao import Envio, reconciliar, resumir
from ponto.nucleo.modelos import Desfecho, Registro
from ponto.nucleo.validacao import regras_padrao

REGRAS = regras_padrao(frozenset({1, 2}))


def reg(i, servidor, tipo, hora):
    return Registro(i, servidor, tipo, datetime(2026, 11, 3, hora), "d")


def envio(i, status, erro=""):
    return Envio(i, 0.0, 0.0, 0.01, status, erro)


E1, S1 = reg("e1", 1, "entrada", 8), reg("s1", 1, "saida", 12)
E2, S2 = reg("e2", 2, "entrada", 8), reg("s2", 2, "saida", 12)
REGS = [E1, S1, E2, S2]
GABARITO = {r.id_evento: Desfecho(r.id_evento, "gravado") for r in REGS}


def categorias(envios, banco):
    return {a.id_evento: a.categoria for a in reconciliar(REGS, GABARITO, envios, banco, REGRAS)}


def test_tudo_correto():
    cats = categorias([envio(r.id_evento, 202) for r in REGS], GABARITO)
    assert set(cats.values()) == {"correto"}


def test_recusa_nao_e_erro_de_integridade_e_ajusta_o_esperado():
    """Se a entrada foi recusada (503), rejeitar a saída é o correto."""
    envios = [envio("e1", 503, "fila_cheia"), envio("s1", 202), envio("e2", 202), envio("s2", 202)]
    banco = {**GABARITO, "s1": Desfecho("s1", "rejeitado", "saida_sem_entrada")}
    del banco["e1"]
    cats = categorias(envios, banco)
    assert cats["e1"] == "recusado:fila_cheia"
    assert cats["s1"] == "correto"
    r = resumir(reconciliar(REGS, GABARITO, envios, banco, REGRAS))
    assert r["erros_de_carga"] == 1 and r["erros_de_integridade"] == 0


def test_perda_silenciosa_e_cascata():
    """Entrada aceita (202) mas ausente no banco: a saída rejeitada é efeito cascata."""
    envios = [envio(r.id_evento, 202) for r in REGS]
    banco = {**GABARITO, "s1": Desfecho("s1", "rejeitado", "saida_sem_entrada")}
    del banco["e1"]
    cats = categorias(envios, banco)
    assert cats["e1"] == "perda_silenciosa"
    assert cats["s1"] == "divergente:cascata_de_perda"


def test_saida_antes_da_entrada_por_concorrencia():
    envios = [envio(r.id_evento, 202) for r in REGS]
    banco = {**GABARITO, "s2": Desfecho("s2", "rejeitado", "saida_sem_entrada")}
    assert categorias(envios, banco)["s2"] == "divergente:saida_antes_da_entrada"


def test_processado_sem_confirmacao():
    envios = [envio("e1", "timeout")] + [envio(r.id_evento, 202) for r in REGS[1:]]
    assert categorias(envios, GABARITO)["e1"] == "processado_sem_confirmacao"
