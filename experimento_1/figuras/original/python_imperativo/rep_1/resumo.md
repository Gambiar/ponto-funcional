| cenario | taxa_alvo | taxa_obtida | atraso_gerador_p99_ms | gerador_valido | drenou | api_sem_reinicio | degrau_valido | incidente | lat_p50_ms | lat_p99_ms | lat_p99_todas_ms | disponibilidade | integridade | erros_de_carga | erros_de_integridade | retries | ok_carga | ok_integridade | sem_erros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 2.4 | 4.9 | 4.9 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 250 | 250.0 | 2.0 | True | True | True | True | 0 | 1.9 | 4.5 | 4.5 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 500 | 499.9 | 1.9 | True | True | True | True | 0 | 1.6 | 11.0 | 11.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| baseline | 1000 | 999.2 | 1.3 | True | True | True | True | 0 | 2.0 | 217.9 | 217.9 | 1.0 | 0.999933 | 0.0 | 4.0 | 0.0 | True | True | False |
| baseline | 1500 | 1494.0 | 175.5 | False | True | True | False | gerador_atrasou | 358.6 | 5022.3 | 5962.1 | 0.819987 | 0.978178 | 16046.0 | 1595.0 | 0.0 | False | False | False |
| baseline | 2000 | 1514.5 | 39471.0 | False | True | True | False | gerador_atrasou | 3083.7 | 9802.6 | 85991.2 | 0.086763 | 0.995731 | 108488.0 | 44.0 | 0.0 | False | False | False |
| falha_baseline_com_retry | 500 | 499.9 | 2.9 | True | True | True | True | 0 | 1.7 | 3775.9 | 5962.7 | 0.772648 | 0.927633 | 3383.0 | 832.0 | 23834.0 | False | False | False |
| falha_baseline_sem_retry | 500 | 499.9 | 1.7 | True | True | True | True | 0 | 1.5 | 4.2 | 51.6 | 0.663911 | 1.0 | 5001.0 | 0.0 | 0.0 | False | True | False |
| falha_com_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 6.0 | True | True | True |
| falha_com_retry_20s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.94016 | 0.995082 | 1333.0 | 103.0 | 12.0 | False | False | False |
| falha_com_retry_30s | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 0.765503 | 0.995009 | 6383.0 | 104.0 | 14.0 | False | False | False |
| falha_sem_retry | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 0.9 | 0.9 | 1.0 | 0.497446 | 0.0 | 7478.0 | 0.0 | True | False | False |
| lote_1000 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.6 | 1.1 | 1.1 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.1 | 1.1 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 1000 | 999.6 | 1.1 | True | True | True | True | 0 | 0.4 | 1.4 | 1.4 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 1500 | 1499.0 | 25.0 | False | True | True | False | gerador_atrasou | 0.4 | 14.2 | 14.2 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_1000 | 2000 | 1998.3 | 97.2 | False | True | True | False | gerador_atrasou | 0.4 | 208.0 | 208.0 | 1.0 | 0.999983 | 0.0 | 2.0 | 0.0 | True | True | False |
| lote_200 | 100 | 100.0 | 2.2 | True | True | True | True | 0 | 0.9 | 1.3 | 1.3 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 250 | 250.0 | 1.2 | True | True | True | True | 0 | 0.7 | 1.1 | 1.1 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 500 | 499.9 | 1.6 | True | True | True | True | 0 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 1000 | 999.5 | 1.1 | True | True | True | True | 0 | 0.4 | 1.7 | 1.7 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 1500 | 1499.0 | 22.1 | False | True | True | False | gerador_atrasou | 0.4 | 26.5 | 26.5 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | True | True | True |
| lote_200 | 2000 | 1998.1 | 116.8 | False | True | True | False | gerador_atrasou | 0.5 | 250.7 | 250.7 | 1.0 | 0.999949 | 0.0 | 6.0 | 0.0 | True | True | False |
| lote_50 | 100 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | False | False | False |
| lote_50 | 250 | 0.0 | 0.0 | False | False | False | False | falha_execucao: ClientConnectorError: Cannot connect to host api:8000 ssl:default [Cannot assign requested address] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | False | False | False |

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
| lote_200 | 1000 | 1000 | 1000 |
| lote_50 | None | None | None |
