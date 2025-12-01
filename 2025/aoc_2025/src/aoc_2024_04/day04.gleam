import gleam/dict
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/result
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2024

const day = 4

fn parse_lines(lines: List(String)) -> dict.Dict(#(Int, Int), String) {
  lines
  |> list.index_fold(dict.new(), fn(map, line, y) {
    line
    |> string.split("")
    |> list.index_fold(map, fn(map, char, x) {
      map |> dict.insert(#(x, y), char)
    })
  })
}

fn run1(lines: List(String)) -> Int {
  let map = parse_lines(lines)

  let xmas = "XMAS" |> string.split("")

  let test_word = fn(x: Int, y: Int, dx: Int, dy: Int) -> Int {
    case
      xmas
      |> list.index_map(fn(char, i) {
        case dict.get(map, #(x + i * dx, y + i * dy)) {
          Ok(c) if c == char -> True
          _ -> False
        }
      })
      |> list.all(fn(b) { b })
    {
      True -> 1
      False -> 0
    }
  }

  let test_position = fn(x: Int, y: Int) -> Int {
    test_word(x, y, 1, 1)
    + test_word(x, y, 1, 0)
    + test_word(x, y, 1, -1)
    + test_word(x, y, -1, 1)
    + test_word(x, y, -1, 0)
    + test_word(x, y, -1, -1)
    + test_word(x, y, 0, 1)
    + test_word(x, y, 0, -1)
  }

  lines
  |> list.index_map(fn(line, y) {
    list.range(0, string.length(line) - 1)
    |> list.map(fn(x) { test_position(x, y) })
    |> int.sum
  })
  |> int.sum
}

fn run2(lines: List(String)) -> Int {
  let map = parse_lines(lines)

  let get_around = fn(x: Int, y: Int, dx: Int, dy: Int) -> Bool {
    case dict.get(map, #(x + dx, y + dy)), dict.get(map, #(x - dx, y - dy)) {
      Ok(c1), Ok(c2) if c1 == "M" && c2 == "S" -> True
      _, _ -> False
    }
  }

  let test_position = fn(x: Int, y: Int) -> Int {
    case
      dict.get(map, #(x, y)) |> result.unwrap("") == "A"
      && { get_around(x, y, 1, 1) || get_around(x, y, -1, -1) }
      && { get_around(x, y, -1, 1) || get_around(x, y, 1, -1) }
    {
      True -> 1
      False -> 0
    }
  }

  lines
  |> list.index_map(fn(line, y) {
    list.range(0, string.length(line) - 1)
    |> list.map(fn(x) { test_position(x, y) })
    |> int.sum
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(18), Some(9)),
      Expected(0, Some(2644), Some(1952)),
    ],
    run1,
    run2,
    False,
  )
}
