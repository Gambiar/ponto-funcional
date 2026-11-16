| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.7 | 8.9 | 8.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.1 | True | True | True | True | 0 | 2.8 | 10.7 | 10.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 2.0 | 13.9 | 13.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.8 | 165.3 | 165.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1438.1 | 1396.6 | False | True | True | False | gerador_atrasou | 428.6 | 5507.5 | 7787.9 | 0.671515 | 0.966683 | 29291 | 1995 | 0 | False | False | False |
| baseline | 2000 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 2.0 | 3916.2 | 5961.5 | 0.777763 | 0.941487 | 3306 | 677 | 23632 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.6 | 5.4 | 51.5 | 0.663888 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.940121 | 0.99499 | 1335 | 105 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.765337 | 0.994864 | 6388 | 107 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 0.506588 | 0 | 7340 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.5 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.2 | True | True | True | True | 0 | 0.5 | 8.2 | 8.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 63.9 | False | True | True | False | gerador_atrasou | 0.5 | 162.8 | 162.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.8 | 746.1 | False | True | True | False | gerador_atrasou | 1.9 | 2834.1 | 2834.1 | 1.0 | 0.999877 | 0 | 22 | 0 | True | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 28.6 | False | True | True | False | gerador_atrasou | 0.5 | 16.4 | 16.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 10.9 | True | True | True | True | 0 | 0.5 | 12.8 | 12.8 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_200 | 2000 | 1998.1 | 105.1 | False | True | True | False | gerador_atrasou | 0.5 | 452.6 | 452.6 | 1.0 | 0.999916 | 0 | 10 | 0 | True | True | False |
| lote_200 | 3000 | 2995.8 | 303.5 | False | True | True | False | gerador_atrasou | 0.8 | 849.8 | 849.8 | 1.0 | 0.99991 | 0 | 16 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.3 | True | True | True | True | 0 | 0.5 | 12.8 | 12.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.1 | 46.9 | False | True | True | False | gerador_atrasou | 0.5 | 73.3 | 73.3 | 1.0 | 0.999966 | 0 | 4 | 0 | True | True | False |
| lote_50 | 3000 | 2995.8 | 718.3 | False | True | True | False | gerador_atrasou | 1.1 | 2955.1 | 2955.1 | 1.0 | 0.999809 | 0 | 34 | 0 | True | False | False |

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
| lote_200 | 500 | 500 | 500 |
| lote_50 | 1500 | 1500 | 1500 |
