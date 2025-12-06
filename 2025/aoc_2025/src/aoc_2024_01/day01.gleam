import gleam/dict
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2024

const day = 1

fn parse_lines(lines: List(String)) -> #(List(Int), List(Int)) {
  lines
  |> list.filter_map(fn(s) {
    case string.split(s, " ") |> list.filter(fn(s) { s != "" }) {
      [left, right] -> {
        case int.parse(left), int.parse(right) {
          Ok(left), Ok(right) -> Ok(#(left, right))
          _, _ -> Error(Nil)
        }
      }
      _ -> Error(Nil)
    }
  })
  |> list.unzip()
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(left, right) = parse_lines(lines)

  let left = list.sort(left, int.compare)
  let right = list.sort(right, int.compare)
  list.zip(left, right)
  |> list.map(fn(pair) {
    let #(left, right) = pair
    int.absolute_value(right - left)
  })
  |> int.sum()
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let #(left, right) = parse_lines(lines)

  let counts =
    right
    |> list.fold(dict.new(), fn(counts, n) {
      counts
      |> dict.upsert(n, fn(count) {
        case count {
          Some(count) -> count + 1
          _ -> 1
        }
      })
    })

  left
  |> list.map(fn(n) {
    case counts |> dict.get(n) {
      Ok(count) -> n * count
      _ -> 0
    }
  })
  |> int.sum()
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(11), Some(31)),
      Expected(0, Some(1_889_772), Some(23_228_917)),
    ],
    run1,
    run2,
    False,
  )
}
