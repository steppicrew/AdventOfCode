import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

pub const year = 2025

pub const day = 1

fn parse_lines(lines: List(String)) -> List(Int) {
  lines
  |> list.map(fn(line) {
    case string.drop_start(line, 1) |> int.parse {
      Ok(num) ->
        case line |> string.first {
          Ok("L") -> -num
          Ok("R") -> num
          _ -> 0
        }
      _ -> 0
    }
  })
}

fn get_count(count_pos: #(Int, Int)) -> Int {
  let #(count, _) = count_pos
  count
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  lines
  |> parse_lines
  |> list.fold(#(0, 50), fn(count_pos, turn) {
    let #(count, pos) = count_pos
    let next_pos = { pos + turn } % 100
    case next_pos {
      0 -> #(count + 1, next_pos)
      _ -> #(count, next_pos)
    }
  })
  |> get_count
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  lines
  |> parse_lines
  |> list.fold(#(0, 50), fn(count_pos, turn) {
    let #(count, pos) = count_pos
    let next_pos = pos + turn
    let new_count = case pos, next_pos {
      0, np if np < 0 -> count - np / 100
      _, np if np <= 0 -> count + 1 - np / 100
      _, np -> count + np / 100
    }

    #(new_count, { next_pos % 100 + 100 } % 100)
  })
  |> get_count
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(3), Some(6)),
      Expected(0, Some(1066), Some(6223)),
    ],
    run1,
    run2,
    False,
  )
}
