| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 2.3 | 7.1 | 7.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 250 | 250.0 | 1.9 | True | True | True | True | 0 | 1.8 | 6.4 | 6.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.5 | 6.7 | 6.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1000 | 999.6 | 1.2 | True | True | True | True | 0 | 2.0 | 217.6 | 217.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| baseline | 1250 | 1249.3 | 1.2 | True | True | True | True | 0 | 2.9 | 446.1 | 446.1 | 1.0 | 0.999758 | 0 | 18 | 0 | True | False | False |
| baseline | 1500 | 1499.0 | 96.6 | False | True | True | True | 0 | 347.5 | 5481.3 | 5960.9 | 0.811264 | 0.974569 | 16823 | 1839 | 0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.1 | True | True | True | True | 0 | 1.9 | 3674.7 | 5963.8 | 0.778479 | 0.940207 | 3298 | 693 | 23693 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.5 | True | True | True | True | 0 | 1.7 | 11.5 | 51.5 | 0.664159 | 1.0 | 5000 | 0 | 0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.940278 | 0.995092 | 1333 | 103 | 12 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.3 | 1.1 | 0.765976 | 0.99507 | 6383 | 103 | 14 | False | False | False |
| falha_real_baseline_sem_retry | 500 | 499.9 | 2.0 | True | True | True | True | 0 | 1.7 | 5097.2 | 5850.6 | 0.772569 | 0.996522 | 3386 | 40 | 0 | False | False | False |
| falha_real_com_retry | 500 | 500.0 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 6 | True | True | True |
| falha_real_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.2 | 1.2 | 1.0 | 0.503358 | 0 | 7394 | 0 | True | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 0.50262 | 0 | 7405 | 0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 500 | 499.8 | 1.7 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.5 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1250 | 1249.0 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.5 | 2.6 | 2.6 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 1750 | 1748.6 | 1.1 | True | True | True | True | 0 | 0.5 | 8.2 | 8.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2000 | 1998.2 | 1.1 | True | True | True | True | 0 | 0.4 | 8.0 | 8.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 2500 | 2497.4 | 1.3 | True | True | True | True | 0 | 0.5 | 42.4 | 42.4 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_1000 | 3000 | 2995.8 | 24.3 | False | True | True | False | gerador_atrasou | 0.6 | 100.8 | 100.8 | 1.0 | 0.999978 | 0 | 4 | 0 | True | True | False |
| lote_1000 | 4000 | 3992.7 | 147.3 | False | True | True | False | gerador_atrasou | 3.7 | 285.7 | 285.7 | 1.0 | 0.999899 | 0 | 24 | 0 | True | False | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.8 | 1.2 | 1.2 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1000 | 999.2 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.5 | 1.5 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 2.8 | 2.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.4 | 4.3 | 4.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2000 | 1998.4 | 1.1 | True | True | True | True | 0 | 0.4 | 7.0 | 7.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.5 | 11.8 | 11.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_200 | 3000 | 2996.0 | 16.4 | True | True | True | True | 0 | 0.5 | 113.5 | 113.5 | 1.0 | 0.999989 | 0 | 2 | 0 | True | True | False |
| lote_200 | 4000 | 3992.9 | 123.2 | False | True | True | False | gerador_atrasou | 1.0 | 257.3 | 257.3 | 1.0 | 0.999815 | 0 | 44 | 0 | True | False | False |
| lote_200 | 6000 | 4244.8 | 19842.0 | False | True | True | True | 0 | 65.6 | 5713.3 | 29035.0 | 0.455947 | 0.997139 | 193968 | 465 | 0 | False | False | False |
| lote_50 | 100 | 100.0 | 2.1 | True | True | True | True | 0 | 0.8 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.1 | 1.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1250 | 1249.4 | 1.1 | True | True | True | True | 0 | 0.4 | 1.3 | 1.3 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1500 | 1499.1 | 1.1 | True | True | True | True | 0 | 0.4 | 4.1 | 4.1 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 1750 | 1748.7 | 1.1 | True | True | True | True | 0 | 0.5 | 6.8 | 6.8 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 2000 | 1998.3 | 1.1 | True | True | True | True | 0 | 0.5 | 8.4 | 8.4 | 1.0 | 0.999983 | 0 | 2 | 0 | True | True | False |
| lote_50 | 2500 | 2497.5 | 1.2 | True | True | True | True | 0 | 0.5 | 23.7 | 23.7 | 1.0 | 1.0 | 0 | 0 | 0 | True | True | True |
| lote_50 | 3000 | 2996.2 | 13.9 | True | True | True | True | 0 | 0.6 | 101.0 | 101.0 | 1.0 | 0.999966 | 0 | 6 | 0 | True | True | False |
| lote_50 | 4000 | 3992.9 | 141.6 | False | True | True | True | 0 | 1.0 | 385.3 | 394.9 | 0.979872 | 0.999794 | 4785 | 48 | 0 | False | False | False |
| lote_50 | 6000 | 4123.7 | 23159.0 | False | True | True | True | 0 | 15.8 | 5970.1 | 31098.7 | 0.215674 | 0.996749 | 279631 | 250 | 0 | False | False | False |

Limite por cenário (maior taxa antes do primeiro degrau reprovado, req/s):

| cenário | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|
| baseline | 1250 | 1000 | 1000 |
| falha_baseline_com_retry | None | None | None |
| falha_baseline_sem_retry | None | 500 | None |
| falha_com_retry | 500 | 500 | 500 |
| falha_com_retry_20s | None | None | None |
| falha_com_retry_30s | None | None | None |
| falha_real_baseline_sem_retry | None | None | None |
| falha_real_com_retry | 500 | 500 | 500 |
| falha_real_sem_retry | 500 | None | None |
| falha_sem_retry | 500 | None | None |
| lote_1000 | 2500 | 2500 | 2500 |
| lote_200 | 3000 | 3000 | 2500 |
| lote_50 | 3000 | 3000 | 1750 |
