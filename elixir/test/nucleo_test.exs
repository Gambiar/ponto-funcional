defmodule Ponto.NucleoTest do
  @moduledoc "Mesmos casos de tests/test_nucleo.py, para o núcleo Elixir (sem banco nem rede)."
  use ExUnit.Case, async: true
  alias Ponto.{Nucleo, Registro}

  @cadastro MapSet.new(1..100)

  defp reg(id \\ "a", servidor \\ 1, tipo \\ "entrada", hora \\ 8) do
    %Registro{id_evento: id, servidor: servidor, tipo: tipo,
              instante: NaiveDateTime.new!(2026, 11, 3, hora, 0, 0), dispositivo: "rep-1"}
  end

  defp validar(r), do: Nucleo.criar_validador(Nucleo.regras_padrao(@cadastro)).(r)

  # ------------------------------------------------------------- interpretar

  test "interpreta payload válido" do
    payload = %{"id_evento" => "x", "servidor" => 5, "tipo" => "entrada",
                "instante" => "2026-11-03T08:00:00", "dispositivo" => "d"}
    assert Nucleo.interpretar(payload) ==
             %Registro{id_evento: "x", servidor: 5, tipo: "entrada",
                       instante: ~N[2026-11-03 08:00:00], dispositivo: "d"}
  end

  test "recusa payloads inválidos" do
    base = %{"id_evento" => "x", "servidor" => 5, "tipo" => "entrada",
             "instante" => "2026-11-03T08:00:00", "dispositivo" => "d"}

    for payload <- [nil, [], %{}, %{"id_evento" => "x"},
                    %{base | "servidor" => "5"},
                    %{base | "servidor" => true},
                    %{base | "instante" => "ontem"}] do
      assert Nucleo.interpretar(payload) == nil, "deveria recusar #{inspect(payload)}"
    end
  end

  # ---------------------------------------------------------------- validar

  test "regras de validação, primeira violada vence" do
    casos = [
      {reg(), nil},
      {reg("a", 1, "saida"), nil},
      {reg("a", 1, "intervalo"), "tipo_invalido"},
      {reg("a", 999), "servidor_inexistente"},
      {reg("a", 1, "entrada", 3), "fora_da_jornada"},
      {reg("a", 999, "xyz", 3), "tipo_invalido"}
    ]

    for {r, esperado} <- casos do
      case validar(r) do
        {:aceito, _} -> assert esperado == nil
        {:rejeitado, _, motivo} -> assert motivo == esperado
      end
    end
  end

  # ------------------------------------------------------------------ lotes

  test "bissectar divide ao meio como a versão Python" do
    assert Nucleo.bissectar([1, 2, 3]) == {[1], [2, 3]}
  end

  test "ordenar: o mais antigo primeiro, desempate por id" do
    tardio = {:aceito, reg("b", 1, "entrada", 9)}
    cedo = {:aceito, reg("z", 1, "entrada", 8)}
    empate = {:aceito, reg("a", 1, "entrada", 8)}
    assert Nucleo.ordenar([tardio, cedo, empate]) == [empate, cedo, tardio]
  end

  test "separar saídas com e sem entrada" do
    s1 = reg("s1", 1, "saida", 12)
    s2 = reg("s2", 2, "saida", 12)
    assert Nucleo.separar_saidas([s1, s2], MapSet.new([{1, ~D[2026-11-03]}])) == {[s1], [s2]}
  end

  test "desfechos: gravado, duplicado, saída sem entrada e rejeitado" do
    resultados = [
      {:aceito, reg("e1")},
      {:aceito, reg("e2")},
      {:aceito, reg("s1", 3, "saida")},
      {:rejeitado, reg("x", 999), "servidor_inexistente"}
    ]

    assert Nucleo.resolver_desfechos(resultados, MapSet.new(["e1"]), MapSet.new(["s1"])) == [
             {"e1", "gravado", nil},
             {"e2", "descartado", "duplicado"},
             {"s1", "rejeitado", "saida_sem_entrada"},
             {"x", "rejeitado", "servidor_inexistente"}
           ]
  end

  test "aceitos_por_tipo ignora rejeitados" do
    e = reg("e")
    resultados = [{:aceito, e}, {:aceito, reg("s", 1, "saida")}, {:rejeitado, reg("r"), "tipo_invalido"}]
    assert Nucleo.aceitos_por_tipo(resultados, "entrada") == [e]
  end
end
