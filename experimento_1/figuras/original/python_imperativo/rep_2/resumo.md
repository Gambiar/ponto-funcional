| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.2 | 4.8 | 4.8 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 250 | 250.0 | 1.8 | True | True | True | True | 0 | 1.7 | 6.5 | 6.5 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 10.7 | 10.7 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 1.8 | 128.9 | 128.9 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 1500 | 1498.5 | 51.3 | False | True | True | False | gerador_atrasou | 86.0 | 1770.0 | 1770.0 | 1.0 | 0.999439 | 0.0 | 50.0 | 0.0 | True | False | False |
| baseline | 2000 | 1079.2 | 54138.9 | False | True | True | False | gerador_atrasou | 2097.4 | 6598.6 | 56979.6 | 0.165804 | 0.951767 | 99095.0 | 950.0 | 0.0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.2 | True | True | True | True | 0 | 1.6 | 3749.5 | 5955.9 | 0.777082 | 0.941553 | 3313.0 | 675.0 | 23571.0 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.7 | 10.1 | 51.5 | 0.663572 | 1.0 | 5000.0 | 0.0 | 0.0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0.0 | 0.0 | 6.0 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.94013 | 0.995079 | 1333.0 | 103.0 | 12.0 | False | False | False |
| falha_com_retry_30s | 500 | 499.8 | 1.5 | True | True | True | True | 0 | 0.5 | 0.8 | 0.9 | 0.765421 | 0.995104 | 6385.0 | 102.0 | 14.0 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.506863 | 0.0 | 7329.0 | 0.0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 1500 | 1498.7 | 11.4 | True | True | True | True | 0 | 0.4 | 12.3 | 12.3 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 2000 | 1998.4 | 40.7 | False | True | True | False | gerador_atrasou | 0.4 | 42.8 | 42.8 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 3000 | 2996.0 | 749.5 | False | True | True | False | gerador_atrasou | 0.6 | 2020.3 | 2020.3 | 1.0 | 0.999888 | 0.0 | 20.0 | 0.0 | True | False | False |
| lote_200 | 100 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | False | False | False |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.2 | True | True | True | True | 0 | 0.4 | 6.0 | 6.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 2000 | 1998.3 | 50.2 | False | True | True | False | gerador_atrasou | 0.4 | 52.0 | 52.0 | 1.0 | 0.999983 | 0.0 | 2.0 | 0.0 | True | True | False |
| lote_200 | 3000 | 2995.7 | 728.1 | False | True | True | False | gerador_atrasou | 0.7 | 1692.4 | 1692.4 | 1.0 | 0.999854 | 0.0 | 26.0 | 0.0 | True | False | False |
| lote_50 | 100 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | False | False | False |
| lote_50 | 250 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1500 | 1500 | 1500 |
| lote_200 | None | None | None |
| lote_50 | None | None | None |
