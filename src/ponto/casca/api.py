"""API HTTP (casca imperativa).

Modos de gravação, trocáveis em execução por POST /admin/config:
- "baseline": cada requisição grava seu registro no banco antes de responder;
- "lote":     a requisição só enfileira (202); um consumidor grava em lotes.
"""
from __future__ import annotations

import logging
import os
import time
from collections.abc import Sequence
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from functools import wraps
from statistics import mean

import asyncpg
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse

from ..nucleo.modelos import Resultado
from ..nucleo.validacao import criar_validador, interpretar, regras_padrao
from ..util.retry import com_falha_simulada, com_retry
from . import repositorio
from .fila import ErroDeDados, ProcessadorDeLotes

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("ponto.api")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto")
FILA_CAPACIDADE = int(os.getenv("FILA_CAPACIDADE", "10000"))
CONSUMIDORES = int(os.getenv("CONSUMIDORES", "1"))
POOL_MAX = int(os.getenv("POOL_MAX", "20"))

ERROS_DE_CONEXAO = (
    ConnectionError,
    OSError,
    asyncpg.PostgresConnectionError,
    asyncpg.InterfaceError,
    asyncpg.TooManyConnectionsError,
)


@dataclass
class Config:
    modo: str = os.getenv("MODO", "lote")
    tamanho_lote: int = int(os.getenv("TAMANHO_LOTE", "200"))
    espera_ms: int = int(os.getenv("ESPERA_MS", "100"))
    tentativas: int = int(os.getenv("TENTATIVAS", "8"))


class Estado:
    def __init__(self) -> None:
        self.config = Config()
        self.pool: asyncpg.Pool | None = None
        self.validar = criar_validador(regras_padrao(frozenset()))
        self.falha_ate = 0.0
        self.gravar = None
        self.processador: ProcessadorDeLotes | None = None
        self.retries = 0
        self.em_andamento = 0  # requisições /registros ainda sendo atendidas

    def montar_gravador(self) -> None:
        """Compõe o gravador a partir de funções menores (decoradores)."""

        def contar_retry(n, erro):
            self.retries += 1
            log.warning("tentativa %d falhou: %s", n, erro)

        @com_retry(self.config.tentativas, excecoes=ERROS_DE_CONEXAO, ao_falhar=contar_retry)
        @com_falha_simulada(lambda: self.falha_ate)
        @traduzir_erros
        async def gravar(lote: Sequence[Resultado]):
            return await repositorio.gravar_lote(self.pool, lote)

        self.gravar = gravar


def traduzir_erros(func):
    """Converte erros de conteúdo do asyncpg em ErroDeDados (sem retry)."""

    @wraps(func)
    async def envolvida(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncpg.DataError as erro:
            raise ErroDeDados(str(erro)) from erro

    return envolvida


estado = Estado()


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    # o banco pode demorar a aceitar conexões: o mesmo decorador de retry resolve
    conectar = com_retry(10, base=0.5, excecoes=ERROS_DE_CONEXAO)(asyncpg.create_pool)
    estado.pool = await conectar(DATABASE_URL, min_size=2, max_size=POOL_MAX)
    await repositorio.criar_esquema(estado.pool)
    estado.validar = criar_validador(regras_padrao(await repositorio.carregar_cadastro(estado.pool)))
    estado.montar_gravador()
    estado.processador = ProcessadorDeLotes(
        gravar=lambda: estado.gravar,
        tamanho=lambda: estado.config.tamanho_lote,
        espera_ms=lambda: estado.config.espera_ms,
        capacidade=FILA_CAPACIDADE,
        consumidores=CONSUMIDORES,
    )
    estado.processador.iniciar()
    log.info("API pronta: %s, fila=%d, consumidores=%d", asdict(estado.config), FILA_CAPACIDADE, CONSUMIDORES)
    yield
    await estado.processador.parar()
    await estado.pool.close()


app = FastAPI(title="Ponto funcional", lifespan=ciclo_de_vida)


def _resposta(status: int, **corpo) -> JSONResponse:
    return JSONResponse(corpo, status_code=status)


@app.post("/registros")
async def registrar(payload: dict = Body(...)):
    # o servidor continua atendendo mesmo se o cliente desistiu (timeout);
    # o experimento espera este contador zerar antes de reiniciar o banco
    estado.em_andamento += 1
    try:
        return await _registrar(payload)
    finally:
        estado.em_andamento -= 1


async def _registrar(payload: dict):
    registro = interpretar(payload)
    if registro is None:
        return _resposta(422, erro="payload_invalido")
    resultado = estado.validar(registro)

    match estado.config.modo:
        case "lote":
            if not estado.processador.enfileirar(resultado):
                return _resposta(503, erro="fila_cheia")
            return _resposta(202, id_evento=registro.id_evento, situacao="enfileirado")
        case "baseline":
            try:
                [d] = await estado.gravar([resultado])
            except ErroDeDados:
                return _resposta(422, erro="dado_corrompido")
            except ERROS_DE_CONEXAO:
                return _resposta(503, erro="banco_indisponivel")
            return _resposta(201, id_evento=d.id_evento, desfecho=d.desfecho, motivo=d.motivo)
        case outro:
            return _resposta(500, erro=f"modo desconhecido: {outro}")


@app.get("/saude")
async def saude():
    return {"ok": True}


# ------------------------------------------------------------- administração

@app.post("/admin/config")
async def configurar(novo: dict = Body(...)):
    campos = {k: v for k, v in novo.items() if k in Config.__dataclass_fields__}
    estado.config = Config(**{**asdict(estado.config), **campos})
    estado.montar_gravador()
    return asdict(estado.config)


@app.post("/admin/reset")
async def reset(corpo: dict = Body(...)):
    """Esvazia o banco, recria o cadastro e zera contadores."""
    n = int(corpo["servidores"])
    await repositorio.reiniciar(estado.pool, n)
    estado.validar = criar_validador(regras_padrao(frozenset(range(1, n + 1))))
    estado.processador.contadores.__init__()
    estado.retries = 0
    estado.falha_ate = 0.0
    return {"servidores": n}


@app.post("/admin/falha")
async def falha(segundos: float = 10.0):
    estado.falha_ate = time.monotonic() + segundos
    log.warning("falha simulada do banco por %.1f s", segundos)
    return {"segundos": segundos}


@app.get("/admin/estado")
async def situacao():
    p = estado.processador
    c = p.contadores
    return {
        "config": asdict(estado.config),
        "fila": p.fila.qsize(),
        "em_processamento": p.em_processamento,
        "ocioso": p.ocioso and estado.em_andamento == 0,
        "em_andamento": estado.em_andamento,
        "retries": estado.retries,
        "lote_medio": round(mean(c.tamanhos_de_lote), 1) if c.tamanhos_de_lote else 0,
        **{k: v for k, v in asdict(c).items() if k != "tamanhos_de_lote"},
    }
