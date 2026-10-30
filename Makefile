COMPOSE = docker compose
RODAR = $(COMPOSE) run --rm carga

.PHONY: subir testes dados experimento rapido graficos tudo logs parar limpar

subir:          ## sobe banco e API
	$(COMPOSE) up -d --build --wait db api

testes:         ## testes unitários e de propriedades (sem banco)
	$(COMPOSE) run --rm --no-deps --entrypoint pytest carga -q

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
IMPERATIVO = $(COMPOSE) -f docker-compose.yml -f compose.imperativo.yml
ELIXIR     = $(COMPOSE) -f docker-compose.yml -f compose.elixir.yml
REPETICOES ?= 5
DURACAO    ?= 60
SUITE      = $(COMPOSE) run --rm --no-deps carga ponto.carga.experimento --suite padrao --repeticoes $(REPETICOES) --duracao-suite $(DURACAO)

.PHONY: comparacao comparar-funcional comparar-imperativo comparar-elixir figuras-comparacao

comparar-funcional:
	$(COMPOSE) up -d --build --wait db api
	$(SUITE) --saida resultados/python_funcional

comparar-imperativo:
	$(IMPERATIVO) up -d --build --wait db api
	$(SUITE) --saida resultados/python_imperativo

comparar-elixir:
	$(ELIXIR) up -d --build --wait db api
	$(SUITE) --saida resultados/elixir

figuras-comparacao:  ## figuras por implementação/repetição + tabela e gráfico comparativos
	$(COMPOSE) run --rm --no-deps carga ponto.analise.graficos --tudo --resultados resultados --saida figuras
	$(COMPOSE) run --rm --no-deps carga ponto.analise.comparar --resultados resultados --saida figuras/comparacao

comparacao: calibrar comparar-funcional comparar-imperativo comparar-elixir figuras-comparacao  ## pipeline completo do artigo

calibrar:       ## mede a taxa máxima que o gerador sustenta (servidor nulo)
	$(COMPOSE) --profile ferramentas up -d --build eco
	$(COMPOSE) run --rm --no-deps -e ECO_URL=http://eco:8001 carga ponto.carga.calibrar
