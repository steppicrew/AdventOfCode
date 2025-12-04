import gleam/list
import gleam/option.{Some}
import gleam/set.{type Set}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 4

fn parse_lines(lines: List(String)) -> Set(#(Int, Int)) {
  lines
  |> list.index_map(fn(line, y) {
    line
    |> string.split("")
    |> list.index_map(fn(char, x) {
      case char {
        "@" -> Ok(#(x, y))
        _ -> Error(Nil)
      }
    })
    |> list.filter_map(fn(r) { r })
  })
  |> list.flatten
  |> set.from_list()
}

fn get_test(rolls: Set(#(Int, Int))) -> fn(#(Int, Int)) -> Bool {
  fn(pos: #(Int, Int)) -> Bool {
    let #(x, y) = pos
    [
      #(x - 1, y),
      #(x + 1, y),
      #(x, y - 1),
      #(x, y + 1),
      #(x - 1, y - 1),
      #(x - 1, y + 1),
      #(x + 1, y - 1),
      #(x + 1, y + 1),
    ]
    |> list.count(fn(n) { set.contains(rolls, n) })
    < 4
  }
}

fn run1(lines: List(String)) -> Int {
  let rolls = parse_lines(lines)

  rolls
  |> set.to_list
  |> list.filter(get_test(rolls))
  |> list.length
}

fn remove_rolls(rolls: Set(#(Int, Int))) -> Set(#(Int, Int)) {
  let rolls_to_remove =
    rolls
    |> set.to_list
    |> list.filter(get_test(rolls))
    |> set.from_list

  case rolls_to_remove |> set.is_empty {
    True -> rolls
    False ->
      remove_rolls(
        rolls
        |> set.difference(rolls_to_remove),
      )
  }
}

fn run2(lines: List(String)) -> Int {
  let rolls = parse_lines(lines)

  set.size(rolls) - set.size(remove_rolls(rolls))
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(13), Some(43)),
      Expected(0, Some(1467), Some(8484)),
    ],
    run1,
    run2,
    False,
  )
}
