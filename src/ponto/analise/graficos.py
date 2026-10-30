"""Gera as figuras do artigo a partir de resultados/<cenario>/*.csv.

Uso:
    python -m ponto.analise.graficos --resultados resultados --saida figuras
    # todas as implementações e repetições de uma vez (espelha a árvore em --saida):
    python -m ponto.analise.graficos --tudo --resultados resultados --saida figuras
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

# Paleta categórica validada (ordem fixa; cor segue a entidade, não a posição)
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
TEXTO, TEXTO_2, GRADE, FUNDO = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"

CORES_CENARIO = {
    "baseline": SERIES[1], "lote_50": SERIES[2], "lote_200": SERIES[0], "lote_1000": SERIES[6],
}
ORDEM_CATEGORIAS = [
    "recusado:fila_cheia", "recusado:banco_indisponivel", "timeout", "falha_conexao",
    "processado_sem_confirmacao", "perda_silenciosa", "divergente:cascata_de_perda",
    "divergente:saida_antes_da_entrada", "divergente:ordem_invertida",
    "divergente:outro", "erro_servidor", "requisicao_invalida",
]
ROTULOS = {
    "correto": "correto",
    "recusado:fila_cheia": "recusado (fila cheia)",
    "recusado:banco_indisponivel": "recusado (banco)",
    "timeout": "timeout",
    "falha_conexao": "falha de conexão",
    "processado_sem_confirmacao": "processado sem confirmação",
    "perda_silenciosa": "perda silenciosa",
    "divergente:cascata_de_perda": "efeito cascata da perda",
    "divergente:saida_antes_da_entrada": "saída antes da entrada",
    "divergente:ordem_invertida": "ordem invertida",
    "divergente:outro": "outra divergência",
    "erro_servidor": "erro do servidor (5xx)",
    "requisicao_invalida": "requisição inválida (4xx)",
}
# cor fixa por categoria (a cor segue a categoria em todas as figuras)
COR_CATEGORIA = {
    "correto": "#c3c2b7",
    "recusado:fila_cheia": SERIES[0],
    "recusado:banco_indisponivel": SERIES[6],
    "timeout": SERIES[2],
    "falha_conexao": TEXTO_2,
    "processado_sem_confirmacao": SERIES[4],
    "perda_silenciosa": SERIES[5],
    "divergente:cascata_de_perda": SERIES[3],
    "divergente:saida_antes_da_entrada": SERIES[1],
    "divergente:ordem_invertida": SERIES[7],
    "divergente:outro": "#7a7974",
    "erro_servidor": "#3d3c39",
    "requisicao_invalida": "#a8a79f",
}
CRITERIOS = ("ok_carga", "ok_integridade", "sem_erros")


def limite(grupo: pd.DataFrame, criterio: str = "sem_erros") -> int | None:
    """Maior taxa antes do primeiro degrau reprovado; degrau com gerador inválido encerra (C3)."""
    g = grupo.sort_values("taxa_alvo")
    ok = g[criterio].astype(bool)
    if "gerador_valido" in g:
        ok &= g["gerador_valido"].astype(bool)
    ok = ok.cumprod().astype(bool)
    return int(g.taxa_alvo[ok].max()) if ok.any() else None


def _estilo() -> None:
    plt.rcParams.update({
        "figure.facecolor": FUNDO, "axes.facecolor": FUNDO,
        "axes.edgecolor": GRADE, "axes.labelcolor": TEXTO_2, "text.color": TEXTO,
        "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
        "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 9, "legend.frameon": False, "lines.linewidth": 2,
    })


def _cor(cenario: str, i: int) -> str:
    return CORES_CENARIO.get(cenario, SERIES[i % len(SERIES)])


def carregar(raiz: Path) -> pd.DataFrame:
    tabelas = [pd.read_csv(p) for p in sorted(raiz.glob("*/resumo.csv")) if p.stat().st_size]
    return pd.concat(tabelas, ignore_index=True).fillna(0) if tabelas else pd.DataFrame()


def fig_latencia(df: pd.DataFrame, saida: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 3.2))
    for i, (cen, g) in enumerate(df.groupby("cenario", sort=False)):
        cor = _cor(cen, i)
        ax.plot(g.taxa_alvo, g.lat_p99_ms, marker="o", markersize=5, color=cor, label=cen)
        if "lat_p99_todas_ms" in g:  # C4: inclui timeouts
            ax.plot(g.taxa_alvo, g.lat_p99_todas_ms, linestyle=":", linewidth=1.2, color=cor)
        if "gerador_valido" in g:  # C3: degraus em que o gerador não cumpriu a agenda
            inv = g[~g.gerador_valido.astype(bool)]
            ax.scatter(inv.taxa_alvo, inv.lat_p99_ms, s=70, facecolors=FUNDO, edgecolors=cor, zorder=4)
    ax.set_yscale("log")
    ax.set_xlabel("taxa de requisições (req/s)")
    ax.set_ylabel("latência p99 (ms, escala log)")
    if "gerador_valido" in df:
        ax.set_title("contínua: 2xx · pontilhada: todas · vazado: gerador inválido", fontsize=7, loc="left")
    ax.legend()
    fig.tight_layout()
    fig.savefig(saida / "latencia_p99.png", dpi=200)
    plt.close(fig)


def fig_correcao(df: pd.DataFrame, saida: Path) -> None:
    fig, eixos = plt.subplots(1, 2, figsize=(7, 3), sharey=True)
    for ax, coluna, titulo in zip(eixos, ["disponibilidade", "integridade"],
                                  ["Disponibilidade (requisições aceitas)", "Integridade (aceitos e corretos)"]):
        for i, (cen, g) in enumerate(df.groupby("cenario", sort=False)):
            ax.plot(g.taxa_alvo, g[coluna] * 100, marker="o", markersize=5, color=_cor(cen, i), label=cen)
        ax.set_title(titulo, fontsize=9, loc="left")
        ax.set_xlabel("taxa (req/s)")
    eixos[0].set_ylabel("%")
    eixos[1].legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(saida / "correcao.png", dpi=200)
    plt.close(fig)


def fig_mapa_erros(df: pd.DataFrame, saida: Path) -> None:
    """Barras empilhadas: composição dos erros por cenário e taxa."""
    com_erro = df[~df.sem_erros.astype(bool)].copy()
    if com_erro.empty:
        return
    cats = [c for c in ORDEM_CATEGORIAS if f"n_{c}" in com_erro]
    rotulos = [f"{c}\n{int(t)}" for c, t in zip(com_erro.cenario, com_erro.taxa_alvo)]
    fig, ax = plt.subplots(figsize=(max(5, 0.8 * len(rotulos) + 2), 3.4))
    base = pd.Series(0.0, index=com_erro.index)
    for c in cats:
        valores = com_erro[f"n_{c}"] / com_erro.registros * 100
        ax.bar(rotulos, valores, bottom=base, color=COR_CATEGORIA[c], label=ROTULOS[c],
               width=0.6, edgecolor=FUNDO, linewidth=1)
        base += valores
    ax.set_ylabel("% dos registros enviados")
    ax.tick_params(axis="x", labelsize=7)
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1, 1))
    fig.tight_layout()
    fig.savefig(saida / "mapa_de_erros.png", dpi=200)
    plt.close(fig)


def linha_do_tempo(pasta: Path) -> pd.DataFrame | None:
    """Por segundo do degrau: quantos registros terminaram em cada categoria."""
    envios = sorted(pasta.glob("envios_*.csv"))
    if not envios:
        return None
    arq = envios[0]
    e = pd.read_csv(arq)
    erros_arq = pasta / arq.name.replace("envios_", "erros_")
    erros = pd.read_csv(erros_arq) if erros_arq.stat().st_size else pd.DataFrame(columns=["id_evento", "categoria"])
    e = e.merge(erros[["id_evento", "categoria"]], on="id_evento", how="left").fillna({"categoria": "correto"})
    e["segundo"] = e.t_agendado.astype(int)
    return e.pivot_table(index="segundo", columns="categoria", values="id_evento", aggfunc="count", fill_value=0)


def fig_falha(raiz: Path, saida: Path) -> None:
    pastas = [p for p in sorted(raiz.glob("falha*")) if p.is_dir()]
    series = [(p.name, linha_do_tempo(p)) for p in pastas]
    series = [(n, s) for n, s in series if s is not None]
    if not series:
        return
    fig, eixos = plt.subplots(len(series), 1, figsize=(6, 2.4 * len(series)), sharex=True, squeeze=False)
    for ax, (nome, tab) in zip(eixos[:, 0], series):
        base = pd.Series(0, index=tab.index)
        for c in ["correto"] + ORDEM_CATEGORIAS:
            if c in tab:
                ax.bar(tab.index, tab[c], bottom=base, color=COR_CATEGORIA[c], label=ROTULOS[c],
                       width=0.9, edgecolor=FUNDO, linewidth=0.5)
                base += tab[c]
        cfg = pd.read_json(raiz / nome / "config.json", typ="series")
        if cfg.get("falha_em") is not None:
            ax.axvspan(cfg.falha_em - 0.5, cfg.falha_em + cfg.falha_seg - 0.5, color=TEXTO, alpha=0.12, zorder=3, lw=0)
        ax.set_title(nome, fontsize=9, loc="left")
        ax.set_ylabel("registros/s")
        ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1, 1))
    eixos[-1, 0].set_xlabel("segundo do teste (faixa sombreada = banco indisponível)")
    fig.tight_layout()
    fig.savefig(saida / "falha_linha_do_tempo.png", dpi=200)
    plt.close(fig)


def tabela_markdown(df: pd.DataFrame, saida: Path) -> None:
    desejadas = ["cenario", "taxa_alvo", "taxa_obtida", "atraso_gerador_p99_ms", "gerador_valido",
                 "lat_p50_ms", "lat_p99_ms", "lat_p99_todas_ms", "disponibilidade", "integridade",
                 "erros_de_carga", "erros_de_integridade", "retries", "ok_carga", "ok_integridade", "sem_erros"]
    cols = [c for c in desejadas if c in df]  # resultados antigos não têm as colunas novas
    criterios = [c for c in CRITERIOS if c in df]
    linhas = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    linhas += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for _, r in df[cols].iterrows()]
    linhas += ["", "Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):", "",
               "| cenário | " + " | ".join(criterios) + " |", "|---" * (len(criterios) + 1) + "|"]
    linhas += [f"| {c} | " + " | ".join(str(limite(g, k)) for k in criterios) + " |"
               for c, g in df.groupby("cenario", sort=False)]
    (saida / "resumo.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def gerar_figuras(resultados: Path, saida: Path) -> None:
    """Figuras de UMA pasta de resultados (resultados/<cenario>/...)."""
    saida.mkdir(parents=True, exist_ok=True)
    df = carregar(resultados)
    rampa = df[~df.cenario.str.startswith("falha")] if not df.empty else df
    if not rampa.empty:
        fig_latencia(rampa, saida)
        fig_correcao(rampa, saida)
    if not df.empty:
        fig_mapa_erros(df, saida)
        tabela_markdown(df, saida)
    fig_falha(resultados, saida)
    print(f"figuras em {saida}/: " + ", ".join(sorted(f.name for f in saida.iterdir() if f.is_file())))


def pastas_de_resultados(raiz: Path) -> list[Path]:
    """Toda pasta que contém <cenario>/resumo.csv (ex.: resultados/elixir/rep_2)."""
    return sorted({csv.parent.parent for csv in raiz.glob("**/resumo.csv")})


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--resultados", type=Path, default=Path("resultados"))
    p.add_argument("--saida", type=Path, default=Path("figuras"))
    p.add_argument("--tudo", action="store_true",
                   help="gera figuras para cada implementação/repetição, espelhando a árvore")
    a = p.parse_args()
    _estilo()
    if not a.tudo:
        gerar_figuras(a.resultados, a.saida)
        return
    for pasta in pastas_de_resultados(a.resultados):
        gerar_figuras(pasta, a.saida / pasta.relative_to(a.resultados))


if __name__ == "__main__":
    main()
