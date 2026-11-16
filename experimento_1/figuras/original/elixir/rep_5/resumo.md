| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.9 | 8.1 | 8.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.2 | 4.4 | 4.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.8 | 1.4 | True | True | True | True | 0 | 2.0 | 6.0 | 6.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.7 | 93.1 | 93.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1498.8 | 145.8 | False | True | True | False | gerador_atrasou | 159.8 | 3781.9 | 5977.5 | 0.773176 | 0.974288 | 20218 | 1772 | 183794 | False | False | False |
| baseline | 2000 | 1586.6 | 25567.9 | False | True | True | False | gerador_atrasou | 429.1 | 3949.9 | 37826.1 | 0.162807 | 0.99654 | 99564 | 67 | 128560 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 4.5 | True | True | True | True | 0 | 3.4 | 4548.6 | 5969.2 | 0.739387 | 0.91815 | 3880 | 901 | 28813 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 1.9 | 5.9 | 51.6 | 0.664159 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.93974 | 0.994946 | 1345 | 106 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.7655 | 0.995067 | 6396 | 103 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 0.502687 | 0 | 7404 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.0 | 27.2 | False | True | True | False | gerador_atrasou | 0.4 | 8.6 | 8.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1997.9 | 103.4 | False | True | True | False | gerador_atrasou | 0.4 | 99.1 | 99.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 4.7 | True | True | True | True | 0 | 0.4 | 5.7 | 5.7 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_200 | 2000 | 1998.2 | 152.1 | False | True | True | False | gerador_atrasou | 0.4 | 194.2 | 194.2 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_200 | 3000 | 2993.2 | 804.4 | False | True | True | False | gerador_atrasou | 0.4 | 1771.4 | 1850.3 | 0.978554 | 0.999748 | 3824 | 44 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.8 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.4 | 1.2 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 38.9 | False | True | True | False | gerador_atrasou | 0.4 | 64.0 | 64.0 | 1.0 | 0.999978 | 0 | 2 | 0 | True | True | False |
| lote_50 | 2000 | 1998.3 | 104.7 | False | True | True | False | gerador_atrasou | 0.4 | 161.4 | 161.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |

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
| lote_200 | 1500 | 1500 | 1000 |
| lote_50 | 1000 | 1000 | 1000 |
