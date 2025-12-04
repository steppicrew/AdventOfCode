import gleam/list
import gleam/option.{Some}
import gleam/set.{type Set}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 4

const neighbour_offsets: List(#(Int, Int)) = [
  #(-1, 0),
  #(1, 0),
  #(0, -1),
  #(0, 1),
  #(-1, -1),
  #(-1, 1),
  #(1, -1),
  #(1, 1),
]

fn parse_lines(lines: List(String)) -> Set(#(Int, Int)) {
  lines
  |> list.index_map(fn(line, y) {
    line
    |> string.to_graphemes
    |> list.index_map(fn(char, x) {
      case char {
        "@" -> Ok(#(x, y))
        _ -> Error(Nil)
      }
    })
    |> list.filter_map(fn(position) { position })
  })
  |> list.flatten
  |> set.from_list()
}

fn get_test_removable(rolls: Set(#(Int, Int))) -> fn(#(Int, Int)) -> Bool {
  fn(pos: #(Int, Int)) -> Bool {
    let #(x, y) = pos
    neighbour_offsets
    |> list.count(fn(offset) {
      let #(dx, dy) = offset
      set.contains(rolls, #(x + dx, y + dy))
    })
    < 4
  }
}

fn run1(lines: List(String)) -> Int {
  let rolls = parse_lines(lines)

  rolls
  |> set.to_list
  |> list.filter(get_test_removable(rolls))
  |> list.length
}

fn remove_rolls(rolls: Set(#(Int, Int))) -> Set(#(Int, Int)) {
  let rolls_to_remove =
    rolls
    |> set.to_list
    |> list.filter(get_test_removable(rolls))
    |> set.from_list

  case set.is_empty(rolls_to_remove) {
    True -> rolls
    False ->
      rolls
      |> set.difference(rolls_to_remove)
      |> remove_rolls
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
