"""Métricas de código das três implementações, para a segunda parte de H1 (C17).

H1 diz que o estilo funcional não muda vazão nem erros, e que o ganho aparece em
testabilidade e clareza. Esta é a medida dessa segunda parte, com a mesma definição
para as três versões, contando só o código do serviço (sem gerador, análise e testes):

- SLOC: linhas com código (sem linhas em branco, comentários e docstrings/@doc);
- funções: `def`/`async def`/`lambda` em Python, cláusulas `def`/`defp` e `fn` em Elixir;
- pontos de decisão (complexidade ciclomática de McCabe menos 1 por função): if/elif,
  laços, except, `and`/`or`, condicionais em compreensões, cada `case` de um match;
  em Elixir, cada cláusula `->` (case/cond/fn/rescue/with), `if`/`unless`, guardas `when`,
  operadores booleanos e cada cláusula extra de uma função com o mesmo nome;
- mutação compartilhada: escrita em estado que sobrevive à chamada (atributo, item de
  coleção, global/nonlocal, método que altera coleção; em Elixir, :counters,
  :persistent_term, :ets, Agent, Process.put e as funções do Ponto.Estado que os usam);
- mutação local: acumuladores (`x += ...` em variável local), só em Python;
- funções isoláveis: não fazem I/O (banco, rede, relógio, log, processos) nem mutação
  compartilhada, então podem ser testadas sem infraestrutura.

Python é medido pela árvore sintática (ast); Elixir, lexicamente, por expressões regulares.
As duas contagens seguem a mesma definição, mas a de Elixir é aproximada: serve para
comparar ordens de grandeza, não diferenças de poucas unidades.

Uso:
    python -m ponto.analise.codigo --raiz . --saida figuras/comparacao
"""
from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

# implementação -> parte -> arquivos (relativos à raiz do repositório)
FONTES = {
    "python_imperativo": {"tudo": ["src/ponto_imperativo/*.py"]},
    # o oráculo (nucleo/referencia.py) é do experimento, não do serviço: o imperativo não tem
    "python_funcional": {"núcleo": ["src/ponto/nucleo/[!r]*.py"],
                         "casca": ["src/ponto/casca/*.py", "src/ponto/util/*.py"]},
    "elixir": {"núcleo": ["elixir/lib/ponto/nucleo.ex"],
               "casca": ["elixir/lib/ponto/[!n]*.ex"]},
}

MUTADORES = {"append", "extend", "insert", "pop", "popleft", "remove", "clear", "update", "add",
             "discard", "setdefault", "sort", "reverse", "put_nowait", "task_done"}
IO_PY = {"asyncpg", "aiohttp", "asyncio", "time", "os", "logging", "log", "print", "open",
         "uuid", "random", "repositorio", "pool", "conn", "conexao", "fastapi", "request"}
MUTACAO_EX = re.compile(r":counters\.(add|sub|put)|:persistent_term\.put|:ets\.\w+|Agent\.\w*update"
                        r"|Process\.put|\b(Estado\.)?(incr|decr|zerar|configurar|definir_cadastro|falhar_por)\(")
IO_EX = re.compile(r"\bRepo\.|Postgrex|GenServer\.|:counters|:persistent_term|Logger\.|Process\.|\bsend\("
                   r"|System\.|File\.|\bEstado\.|\bFila\.|Bandit|conn\b|\bTask\.")
DECISAO_EX = re.compile(r"->|\bif\b|\bunless\b|\bwhen\b|\band\b|\bor\b|&&|\|\|")


@dataclass
class Metricas:
    sloc: int = 0
    funcoes: int = 0
    decisoes: int = 0
    mutacao_compartilhada: int = 0
    mutacao_local: int = 0
    isolaveis: int = 0
    max_decisoes: int = 0
    arquivos: list[str] = field(default_factory=list)

    def somar(self, o: Metricas) -> Metricas:
        return Metricas(self.sloc + o.sloc, self.funcoes + o.funcoes, self.decisoes + o.decisoes,
                        self.mutacao_compartilhada + o.mutacao_compartilhada,
                        self.mutacao_local + o.mutacao_local, self.isolaveis + o.isolaveis,
                        max(self.max_decisoes, o.max_decisoes), self.arquivos + o.arquivos)


# ------------------------------------------------------------ Python (ast)

def _decisoes(no: ast.AST) -> int:
    """Pontos de decisão dentro de `no`, sem descer em funções aninhadas."""
    total = 0
    for filho in ast.iter_child_nodes(no):
        if isinstance(filho, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        match filho:
            case ast.If() | ast.IfExp() | ast.For() | ast.AsyncFor() | ast.While() | ast.ExceptHandler():
                total += 1
            case ast.BoolOp(values=v):
                total += len(v) - 1
            case ast.comprehension(ifs=ifs):
                total += 1 + len(ifs)
            case ast.match_case():
                total += 1
        total += _decisoes(filho)
    return total


def _mutacoes(no: ast.AST) -> tuple[int, int]:
    """(compartilhada, local) dentro de `no`, incluindo funções aninhadas."""
    comp = local = 0
    for n in ast.walk(no):
        match n:
            case ast.Assign(targets=alvos):
                comp += sum(isinstance(a, (ast.Attribute, ast.Subscript)) for a in alvos)
            case ast.AugAssign(target=ast.Attribute() | ast.Subscript()) | ast.AnnAssign(target=ast.Attribute()):
                comp += 1
            case ast.AugAssign(target=ast.Name()):
                local += 1
            case ast.Global(names=nomes) | ast.Nonlocal(names=nomes):
                comp += len(nomes)
            case ast.Call(func=ast.Attribute(attr=metodo)) if metodo in MUTADORES:
                comp += 1
    return comp, local


def _faz_io(no: ast.AST) -> bool:
    for n in ast.walk(no):
        match n:
            case ast.Await() | ast.AsyncWith() | ast.AsyncFor():
                return True
            case ast.Name(id=nome) if nome in IO_PY:
                return True
            case ast.Attribute(attr=nome) if nome in IO_PY:
                return True
    return False


def _linhas_de_docstring(arvore: ast.AST) -> set[int]:
    linhas = set()
    for n in ast.walk(arvore):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.body:
            primeiro = n.body[0]
            if isinstance(primeiro, ast.Expr) and isinstance(getattr(primeiro, "value", None), ast.Constant) \
                    and isinstance(primeiro.value.value, str):
                linhas |= set(range(primeiro.lineno, primeiro.end_lineno + 1))
    return linhas


def medir_python(texto: str) -> Metricas:
    arvore = ast.parse(texto)
    doc = _linhas_de_docstring(arvore)
    sloc = sum(1 for i, l in enumerate(texto.splitlines(), 1)
               if l.strip() and not l.strip().startswith("#") and i not in doc)
    m = Metricas(sloc=sloc)
    m.mutacao_compartilhada, m.mutacao_local = _mutacoes(arvore)
    for f in ast.walk(arvore):
        if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            d = _decisoes(f)
            m.funcoes += 1
            m.decisoes += d
            m.max_decisoes = max(m.max_decisoes, d)
            m.isolaveis += not _faz_io(f) and _mutacoes(f)[0] == 0
    # decisões fora de funções (nível de módulo/classe)
    m.decisoes += sum(_decisoes(n) for n in arvore.body
                      if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    return m


# ------------------------------------------------------------ Elixir (léxico)

_DEF_EX = re.compile(r"^\s*(def|defp)\s+([a-z_][\w?!]*)")


def _sem_doc_e_comentarios(texto: str) -> list[str]:
    """Remove @moduledoc/@doc (inclusive heredocs), comentários e strings."""
    texto = re.sub(r'@(module)?doc\s+(false|"""[\s\S]*?"""|"[^"\n]*")', "", texto)
    linhas = []
    for linha in texto.splitlines():
        linha = re.sub(r'"(\\.|[^"\\])*"', '""', linha)  # strings não contam como código de decisão
        linha = re.sub(r"#.*$", "", linha)
        linhas.append(linha)
    return linhas


def medir_elixir(texto: str) -> Metricas:
    linhas = _sem_doc_e_comentarios(texto)
    m = Metricas(sloc=sum(1 for l in linhas if l.strip()))
    blocos: list[tuple[str, list[str]]] = []  # (nome, linhas) de cada cláusula def/defp
    for linha in linhas:
        if d := _DEF_EX.match(linha):
            blocos.append((d.group(2), [linha]))
        elif blocos:
            blocos[-1][1].append(linha)
    vistos = set()
    for nome, corpo in blocos:
        texto_corpo = "\n".join(corpo)
        d = len(DECISAO_EX.findall(texto_corpo)) + (nome in vistos)  # cláusula extra = um ramo
        vistos.add(nome)
        anonimas = len(re.findall(r"\bfn\b", texto_corpo))
        m.funcoes += 1 + anonimas
        m.decisoes += d
        m.max_decisoes = max(m.max_decisoes, d)
        mut = len([x for x in corpo if MUTACAO_EX.search(x) and not _DEF_EX.match(x)])
        m.mutacao_compartilhada += mut
        m.isolaveis += (1 + anonimas) * (mut == 0 and not IO_EX.search(texto_corpo))
    return m


# ------------------------------------------------------------ agregação

def medir(raiz: Path) -> dict[str, dict[str, Metricas]]:
    resultado = {}
    for impl, partes in FONTES.items():
        resultado[impl] = {}
        for parte, padroes in partes.items():
            total = Metricas()
            for arq in sorted({a for p in padroes for a in raiz.glob(p)}):
                texto = arq.read_text(encoding="utf-8")
                m = medir_python(texto) if arq.suffix == ".py" else medir_elixir(texto)
                m.arquivos = [arq.relative_to(raiz).as_posix()]
                total = total.somar(m)
            resultado[impl][parte] = total
    return resultado


def _linha(nome: str, m: Metricas) -> str:
    media = m.decisoes / m.funcoes if m.funcoes else 0
    iso = 100 * m.isolaveis / m.funcoes if m.funcoes else 0
    return (f"| {nome} | {m.sloc} | {m.funcoes} | {m.decisoes} | {media:.1f} | {m.max_decisoes} | "
            f"{m.mutacao_compartilhada} | {m.mutacao_local} | {m.isolaveis} ({iso:.0f}%) |")


def tabela(medidas: dict[str, dict[str, Metricas]]) -> str:
    linhas = ["| implementação | SLOC | funções | pontos de decisão | decisões/função | máx. numa função | "
              "mutação compartilhada | mutação local | funções isoláveis |", "|---" * 9 + "|"]
    for impl, partes in medidas.items():
        total = Metricas()
        for m in partes.values():
            total = total.somar(m)
        linhas.append(_linha(f"**{impl}**", total))
        if len(partes) > 1:
            linhas += [_linha(f"  {impl} – {parte}", m) for parte, m in partes.items()]
    arquivos = "; ".join(f"{impl}: " + ", ".join(a for m in p.values() for a in m.arquivos)
                         for impl, p in medidas.items())
    return ("## Métricas de código (H1, C17)\n\n" + "\n".join(linhas) + "\n\n"
            "Definições em `ponto.analise.codigo`. Python medido pela árvore sintática; Elixir, "
            "lexicamente (aproximado). Só o código do serviço.\n\n"
            f"Arquivos: {arquivos}\n")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raiz", type=Path, default=Path("."))
    p.add_argument("--saida", type=Path, default=Path("figuras/comparacao"))
    a = p.parse_args()
    texto = tabela(medir(a.raiz))
    a.saida.mkdir(parents=True, exist_ok=True)
    (a.saida / "codigo.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
