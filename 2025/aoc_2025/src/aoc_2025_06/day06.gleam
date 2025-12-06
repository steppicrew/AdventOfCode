import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/result
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 6

fn parse_lines(lines: List(String)) -> List(#(List(Int), String)) {
  let assert Ok(re_numbers) = regexp.from_string("\\d+")
  let assert Ok(re_operators) = regexp.from_string("[+*]")

  let operators =
    regexp.scan(
      re_operators,
      lines
        |> list.last
        |> result.unwrap(""),
    )
    |> list.map(fn(op_str) -> String { op_str.content })

  let init =
    operators
    |> list.map(fn(op) -> #(List(Int), String) { #([], op) })

  lines
  |> list.fold(init, fn(acc, line) -> List(#(List(Int), String)) {
    case regexp.scan(re_numbers, line) {
      [] -> acc
      numbers_strs -> {
        numbers_strs
        |> list.map(fn(n_str) -> Int {
          int.parse(n_str.content) |> result.unwrap(0)
        })
        |> list.zip(acc)
        |> list.map(fn(pair) {
          let #(num, #(nums, op)) = pair
          #([num, ..nums], op)
        })
      }
    }
  })
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  parse_lines(lines)
  |> list.map(fn(quest) -> Int {
    let #(nums, op) = quest
    case op {
      "+" -> int.sum(nums)
      "*" -> int.product(nums)
      _ -> 0
    }
  })
  |> int.sum()
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let assert Ok(re_numbers) = regexp.from_string("\\d+")
  let assert Ok(re_operators) = regexp.from_string("[+*]")

  let #(sum, current, _) =
    lines
    |> list.map(fn(line) { string.to_graphemes(line) })
    |> list.transpose()
    |> list.map(fn(chars) { string.join(chars, "") })
    |> list.fold(#(0, 0, ""), fn(acc, part) {
      let #(sum, current_value, current_op) = acc
      case regexp.scan(re_numbers, part) {
        [num] ->
          case int.parse(num.content) {
            Ok(num) -> {
              case regexp.scan(re_operators, part) {
                [op] -> #(sum + current_value, num, op.content)
                _ ->
                  case current_op {
                    "+" -> #(sum, current_value + num, current_op)
                    "*" -> #(sum, current_value * num, current_op)
                    _ -> acc
                  }
              }
            }
            Error(_) -> acc
          }
        _ -> acc
      }
    })
  sum + current
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
