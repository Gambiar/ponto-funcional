| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.6 | 5.7 | 5.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.1 | 6.9 | 6.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 1.9 | 7.2 | 7.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.5 | 49.5 | 49.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1498.6 | 145.8 | False | True | True | False | gerador_atrasou | 122.9 | 3748.9 | 5975.6 | 0.788763 | 0.972318 | 18836 | 1947 | 178214 | False | False | False |
| baseline | 2000 | 1101.0 | 47454.8 | False | True | True | False | gerador_atrasou | 510.0 | 5126.9 | 51386.4 | 0.180602 | 0.9952 | 97356 | 103 | 140922 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 3.5 | True | True | True | True | 0 | 47.3 | 5083.0 | 5970.4 | 0.73427 | 0.894901 | 3953 | 1148 | 29717 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 1.9 | 11.9 | 51.5 | 0.663821 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.8 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.939673 | 0.995131 | 1345 | 102 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.8 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 0.765043 | 0.995006 | 6396 | 104 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.507126 | 0 | 7332 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.4 | 1.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1498.9 | 77.4 | False | True | True | False | gerador_atrasou | 0.4 | 106.2 | 106.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 120.1 | False | True | True | False | gerador_atrasou | 0.4 | 118.2 | 118.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 17.2 | True | True | True | True | 0 | 0.4 | 7.9 | 7.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.3 | 102.4 | False | True | True | False | gerador_atrasou | 0.4 | 111.6 | 111.6 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_200 | 3000 | 2995.6 | 329.6 | False | True | True | False | gerador_atrasou | 0.4 | 615.8 | 615.8 | 1.0 | 0.999933 | 0 | 12 | 0 | True | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.6 | True | True | True | True | 0 | 0.4 | 3.5 | 3.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.0 | 228.1 | False | True | True | False | gerador_atrasou | 0.4 | 223.6 | 223.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2995.6 | 602.6 | False | True | True | False | gerador_atrasou | 0.4 | 1489.7 | 1489.2 | 0.991203 | 0.999887 | 1569 | 20 | 0 | False | False | False |

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
