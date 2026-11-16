| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.4 | 5.3 | 5.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.8 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.6 | 8.3 | 8.3 | 1.0 | 0.999933 | 0 | 2 | 0 | True | True | False |
| baseline | 1000 | 999.3 | 1.2 | True | True | True | True | 0 | 2.1 | 166.1 | 166.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1368.4 | 5196.4 | False | True | True | False | gerador_atrasou | 522.4 | 8596.6 | 12219.5 | 0.653931 | 0.965667 | 30859 | 2002 | 0 | False | False | False |
| baseline | 2000 | 1589.0 | 23405.4 | False | True | True | False | gerador_atrasou | 4.5 | 580.7 | 31715.2 | 0.499739 | 0.999629 | 59438 | 22 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.4 | True | True | True | True | 0 | 1.8 | 3808.4 | 5963.9 | 0.771511 | 0.934129 | 3399 | 756 | 23765 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.5 | 7.8 | 51.5 | 0.663888 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.0 | 0.940211 | 0.995086 | 1333 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.0 | 0.765521 | 0.994961 | 6383 | 105 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 0.506319 | 0 | 7344 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 1.0 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.9 | 13.5 | True | True | True | True | 0 | 0.5 | 17.9 | 17.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.0 | 117.9 | False | True | True | False | gerador_atrasou | 0.5 | 220.5 | 220.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.8 | 316.0 | False | True | True | False | gerador_atrasou | 0.6 | 741.1 | 741.1 | 1.0 | 0.999978 | 0 | 4 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.8 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 8.7 | True | True | True | True | 0 | 0.4 | 8.5 | 8.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1997.3 | 47.2 | False | True | True | False | gerador_atrasou | 0.5 | 51.6 | 51.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2995.4 | 913.5 | False | True | True | False | gerador_atrasou | 2.2 | 3241.6 | 3241.6 | 1.0 | 0.999753 | 0 | 44 | 0 | True | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.4 | 1.6 | 1.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1498.3 | 32.4 | False | True | True | False | gerador_atrasou | 0.5 | 65.4 | 65.4 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_50 | 2000 | 1998.0 | 99.0 | False | True | True | False | gerador_atrasou | 0.5 | 253.6 | 253.6 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 250 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 1500 | 1500 | 1500 |
| lote_200 | 1500 | 1500 | 1500 |
| lote_50 | 1000 | 1000 | 1000 |
