defmodule Ponto.Repo do
  @moduledoc "Persistência em lote no PostgreSQL (casca). Mesmo SQL da versão Python."
  alias Ponto.{Nucleo, Registro}

  @db Ponto.DB

  @esquema [
    "CREATE TABLE IF NOT EXISTS servidores (id INTEGER PRIMARY KEY)",
    """
    CREATE TABLE IF NOT EXISTS pontos (
        id_evento UUID PRIMARY KEY, servidor INTEGER NOT NULL, tipo TEXT NOT NULL,
        dia DATE NOT NULL, instante TIMESTAMP NOT NULL, dispositivo TEXT NOT NULL,
        UNIQUE (servidor, tipo, dia))
    """,
    """
    CREATE TABLE IF NOT EXISTS eventos (
        id_evento UUID PRIMARY KEY, servidor INTEGER NOT NULL, tipo TEXT NOT NULL,
        instante TIMESTAMP NOT NULL, desfecho TEXT NOT NULL, motivo TEXT,
        processado_em TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp())
    """
  ]

  # uuid chega como texto e é convertido no SQL (Postgrex esperaria 16 bytes)
  @inserir_pontos """
  INSERT INTO pontos (id_evento, servidor, tipo, dia, instante, dispositivo)
  SELECT u::uuid, s, t, d, i, x
  FROM unnest($1::text[], $2::int[], $3::text[], $4::date[], $5::timestamp[], $6::text[]) AS q(u, s, t, d, i, x)
  ON CONFLICT DO NOTHING
  RETURNING id_evento::text
  """

  @entradas_existentes """
  SELECT p.servidor, p.dia FROM pontos p
  JOIN unnest($1::int[], $2::date[]) AS q(servidor, dia) USING (servidor, dia)
  WHERE p.tipo = 'entrada'
  """

  @inserir_eventos """
  INSERT INTO eventos (id_evento, servidor, tipo, instante, desfecho, motivo)
  SELECT u::uuid, s, t, i, d, m
  FROM unnest($1::text[], $2::int[], $3::text[], $4::timestamp[], $5::text[], $6::text[]) AS q(u, s, t, i, d, m)
  ON CONFLICT (id_evento) DO NOTHING
  """

  def criar_esquema(_ \\ nil), do: Enum.each(@esquema, &Postgrex.query!(@db, &1, []))

  def reiniciar(n) do
    Postgrex.transaction(@db, fn conn ->
      Postgrex.query!(conn, "TRUNCATE pontos, eventos, servidores", [])
      Postgrex.query!(conn, "INSERT INTO servidores SELECT generate_series(1, $1::int)", [n])
    end)
  end

  def carregar_cadastro do
    %{rows: rows} = Postgrex.query!(@db, "SELECT id FROM servidores", [])
    MapSet.new(rows, fn [id] -> id end)
  end

  @doc "Grava um lote numa única transação e devolve o desfecho de cada registro."
  def gravar_lote(resultados) do
    lote = Nucleo.ordenar(resultados)
    entradas = Nucleo.aceitos_por_tipo(lote, "entrada")
    saidas = Nucleo.aceitos_por_tipo(lote, "saida")

    transacao =
      Postgrex.transaction(@db, fn conn ->
        # entradas antes: uma saída do mesmo lote pode depender delas
        inseridos_entradas = inserir(conn, entradas)
        {validas, sem_entrada} = Nucleo.separar_saidas(saidas, entradas_existentes(conn, saidas))
        inseridos = MapSet.union(inseridos_entradas, inserir(conn, validas))
        desfechos = Nucleo.resolver_desfechos(lote, inseridos, MapSet.new(sem_entrada, & &1.id_evento))
        regs = Enum.map(lote, &Nucleo.registro/1)

        Postgrex.query!(conn, @inserir_eventos, [
          Enum.map(regs, & &1.id_evento),
          Enum.map(regs, & &1.servidor),
          Enum.map(regs, & &1.tipo),
          Enum.map(regs, & &1.instante),
          Enum.map(desfechos, &elem(&1, 1)),
          Enum.map(desfechos, &elem(&1, 2))
        ])

        desfechos
      end)

    case transacao do
      {:ok, desfechos} -> desfechos
      {:error, motivo} -> raise DBConnection.ConnectionError, "transação abortada: #{inspect(motivo)}"
    end
  end

  defp entradas_existentes(_conn, []), do: MapSet.new()

  defp entradas_existentes(conn, saidas) do
    %{rows: rows} =
      Postgrex.query!(conn, @entradas_existentes, [
        Enum.map(saidas, & &1.servidor),
        Enum.map(saidas, &Registro.dia/1)
      ])

    MapSet.new(rows, fn [servidor, dia] -> {servidor, dia} end)
  end

  defp inserir(_conn, []), do: MapSet.new()

  defp inserir(conn, regs) do
    %{rows: rows} =
      Postgrex.query!(conn, @inserir_pontos, [
        Enum.map(regs, & &1.id_evento),
        Enum.map(regs, & &1.servidor),
        Enum.map(regs, & &1.tipo),
        Enum.map(regs, &Registro.dia/1),
        Enum.map(regs, & &1.instante),
        Enum.map(regs, & &1.dispositivo)
      ])

    MapSet.new(rows, fn [id] -> id end)
  end
end
