| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.3 | 5.5 | 5.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.8 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.6 | 14.3 | 14.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.5 | 1.2 | True | True | True | True | 0 | 2.1 | 202.7 | 202.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1191.3 | 18617.1 | False | True | True | False | gerador_atrasou | 274.0 | 5580.3 | 22207.4 | 0.438878 | 0.973764 | 50047 | 1027 | 0 | False | False | False |
| baseline | 2000 | 1608.6 | 34054.8 | False | True | True | False | gerador_atrasou | 2825.4 | 15250.4 | 66639.8 | 0.131264 | 0.986212 | 103198 | 215 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.7 | 3480.9 | 5962.1 | 0.771296 | 0.938498 | 3399 | 705 | 23607 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 8.3 | 51.5 | 0.663639 | 1.0 | 4999 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.5 | 1.0 | 0.9 | 0.940085 | 0.994601 | 1334 | 113 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.765458 | 0.995104 | 6384 | 102 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.2 | 1.2 | 1.0 | 0.506863 | 0 | 7329 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.4 | 2.4 | 2.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 48.7 | False | True | True | False | gerador_atrasou | 0.4 | 93.2 | 93.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1997.2 | 86.1 | False | True | True | False | gerador_atrasou | 0.5 | 358.3 | 358.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 2.3 | 2.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 14.8 | True | True | True | True | 0 | 0.5 | 15.4 | 15.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.3 | 84.4 | False | True | True | False | gerador_atrasou | 0.5 | 431.9 | 431.9 | 1.0 | 0.999949 | 0 | 6 | 0 | True | True | False |
| lote_200 | 3000 | 2983.9 | 797.5 | False | True | True | False | gerador_atrasou | 1.3 | 2624.4 | 2624.4 | 1.0 | 0.999854 | 0 | 26 | 0 | True | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.8 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1498.7 | 1.2 | True | True | True | True | 0 | 0.5 | 11.1 | 11.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.0 | 38.1 | False | True | True | False | gerador_atrasou | 0.5 | 52.7 | 52.7 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 2995.5 | 797.6 | False | True | True | False | gerador_atrasou | 1.3 | 3252.7 | 3480.0 | 0.997839 | 0.999798 | 385 | 36 | 0 | False | False | False |

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
| lote_1000 | 1000 | 1000 | 1000 |
| lote_200 | 1500 | 1500 | 1500 |
| lote_50 | 1500 | 1500 | 1500 |
