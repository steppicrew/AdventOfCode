import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 5

fn parse_line(lines: List(String)) -> #(List(#(Int, Int)), List(Int)) {
  let assert Ok(re) = regexp.from_string("(\\d+)-(\\d+)")

  let ranges =
    lines
    |> list.filter_map(fn(line) {
      case regexp.scan(re, line) {
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

  let assert Ok(re) = regexp.from_string("^(\\d+)$")

  let ingredients =
    lines
    |> list.filter_map(fn(line) {
      case regexp.scan(re, line) {
        [match] ->
          case match.submatches {
            [Some(a)] -> {
              case int.parse(a) {
                Ok(a) -> Ok(a)
                _ -> Error(Nil)
              }
            }
            _ -> Error(Nil)
          }
        _ -> Error(Nil)
      }
    })

  #(ranges, ingredients)
}

fn run1(lines: List(String)) -> Int {
  let #(ranges, ingredients) = parse_line(lines)

  ingredients
  |> list.filter(fn(ingredient) {
    ranges
    |> list.any(fn(range) {
      let #(from, to) = range
      ingredient >= from && ingredient <= to
    })
  })
  |> list.length
}

fn run2(lines: List(String)) -> Int {
  let #(ranges, _) = parse_line(lines)

  let #(count, _) =
    ranges
    |> list.sort(fn(a, b) {
      let #(a_from, _) = a
      let #(b_from, _) = b
      int.compare(a_from, b_from)
    })
    |> list.fold(#(0, 0), fn(acc, range) {
      let #(count, current_end) = acc
      let #(from, to) = range
      case from > current_end {
        True -> #(count + { to - from + 1 }, to)
        False ->
          case to > current_end {
            True -> #(count + { to - current_end }, to)
            False -> #(count, current_end)
          }
      }
    })

  count
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(3), Some(14)),
      Expected(0, Some(756), Some(355_555_479_253_787)),
    ],
    run1,
    run2,
    False,
  )
}
