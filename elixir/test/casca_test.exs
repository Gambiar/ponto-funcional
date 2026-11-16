defmodule Ponto.CascaTest do
  @moduledoc "Retry, falha simulada e fila com back-pressure (sem banco)."
  use ExUnit.Case, async: false
  alias Ponto.{Fila, Retry}

  test "retry repete erros de conexão e devolve o resultado" do
    {:ok, n} = Agent.start_link(fn -> 0 end)

    instavel = fn x ->
      if Agent.get_and_update(n, &{&1, &1 + 1}) < 2, do: raise(Ponto.FalhaSimulada), else: x * 2
    end

    assert Retry.com_retry(instavel, 5, base: 0.001).(21) == 42
    assert Agent.get(n, & &1) == 3
  end

  test "retry desiste depois das tentativas e propaga o erro" do
    sempre = fn _ -> raise Ponto.FalhaSimulada end
    assert_raise Ponto.FalhaSimulada, fn -> Retry.com_retry(sempre, 2, base: 0.001).(nil) end
  end

  test "retry não repete erro que não é de conexão" do
    {:ok, n} = Agent.start_link(fn -> 0 end)
    ruim = fn _ -> Agent.update(n, &(&1 + 1)); raise ArgumentError end
    assert_raise ArgumentError, fn -> Retry.com_retry(ruim, 5, base: 0.001).(nil) end
    assert Agent.get(n, & &1) == 1
  end

  test "falha simulada só enquanto o relógio estiver antes do prazo" do
    f = Retry.com_falha_simulada(&(&1 + 1), fn -> 10 end, fn -> 20 end)
    assert_raise Ponto.FalhaSimulada, fn -> f.(1) end
    assert Retry.com_falha_simulada(&(&1 + 1), fn -> 30 end, fn -> 20 end).(1) == 2
  end

  test "fila recusa quando cheia e entrega lotes até o máximo" do
    start_supervised!({Fila, 3})
    assert Enum.map(1..4, &Fila.enfileirar/1) == [true, true, true, false]
    assert Fila.tamanho() == 3
    assert Fila.coletar(2, 50) == [1, 2]
    assert Fila.coletar(10, 50) == [3]
  end

  test "a fila só conta como pendente o que de fato entrou (C16)" do
    {:ok, n} = Agent.start_link(fn -> 0 end)
    start_supervised!({Fila, {2, fn -> Agent.update(n, &(&1 + 1)) end}})
    assert Enum.map(1..5, &Fila.enfileirar/1) == [true, true, false, false, false]
    assert Agent.get(n, & &1) == 2
  end

  test "enfileirar sem resposta no prazo não derruba o chamador" do
    start_supervised!({Fila, {10, fn -> Process.sleep(200) end}})
    assert Fila.enfileirar(:a, 10) == :sem_resposta
  end
end
