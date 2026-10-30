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

from .graficos import SERIES, limite  # noqa: E402

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


def figura_p99(df: pd.DataFrame, saida: Path) -> None:
    cenarios = sorted(c for c in df.cenario.unique() if not c.startswith("falha"))
    fig, eixos = plt.subplots(1, len(cenarios), figsize=(4 * len(cenarios), 3.6), sharey=True, squeeze=False)
    for ax, cenario in zip(eixos[0], cenarios):
        for impl, cor in IMPLEMENTACOES.items():
            g = df[(df.cenario == cenario) & (df.impl == impl)]
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
    figura_p99(df, a.saida)
    texto = "".join(f"## Limite (req/s), critério `{c}`\n\n{tabela(df, c)}\n\n" for c in criterios)
    (a.saida / "comparacao.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
