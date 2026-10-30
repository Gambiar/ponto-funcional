# Rodando o experimento numa VM

Guia para executar a suíte completa numa máquina virtual Linux (nuvem ou local). Uma VM dedicada é **melhor** que um notebook com Docker Desktop: nada mais disputa a CPU, o Docker roda nativo (sem a camada do WSL2) e o ambiente fica fácil de descrever no artigo.

---

## 1. Tamanho da VM

Os contêineres têm limites fixos de CPU. A VM precisa ter **pelo menos esses núcleos, mais folga** para o sistema e o Docker.

| Contêiner | CPUs | Memória |
|---|---|---|
| API (qualquer implementação) | 1 | até 1 GB |
| PostgreSQL | 2 | até 1 GB |
| Gerador de carga | 4 (`CARGA_CPUS`) | ~1–2 GB nos degraus altos |
| **Total** | **7** | ~4 GB |

| Configuração | vCPUs | RAM | Disco | Observação |
|---|---|---|---|---|
| **Recomendada** | **8–12** | **16 GB** | 40 GB SSD | suíte completa sem ajustes |
| Mínima | 8 | 8 GB | 30 GB | sem folga: feche tudo o mais |
| Reduzida | 4 | 8 GB | 30 GB | `CARGA_CPUS=1 GERADOR_PROCESSOS=1` e `--escala 0.5`; **não** compare com execuções na configuração padrão |

Na nuvem, prefira **vCPUs dedicadas** (não as "burstable"/compartilhadas: t3/t4g na AWS, B-series na Azure, e2-micro/small no GCP). Com vCPU compartilhada, o *CPU steal* do hipervisor contamina a latência.

> Se a VM tiver menos núcleos que algum `cpus:` do compose, o Docker recusa subir o contêiner ("range of CPUs is from 0.01 to N"). Reduza `CARGA_CPUS` nesse caso.

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
make subir        # banco + API Python funcional
make testes       # 46 testes, sem banco
make calibrar     # teto do gerador de carga nesta VM
```

Na saída do `make calibrar`, procure a **maior taxa com `atraso_p99_ms` ≤ 20**. É o teto confiável do gerador nesta VM. Se for menor que 6000, os degraus acima disso serão marcados como inválidos automaticamente (`gerador_valido=False`); anote o valor no artigo.

Teste rápido das três implementações (≈ 30–40 min), que também compila a versão Elixir pela primeira vez:

```bash
make comparacao REPETICOES=1 DURACAO=20
```

---

## 4. Rodar a suíte completa

A execução completa é **longa**. Estimativa com os padrões (5 repetições × degraus de 60 s):

| Etapa | Duração aproximada |
|---|---|
| Uma suíte (1 implementação, 1 repetição) | 45–60 min |
| Uma implementação, 5 repetições | 4–5 h |
| **Três implementações** | **12–15 h** |

Rode dentro do `tmux`, para sobreviver à queda da conexão SSH:

```bash
tmux new -s experimento
make comparacao 2>&1 | tee resultados/execucao.log
# desconectar sem parar: Ctrl+B, depois D
# voltar depois:        tmux attach -t experimento
```

Também dá para rodar uma implementação por vez (por exemplo, uma por noite):

```bash
make ambiente calibrar
make comparar-funcional
make comparar-imperativo
make comparar-elixir
make figuras-comparacao
```

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
| build do Elixir falha | primeira compilação; dependências | `docker compose -f docker-compose.yml -f compose.elixir.yml build api` e ver o erro |
| latência irregular entre repetições | vCPU compartilhada (*steal*) | conferir `steal` no `top`; trocar por vCPU dedicada |
