"""Compara as implementações a partir de resultados/<impl>/[rep_<k>/]<cenario>/resumo.csv.

Uso:
    python -m ponto.analise.comparar --resultados resultados --saida figuras/comparacao
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .graficos import FUNDO, GRADE, SERIES, TEXTO, TEXTO_2, _estilo, limite  # noqa: E402

IMPLEMENTACOES = {"python_imperativo": SERIES[1], "python_funcional": SERIES[0], "elixir": SERIES[6]}
CRITERIOS = ("ok_carga", "ok_integridade", "sem_erros")


def _rep(csv: Path) -> str:
    pai = csv.parent.parent.name
    return pai if pai.startswith("rep_") else "rep_1"


def carregar(raiz: Path) -> pd.DataFrame:
    """Aceita resultados/<impl>/<cenario>/ e resultados/<impl>/rep_<k>/<cenario>/."""
    tabelas = [
        pd.read_csv(csv).assign(impl=impl, rep=_rep(csv))
        for impl in IMPLEMENTACOES
        for csv in sorted((raiz / impl).glob("**/resumo.csv"))
    ]
    return pd.concat(tabelas, ignore_index=True) if tabelas else pd.DataFrame()


def celula(g: pd.DataFrame, criterio: str) -> str:
    """Mediana entre repetições, com mínimo e máximo quando há mais de uma (C9)."""
    if g.empty:
        return "-"
    # repetição sem nenhum degrau aprovado conta como 0, para não inflar a mediana
    lims = pd.Series([limite(r, criterio) or 0 for _, r in g.groupby("rep")], dtype="float")
    if (lims == 0).all():
        return "nenhum"
    if len(lims) == 1:
        return f"{lims.iloc[0]:.0f}"
    return f"{lims.median():.0f} [{lims.min():.0f}–{lims.max():.0f}] (n={len(lims)})"


def tabela(df: pd.DataFrame, criterio: str) -> str:
    linhas = ["| cenário | " + " | ".join(IMPLEMENTACOES) + " |", "|---" * (len(IMPLEMENTACOES) + 1) + "|"]
    for cenario, g in df.groupby("cenario"):
        valores = [celula(g[g.impl == impl], criterio) for impl in IMPLEMENTACOES]
        linhas.append(f"| {cenario} | " + " | ".join(valores) + " |")
    return "\n".join(linhas)


def tabela_validade(df: pd.DataFrame) -> str:
    """Quantos degraus de cada implementação foram invalidados e por quê (C13).
    Vai para os resultados finais: um limite só é comparável se os degraus valem."""
    if "degrau_valido" not in df:
        return "_resultados anteriores a C13: sem informação de validade por degrau_\n"
    vazio = pd.Series("", index=df.index)
    d = df.assign(
        incidente=(df["incidente"] if "incidente" in df else vazio).fillna("").astype(str).replace("0", ""),
        perdidos=(df["perdidos_servidor"] if "perdidos_servidor" in df else vazio.replace("", 0)).fillna(0),
    )
    motivos = ["api_reiniciou", "fila_nao_drenou", "gerador_atrasou", "falha_execucao"]
    linhas = ["| implementação | degraus | válidos | " + " | ".join(motivos) + " | registros perdidos pela fila |",
              "|---" * (len(motivos) + 4) + "|"]
    for impl in IMPLEMENTACOES:
        g = d[d.impl == impl]
        if g.empty:
            continue
        contagens = [str(int(g.incidente.str.contains(m).sum())) for m in motivos]
        linhas.append(f"| {impl} | {len(g)} | {int(g.degrau_valido.astype(bool).sum())} | "
                      + " | ".join(contagens) + f" | {int(g.perdidos.astype(float).sum())} |")
    detalhes = d[d.incidente != ""]
    if not detalhes.empty:
        linhas += ["", "Degraus inválidos:", "", "| implementação | repetição | cenário | taxa | motivo |",
                   "|---|---|---|---|---|"]
        linhas += [f"| {r.impl} | {r.rep} | {r.cenario} | {r.taxa_alvo} | {r.incidente} |"
                   for r in detalhes.itertuples()]
    return "\n".join(linhas) + "\n"


# motivo principal de um degrau inválido, na ordem de gravidade; cor fixa por motivo
MOTIVOS = {
    "falha_execucao": ("interrompido (API fora)", SERIES[3]),
    "api_reiniciou": ("API reiniciou", SERIES[0]),
    "fila_nao_drenou": ("fila não esvaziou", SERIES[1]),
    "gerador_atrasou": ("gerador atrasou", SERIES[2]),
}
COR_VALIDO = "#c3c2b7"


def motivo_principal(incidente: str) -> str:
    return next((m for m in MOTIVOS if m in str(incidente)), "valido")


def figura_validade(df: pd.DataFrame, saida: Path) -> None:
    """Degraus válidos e inválidos por implementação (C13): mostra no artigo se a API caiu,
    se a fila não esvaziou ou se o gerador não cumpriu a agenda, e quantas vezes."""
    if "degrau_valido" not in df:
        return
    inc = df["incidente"] if "incidente" in df else pd.Series("", index=df.index)
    d = df.assign(motivo=inc.fillna("").map(motivo_principal))
    impls = [i for i in IMPLEMENTACOES if (d.impl == i).any()]
    categorias = [("valido", "válido", COR_VALIDO)] + [(m, r, c) for m, (r, c) in MOTIVOS.items()]

    fig, ax = plt.subplots(figsize=(6.4, 0.7 * len(impls) + 1.4))
    for y, impl in enumerate(impls):
        g = d[d.impl == impl]
        x = 0
        for chave, _, cor in categorias:
            n = int((g.motivo == chave).sum())
            if n:
                ax.barh(y, n, left=x, height=0.5, color=cor, edgecolor=FUNDO, linewidth=2)
                x += n
        invalidos = int((g.motivo != "valido").sum())
        ax.text(x, y, f"  {invalidos} de {len(g)} inválidos" if invalidos else "  todos válidos",
                va="center", fontsize=8, color=TEXTO_2)
    ax.set_yticks(range(len(impls)), impls, color=TEXTO)
    ax.invert_yaxis()
    ax.set_xlabel("degraus executados (todas as repetições e cenários)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, d.groupby("impl").size().max() * 1.35)
    presentes = [(r, c) for k, r, c in categorias if (d.motivo == k).any()]
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for _, c in presentes],
              labels=[r for r, _ in presentes], fontsize=7, loc="upper center",
              bbox_to_anchor=(0.5, -0.3), ncol=min(3, len(presentes)), frameon=False)
    ax.set_title("Validade da execução: degraus que valem para o limite", fontsize=9, loc="left")
    fig.tight_layout()
    fig.savefig(saida / "validade.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def figura_p99(df: pd.DataFrame, saida: Path) -> None:
    cenarios = sorted(c for c in df.cenario.unique() if not c.startswith("falha"))
    fig, eixos = plt.subplots(1, len(cenarios), figsize=(4 * len(cenarios), 3.6), sharey=True, squeeze=False)
    for ax, cenario in zip(eixos[0], cenarios):
        for impl, cor in IMPLEMENTACOES.items():
            g = df[(df.cenario == cenario) & (df.impl == impl)]
            if "degrau_valido" in g:  # degrau inválido não entra na mediana (C13)
                g = g[g.degrau_valido.astype(bool)]
            if len(g):
                mediana = g.groupby("taxa_alvo").lat_p99_ms.median()
                ax.plot(mediana.index, mediana.values, marker="o", color=cor, label=impl)
        ax.set_title(cenario)
        ax.set_xlabel("taxa alvo (req/s)")
        ax.set_yscale("log")
        ax.grid(alpha=0.3)
    eixos[0][0].set_ylabel("latência p99 (ms), mediana das repetições")
    eixos[0][-1].legend()
    fig.tight_layout()
    fig.savefig(saida / "comparacao_p99.png", dpi=150)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--resultados", type=Path, default=Path("resultados"))
    p.add_argument("--saida", type=Path, default=Path("figuras/comparacao"))
    a = p.parse_args()
    df = carregar(a.resultados)
    if df.empty:
        raise SystemExit(f"nenhum resumo.csv em {a.resultados}/<impl>/")
    # resultados antigos (antes de C5) só têm sem_erros
    criterios = [c for c in CRITERIOS if c in df]
    a.saida.mkdir(parents=True, exist_ok=True)
    _estilo()
    figura_p99(df, a.saida)
    figura_validade(df, a.saida)
    texto = "".join(f"## Limite (req/s), critério `{c}`\n\n{tabela(df, c)}\n\n" for c in criterios)
    texto += f"## Validade da execução (C13)\n\n{tabela_validade(df)}\n"
    (a.saida / "comparacao.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
