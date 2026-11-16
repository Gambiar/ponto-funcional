| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.6 | 6.9 | 6.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 2.1 | 5.4 | 5.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.4 | True | True | True | True | 0 | 1.9 | 6.1 | 6.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.5 | 96.2 | 96.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1500 | 1498.9 | 155.8 | False | True | True | False | gerador_atrasou | 123.3 | 3721.2 | 5978.9 | 0.790392 | 0.973713 | 18684 | 1852 | 174567 | False | False | False |
| baseline | 2000 | 1183.2 | 48031.7 | False | True | True | False | gerador_atrasou | 556.8 | 6838.2 | 51206.5 | 0.201077 | 0.988906 | 94908 | 265 | 147519 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 3.7 | True | True | True | True | 0 | 95.2 | 5311.6 | 5960.8 | 0.769355 | 0.916143 | 3432 | 960 | 29227 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.3 | True | True | True | True | 0 | 1.7 | 3.8 | 51.6 | 0.663911 | 1.0 | 5001 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 0.939576 | 0.995031 | 1346 | 104 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 0.4 | 0.7 | 0.8 | 0.764989 | 0.995006 | 6397 | 104 | 14 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.8 | 0.8 | 1.0 | 0.497782 | 0 | 7473 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.3 | True | True | True | True | 0 | 0.4 | 2.4 | 2.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 55.0 | False | True | True | False | gerador_atrasou | 0.4 | 15.2 | 15.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.9 | 729.8 | False | True | True | False | gerador_atrasou | 0.4 | 1165.7 | 1165.7 | 1.0 | 0.999921 | 0 | 14 | 0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1498.7 | 16.9 | True | True | True | True | 0 | 0.4 | 6.2 | 6.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1997.7 | 107.8 | False | True | True | False | gerador_atrasou | 0.4 | 107.4 | 107.4 | 1.0 | 0.999949 | 0 | 6 | 0 | True | True | False |
| lote_200 | 3000 | 2995.7 | 392.3 | False | True | True | False | gerador_atrasou | 0.5 | 3498.5 | 5791.5 | 0.847466 | 0.999907 | 27183 | 14 | 0 | False | True | False |
| lote_50 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.3 | 1.1 | True | True | True | True | 0 | 0.4 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.0 | 20.8 | False | True | True | False | gerador_atrasou | 0.4 | 6.3 | 6.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.2 | 108.3 | False | True | True | False | gerador_atrasou | 0.4 | 90.6 | 90.6 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |

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
| lote_200 | 1500 | 1500 | 1500 |
| lote_50 | 1000 | 1000 | 1000 |
