defmodule Ponto.FalhaSimulada do
  defexception message: "banco indisponível (falha simulada)"
end

defmodule Ponto.ErroDeDados do
  @moduledoc "Erro causado pelo conteúdo do lote (não adianta repetir)."
  defexception [:message]
end

defmodule Ponto.Retry do
  @moduledoc """
  Funções de ordem superior para resiliência: recebem uma função e devolvem
  outra (o equivalente aos decoradores de `ponto.util.retry`).
  """
  require Logger

  @doc "Repete com backoff exponencial: base, 2*base, 4*base... até `maximo` (s)."
  def com_retry(fun, tentativas, opts \\ []) do
    base = Keyword.get(opts, :base, 0.2)
    maximo = Keyword.get(opts, :maximo, 5.0)
    ao_falhar = Keyword.get(opts, :ao_falhar, fn _n, _erro -> :ok end)
    fn arg -> tentar(fun, arg, 1, tentativas, base, maximo, ao_falhar) end
  end

  defp tentar(fun, arg, n, tentativas, base, maximo, ao_falhar) do
    fun.(arg)
  rescue
    erro ->
      if conexao?(erro) and n < tentativas do
        ao_falhar.(n, erro)
        Process.sleep(round(min(maximo, base * :math.pow(2, n - 1)) * 1000))
        tentar(fun, arg, n + 1, tentativas, base, maximo, ao_falhar)
      else
        reraise erro, __STACKTRACE__
      end
  end

  @doc "Falha enquanto o relógio estiver antes de `falha_ate.()`."
  def com_falha_simulada(fun, agora, falha_ate) do
    fn arg ->
      if agora.() < falha_ate.() do
        Process.sleep(50)
        raise Ponto.FalhaSimulada
      else
        fun.(arg)
      end
    end
  end

  @doc "Converte erros de conteúdo do Postgres (classe 22) em ErroDeDados (sem retry)."
  def traduzir_erros(fun) do
    fn arg ->
      try do
        fun.(arg)
      rescue
        erro in Postgrex.Error ->
          case erro do
            %Postgrex.Error{postgres: %{pg_code: "22" <> _}} ->
              reraise Ponto.ErroDeDados, [message: Exception.message(erro)], __STACKTRACE__

            _ ->
              reraise erro, __STACKTRACE__
          end
      end
    end
  end

  def conexao?(%DBConnection.ConnectionError{}), do: true
  def conexao?(%Ponto.FalhaSimulada{}), do: true

  def conexao?(%Postgrex.Error{postgres: %{code: code}})
      when code in [:too_many_connections, :cannot_connect_now, :admin_shutdown],
      do: true

  def conexao?(_), do: false
end
