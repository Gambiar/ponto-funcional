"""Testes baseados em propriedades (Hypothesis).

Em vez de exemplos fixos, o Hypothesis gera milhares de entradas aleatórias
e verifica propriedades que devem valer para todas elas.
"""
from datetime import datetime, timedelta

from hypothesis import given, settings
from hypothesis import strategies as st

from ponto.nucleo.lotes import particionar
from ponto.nucleo.modelos import Registro
from ponto.nucleo.referencia import desfechos_esperados
from ponto.nucleo.validacao import regras_padrao

CADASTRO = frozenset(range(1, 21))
REGRAS = regras_padrao(CADASTRO)
BASE = datetime(2026, 11, 3)

registros = st.builds(
    Registro,
    id_evento=st.uuids().map(str),
    servidor=st.integers(1, 25),
    tipo=st.sampled_from(["entrada", "saida", "xyz"]),
    instante=st.integers(0, 24 * 60 - 1).map(lambda m: BASE + timedelta(minutes=m)),
    dispositivo=st.just("rep"),
)
listas = st.lists(registros, max_size=60, unique_by=lambda r: r.id_evento)


@given(st.lists(st.integers(), max_size=500), st.integers(1, 50))
def test_particionar_preserva_elementos(itens, tamanho):
    blocos = particionar(itens, tamanho)
    assert [x for b in blocos for x in b] == itens
    assert all(1 <= len(b) <= tamanho for b in blocos)


@given(listas)
def test_todo_registro_tem_exatamente_um_desfecho(regs):
    assert set(desfechos_esperados(regs, REGRAS)) == {r.id_evento for r in regs}


@given(listas)
def test_no_maximo_um_gravado_por_chave(regs):
    """Idempotência: nunca há duas gravações para o mesmo servidor, tipo e dia."""
    d = desfechos_esperados(regs, REGRAS)
    gravadas = [r.chave for r in regs if d[r.id_evento].desfecho == "gravado"]
    assert len(gravadas) == len(set(gravadas))


@given(listas)
def test_reenvio_nao_regrava_chave_ja_gravada(regs):
    """Reenviar tudo (novos IDs, mesmos dados) nunca grava de novo uma chave já gravada.

    Obs.: o reenvio PODE gravar algo novo — ex.: saída rejeitada por chegar no mesmo
    instante que a entrada, mas ordenada antes dela; o reenvio 1 s depois é válido.
    """
    reenvio = [Registro(r.id_evento + "-r", r.servidor, r.tipo, r.instante + timedelta(seconds=1), r.dispositivo)
               for r in regs]
    d = desfechos_esperados(regs + reenvio, REGRAS)
    originais = {r.chave for r in regs if d[r.id_evento].desfecho == "gravado"}
    assert not any(d[r.id_evento].desfecho == "gravado" and r.chave in originais for r in reenvio)


def test_reenvio_pode_gravar_saida_antes_rejeitada():
    """Contraexemplo da propriedade ingênua 'reenvio não grava nada novo'."""
    t = BASE.replace(hour=9)
    regs = [Registro("a", 1, "saida", t, "r"), Registro("b", 1, "entrada", t, "r")]
    reenvio = [Registro(r.id_evento + "-r", r.servidor, r.tipo, r.instante + timedelta(seconds=1), r.dispositivo)
               for r in regs]
    d = desfechos_esperados(regs + reenvio, REGRAS)
    assert d["a"].rotulo == "rejeitado:saida_sem_entrada" and d["a-r"].rotulo == "gravado"


@given(listas)
@settings(max_examples=200)
def test_resultado_independe_da_ordem_de_chegada(regs):
    """O oráculo ordena cronologicamente; a ordem da lista não importa."""
    assert desfechos_esperados(regs, REGRAS) == desfechos_esperados(list(reversed(regs)), REGRAS)
