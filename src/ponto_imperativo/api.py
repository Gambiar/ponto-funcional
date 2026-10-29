"""Variante IMPERATIVA da API (grupo de controle do experimento).

Mesmo contrato HTTP, mesmo esquema de banco e mesma arquitetura (baseline ×
fila em lote, retry com backoff, falha simulada, bisseção de lote corrompido)
da versão funcional em `ponto.casca` + `ponto.nucleo`, mas escrita no estilo
imperativo/orientado a objetos tradicional:

- sem núcleo puro: validação, regras e decisões ficam dentro dos métodos que
  falam com o banco;
- estado mutável compartilhado (listas, dicts, atributos) em vez de valores
  imutáveis;
- laços `for`/`while` com acumuladores em vez de map/filter/reduce/recursão;
- if/elif em vez de pattern matching;
- retry e falha simulada escritos inline, sem decoradores/funções de ordem superior.

Não importa nada de `ponto.*`: a comparação mede o estilo, não código compartilhado.
"""
from __future__ import annotations

import asyncio
import logging
import os
import time
from datetime import datetime

import asyncpg
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("ponto.imperativo")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ponto:ponto@localhost:5432/ponto")
FILA_CAPACIDADE = int(os.getenv("FILA_CAPACIDADE", "10000"))
POOL_MAX = int(os.getenv("POOL_MAX", "20"))

ERROS_DE_CONEXAO = (
    ConnectionError,
    OSError,
    asyncpg.PostgresConnectionError,
    asyncpg.InterfaceError,
    asyncpg.TooManyConnectionsError,
)

ESQUEMA = """
CREATE TABLE IF NOT EXISTS servidores (id INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS pontos (
    id_evento UUID PRIMARY KEY, servidor INTEGER NOT NULL, tipo TEXT NOT NULL,
    dia DATE NOT NULL, instante TIMESTAMP NOT NULL, dispositivo TEXT NOT NULL,
    UNIQUE (servidor, tipo, dia)
);
CREATE TABLE IF NOT EXISTS eventos (
    id_evento UUID PRIMARY KEY, servidor INTEGER NOT NULL, tipo TEXT NOT NULL,
    instante TIMESTAMP NOT NULL, desfecho TEXT NOT NULL, motivo TEXT,
    processado_em TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);
"""


class BancoIndisponivel(ConnectionError):
    pass


class DadoCorrompido(Exception):
    pass


class Servico:
    """Objeto único com todo o estado mutável do serviço."""

    def __init__(self):
        self.modo = os.getenv("MODO", "lote")
        self.tamanho_lote = int(os.getenv("TAMANHO_LOTE", "200"))
        self.espera_ms = int(os.getenv("ESPERA_MS", "100"))
        self.tentativas = int(os.getenv("TENTATIVAS", "8"))
        self.pool = None
        self.cadastro = set()
        self.falha_ate = 0.0
        self.fila = asyncio.Queue(maxsize=FILA_CAPACIDADE)
        self.pendentes = 0
        self.em_processamento = 0
        self.em_andamento = 0
        self.zerar_contadores()
        self.tarefa = None

    def zerar_contadores(self):
        self.enfileirados = 0
        self.recusados = 0
        self.lotes = 0
        self.registros_gravados_em_lote = 0
        self.registros_perdidos = 0
        self.registros_corrompidos = 0
        self.retries = 0
        self.tamanhos = []

    # ------------------------------------------------------------ validação

    def ler_payload(self, payload):
        """Devolve dict com o registro ou None se o formato for inválido."""
        if not isinstance(payload, dict):
            return None
        for campo in ("id_evento", "tipo", "instante", "dispositivo"):
            if not isinstance(payload.get(campo), str):
                return None
        servidor = payload.get("servidor")
        if not isinstance(servidor, int) or isinstance(servidor, bool):
            return None
        try:
            instante = datetime.fromisoformat(payload["instante"])
        except ValueError:
            return None
        return {
            "id_evento": payload["id_evento"],
            "servidor": servidor,
            "tipo": payload["tipo"],
            "instante": instante,
            "dispositivo": payload["dispositivo"],
            "motivo": None,
        }

    def validar(self, reg):
        """Escreve o motivo de rejeição no próprio registro (mutação)."""
        if reg["tipo"] != "entrada" and reg["tipo"] != "saida":
            reg["motivo"] = "tipo_invalido"
        elif reg["servidor"] not in self.cadastro:
            reg["motivo"] = "servidor_inexistente"
        elif reg["instante"].hour < 6:
            reg["motivo"] = "fora_da_jornada"

    # ------------------------------------------------------------ gravação

    async def gravar_com_retry(self, lote):
        n = 1
        while True:
            try:
                if time.monotonic() < self.falha_ate:
                    await asyncio.sleep(0.05)
                    raise BancoIndisponivel("banco indisponível (falha simulada)")
                return await self.gravar(lote)
            except ERROS_DE_CONEXAO as erro:
                if n >= self.tentativas:
                    raise
                self.retries += 1
                log.warning("tentativa %d falhou: %s", n, erro)
                espera = 0.2 * 2 ** (n - 1)
                if espera > 5.0:
                    espera = 5.0
                await asyncio.sleep(espera)
                n += 1

    async def gravar(self, lote):
        lote.sort(key=lambda r: (r["instante"], r["id_evento"]))
        entradas = []
        saidas = []
        for r in lote:
            if r["motivo"] is None:
                if r["tipo"] == "entrada":
                    entradas.append(r)
                else:
                    saidas.append(r)

        try:
            async with self.pool.acquire() as conn, conn.transaction():
                inseridos = set()
                if entradas:
                    for linha in await conn.fetch(INSERIR_PONTOS, *colunas(entradas)):
                        inseridos.add(linha[0])
                sem_entrada = set()
                if saidas:
                    linhas = await conn.fetch(
                        ENTRADAS_EXISTENTES, [r["servidor"] for r in saidas], [r["instante"].date() for r in saidas])
                    existentes = set()
                    for e in linhas:
                        existentes.add((e["servidor"], e["dia"]))
                    validas = []
                    for r in saidas:
                        if (r["servidor"], r["instante"].date()) in existentes:
                            validas.append(r)
                        else:
                            sem_entrada.add(r["id_evento"])
                    if validas:
                        for linha in await conn.fetch(INSERIR_PONTOS, *colunas(validas)):
                            inseridos.add(linha[0])

                ids, servs, tipos, insts, desfechos, motivos = [], [], [], [], [], []
                for r in lote:
                    if r["motivo"] is not None:
                        desfecho, motivo = "rejeitado", r["motivo"]
                    elif r["id_evento"] in sem_entrada:
                        desfecho, motivo = "rejeitado", "saida_sem_entrada"
                    elif r["id_evento"] in inseridos:
                        desfecho, motivo = "gravado", None
                    else:
                        desfecho, motivo = "descartado", "duplicado"
                    ids.append(r["id_evento"])
                    servs.append(r["servidor"])
                    tipos.append(r["tipo"])
                    insts.append(r["instante"])
                    desfechos.append(desfecho)
                    motivos.append(motivo)
                await conn.execute(INSERIR_EVENTOS, ids, servs, tipos, insts, desfechos, motivos)
        except asyncpg.DataError as erro:
            raise DadoCorrompido(str(erro)) from erro
        return desfechos, motivos

    async def gravar_isolando(self, lote):
        """Bisseção iterativa com pilha explícita (sem recursão)."""
        pilha = [lote]
        while pilha:
            atual = pilha.pop()
            try:
                await self.gravar_com_retry(atual)
            except DadoCorrompido as erro:
                if len(atual) == 1:
                    self.registros_corrompidos += 1
                    log.warning("registro %s descartado: %s", atual[0]["id_evento"], erro)
                else:
                    meio = len(atual) // 2
                    pilha.append(atual[meio:])
                    pilha.append(atual[:meio])

    # ------------------------------------------------------------ consumidor

    async def consumir(self):
        while True:
            lote = [await self.fila.get()]
            limite = time.monotonic() + self.espera_ms / 1000
            while len(lote) < self.tamanho_lote:
                if not self.fila.empty():
                    lote.append(self.fila.get_nowait())
                    continue
                restante = limite - time.monotonic()
                if restante <= 0:
                    break
                try:
                    lote.append(await asyncio.wait_for(self.fila.get(), restante))
                except TimeoutError:
                    break

            self.em_processamento += len(lote)
            try:
                await self.gravar_isolando(lote)
                self.lotes += 1
                self.registros_gravados_em_lote += len(lote)
                self.tamanhos.append(len(lote))
            except Exception as erro:
                self.registros_perdidos += len(lote)
                log.error("lote de %d registros perdido: %r", len(lote), erro)
            finally:
                self.em_processamento -= len(lote)
                self.pendentes -= len(lote)
                for _ in lote:
                    self.fila.task_done()


INSERIR_PONTOS = """
INSERT INTO pontos (id_evento, servidor, tipo, dia, instante, dispositivo)
SELECT * FROM unnest($1::uuid[], $2::int[], $3::text[], $4::date[], $5::timestamp[], $6::text[])
ON CONFLICT DO NOTHING
RETURNING id_evento::text
"""
ENTRADAS_EXISTENTES = """
SELECT p.servidor, p.dia FROM pontos p
JOIN unnest($1::int[], $2::date[]) AS q(servidor, dia) USING (servidor, dia)
WHERE p.tipo = 'entrada'
"""
INSERIR_EVENTOS = """
INSERT INTO eventos (id_evento, servidor, tipo, instante, desfecho, motivo)
SELECT * FROM unnest($1::uuid[], $2::int[], $3::text[], $4::timestamp[], $5::text[], $6::text[])
ON CONFLICT (id_evento) DO NOTHING
"""


def colunas(regs):
    ids, servs, tipos, dias, insts, disps = [], [], [], [], [], []
    for r in regs:
        ids.append(r["id_evento"])
        servs.append(r["servidor"])
        tipos.append(r["tipo"])
        dias.append(r["instante"].date())
        insts.append(r["instante"])
        disps.append(r["dispositivo"])
    return ids, servs, tipos, dias, insts, disps


servico = Servico()
app = FastAPI(title="Ponto imperativo")


@app.on_event("startup")
async def iniciar():
    for n in range(1, 11):
        try:
            servico.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=POOL_MAX)
            break
        except ERROS_DE_CONEXAO:
            if n == 10:
                raise
            await asyncio.sleep(min(5.0, 0.5 * 2 ** (n - 1)))
    async with servico.pool.acquire() as conn:
        await conn.execute(ESQUEMA)
        for linha in await conn.fetch("SELECT id FROM servidores"):
            servico.cadastro.add(linha["id"])
    servico.tarefa = asyncio.create_task(servico.consumir())


@app.on_event("shutdown")
async def encerrar():
    servico.tarefa.cancel()
    await servico.pool.close()


@app.post("/registros")
async def registrar(payload: dict = Body(...)):
    servico.em_andamento += 1
    try:
        reg = servico.ler_payload(payload)
        if reg is None:
            return JSONResponse({"erro": "payload_invalido"}, status_code=422)
        servico.validar(reg)

        if servico.modo == "lote":
            try:
                servico.fila.put_nowait(reg)
            except asyncio.QueueFull:
                servico.recusados += 1
                return JSONResponse({"erro": "fila_cheia"}, status_code=503)
            servico.enfileirados += 1
            servico.pendentes += 1
            return JSONResponse({"id_evento": reg["id_evento"], "situacao": "enfileirado"}, status_code=202)
        elif servico.modo == "baseline":
            try:
                desfechos, motivos = await servico.gravar_com_retry([reg])
            except DadoCorrompido:
                return JSONResponse({"erro": "dado_corrompido"}, status_code=422)
            except ERROS_DE_CONEXAO:
                return JSONResponse({"erro": "banco_indisponivel"}, status_code=503)
            return JSONResponse({"id_evento": reg["id_evento"], "desfecho": desfechos[0], "motivo": motivos[0]},
                                status_code=201)
        else:
            return JSONResponse({"erro": f"modo desconhecido: {servico.modo}"}, status_code=500)
    finally:
        servico.em_andamento -= 1


@app.get("/saude")
async def saude():
    return {"ok": True}


@app.post("/admin/config")
async def configurar(novo: dict = Body(...)):
    if "modo" in novo:
        servico.modo = novo["modo"]
    if "tamanho_lote" in novo:
        servico.tamanho_lote = int(novo["tamanho_lote"])
    if "espera_ms" in novo:
        servico.espera_ms = int(novo["espera_ms"])
    if "tentativas" in novo:
        servico.tentativas = int(novo["tentativas"])
    return {"modo": servico.modo, "tamanho_lote": servico.tamanho_lote,
            "espera_ms": servico.espera_ms, "tentativas": servico.tentativas}


@app.post("/admin/reset")
async def reset(corpo: dict = Body(...)):
    n = int(corpo["servidores"])
    async with servico.pool.acquire() as conn, conn.transaction():
        await conn.execute("TRUNCATE pontos, eventos, servidores")
        await conn.execute("INSERT INTO servidores SELECT generate_series(1, $1)", n)
    servico.cadastro = set(range(1, n + 1))
    servico.zerar_contadores()
    servico.falha_ate = 0.0
    return {"servidores": n}


@app.post("/admin/falha")
async def falha(segundos: float = 10.0):
    servico.falha_ate = time.monotonic() + segundos
    log.warning("falha simulada do banco por %.1f s", segundos)
    return {"segundos": segundos}


@app.get("/admin/estado")
async def situacao():
    s = servico
    return {
        "config": {"modo": s.modo, "tamanho_lote": s.tamanho_lote, "espera_ms": s.espera_ms,
                   "tentativas": s.tentativas},
        "fila": s.fila.qsize(),
        "em_processamento": s.em_processamento,
        "ocioso": s.pendentes == 0 and s.em_andamento == 0,
        "em_andamento": s.em_andamento,
        "retries": s.retries,
        "lote_medio": round(sum(s.tamanhos) / len(s.tamanhos), 1) if s.tamanhos else 0,
        "enfileirados": s.enfileirados,
        "recusados": s.recusados,
        "lotes": s.lotes,
        "registros_gravados_em_lote": s.registros_gravados_em_lote,
        "registros_perdidos": s.registros_perdidos,
        "registros_corrompidos": s.registros_corrompidos,
    }
