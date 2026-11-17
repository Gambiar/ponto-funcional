## Métricas de código (H1, C17)

| implementação | SLOC | funções | pontos de decisão | decisões/função | máx. numa função | mutação compartilhada | mutação local | funções isoláveis |
|---|---|---|---|---|---|---|---|---|
| **python_imperativo** | 336 | 18 | 60 | 3.3 | 18 | 74 | 1 | 4 (22%) |
| **python_funcional** | 542 | 64 | 85 | 1.3 | 16 | 42 | 2 | 34 (53%) |
|   python_funcional – núcleo | 147 | 24 | 31 | 1.3 | 4 | 0 | 0 | 24 (100%) |
|   python_funcional – casca | 395 | 40 | 54 | 1.4 | 16 | 42 | 2 | 10 (25%) |
| **elixir** | 502 | 96 | 81 | 0.8 | 7 | 21 | 0 | 42 (44%) |
|   elixir – núcleo | 71 | 22 | 25 | 1.1 | 7 | 0 | 0 | 22 (100%) |
|   elixir – casca | 431 | 74 | 56 | 0.8 | 4 | 21 | 0 | 20 (27%) |

Definições em `ponto.analise.codigo`. Python medido pela árvore sintática; Elixir, lexicamente (aproximado). Só o código do serviço.

Arquivos: python_imperativo: src/ponto_imperativo/__init__.py, src/ponto_imperativo/api.py; python_funcional: src/ponto/nucleo/__init__.py, src/ponto/nucleo/lotes.py, src/ponto/nucleo/modelos.py, src/ponto/nucleo/validacao.py, src/ponto/casca/__init__.py, src/ponto/casca/api.py, src/ponto/casca/fila.py, src/ponto/casca/repositorio.py, src/ponto/util/__init__.py, src/ponto/util/retry.py; elixir: elixir/lib/ponto/nucleo.ex, elixir/lib/ponto/api.ex, elixir/lib/ponto/application.ex, elixir/lib/ponto/estado.ex, elixir/lib/ponto/fila.ex, elixir/lib/ponto/repo.ex, elixir/lib/ponto/retry.ex
