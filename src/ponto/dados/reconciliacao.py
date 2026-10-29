"""Reconciliação: compara o que foi enviado, o que o cliente recebeu e o que
ficou no banco, e classifica cada registro numa taxonomia de erros.

Duas referências de "esperado":
- gabarito original: desfecho previsto pelo gerador, supondo entrega total;
- gabarito ajustado: o oráculo recalculado só sobre os registros que de fato
  chegaram ao sistema. Separa erros de carga (o registro nem entrou) de erros
  de integridade (entrou e foi processado errado ou se perdeu).
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace

from ..nucleo.modelos import Desfecho, Registro
from ..nucleo.referencia import desfechos_esperados
from ..nucleo.validacao import Regra

SUCESSO = (201, 202)

# Categoria -> componente onde o erro se manifesta (para o mapeamento)
COMPONENTE = {
    "correto": "-",
    "recusado:fila_cheia": "fila (back-pressure)",
    "recusado:banco_indisponivel": "banco",
    "timeout": "API (saturação)",
    "falha_conexao": "API (saturação)",
    "erro_servidor": "API",
    "requisicao_invalida": "API",
    "processado_sem_confirmacao": "API (resposta perdida)",
    "perda_silenciosa": "persistência",
    "divergente:ordem_invertida": "concorrência",
    "divergente:saida_antes_da_entrada": "concorrência",
    "divergente:cascata_de_perda": "persistência",
    "divergente:outro": "regra de negócio",
}

# Categorias que significam dado errado ou perdido sem o cliente saber
ERROS_DE_INTEGRIDADE = {"perda_silenciosa", "divergente:ordem_invertida", "divergente:cascata_de_perda",
                        "divergente:saida_antes_da_entrada", "divergente:outro"}


@dataclass(frozen=True, slots=True)
class Envio:
    """Resultado de uma requisição, do ponto de vista do cliente."""
    id_evento: str
    t_agendado: float   # segundos desde o início do degrau
    t_envio: float
    latencia: float     # segundos entre envio e resposta (ou desistência)
    status: int | str   # código HTTP, "timeout" ou "conexao"
    erro: str = ""      # campo "erro" do corpo da resposta, se houver


@dataclass(frozen=True, slots=True)
class Avaliacao:
    id_evento: str
    categoria: str
    esperado: str
    ajustado: str
    obtido: str


def _divergencia(ajustado: Desfecho, obtido: Desfecho) -> str:
    match (ajustado.rotulo, obtido.rotulo):
        case ("gravado", "descartado:duplicado") | ("descartado:duplicado", "gravado"):
            return "divergente:ordem_invertida"
        case ("gravado", "rejeitado:saida_sem_entrada"):
            return "divergente:saida_antes_da_entrada"
        case _:
            return "divergente:outro"


def categorizar(envio: Envio, obtido: Desfecho | None, ajustado: Desfecho | None) -> str:
    match (envio.status, obtido):
        case (int(s), None) if s in SUCESSO:
            return "perda_silenciosa"
        case (int(s), Desfecho() as d) if s in SUCESSO:
            return "correto" if d.rotulo == ajustado.rotulo else _divergencia(ajustado, d)
        case (_, Desfecho()):
            return "processado_sem_confirmacao"
        case (503, None):
            return f"recusado:{envio.erro or 'fila_cheia'}"
        case ("timeout", None):
            return "timeout"
        case ("conexao", None):
            return "falha_conexao"
        case (int(s), None) if 400 <= s < 500:
            return "requisicao_invalida"
        case _:
            return "erro_servidor"


def reconciliar(
    registros: Iterable[Registro],
    gabarito: Mapping[str, Desfecho],
    envios: Iterable[Envio],
    banco: Mapping[str, Desfecho],
    regras: list[Regra],
) -> list[Avaliacao]:
    regs = list(registros)
    por_id = {e.id_evento: e for e in envios}
    chegaram = [r for r in regs if r.id_evento in banco
                or (isinstance(por_id[r.id_evento].status, int) and por_id[r.id_evento].status in SUCESSO)]
    ajustado = desfechos_esperados(chegaram, regras)

    def avaliar(r: Registro) -> Avaliacao:
        obtido, aj = banco.get(r.id_evento), ajustado.get(r.id_evento)
        return Avaliacao(
            r.id_evento,
            categorizar(por_id[r.id_evento], obtido, aj),
            gabarito[r.id_evento].rotulo,
            aj.rotulo if aj else "",
            obtido.rotulo if obtido else "",
        )

    avaliacoes = list(map(avaliar, regs))

    # Divergência num servidor que teve perda silenciosa é consequência da
    # perda (ex.: a entrada sumiu, então a saída foi rejeitada), não de concorrência.
    servidor = {r.id_evento: r.servidor for r in regs}
    com_perda = {servidor[a.id_evento] for a in avaliacoes if a.categoria == "perda_silenciosa"}

    def atribuir_causa(a: Avaliacao) -> Avaliacao:
        match a:
            case Avaliacao(categoria=c) if c.startswith("divergente:") and servidor[a.id_evento] in com_perda:
                return replace(a, categoria="divergente:cascata_de_perda")
            case _:
                return a

    return list(map(atribuir_causa, avaliacoes))


def resumir(avaliacoes: Iterable[Avaliacao]) -> dict[str, float | int]:
    lista = list(avaliacoes)
    total = len(lista)
    cats = Counter(a.categoria for a in lista)
    integridade_erros = sum(cats[c] for c in ERROS_DE_INTEGRIDADE)
    # aceitos = cliente recebeu 2xx; o resto (inclusive processado_sem_confirmacao,
    # em que o cliente viu erro) é erro de carga do ponto de vista do cliente
    aceitos = cats["correto"] + integridade_erros
    return {
        "registros": total,
        "corretos": cats["correto"],
        "erros_de_carga": total - aceitos,
        "erros_de_integridade": integridade_erros,
        "acerto_gabarito": round(sum(a.obtido == a.esperado for a in lista) / total, 6) if total else 0,
        "disponibilidade": round(aceitos / total, 6) if total else 0,
        "integridade": round(1 - integridade_erros / aceitos, 6) if aceitos else 0,
        "taxa_erro_integridade": round(integridade_erros / aceitos, 8) if aceitos else 0,
        # ordem_invertida é dominada pela compressão de tempo do experimento (ver docs/metodologia.md, C6)
        "erros_de_integridade_sem_ordem": integridade_erros - cats["divergente:ordem_invertida"],
        "sem_erros": cats["correto"] == total,
        **{f"n_{c}": n for c, n in sorted(cats.items()) if c != "correto"},
    }
