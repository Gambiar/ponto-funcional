# Rodando o experimento numa VM

Guia para executar a suíte completa numa máquina virtual Linux (nuvem ou local). Uma VM dedicada é **melhor** que um notebook com Docker Desktop: nada mais disputa a CPU, o Docker roda nativo (sem a camada do WSL2) e o ambiente fica fácil de descrever no artigo.

---

## 1. Tamanho da VM

Os contêineres têm limites fixos de CPU. Com 8 ou mais núcleos (perfil `compose.cpuset.yml`):

| Contêiner | CPUs | Memória |
|---|---|---|
| API (qualquer implementação) | 1 | até 1 GB |
| PostgreSQL | 2 | até 1 GB |
| Gerador de carga | 4 (`CARGA_CPUS`) | ~1–2 GB nos degraus altos |
| **Total** | **7** | ~4 GB |

Com 4 a 7 núcleos, o Makefile usa sozinho o perfil `compose.4cpu.yml` (banco 1, API 1, gerador 2 em 2 processos; C15), que foi o do experimento 1. Ver a seção 3.

| Configuração | vCPUs | RAM | Disco | Observação |
|---|---|---|---|---|
| **Recomendada** | **8–12** | **16 GB** | 40 GB SSD | suíte completa sem ajustes |
| Mínima | 8 | 8 GB | 30 GB | sem folga: feche tudo o mais |
| 4 núcleos | 4 | 8 GB | 30 GB | perfil `compose.4cpu.yml` (automático pelo `make`); teto absoluto menor; **não** compare números absolutos com execuções no perfil de 8 |

Na nuvem, prefira **vCPUs dedicadas** (não as "burstable"/compartilhadas: t3/t4g na AWS, B-series na Azure, e2-micro/small no GCP). Com vCPU compartilhada, o *CPU steal* do hipervisor contamina a latência.

> Se a VM tiver menos núcleos que algum `cpus:` do compose, o Docker recusa subir o contêiner ("range of CPUs is from 0.01 to N"). Pelo `make` isso não acontece, porque o perfil segue o número de núcleos; com `docker compose` direto, reduza `CARGA_CPUS`.

---

## 2. Preparar a VM (Ubuntu 22.04/24.04)

```bash
# Docker Engine + Compose (script oficial)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER && newgrp docker

# ferramentas
sudo apt-get install -y git make tmux

# código
git clone https://github.com/Gambiar/ponto-funcional.git
cd ponto-funcional
```

Opcional, mas recomendado para estabilidade das medições:

```bash
# governador de CPU em desempenho (VMs locais/bare metal; na nuvem geralmente não se aplica)
sudo apt-get install -y linux-tools-common && sudo cpupower frequency-set -g performance
# limite de arquivos abertos: o gerador abre milhares de conexões a 6000 req/s
ulimit -n 65536
```

---

## 3. Conferir o ambiente (≈ 5 min)

```bash
make ambiente     # grava resultados/ambiente.txt (CPU, memória, kernel, versões): vai para o artigo
make construir    # imagens das três APIs (Elixir 1.20.3/OTP 29, Python 3.12, Postgres 16)
make testes       # testes Python (pytest) e Elixir (ExUnit), sem banco
make contrato     # as três APIs a 20 req/s: mesmos desfechos que o gabarito (C14)
make calibrar     # teto do gerador de carga nesta VM
```

Na saída do `make calibrar`, procure a **maior taxa com `atraso_p99_ms` ≤ 20**. É o teto confiável do gerador nesta VM. Se for menor que 6000, os degraus acima disso serão marcados como inválidos automaticamente (`gerador_valido=False`); anote o valor no artigo.

Se o `make contrato` falhar para alguma implementação, **não rode a comparação**: a diferença
apareceria como efeito do estilo ou do runtime.

Teste rápido das três implementações (≈ 30–40 min):

```bash
make comparacao REPETICOES=1 DURACAO=20
```

O Makefile escolhe o **perfil de CPU** pelo número de núcleos da VM, e cada serviço ganha núcleos só seus:

| Núcleos da VM | Perfil | Banco | API | Gerador de carga |
|---|---|---|---|---|
| 8 ou mais | `compose.cpuset.yml` | núcleos 0–1 | núcleo 2 | núcleos 3–6, 4 processos |
| 4 a 7 | `compose.4cpu.yml` | núcleo 0 | núcleo 1 | núcleos 2–3, 2 processos |

Com 4 núcleos, a comparação entre as implementações continua justa (a API tem 1 CPU nos dois
perfis), mas o teto absoluto cai: o banco tem 1 CPU e o gerador só sustenta a taxa medida pelo
`make calibrar`. Degraus acima desse teto ficam inválidos sozinhos. O perfil usado vai para
`resultados/ambiente.txt`; cite-o no artigo. Para forçar outro: `PERFIL=8`, `PERFIL=4` ou `PERFIL=livre`.

---

## 4. Rodar a suíte completa

A execução completa é **longa**. Estimativa com os padrões (5 repetições × degraus de 60 s; rampa de 12 degraus, de 100 a 6000 req/s, com 1250, 1750 e 2500 desde C17; 13 cenários por suíte):

| Etapa | Duração aproximada |
|---|---|
| Uma suíte (1 implementação, 1 repetição) | 45–60 min |
| Uma implementação, 5 repetições | 4–5 h |
| **Três implementações** | **12–15 h** |

Referência: o experimento 1 levou 9h40 no servidor de 4 núcleos; com os degraus de 1250, 1750 e 2500 req/s e os cenários de queda real (C17), conte com cerca de 12–14 h nessa mesma máquina.

Rode dentro do `tmux`, para sobreviver à queda da conexão SSH:

```bash
tmux new -s experimento
make comparacao 2>&1 | tee resultados/execucao.log
# desconectar sem parar: Ctrl+B, depois D
# voltar depois:        tmux attach -t experimento
```

`make comparacao` roda as repetições **intercaladas** (rep 1: funcional, imperativa, Elixir;
rep 2: imperativa, Elixir, funcional; ...), com banco novo a cada implementação (C13, C14).
Para dividir em várias noites, rode uma repetição por vez; a ordem continua rotativa:

```bash
make ambiente construir contrato calibrar
make rodar-uma IMPL=python_funcional  REP=1
make rodar-uma IMPL=python_imperativo REP=1
make rodar-uma IMPL=elixir            REP=1
make rodar-uma IMPL=python_imperativo REP=2   # e assim por diante
make figuras-comparacao
```

Um degrau que falha na execução (portas esgotadas, conexão recusada) é repetido uma vez depois de 60 s (C16).
Se a API cair ou a fila não esvaziar, a suíte **não para**: o degrau entra como inválido, com o
motivo na coluna `incidente`, e aparece na seção *Validade da execução* de
`figuras/comparacao/comparacao.md` e na figura `figuras/comparacao/validade.png`. Inclua as duas no artigo.

Durante a execução, **não use a VM para mais nada**.

---

## 5. Trazer os resultados

```bash
# da sua máquina:
scp -r usuario@ip-da-vm:ponto-funcional/resultados ./resultados
scp -r usuario@ip-da-vm:ponto-funcional/figuras    ./figuras
```

Os mais importantes para o artigo:

- `figuras/comparacao/comparacao.md` e `comparacao_p99.png`
- `figuras/<impl>/rep_<k>/`
- `resultados/ambiente.txt`
- a saída do `make calibrar`

`resultados/` e `figuras/` ficam fora do git (estão no `.gitignore`). Se quiserem versionar uma execução final, copiem para uma pasta própria, como foi feito com `exemplo/`.

---

## 6. O que registrar no artigo

- tipo de VM (provedor, família, vCPUs dedicadas ou não), CPU, RAM e kernel, tudo em `resultados/ambiente.txt`;
- teto do gerador medido pelo `make calibrar`;
- `GERADOR_PROCESSOS` e `CARGA_CPUS`, se forem diferentes do padrão;
- data e duração da execução, e o commit do código (`git rev-parse --short HEAD`, também no `ambiente.txt`).

---

## 7. Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `range of CPUs is from 0.01 to N` | a VM tem menos núcleos que algum `cpus:` | `export CARGA_CPUS=2 GERADOR_PROCESSOS=2` |
| muitos degraus com `gerador_valido=False` | a VM não sustenta a taxa | ver o `make calibrar`; usar uma VM maior ou `--escala 0.5` |
| `falha_conexao` em massa nas taxas altas | limite de arquivos abertos | `ulimit -n 65536` antes de rodar |
| degraus com `api_reiniciou` ou `falha_execucao` | a API caiu (falta de memória, erro) | `docker compose logs api`; `docker inspect --format '{{.RestartCount}}'` no contêiner da API |
| degraus com `fila_nao_drenou` | o consumidor não terminou de gravar em 300 s | normal muito acima do limite; abaixo dele, investigar o banco |
| build do Elixir falha | dependências | `docker compose -f docker-compose.yml -f compose.elixir.yml build api` e ver o erro |
| latência irregular entre repetições | vCPU compartilhada (*steal*) | conferir `steal` no `top`; trocar por vCPU dedicada |
