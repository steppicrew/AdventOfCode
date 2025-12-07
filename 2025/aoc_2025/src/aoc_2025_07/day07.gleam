import gleam/dict.{type Dict}
import gleam/list
import gleam/option.{Some}
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
  len_y: Int,
  positions: List(#(Int, Int)),
  seen_splitters: Set(#(Int, Int)),
  count: Int,
) -> Int {
  case positions {
    [#(x, y), ..rest] -> {
      let next_y = y + 1
      let next_position = #(x, next_y)
      let #(positions, seen_splitters, count) = case
        next_y < len_y,
        seen_splitters |> set.contains(next_position),
        splitters |> set.contains(next_position)
      {
        True, False, True -> #(
          [#(x - 1, next_y), #(x + 1, next_y), ..rest],
          set.insert(seen_splitters, next_position),
          count + 1,
        )
        True, False, False -> #([next_position, ..rest], seen_splitters, count)
        _, _, _ -> #(rest, seen_splitters, count)
      }
      fall_down1(splitters, len_y, positions, seen_splitters, count)
    }
    _ -> count
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start, len_y) = parse_lines(lines)

  fall_down1(splitters, len_y, [start], set.new(), 0)
}

const dxs = [-1, 1]

fn fall_down2(
  splitters: Set(#(Int, Int)),
  len_y: Int,
  position: #(Int, Int),
  seen_pathes: Dict(#(Int, Int), Int),
) -> #(Int, Dict(#(Int, Int), Int)) {
  let #(x, y) = position
  let next_y = y + 1
  let next_position = #(x, next_y)
  case next_y < len_y, dict.get(seen_pathes, next_position) {
    True, Ok(c) -> #(c, seen_pathes)
    True, _ -> {
      case set.contains(splitters, next_position) {
        True -> {
          let #(count, seen_pathes) =
            dxs
            |> list.fold(#(0, seen_pathes), fn(acc, dx) {
              let #(count_acc, seen_pathes) = acc
              let #(count, seen_pathes) =
                fall_down2(splitters, len_y, #(x + dx, next_y), seen_pathes)
              #(count_acc + count, seen_pathes)
            })
          #(count, dict.insert(seen_pathes, next_position, count))
        }
        False -> fall_down2(splitters, len_y, next_position, seen_pathes)
      }
    }
    False, _ -> #(1, seen_pathes)
  }
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start, len_y) = parse_lines(lines)

  let #(count, _) = fall_down2(splitters, len_y, start, dict.new())
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
