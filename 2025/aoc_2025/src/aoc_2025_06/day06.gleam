import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 6

fn run1(lines: List(String), _: RunEnv) -> Int {
  let table =
    lines
    |> list.map(fn(line) {
      line |> string.split(" ") |> list.filter(fn(s) { s != "" })
    })

  let acc0 = case list.first(table) {
    Ok(l) -> list.map(l, fn(_) { [] })
    Error(Nil) -> []
  }

  table
  |> list.fold(acc0, fn(acc, row) {
    list.zip(acc, row)
    |> list.map(fn(pair) {
      let #(numbers, value) = pair
      case int.parse(value) {
        Ok(number) -> [number, ..numbers]
        Error(_) ->
          case value {
            "+" -> [int.sum(numbers)]
            "*" -> [int.product(numbers)]
            _ -> numbers
          }
      }
    })
  })
  |> list.flatten
  |> int.sum
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  lines
  |> list.map(fn(line) { string.to_graphemes(line) })
  |> list.transpose()
  |> list.filter_map(fn(chars) {
    let value = string.join(chars, "") |> string.trim
    case string.is_empty(value) {
      True -> Error(Nil)
      False -> Ok(value)
    }
  })
  |> list.fold([], fn(acc, value) {
    let #(acc, value) = case string.last(value) {
      Ok("+") -> #(
        [#(int.sum, []), ..acc],
        value
          |> string.slice(0, string.length(value) - 1)
          |> string.trim,
      )
      Ok("*") -> #(
        [#(int.product, []), ..acc],
        value
          |> string.slice(0, string.length(value) - 1)
          |> string.trim,
      )
      _ -> #(acc, value)
    }

    case int.parse(value) {
      Ok(value) ->
        case list.first(acc) {
          Ok(#(fun, values)) -> [#(fun, [value, ..values]), ..list.drop(acc, 1)]
          Error(_) -> acc
        }
      Error(_) -> acc
    }
  })
  |> list.map(fn(task) {
    let #(fun, values) = task
    fun(values)
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(4_277_556), Some(3_263_827)),
      Expected(0, Some(5_227_286_044_585), Some(10_227_753_257_799)),
    ],
    run1,
    run2,
    False,
  )
}
