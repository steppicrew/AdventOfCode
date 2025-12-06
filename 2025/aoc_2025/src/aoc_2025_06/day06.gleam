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
      let #(nums, number) = pair
      case int.parse(number) {
        Ok(n) -> [n, ..nums]
        Error(_) ->
          case number {
            "+" -> [int.sum(nums)]
            "*" -> [int.product(nums)]
            _ -> nums
          }
      }
    })
  })
  |> list.map(fn(nums) {
    case list.first(nums) {
      Ok(n) -> n
      Error(_) -> 0
    }
  })
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
    case string.last(value) {
      Ok("+") ->
        case
          value
          |> string.slice(0, string.length(value) - 1)
          |> string.trim
          |> int.parse
        {
          Ok(number) -> [#(int.sum, [number]), ..acc]
          Error(_) -> acc
        }
      Ok("*") ->
        case
          value
          |> string.slice(0, string.length(value) - 1)
          |> string.trim
          |> int.parse
        {
          Ok(number) -> [#(int.product, [number]), ..acc]
          Error(_) -> acc
        }
      _ -> {
        case int.parse(value) {
          Ok(value) ->
            case list.first(acc) {
              Ok(#(fun, values)) -> [
                #(fun, [value, ..values]),
                ..list.drop(acc, 1)
              ]
              Error(_) -> acc
            }
          Error(_) -> acc
        }
      }
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
