import gleam/dict.{type Dict}
import gleam/list
import gleam/option.{None, Some}
import gleam/set.{type Set}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 7

fn parse_lines(lines: List(String)) -> #(Set(#(Int, Int)), #(Int, Int), Int) {
  let splitters =
    lines
    |> list.index_map(fn(line, y) {
      line
      |> string.to_graphemes
      |> list.index_map(fn(char, x) {
        case char {
          "^" -> Ok(#(x, y))
          _ -> Error(Nil)
        }
      })
      |> list.filter_map(fn(x) { x })
    })
    |> list.flatten()
    |> set.from_list

  let start = case list.first(lines) {
    Ok(line) ->
      string.to_graphemes(line)
      |> list.index_fold(#(0, 0), fn(start, char, x) {
        case char {
          "S" -> #(x, 0)
          _ -> start
        }
      })

    Error(Nil) -> #(0, 0)
  }
  #(splitters, start, list.length(lines))
}

fn fall_down1(
  splitters: Set(#(Int, Int)),
  max_y: Int,
  positions: List(#(Int, Int)),
  seen_splitters: Set(#(Int, Int)),
  count: Int,
) -> Int {
  case positions {
    [#(x, y), ..rest] -> {
      let next_y = y + 1
      case next_y >= max_y || set.contains(seen_splitters, #(x, next_y)) {
        False -> {
          let #(positions, seen_splitters, count) = case
            set.contains(splitters, #(x, next_y))
          {
            True -> #(
              [#(x - 1, next_y), #(x + 1, next_y), ..rest],
              set.insert(seen_splitters, #(x, next_y)),
              count + 1,
            )
            False -> #([#(x, next_y), ..rest], seen_splitters, count)
          }
          fall_down1(splitters, max_y, positions, seen_splitters, count)
        }
        True -> fall_down1(splitters, max_y, rest, seen_splitters, count)
      }
    }
    _ -> count
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start, max_y) = parse_lines(lines)

  fall_down1(splitters, max_y, [start], set.new(), 0)
}

fn fall_down2(
  splitters: Set(#(Int, Int)),
  max_y: Int,
  position: #(Int, Int),
  seen_pathes: Dict(#(Int, Int), Int),
) -> #(Int, Dict(#(Int, Int), Int)) {
  let #(x, y) = position
  let next_y = y + 1
  case next_y >= max_y, dict.get(seen_pathes, #(x, next_y)) {
    False, Ok(c) -> #(c, seen_pathes)
    False, _ -> {
      case set.contains(splitters, #(x, next_y)) {
        True -> {
          let #(count1, seen_pathes) =
            fall_down2(splitters, max_y, #(x - 1, next_y), seen_pathes)
          let #(count2, seen_pathes) =
            fall_down2(splitters, max_y, #(x + 1, next_y), seen_pathes)
          let seen_pathes =
            dict.insert(seen_pathes, #(x, next_y), count1 + count2)
          #(count1 + count2, seen_pathes)
        }
        False -> fall_down2(splitters, max_y, #(x, next_y), seen_pathes)
      }
    }
    True, _ -> #(1, seen_pathes)
  }
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start, max_y) = parse_lines(lines)

  let #(count, _) = fall_down2(splitters, max_y, start, dict.new())
  count
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(21), Some(40)),
      Expected(0, Some(1594), Some(15_650_261_281_478)),
    ],
    run1,
    run2,
    False,
  )
}
