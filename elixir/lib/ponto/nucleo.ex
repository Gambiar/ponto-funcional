defmodule Ponto.Registro do
  @moduledoc "Registro de ponto (imutável, como todo dado em Elixir)."
  @enforce_keys [:id_evento, :servidor, :tipo, :instante, :dispositivo]
  defstruct @enforce_keys

  def dia(%__MODULE__{instante: i}), do: NaiveDateTime.to_date(i)
end

defmodule Ponto.Nucleo do
  @moduledoc """
  Núcleo funcional: funções puras, sem rede, banco ou relógio.
  Equivalente a `ponto.nucleo.validacao` + `ponto.nucleo.lotes` da versão Python.

  Resultado de validação: `{:aceito, registro}` | `{:rejeitado, registro, motivo}`.
  Desfecho: `{id_evento, desfecho, motivo | nil}`.
  """
  alias Ponto.Registro

  # ------------------------------------------------------------ interpretar

  def interpretar(%{
        "id_evento" => id,
        "servidor" => servidor,
        "tipo" => tipo,
        "instante" => texto,
        "dispositivo" => disp
      })
      when is_binary(id) and is_integer(servidor) and is_binary(tipo) and is_binary(texto) and
             is_binary(disp) do
    case NaiveDateTime.from_iso8601(texto) do
      {:ok, instante} ->
        %Registro{id_evento: id, servidor: servidor, tipo: tipo, instante: instante, dispositivo: disp}

      {:error, _} ->
        nil
    end
  end

  def interpretar(_), do: nil

  # ----------------------------------------------------------------- regras

  def regra_tipo(%Registro{tipo: t}) when t in ["entrada", "saida"], do: nil
  def regra_tipo(_), do: "tipo_invalido"

  def regra_servidor(cadastro) do
    fn r -> if MapSet.member?(cadastro, r.servidor), do: nil, else: "servidor_inexistente" end
  end

  def regra_jornada(inicio \\ 6, fim \\ 24) do
    fn
      %Registro{instante: %{hour: h}} when h >= inicio and h < fim -> nil
      _ -> "fora_da_jornada"
    end
  end

  def regras_padrao(cadastro), do: [&regra_tipo/1, regra_servidor(cadastro), regra_jornada()]

  def criar_validador(regras) do
    fn registro ->
      # find_value para na primeira regra violada (avaliação preguiçosa)
      case Enum.find_value(regras, & &1.(registro)) do
        nil -> {:aceito, registro}
        motivo -> {:rejeitado, registro, motivo}
      end
    end
  end

  # ------------------------------------------------------------------ lotes

  def registro({:aceito, r}), do: r
  def registro({:rejeitado, r, _}), do: r

  def bissectar(lote), do: Enum.split(lote, div(length(lote), 2))

  @doc "Ordena pelo instante: em duplicatas, o registro mais antigo vence."
  def ordenar(resultados) do
    Enum.sort_by(resultados, fn res ->
      r = registro(res)
      {NaiveDateTime.to_gregorian_seconds(r.instante), r.id_evento}
    end)
  end

  def aceitos_por_tipo(resultados, tipo) do
    for {:aceito, %Registro{tipo: ^tipo} = r} <- resultados, do: r
  end

  @doc "Saídas com entrada correspondente seguem; as demais são rejeitadas."
  def separar_saidas(saidas, entradas_existentes) do
    Enum.split_with(saidas, &MapSet.member?(entradas_existentes, {&1.servidor, Registro.dia(&1)}))
  end

  def desfecho({:rejeitado, r, motivo}, _inseridos, _sem_entrada), do: {r.id_evento, "rejeitado", motivo}

  def desfecho({:aceito, r}, inseridos, sem_entrada) do
    cond do
      MapSet.member?(sem_entrada, r.id_evento) -> {r.id_evento, "rejeitado", "saida_sem_entrada"}
      MapSet.member?(inseridos, r.id_evento) -> {r.id_evento, "gravado", nil}
      true -> {r.id_evento, "descartado", "duplicado"}
    end
  end

  def resolver_desfechos(resultados, inseridos, sem_entrada) do
    Enum.map(resultados, &desfecho(&1, inseridos, sem_entrada))
  end
end
