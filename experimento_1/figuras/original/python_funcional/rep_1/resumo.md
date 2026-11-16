| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.4 | 5.2 | 5.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 1.9 | 5.2 | 5.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.8 | 1.8 | True | True | True | True | 0 | 1.6 | 9.0 | 9.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.0 | 164.7 | 164.7 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1500 | 1334.6 | 6762.4 | False | True | True | False | gerador_atrasou | 366.3 | 6001.4 | 13584.7 | 0.620027 | 0.957643 | 33870 | 2341 | 0 | False | False | False |
| baseline | 2000 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.9 | True | True | True | True | 0 | 1.8 | 3430.5 | 5965.1 | 0.771774 | 0.931034 | 3396 | 792 | 23765 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.6 | 9.7 | 51.6 | 0.663978 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.940115 | 0.995177 | 1334 | 101 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.765467 | 0.995009 | 6384 | 104 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.3 | 1.3 | 1.0 | 0.496774 | 0 | 7488 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 0.5 | 2.7 | 2.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.8 | 21.3 | False | True | True | False | gerador_atrasou | 0.5 | 46.5 | 46.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 109.3 | False | True | True | False | gerador_atrasou | 0.5 | 275.1 | 275.1 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 8.5 | True | True | True | True | 0 | 0.4 | 11.1 | 11.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1997.0 | 175.9 | False | True | True | False | gerador_atrasou | 0.5 | 254.8 | 254.8 | 1.0 | 0.999916 | 0 | 10 | 0 | True | True | False |
| lote_200 | 3000 | 2995.7 | 502.7 | False | True | True | False | gerador_atrasou | 0.7 | 1372.8 | 1372.8 | 1.0 | 0.999865 | 0 | 24 | 0 | True | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.4 | 1.1 | True | True | True | True | 0 | 0.4 | 2.0 | 2.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 1.3 | True | True | True | True | 0 | 0.5 | 9.5 | 9.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 40.2 | False | True | True | False | gerador_atrasou | 0.5 | 63.8 | 63.8 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 2996.0 | 893.1 | False | True | True | False | gerador_atrasou | 1.0 | 3485.6 | 3485.6 | 1.0 | 0.999697 | 0 | 54 | 0 | True | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 500 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1000 | 1000 | 1000 |
| lote_200 | 1500 | 1500 | 1500 |
| lote_50 | 1500 | 1500 | 1500 |
