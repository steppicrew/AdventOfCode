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

type Shape =
  Set(Coord)

type ShapeSet =
  List(Shape)

fn shape_to_string(shape: Shape) -> String {
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

fn print_shape(shape: Shape) -> Nil {
  io.println(shape_to_string(shape))
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

fn parse_lines(
  lines: List(String),
) -> #(List(ShapeSet), List(#(#(Int, Int), List(Int)))) {
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

  let rotate_shape = fn(shape: Shape) -> Shape {
    shape
    |> set.map(fn(c) {
      let #(x, y) = c
      #(y, -x)
    })
  }

  let flip_shape = fn(shape: Shape) -> Shape {
    shape
    |> set.map(fn(c) {
      let #(x, y) = c
      #(-x, y)
    })
  }

  let get_all_patters = fn(shape: Shape) -> ShapeSet {
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
  shape: Shape,
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
  available_shapes: List(List(ShapeSet)),
  shape_name: Int,
  area: Dict(Coord, Int),
) -> Bool {
  case available_shapes {
    [] -> True
    [[], ..rest] -> solve1(max_x, max_y, rest, shape_name, area)
    [[main_shape, ..remaining_shapes1], ..rest] -> {
      let new_available_shapes = [remaining_shapes1, ..rest]
      let test_shapes =
        new_available_shapes
        |> list.fold([], fn(acc, shapes) {
          case shapes {
            [] -> acc
            [first, ..] -> [first, ..acc]
          }
        })

      #(main_shape, test_shapes) |> io.debug("Main/Test")
      True
    }
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(shapes, areas) = parse_lines(lines)

  areas
  |> list.count(fn(area) {
    let #(#(x, y), shape_count) = area
    let available_shapes =
      list.zip(shape_count, shapes)
      |> list.fold([], fn(acc, count_shapes) {
        let #(count, shapes) = count_shapes
        case count {
          0 -> acc
          _ -> [
            list.range(1, count)
              |> list.fold([], fn(acc, _) { [shapes, ..acc] }),
            ..acc
          ]
        }
      })

    solve1(x - 3, y - 3, available_shapes, 0, dict.new())
    |> io.debug("Result")
    True
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
      // Expected(0, None, None),
    ],
    run1,
    run2,
    False,
  )
}
