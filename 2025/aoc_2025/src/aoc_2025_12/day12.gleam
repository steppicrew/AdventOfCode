import gleam/dict.{type Dict}
import gleam/int
import gleam/list
import gleam/option.{type Option, None, Some}
import gleam/order.{Eq}
import gleam/regexp
import gleam/result
import gleam/set.{type Set}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 12

const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

type Coord =
  #(Int, Int)

fn get_shape(shape: Set(Coord)) -> String {
  list.range(-1, 1)
  |> list.fold("", fn(before, y) {
    before
    <> list.range(-1, 1)
    |> list.fold("", fn(before, x) {
      before
      <> case set.contains(shape, #(x, y)) {
        True -> "#"
        False -> "."
      }
    })
    <> "\n"
  })
}

fn print_shape(shape: Set(Coord)) -> Nil {
  io.println(get_shape(shape))
}

fn print_area(max_x: Int, max_y: Int, area: Dict(Coord, Int)) {
  let labels = string.to_graphemes(labels)
  let max = list.length(labels)
  let labels = dict.from_list(list.index_map(labels, fn(c, i) { #(i, c) }))
  io.println("\nArea:")
  let x_range = list.range(-1, max_x)
  list.range(-1, max_y)
  |> list.each(fn(y) {
    io.println(
      x_range
      |> list.fold("", fn(text, x) {
        text
        <> case dict.get(area, #(x, y)) {
          Ok(i) -> dict.get(labels, i % max) |> result.unwrap("#")
          Error(_) -> "."
        }
      }),
    )
  })
}

fn parse_lines(lines: List(String)) {
  let #(shapes, areas) =
    lines
    |> list.fold(#([], []), fn(acc, line) {
      let #(shapes, areas) = acc
      case string.ends_with(line, ":") {
        True -> #([[], ..shapes], areas)
        False ->
          case string.first(line) {
            Ok("#") ->
              case shapes {
                [first, ..remaining] -> #([[line, ..first], ..remaining], areas)
                _ -> #([], [])
              }
            Ok(".") ->
              case shapes {
                [first, ..remaining] -> #([[line, ..first], ..remaining], areas)
                _ -> #([], [])
              }
            _ -> {
              case string.split(line, " ") {
                [first, ..remaining] -> {
                  let dimensions = case
                    first
                    |> string.slice(0, string.length(first) - 1)
                    |> string.split("x")
                  {
                    [x, y] ->
                      case int.parse(x), int.parse(y) {
                        Ok(x), Ok(y) -> #(x, y)
                        _, _ -> #(0, 0)
                      }
                    _ -> #(0, 0)
                  }
                  let fits =
                    remaining
                    |> list.map(fn(n) { int.parse(n) |> result.unwrap(0) })
                  #(shapes, [#(dimensions, fits), ..areas])
                }
                _ -> #(shapes, areas)
              }
            }
          }
      }
    })

  let rotate_shape = fn(shape: Set(Coord)) {
    shape
    |> set.map(fn(c) {
      let #(x, y) = c
      #(y, -x)
    })
  }

  let flip_shape = fn(shape: Set(Coord)) {
    shape
    |> set.map(fn(c) {
      let #(x, y) = c
      #(-x, y)
    })
  }

  let get_all_patters = fn(shape: Set(Coord)) -> List(Set(Coord)) {
    let rotated =
      list.range(1, 3)
      |> list.fold([shape], fn(acc, _) {
        case acc {
          [last_shape, ..] -> [rotate_shape(last_shape), ..acc]
          _ -> acc
        }
      })
      |> set.from_list

    let flipped = rotated |> set.map(flip_shape)

    set.union(rotated, flipped) |> set.to_list
  }

  let shapes =
    shapes
    |> list.reverse
    |> list.map(fn(shape) {
      shape
      |> list.index_fold(set.new(), fn(acc, line, y) {
        string.to_graphemes(line)
        |> list.index_fold(acc, fn(acc, c, x) {
          case c {
            "#" -> set.insert(acc, #(x - 1, y - 1))
            _ -> acc
          }
        })
      })
      |> get_all_patters
    })

  #(shapes, areas |> list.reverse)
}

fn set_shape_at(
  x: Int,
  y: Int,
  shape: Set(Coord),
  area: Dict(Coord, Int),
  value: Int,
) -> Option(Dict(Coord, Int)) {
  shape
  |> set.fold(Some(area), fn(area, coord) {
    case area {
      Some(area) -> {
        let #(dx, dy) = coord
        let new_coord = #(x + dx, y + dy)
        case dict.has_key(area, new_coord) {
          True -> None
          False -> Some(dict.insert(area, new_coord, value))
        }
      }
      None -> None
    }
  })
}

fn solve1(
  max_x: Int,
  max_y: Int,
  shape_counts: List(#(Int, List(Set(Coord)))),
  shape_type: Int,
  area: Dict(Coord, Int),
  last_xy: #(Int, Int),
  last_value: Int,
) -> Bool {
  let #(last_x, last_y) = last_xy
  let last_value = last_value + 1
  case shape_counts {
    [] -> True
    [first_shape_count, ..remaining] -> {
      let #(count, shapes) = first_shape_count
      let x_range = list.range(1, max_x)
      list.range(last_y, max_y)
      |> list.any(fn(y) {
        let x_range = case y == last_y, last_x < max_x {
          False, _ -> x_range
          True, True -> list.range(last_x, max_x)
          True, False -> list.new()
        }
        x_range
        |> list.any(fn(x) {
          shapes
          |> list.any(fn(shape) {
            case set_shape_at(x, y, shape, area, last_value) {
              Some(area) -> {
                // print_area(max_x, max_y, area)
                case count {
                  1 ->
                    solve1(
                      max_x,
                      max_y,
                      remaining,
                      shape_type + 1,
                      area,
                      #(0, 0),
                      last_value,
                    )
                  _ ->
                    solve1(
                      max_x,
                      max_y,
                      [#(count - 1, shapes), ..remaining],
                      shape_type,
                      area,
                      #(x, y),
                      last_value,
                    )
                }
              }
              None -> False
            }
          })
        })
      })
    }
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(shapes, areas) = parse_lines(lines)

  areas
  |> list.count(fn(area) {
    let #(#(x, y), indexes) = area
    solve1(
      x - 3,
      y - 3,
      list.zip(indexes, shapes)
        |> list.filter(fn(pair) { pair.0 > 0 }),
      0,
      dict.new(),
      #(0, 0),
      -1,
    )
    |> io.debug("Result")
  })
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  list.length(lines)
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(2), Some(0)),
      Expected(0, None, None),
    ],
    run1,
    run2,
    False,
  )
}
