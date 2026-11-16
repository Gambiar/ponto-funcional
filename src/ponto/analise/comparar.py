"""Compara as implementações a partir de resultados/<impl>/[rep_<k>/]<cenario>/resumo.csv.

Uso:
    python -m ponto.analise.comparar --resultados resultados --saida figuras/comparacao
"""
from __future__ import annotations

import argparse
import json
import shutil
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from ..carga.experimento import SATURACAO_MIN  # noqa: E402
from .graficos import FUNDO, GRADE, SERIES, TEXTO, TEXTO_2, _estilo, limite  # noqa: E402

IMPLEMENTACOES = {"python_imperativo": SERIES[1], "python_funcional": SERIES[0], "elixir": SERIES[6]}
CRITERIOS = ("ok_carga", "ok_integridade", "sem_erros")


def _rep(csv: Path) -> str:
    pai = csv.parent.parent.name
    return pai if pai.startswith("rep_") else "rep_1"


def carregar(raiz: Path) -> pd.DataFrame:
    """Aceita resultados/<impl>/<cenario>/ e resultados/<impl>/rep_<k>/<cenario>/."""
    tabelas = [
        pd.read_csv(csv).assign(impl=impl, rep=_rep(csv), pasta=str(csv.parent))
        for impl in IMPLEMENTACOES
        for csv in sorted((raiz / impl).glob("**/resumo.csv"))
    ]
    return pd.concat(tabelas, ignore_index=True) if tabelas else pd.DataFrame()


# ------------------------------------------------------------ reanálise da largada (C16)

COLUNA_LARGADA = "atraso_p99_apos_largada_ms"
COLUNA_LAT = "lat_p99_apos_largada_ms"  # p99 das 2xx sem a largada; substitui lat_p99_ms na reanálise


def apos_largada(envios: Path, largada_s: float) -> tuple[float | None, float | None]:
    """(atraso p99 do gerador, latência p99 das 2xx), em ms, só com os registros agendados
    depois de `largada_s`. (None, None) se o arquivo não existe ou está vazio."""
    if not envios.exists() or envios.stat().st_size == 0:
        return None, None
    e = pd.read_csv(envios, usecols=["t_agendado", "t_envio", "latencia", "status"])
    e = e[e.t_agendado >= largada_s]
    if e.empty:
        return None, None
    ok = e[e.status.astype(str).isin(["201", "202"])]
    atraso = round(float((e.t_envio - e.t_agendado).quantile(0.99)) * 1000, 1)
    return atraso, (round(float(ok.latencia.quantile(0.99)) * 1000, 1) if len(ok) else None)


def _atraso_max(pasta: Path) -> float:
    try:
        return float(json.loads((pasta / "config.json").read_text(encoding="utf-8")).get("atraso_max_ms", 20.0))
    except (OSError, ValueError):
        return 20.0


def revalidar(df: pd.DataFrame, largada_s: float) -> pd.DataFrame:
    """Refaz `degrau_valido` medindo o atraso do gerador depois dos `largada_s` iniciais.

    Antes de C16 o gerador em vários processos saía num surto atrasado no começo do degrau
    (a agenda chegava aos processos depois do instante zero), e só isso estourava o p99.
    A coluna `atraso_p99_apos_largada_ms` é lida do resumo quando já existe (resultados
    arquivados sem os envios) e calculada dos envios_<taxa>.csv quando não existe. Os
    demais motivos de invalidade (API reiniciou, fila não drenou, falha de execução) ficam.
    Os valores originais ficam em `degrau_valido_original` e `incidente_original`.
    """
    if df.empty or "degrau_valido" not in df:
        return df
    d = df.copy()
    for coluna in (COLUNA_LARGADA, COLUNA_LAT):
        if coluna not in d:
            d[coluna] = float("nan")
    faltam = d[COLUNA_LARGADA].isna() & ~d.incidente.fillna("").astype(str).str.contains("falha_execucao")
    medidas = [apos_largada(Path(r.pasta) / f"envios_{int(r.taxa_alvo)}.csv", largada_s)
               for r in d[faltam].itertuples()]
    if medidas:
        d.loc[faltam, COLUNA_LARGADA] = [m[0] for m in medidas]
        d.loc[faltam, COLUNA_LAT] = [m[1] for m in medidas]
    limite_ms = d.pasta.map(lambda p: _atraso_max(Path(p)))
    atrasou = ~(d[COLUNA_LARGADA].astype(float) <= limite_ms)  # NaN (sem envios) -> atrasou
    carga = d.get("erros_de_carga", pd.Series(0, index=d.index)).fillna(0).astype(float)
    registros = d.get("registros", pd.Series(0, index=d.index)).fillna(0).astype(float)
    tem_envios = d[COLUNA_LARGADA].notna()
    saturou = atrasou & tem_envios & (registros > 0) & (carga >= SATURACAO_MIN * registros)  # C17
    gerador_ok = ~atrasou | saturou
    incidente = d.incidente.fillna("").astype(str).replace("0", "")
    falha = incidente.str.contains("falha_execucao")
    d["api_saturou"] = saturou
    for coluna in ("degrau_valido", "gerador_valido", "incidente"):
        d[f"{coluna}_original"] = incidente if coluna == "incidente" else d[coluna]
    d["gerador_valido"] = gerador_ok
    sim = pd.Series(True, index=d.index)  # colunas que só existem depois de C13
    d["degrau_valido"] = (gerador_ok & d.get("drenou", sim).astype(bool)
                          & d.get("api_sem_reinicio", sim).astype(bool) & ~falha)

    def motivos(inc: str, ok: bool, interrompido: bool) -> str:
        outros = [m for m in inc.split("; ") if m and m != "gerador_atrasou"]
        return "; ".join(outros + ([] if ok or interrompido else ["gerador_atrasou"]))

    d["incidente"] = [motivos(i, ok, f) for i, ok, f in zip(incidente, gerador_ok, falha)]
    return d


def tabela_revalidacao(d: pd.DataFrame, largada_s: float) -> str:
    """Quantos degraus mudaram de situação com a reanálise, por implementação."""
    linhas = [f"Atraso p99 do gerador medido só depois dos {largada_s:g} s iniciais de cada degrau (C16).",
              "", "| implementação | degraus | válidos (original) | válidos (reanálise) | revalidados |",
              "|---|---|---|---|---|"]
    for impl in IMPLEMENTACOES:
        g = d[d.impl == impl]
        if g.empty:
            continue
        antes, depois = g.degrau_valido_original.astype(bool), g.degrau_valido.astype(bool)
        linhas.append(f"| {impl} | {len(g)} | {int(antes.sum())} | {int(depois.sum())} | {int((depois & ~antes).sum())} |")
    return "\n".join(linhas) + "\n"


def exportar(d: pd.DataFrame, destino: Path) -> None:
    """Grava resumo.csv (com a coluna da reanálise, se houver) e config.json de cada cenário
    em destino/<impl>/<rep>/<cenario>/: arquivo compacto, sem os envios e erros por registro,
    que o `comparar` lê de novo com a mesma reanálise."""
    for (impl, rep, pasta), g in d.groupby(["impl", "rep", "pasta"]):
        alvo = destino / impl / rep / Path(pasta).name
        alvo.mkdir(parents=True, exist_ok=True)
        # o arquivo guarda o resumo medido tal como foi gravado (texto original, linha a linha) e só
        # acrescenta as colunas da reanálise; a reanálise é refeita ao ler
        original = pd.read_csv(Path(pasta) / "resumo.csv", dtype=str, keep_default_na=False)
        novas = [c for c in (COLUNA_LARGADA, COLUNA_LAT) if c in g and c not in original]
        if novas:
            valores = g.set_index(g.taxa_alvo.astype(int).astype(str))[novas]
            for c in novas:
                original[c] = original.taxa_alvo.map(valores[c]).map(lambda v: "" if pd.isna(v) else f"{v:g}")
        original.to_csv(alvo / "resumo.csv", index=False, lineterminator="\n")
        if (Path(pasta) / "config.json").exists():
            shutil.copy(Path(pasta) / "config.json", alvo / "config.json")


def celula(g: pd.DataFrame, criterio: str) -> str:
    """Mediana entre repetições, com mínimo e máximo quando há mais de uma (C9)."""
    if g.empty:
        return "-"
    # repetição cujo primeiro degrau foi reprovado conta como 0, para não inflar a mediana (B5);
    # mas se o primeiro degrau é INVÁLIDO (ex.: abortado por falha de execução), o limite é
    # desconhecido e a repetição fica de fora: contá-la como 0 punia a implementação por um
    # erro do ambiente (C16)
    def mediu(r: pd.DataFrame) -> bool:
        return "degrau_valido" not in r or bool(r.sort_values("taxa_alvo").degrau_valido.astype(bool).iloc[0])

    medidas = [r for _, r in g.groupby("rep") if mediu(r)]
    if not medidas:
        return "sem degrau válido"
    lims = pd.Series([limite(r, criterio) or 0 for r in medidas], dtype="float")
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


# ------------------------------------------------------------ latência (H2, C17)

PARES = (("python_imperativo", "python_funcional"), ("python_funcional", "elixir"))
ROTULO = {"python_imperativo": "imp", "python_funcional": "fun", "elixir": "ex"}


def mann_whitney(a: list[float], b: list[float]) -> float:
    """p bilateral exato do teste de Mann-Whitney (empates por posto médio).

    Exato por enumeração: com 5 repetições de cada lado são C(10, 5) = 252 partições, e o
    menor p possível é 2/252 ≈ 0,008. Com 3 contra 3, o menor é 0,1: nunca significativo."""
    juntos = sorted(a + b)
    posto = {v: sum(i + 1 for i, x in enumerate(juntos) if x == v) / juntos.count(v) for v in juntos}
    postos = [posto[v] for v in a + b]
    n = len(a)
    media = n * (len(postos) + 1) / 2
    observado = abs(sum(postos[:n]) - media)
    particoes = list(combinations(range(len(postos)), n))
    extremos = sum(abs(sum(postos[i] for i in idx) - media) >= observado - 1e-9 for idx in particoes)
    return extremos / len(particoes)


def tabela_latencia(df: pd.DataFrame, minimo: int = 3) -> str:
    """p99 (ms) por implementação nos degraus válidos e aprovados em carga (sem timeouts, então
    o p99 das 2xx é comparável), com o p de Mann-Whitney entre pares. Só entram degraus em
    que as três implementações têm pelo menos `minimo` repetições."""
    d = df[~df.cenario.str.startswith("falha")]
    if "degrau_valido" in d:
        d = d[d.degrau_valido.astype(bool)]
    if "ok_carga" in d:
        d = d[d.ok_carga.astype(bool)]
    impls = list(IMPLEMENTACOES)
    pares = [f"p ({ROTULO[a]}×{ROTULO[b]})" for a, b in PARES]
    linhas = ["| cenário | taxa | " + " | ".join(impls + pares) + " |",
              "|---" * (2 + len(impls) + len(pares)) + "|"]
    for (cenario, taxa), g in d.groupby(["cenario", "taxa_alvo"]):
        coluna = COLUNA_LAT if COLUNA_LAT in g and g[COLUNA_LAT].notna().all() else "lat_p99_ms"
        amostras = {i: g[g.impl == i][coluna].astype(float).tolist() for i in impls}
        if min(len(v) for v in amostras.values()) < minimo:
            continue
        cel = [f"{pd.Series(v).median():.1f} [{min(v):.1f}–{max(v):.1f}]" for v in amostras.values()]
        ps = [mann_whitney(amostras[a], amostras[b]) for a, b in PARES]
        cel += [f"**{p:.3f}**" if p < 0.05 else f"{p:.3f}" for p in ps]
        linhas.append(f"| {cenario} | {int(taxa)} | " + " | ".join(cel) + " |")
    if len(linhas) == 2:
        return "_nenhum degrau com repetições suficientes nas três implementações_\n"
    return ("Latência p99 das respostas 2xx (ms), mediana [mín–máx] das repetições, nos degraus válidos e "
            "sem erro de carga. p: Mann-Whitney exato bilateral; em negrito, p < 0,05. São muitos testes: "
            "um p isolado perto de 0,05 não basta, o que conta é a consistência ao longo das taxas.\n\n"
            + "\n".join(linhas) + "\n")


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
    saturou = d["api_saturou"].fillna(False).astype(bool) if "api_saturou" in d else pd.Series(False, index=d.index)
    linhas = ["| implementação | degraus | válidos | " + " | ".join(motivos)
              + " | registros perdidos pela fila | API saturou (válido, reprovado) |",
              "|---" * (len(motivos) + 5) + "|"]
    for impl in IMPLEMENTACOES:
        g = d[d.impl == impl]
        if g.empty:
            continue
        contagens = [str(int(g.incidente.str.contains(m).sum())) for m in motivos]
        linhas.append(f"| {impl} | {len(g)} | {int(g.degrau_valido.astype(bool).sum())} | "
                      + " | ".join(contagens) + f" | {int(g.perdidos.astype(float).sum())} | {int(saturou[g.index].sum())} |")
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
    p.add_argument("--descontar-largada", type=float, default=0.0, metavar="S",
                   help="reanálise (C16): mede o atraso do gerador só depois dos S s iniciais de cada "
                        "degrau. Para resultados anteriores a C16 use 2. Padrão: 0 (desligada)")
    p.add_argument("--exportar", type=Path, default=None, metavar="DIR",
                   help="grava em DIR só resumo.csv e config.json de cada cenário (com a coluna da "
                        "reanálise, quando ligada), para arquivar uma execução sem os envios")
    a = p.parse_args()
    df = carregar(a.resultados)
    if df.empty:
        raise SystemExit(f"nenhum resumo.csv em {a.resultados}/<impl>/")
    cabecalho = ""
    if a.descontar_largada > 0:
        df = revalidar(df, a.descontar_largada)
        cabecalho = ("> **Reanálise (C16):** degraus revalidados com o atraso do gerador medido depois da "
                     f"largada.\n\n{tabela_revalidacao(df, a.descontar_largada)}\n")
    if a.exportar:
        exportar(df, a.exportar)
    # resultados antigos (antes de C5) só têm sem_erros
    criterios = [c for c in CRITERIOS if c in df]
    a.saida.mkdir(parents=True, exist_ok=True)
    _estilo()
    figura_p99(df, a.saida)
    figura_validade(df, a.saida)
    texto = cabecalho + "".join(f"## Limite (req/s), critério `{c}`\n\n{tabela(df, c)}\n\n" for c in criterios)
    texto += f"## Latência p99 (H2, C17)\n\n{tabela_latencia(df)}\n"
    texto += f"## Validade da execução (C13)\n\n{tabela_validade(df)}\n"
    (a.saida / "comparacao.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
