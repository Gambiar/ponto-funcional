| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.4 | 4.6 | 4.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 1.9 | 5.2 | 5.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.6 | 11.6 | 11.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.4 | 1.3 | True | True | True | True | 0 | 2.1 | 179.1 | 179.1 | 1.0 | 0.999966 | 0 | 2 | 0 | True | True | False |
| baseline | 1500 | 1351.3 | 7026.9 | False | True | True | False | gerador_atrasou | 556.5 | 8619.3 | 13428.4 | 0.654737 | 0.964205 | 30775 | 2089 | 0 | False | False | False |
| baseline | 2000 | 1226.1 | 39518.8 | False | True | True | False | gerador_atrasou | 6.8 | 3560.0 | 43188.2 | 0.527462 | 0.999649 | 56197 | 22 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 3.5 | True | True | True | True | 0 | 1.9 | 3725.8 | 5963.6 | 0.77371 | 0.934282 | 3369 | 757 | 23815 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.8 | True | True | True | True | 0 | 1.6 | 10.2 | 51.5 | 0.664092 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.0 | 0.940278 | 0.995092 | 1333 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.765903 | 0.995069 | 6385 | 103 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 0.502418 | 0 | 7408 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.8 | 1.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.8 | 20.0 | True | True | True | True | 0 | 0.5 | 13.7 | 13.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 48.3 | False | True | True | False | gerador_atrasou | 0.5 | 65.7 | 65.7 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_1000 | 3000 | 2995.8 | 759.3 | False | True | True | False | gerador_atrasou | 1.2 | 1526.0 | 1526.0 | 1.0 | 0.999854 | 0 | 26 | 0 | True | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 1.0 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.9 | 1.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 16.9 | True | True | True | True | 0 | 0.5 | 20.4 | 20.4 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_200 | 2000 | 1997.7 | 91.3 | False | True | True | False | gerador_atrasou | 0.5 | 229.6 | 229.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2995.5 | 575.7 | False | True | True | False | gerador_atrasou | 0.8 | 1207.9 | 1207.9 | 1.0 | 0.99991 | 0 | 16 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 1.5 | True | True | True | True | 0 | 0.5 | 7.8 | 7.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 50.5 | False | True | True | False | gerador_atrasou | 0.5 | 81.8 | 81.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2995.4 | 790.2 | False | True | True | False | gerador_atrasou | 1.0 | 1682.4 | 1682.4 | 1.0 | 0.999764 | 0 | 42 | 0 | True | False | False |

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
| lote_1000 | 1500 | 1500 | 1500 |
| lote_200 | 1500 | 1500 | 1000 |
| lote_50 | 1500 | 1500 | 1500 |
