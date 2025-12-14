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

type ShapeCoords =
  Set(Coord)

type Area =
  Dict(Coord, Int)

type AreaData =
  #(Coord, List(Int))

type SetShapeFn =
  fn(Int, Int, Int, Area) -> Option(Area)

type Shape =
  #(ShapeCoords, Int, SetShapeFn)

type ShapeSet =
  List(Shape)

fn get_shape(shape: Shape) -> String {
  let #(shape, _, _) = shape
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
  io.println(get_shape(shape))
}

fn print_area(max_x: Int, max_y: Int, area: Area) {
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

fn get_set_shape(shape: ShapeCoords) -> SetShapeFn {
  case set.to_list(shape) {
    [#(x1, y1), #(x2, y2), #(x3, y3), #(x4, y4), #(x5, y5)] -> fn(
      x: Int,
      y: Int,
      shape_type: Int,
      area: Area,
    ) -> Option(Area) {
      let c1 = #(x1 + x, y1 + y)
      case dict.has_key(area, c1) {
        True -> None
        False -> {
          let c2 = #(x2 + x, y2 + y)
          case dict.has_key(area, c2) {
            True -> None
            False -> {
              let c3 = #(x3 + x, y3 + y)
              case dict.has_key(area, c3) {
                True -> None
                False -> {
                  let c4 = #(x4 + x, y4 + y)
                  case dict.has_key(area, c4) {
                    True -> None
                    False -> {
                      let c5 = #(x5 + x, y5 + y)
                      case dict.has_key(area, c5) {
                        True -> None
                        False ->
                          Some(
                            area
                            |> dict.insert(c1, shape_type)
                            |> dict.insert(c2, shape_type)
                            |> dict.insert(c3, shape_type)
                            |> dict.insert(c4, shape_type)
                            |> dict.insert(c5, shape_type),
                          )
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    [#(x1, y1), #(x2, y2), #(x3, y3), #(x4, y4), #(x5, y5), #(x6, y6)] -> fn(
      x: Int,
      y: Int,
      shape_type: Int,
      area: Area,
    ) -> Option(Area) {
      let c1 = #(x1 + x, y1 + y)
      case dict.has_key(area, c1) {
        True -> None
        False -> {
          let c2 = #(x2 + x, y2 + y)
          case dict.has_key(area, c2) {
            True -> None
            False -> {
              let c3 = #(x3 + x, y3 + y)
              case dict.has_key(area, c3) {
                True -> None
                False -> {
                  let c4 = #(x4 + x, y4 + y)
                  case dict.has_key(area, c4) {
                    True -> None
                    False -> {
                      let c5 = #(x5 + x, y5 + y)
                      case dict.has_key(area, c5) {
                        True -> None
                        False -> {
                          let c6 = #(x6 + x, y6 + y)
                          case dict.has_key(area, c6) {
                            True -> None
                            False ->
                              Some(
                                area
                                |> dict.insert(c1, shape_type)
                                |> dict.insert(c2, shape_type)
                                |> dict.insert(c3, shape_type)
                                |> dict.insert(c4, shape_type)
                                |> dict.insert(c5, shape_type)
                                |> dict.insert(c6, shape_type),
                              )
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    [
      #(x1, y1),
      #(x2, y2),
      #(x3, y3),
      #(x4, y4),
      #(x5, y5),
      #(x6, y6),
      #(x7, y7),
    ] -> fn(x: Int, y: Int, shape_type: Int, area: Area) -> Option(Area) {
      let c1 = #(x1 + x, y1 + y)
      case dict.has_key(area, c1) {
        True -> None
        False -> {
          let c2 = #(x2 + x, y2 + y)
          case dict.has_key(area, c2) {
            True -> None
            False -> {
              let c3 = #(x3 + x, y3 + y)
              case dict.has_key(area, c3) {
                True -> None
                False -> {
                  let c4 = #(x4 + x, y4 + y)
                  case dict.has_key(area, c4) {
                    True -> None
                    False -> {
                      let c5 = #(x5 + x, y5 + y)
                      case dict.has_key(area, c5) {
                        True -> None
                        False -> {
                          let c6 = #(x6 + x, y6 + y)
                          case dict.has_key(area, c6) {
                            True -> None
                            False -> {
                              let c7 = #(x7 + x, y7 + y)
                              case dict.has_key(area, c7) {
                                True -> None
                                False ->
                                  Some(
                                    area
                                    |> dict.insert(c1, shape_type)
                                    |> dict.insert(c2, shape_type)
                                    |> dict.insert(c3, shape_type)
                                    |> dict.insert(c4, shape_type)
                                    |> dict.insert(c5, shape_type)
                                    |> dict.insert(c6, shape_type)
                                    |> dict.insert(c7, shape_type),
                                  )
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    coords -> fn(x: Int, y: Int, shape_type: Int, area: Area) -> Option(Area) {
      case
        coords
        |> list.map(fn(c) {
          let #(cx, cy) = c
          #(cx + x, cy + y)
        })
        |> list.any(fn(c) { dict.has_key(area, c) })
      {
        True -> None
        False ->
          Some(
            coords
            |> list.fold(area, fn(area, c) { dict.insert(area, c, shape_type) }),
          )
      }
    }
  }
}

fn parse_lines(lines: List(String)) -> #(List(ShapeSet), List(AreaData)) {
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

  let get_all_patterns = fn(shape: ShapeCoords) -> List(ShapeCoords) {
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
      |> get_all_patterns
      |> list.map(fn(shape) { #(shape, set.size(shape), get_set_shape(shape)) })
    })

  #(shapes, areas |> list.reverse)
}

fn solve1(
  max_x: Int,
  max_y: Int,
  shape_counts: List(#(Int, ShapeSet)),
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
            let #(_, _, set_shape) = shape
            case set_shape(x, y, last_value, area) {
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
