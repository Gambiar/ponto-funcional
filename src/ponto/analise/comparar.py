"""Compara as implementações a partir de resultados/<impl>/<cenario>/resumo.csv.

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

from .graficos import SERIES  # noqa: E402

IMPLEMENTACOES = {"python_imperativo": SERIES[1], "python_funcional": SERIES[0], "elixir": SERIES[6]}


def carregar(raiz: Path) -> pd.DataFrame:
    tabelas = [
        pd.read_csv(csv).assign(impl=impl)
        for impl in IMPLEMENTACOES
        for csv in sorted((raiz / impl).glob("*/resumo.csv"))
    ]
    return pd.concat(tabelas, ignore_index=True) if tabelas else pd.DataFrame()


def limite(grupo: pd.DataFrame) -> float | None:
    ok = grupo.sort_values("taxa_alvo")
    primeiro_erro = ok.index[~ok["sem_erros"].astype(bool)]
    antes = ok.loc[: primeiro_erro[0]].iloc[:-1] if len(primeiro_erro) else ok
    return antes["taxa_alvo"].max() if len(antes) else None


def tabela(df: pd.DataFrame) -> str:
    linhas = ["| cenário | " + " | ".join(IMPLEMENTACOES) + " |", "|---" * (len(IMPLEMENTACOES) + 1) + "|"]
    for cenario, g in df.groupby("cenario"):
        valores = [limite(g[g.impl == impl]) if (g.impl == impl).any() else "-" for impl in IMPLEMENTACOES]
        linhas.append(f"| {cenario} | " + " | ".join(str(v) for v in valores) + " |")
    return "\n".join(linhas)


def figura_p99(df: pd.DataFrame, saida: Path) -> None:
    cenarios = sorted(c for c in df.cenario.unique() if not c.startswith("falha"))
    fig, eixos = plt.subplots(1, len(cenarios), figsize=(4 * len(cenarios), 3.6), sharey=True, squeeze=False)
    for ax, cenario in zip(eixos[0], cenarios):
        for impl, cor in IMPLEMENTACOES.items():
            g = df[(df.cenario == cenario) & (df.impl == impl)].sort_values("taxa_alvo")
            if len(g):
                ax.plot(g.taxa_alvo, g.lat_p99_ms, marker="o", color=cor, label=impl)
        ax.set_title(cenario)
        ax.set_xlabel("taxa alvo (req/s)")
        ax.set_yscale("log")
        ax.grid(alpha=0.3)
    eixos[0][0].set_ylabel("latência p99 (ms)")
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
    a.saida.mkdir(parents=True, exist_ok=True)
    figura_p99(df, a.saida)
    texto = "Limite sem erros (req/s) por implementação:\n\n" + tabela(df) + "\n"
    (a.saida / "comparacao.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
