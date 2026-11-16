| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.5 | 8.9 | 8.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.0 | 6.1 | 6.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 1.8 | 6.5 | 6.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.2 | 43.8 | 43.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1498.5 | 116.6 | False | True | True | False | gerador_atrasou | 118.8 | 3683.6 | 5947.3 | 0.865054 | 0.986948 | 12036 | 1007 | 132330 | False | False | False |
| baseline | 2000 | 1808.6 | 20052.7 | False | True | True | False | gerador_atrasou | 415.2 | 3809.5 | 43736.8 | 0.218964 | 0.994502 | 92780 | 143 | 193913 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 3.3 | True | False | True | False | fila_nao_drenou | 3.5 | 4830.1 | 5962.7 | 0.777352 | 0.937419 | 3309 | 723 | 26965 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | False | True | False | fila_nao_drenou | 1.9 | 6.6 | 51.6 | 0.663572 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | False | True | False | fila_nao_drenou | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | False | True | False | fila_nao_drenou | 0.4 | 0.8 | 0.8 | 0.939636 | 0.995077 | 1344 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | False | True | False | fila_nao_drenou | 0.4 | 0.7 | 0.7 | 0.765017 | 0.994909 | 6396 | 106 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.5 | True | False | True | False | fila_nao_drenou | 0.4 | 0.7 | 0.7 | 1.0 | 0.5072 | 0 | 7324 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | False | True | False | fila_nao_drenou | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | False | True | False | fila_nao_drenou | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 100 | 100.0 | 2.2 | True | False | True | False | fila_nao_drenou | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | False | True | False | fila_nao_drenou | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 15.3 | True | True | True | True | 0 | 0.4 | 10.3 | 10.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1997.1 | 38.1 | False | True | True | False | gerador_atrasou | 0.4 | 11.4 | 11.4 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 3000 | 1405.9 | 70625.1 | False | False | True | False | fila_nao_drenou; gerador_atrasou | 1968.0 | 4574.5 | 121161.5 | 0.065009 | 0.998964 | 166591 | 12 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1000 | 1000 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | None | None |
| falha_com_retry | None | None | None |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_sem_retry | None | None | None |
| lote_1000 | None | None | None |
| lote_200 | None | None | None |
| lote_50 | 1500 | 1500 | 1500 |
