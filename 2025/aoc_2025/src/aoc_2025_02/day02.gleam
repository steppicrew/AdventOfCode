import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 2

fn parse_lines(lines: List(String)) -> List(#(Int, Int)) {
  let assert Ok(re) = regexp.from_string("(\\d+)-(\\d+)")
  lines
  |> string.join("")
  |> string.split(",")
  |> list.filter_map(fn(part) {
    case regexp.scan(re, part) {
      [match] ->
        case match.submatches {
          [Some(a), Some(b)] -> {
            case int.parse(a), int.parse(b) {
              Ok(a), Ok(b) -> Ok(#(a, b))
              _, _ -> Error(Nil)
            }
          }
          _ -> Error(Nil)
        }
      _ -> Error(Nil)
    }
  })
}

fn run1(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("^(\\d+)(\\1)$")
  lines
  |> parse_lines
  |> list.map(fn(range) {
    let #(from, until) = range
    list.range(from, until)
    |> list.filter(fn(n) { regexp.check(re, int.to_string(n)) })
    |> int.sum
  })
  |> int.sum
}

fn run2(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("^(\\d+)(\\1)+$")
  lines
  |> parse_lines
  |> list.map(fn(range) {
    let #(from, until) = range
    list.range(from, until)
    |> list.filter(fn(n) { regexp.check(re, int.to_string(n)) })
    |> int.sum
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(1_227_775_554), Some(4_174_379_265)),
      Expected(0, Some(31_000_881_061), Some(46_769_308_485)),
    ],
    run1,
    run2,
    False,
  )
}
