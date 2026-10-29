from datetime import date, datetime

import pytest

from ponto.dados.gerador import gerar
from ponto.nucleo.lotes import (
    bissectar,
    contar_por_rotulo,
    ordenar,
    particionar,
    resolver_desfechos,
    separar_saidas,
)
from ponto.nucleo.modelos import Aceito, Registro, Rejeitado
from ponto.nucleo.referencia import desfechos_esperados
from ponto.nucleo.validacao import criar_validador, interpretar, regras_padrao

CADASTRO = frozenset(range(1, 101))
validar = criar_validador(regras_padrao(CADASTRO))


def reg(id_evento="a", servidor=1, tipo="entrada", hora=8, minuto=0):
    return Registro(id_evento, servidor, tipo, datetime(2026, 11, 3, hora, minuto), "rep-1")


# ------------------------------------------------------------- interpretar

def test_interpretar_payload_valido():
    r = interpretar({"id_evento": "x", "servidor": 5, "tipo": "entrada",
                     "instante": "2026-11-03T08:00:00", "dispositivo": "d"})
    assert r == Registro("x", 5, "entrada", datetime(2026, 11, 3, 8), "d")


@pytest.mark.parametrize("payload", [
    None, [], {}, {"id_evento": "x"},
    {"id_evento": "x", "servidor": "5", "tipo": "entrada", "instante": "2026-11-03T08:00:00", "dispositivo": "d"},
    {"id_evento": "x", "servidor": True, "tipo": "entrada", "instante": "2026-11-03T08:00:00", "dispositivo": "d"},
    {"id_evento": "x", "servidor": 5, "tipo": "entrada", "instante": "ontem", "dispositivo": "d"},
])
def test_interpretar_payload_invalido(payload):
    assert interpretar(payload) is None


# ---------------------------------------------------------------- validar

@pytest.mark.parametrize("registro, esperado", [
    (reg(), None),
    (reg(tipo="saida"), None),
    (reg(tipo="intervalo"), "tipo_invalido"),
    (reg(servidor=999), "servidor_inexistente"),
    (reg(hora=3), "fora_da_jornada"),
    (reg(tipo="xyz", servidor=999, hora=3), "tipo_invalido"),  # primeira regra vence
])
def test_validar(registro, esperado):
    match validar(registro):
        case Aceito():
            assert esperado is None
        case Rejeitado(motivo=m):
            assert m == esperado


# ------------------------------------------------------------------ lotes

def test_particionar_mantem_ordem_e_tamanho():
    blocos = particionar(list(range(1050)), 100)
    assert [x for b in blocos for x in b] == list(range(1050))
    assert all(len(b) <= 100 for b in blocos)
    assert len(blocos) == 11


def test_particionar_grande_nao_estoura_recursao():
    assert len(particionar(range(1_000_000), 1)) == 1_000_000


def test_bissectar():
    assert bissectar([1, 2, 3]) == ([1], [2, 3])


def test_separar_saidas():
    s1, s2 = reg("s1", 1, "saida", 12), reg("s2", 2, "saida", 12)
    com, sem = separar_saidas([s1, s2], frozenset({(1, date(2026, 11, 3))}))
    assert com == [s1] and sem == [s2]


def test_resolver_desfechos():
    resultados = ordenar([
        Aceito(reg("b", minuto=1)),
        Aceito(reg("a")),
        Rejeitado(reg("c", tipo="x"), "tipo_invalido"),
        Aceito(reg("d", tipo="saida", hora=12)),
    ])
    finais = resolver_desfechos(resultados, inseridos={"a"}, sem_entrada={"d"})
    assert {d.id_evento: d.rotulo for d in finais} == {
        "a": "gravado",
        "b": "descartado:duplicado",
        "c": "rejeitado:tipo_invalido",
        "d": "rejeitado:saida_sem_entrada",
    }


# ------------------------------------------------- gabarito × oráculo

def test_gabarito_do_gerador_coincide_com_oraculo():
    """Duas especificações independentes devem concordar."""
    base = gerar(3000, taxa_anomalia=0.3, seed=7)
    oraculo = desfechos_esperados(base.registros, regras_padrao(frozenset(range(1, 3001))))
    assert oraculo == base.gabarito


def test_gerador_reprodutivel():
    assert gerar(500, seed=1).gabarito == gerar(500, seed=1).gabarito


def test_gerador_cobre_todas_as_anomalias():
    rotulos = contar_por_rotulo(gerar(5000, taxa_anomalia=0.2).gabarito.values())
    assert set(rotulos) == {
        "gravado", "descartado:duplicado", "rejeitado:tipo_invalido",
        "rejeitado:fora_da_jornada", "rejeitado:servidor_inexistente",
        "rejeitado:saida_sem_entrada",
    }
