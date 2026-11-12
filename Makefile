# Perfil de CPU (C14, C15), escolhido pelo número de núcleos da máquina:
#   8 ou mais -> compose.cpuset.yml (banco 0-1, API 2, gerador 3-6, 4 processos)
#   menos     -> compose.4cpu.yml   (banco 0,   API 1, gerador 2-3, 2 processos)
# Para forçar: make ... PERFIL=8 | PERFIL=4 | PERFIL=livre (sem núcleos fixos)
NUCLEOS ?= $(shell nproc 2>/dev/null || echo 8)
PERFIL  ?= $(shell [ $(NUCLEOS) -ge 8 ] && echo 8 || echo 4)
ARQ_PERFIL_8     = -f compose.cpuset.yml
ARQ_PERFIL_4     = -f compose.4cpu.yml
ARQ_PERFIL_livre =
BASE    = -f docker-compose.yml $(ARQ_PERFIL_$(PERFIL))
COMPOSE = docker compose $(BASE)
RODAR = $(COMPOSE) run --rm carga

.PHONY: subir testes dados experimento rapido graficos tudo logs parar limpar ambiente calibrar

subir:          ## sobe banco e API
	$(COMPOSE) up -d --build --wait db api

testes:         ## testes unitários e de propriedades (sem banco)
	$(COMPOSE) run --rm --no-deps --entrypoint pytest carga -q
	$(COMPOSE) -f compose.elixir.yml run --rm --no-deps -e MIX_ENV=test --entrypoint mix api test

dados:          ## gera base sintética de 40 mil servidores em ./dados
	$(RODAR) ponto.dados.gerador --servidores 40000 --saida dados

experimento:    ## suíte completa do artigo (~15-25 min)
	$(RODAR) ponto.carga.experimento --suite padrao

rapido:         ## rampa curta para conferir o ambiente (~2 min)
	$(RODAR) ponto.carga.experimento --cenario rapido --taxas 100,500,1000 --duracao 10

graficos:       ## figuras e tabela em ./figuras
	$(RODAR) ponto.analise.graficos --resultados resultados --saida figuras

tudo: subir testes experimento graficos

logs:
	$(COMPOSE) logs -f api

parar:
	$(COMPOSE) down

limpar:
	$(COMPOSE) down -v
	rm -rf resultados figuras dados

# ------------------------------------------------ comparação entre implementações
# Mesma suíte, mesmo banco e mesmo gerador de carga; só a API muda.
# --no-deps: impede que o `run` recrie a API com a configuração padrão.
IMPERATIVO = $(COMPOSE) -f compose.imperativo.yml
ELIXIR     = $(COMPOSE) -f compose.elixir.yml
REPETICOES ?= 5
DURACAO    ?= 60
# banco novo a cada implementação: autovacuum, checkpoints e cache não passam de uma para outra (C13)
BANCO_NOVO = $(COMPOSE) rm -sfv db && docker volume rm -f ponto_pgdata

.PHONY: comparacao comparar-funcional comparar-imperativo comparar-elixir figuras-comparacao         construir rodar-uma comparar-intercalado contrato contrato-funcional contrato-imperativo contrato-elixir

IMPLS = python_funcional python_imperativo elixir
compose_python_funcional  = $(COMPOSE)
compose_python_imperativo = $(IMPERATIVO)
compose_elixir            = $(ELIXIR)

construir:      ## constrói as imagens das três APIs antes de medir (nada é compilado no meio da execução)
	$(COMPOSE) build api carga
	$(IMPERATIVO) build api
	$(ELIXIR) build api

# uma implementação, uma repetição: make rodar-uma IMPL=elixir REP=2
rodar-uma:
	$(BANCO_NOVO)
	$(compose_$(IMPL)) up -d --wait db api
	$(COMPOSE) run --rm --no-deps carga ponto.carga.experimento --suite padrao --rep $(REP) 		--duracao-suite $(DURACAO) --saida resultados/$(IMPL)/rep_$(REP)

# repetições intercaladas com ordem rotativa (C14): rep 1 = F I E, rep 2 = I E F, rep 3 = E F I...
# Uma deriva da máquina ao longo das horas se espalha entre as implementações em vez de
# virar diferença entre elas.
comparar-intercalado: construir
	@for k in $$(seq 1 $(REPETICOES)); do 	  set -- $(IMPLS); i=1; while [ $$i -lt $$k ]; do set -- $$2 $$3 $$1; i=$$((i+1)); done; 	  for impl in "$$@"; do 	    echo "######## repetição $$k: $$impl"; 	    $(MAKE) --no-print-directory rodar-uma IMPL=$$impl REP=$$k || exit 1; 	  done; 	done

# execução não intercalada de uma implementação só (para depurar)
comparar-funcional:
	$(MAKE) --no-print-directory rodar-uma IMPL=python_funcional REP=1
comparar-imperativo:
	$(MAKE) --no-print-directory rodar-uma IMPL=python_imperativo REP=1
comparar-elixir:
	$(MAKE) --no-print-directory rodar-uma IMPL=elixir REP=1

# teste de contrato (C14): 20 req/s por poucos segundos, não é teste de carga
contrato-%:
	$(BANCO_NOVO)
	$(compose_$(subst funcional,python_funcional,$(subst imperativo,python_imperativo,$*))) up -d --build --wait db api
	$(COMPOSE) run --rm --no-deps -e GERADOR_PROCESSOS=1 carga ponto.carga.contrato

contrato: contrato-funcional contrato-imperativo contrato-elixir  ## confere que as três APIs cumprem o mesmo contrato

figuras-comparacao:  ## figuras por implementação/repetição + tabela e gráfico comparativos
	$(COMPOSE) run --rm --no-deps carga ponto.analise.graficos --tudo --resultados resultados --saida figuras
	$(COMPOSE) run --rm --no-deps carga ponto.analise.comparar --resultados resultados --saida figuras/comparacao

comparacao: ambiente construir contrato calibrar comparar-intercalado figuras-comparacao  ## pipeline completo do artigo

calibrar:       ## grava resultados/calibracao.txt; mede a taxa máxima que o gerador sustenta (servidor nulo)
	mkdir -p resultados
	$(COMPOSE) --profile ferramentas up -d --build eco
	$(COMPOSE) run --rm --no-deps -e ECO_URL=http://eco:8001 carga ponto.carga.calibrar | tee resultados/calibracao.txt
	$(COMPOSE) --profile ferramentas stop eco    # libera as CPUs antes do experimento

ambiente:       ## registra hardware e versões em resultados/ambiente.txt (vai para o artigo)
	mkdir -p resultados
	{ echo "data: $$(date -Iseconds)"; \
	  echo "commit: $$(git rev-parse --short HEAD 2>/dev/null)"; \
	  echo "perfil de CPU: $(PERFIL) (núcleos da máquina: $(NUCLEOS))"; \
	  $(COMPOSE) config | grep -E "^  [a-z]+:$$|cpus:|cpuset:|GERADOR_PROCESSOS"; \
	  echo; uname -a; echo; lscpu 2>/dev/null || sysctl -a 2>/dev/null | grep machdep.cpu; \
	  echo; free -h 2>/dev/null; echo; nproc 2>/dev/null; \
	  echo; docker version --format 'docker {{.Server.Version}}'; docker compose version; \
	} > resultados/ambiente.txt
	@cat resultados/ambiente.txt | head -5
