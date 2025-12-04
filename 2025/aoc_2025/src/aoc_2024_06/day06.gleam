import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/result
import gleam/set.{type Set}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2024

const day = 6

fn parse_lines(
  lines: List(String),
) -> #(Set(#(Int, Int)), #(Int, Int), #(Int, Int)) {
  let obsticles =
    lines
    |> list.index_map(fn(line, y) {
      line
      |> string.to_graphemes
      |> list.index_map(fn(char, x) {
        case char {
          "#" -> Ok(#(x, y))
          _ -> Error(Nil)
        }
      })
    })
    |> list.flatten
    |> list.filter_map(fn(x) { x })
    |> set.from_list

  let #(start_position, direction) =
    lines
    |> list.index_map(fn(line, y) {
      line
      |> string.to_graphemes
      |> list.index_map(fn(char, x) {
        case char {
          "^" -> Ok(#(#(x, y), #(0, -1)))
          "v" -> Ok(#(#(x, y), #(0, 1)))
          "<" -> Ok(#(#(x, y), #(-1, 0)))
          ">" -> Ok(#(#(x, y), #(1, 0)))
          _ -> Error(Nil)
        }
      })
    })
    |> list.flatten
    |> list.filter_map(fn(x) { x })
    |> list.first
    |> result.unwrap(#(#(0, 0), #(0, 0)))

  #(obsticles, start_position, direction)
}

fn walk1(
  position: #(Int, Int),
  direction: #(Int, Int),
  visited: Set(#(Int, Int)),
  max_xy: #(Int, Int),
  obsticles: Set(#(Int, Int)),
) -> Set(#(Int, Int)) {
  let #(x, y) = position
  let #(dx, dy) = direction
  let next_pos = #(x + dx, y + dy)

  case next_pos {
    #(-1, _) -> visited
    #(_, -1) -> visited
    #(x, _) if x == max_xy.0 -> visited
    #(_, y) if y == max_xy.1 -> visited
    #(x, y) -> {
      case obsticles |> set.contains(#(x, y)) {
        True -> walk1(position, #(-dy, dx), visited, max_xy, obsticles)
        False ->
          walk1(
            next_pos,
            direction,
            set.insert(visited, next_pos),
            max_xy,
            obsticles,
          )
      }
    }
  }
}

fn run1(lines: List(String)) -> Int {
  let #(obsticles, start_position, direction) = parse_lines(lines)

  let max_xy = #(
    lines
      |> list.map(string.length)
      |> list.max(int.compare)
      |> result.unwrap(0),
    lines |> list.length,
  )

  walk1(
    start_position,
    direction,
    set.from_list([start_position]),
    max_xy,
    obsticles,
  )
  |> set.size
}

fn walk2(
  position: #(Int, Int),
  direction: #(Int, Int),
  visited: Set(#(#(Int, Int), #(Int, Int))),
  max_xy: #(Int, Int),
  obsticles: Set(#(Int, Int)),
) -> Bool {
  let pos_dir = #(position, direction)
  case visited |> set.contains(pos_dir) {
    True -> True
    False -> {
      let visited = set.insert(visited, pos_dir)
      let #(x, y) = position
      let #(dx, dy) = direction
      let next_pos = #(x + dx, y + dy)

      case next_pos {
        #(-1, _) -> False
        #(_, -1) -> False
        #(x, _) if x == max_xy.0 -> False
        #(_, y) if y == max_xy.1 -> False
        #(x, y) -> {
          let #(position, direction) = case obsticles |> set.contains(#(x, y)) {
            True -> #(position, #(-dy, dx))
            False -> #(next_pos, direction)
          }
          walk2(position, direction, visited, max_xy, obsticles)
        }
      }
    }
  }
}

fn run2(lines: List(String)) -> Int {
  let #(obsticles, start_position, direction) = parse_lines(lines)

  let max_xy = #(
    lines
      |> list.map(string.length)
      |> list.max(int.compare)
      |> result.unwrap(0),
    lines |> list.length,
  )

  walk1(start_position, direction, set.new(), max_xy, obsticles)
  |> set.delete(start_position)
  |> set.to_list
  |> list.count(fn(pos) {
    walk2(
      start_position,
      direction,
      set.new(),
      max_xy,
      obsticles |> set.insert(pos),
    )
  })
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(41), Some(6)),
      Expected(0, Some(5131), Some(1784)),
    ],
    run1,
    run2,
    False,
  )
}
