import gleam/dict
import gleam/int
import gleam/list
import gleam/option.{None, Some}
import gleam/order
import gleam/result
import gleam/set
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 9

type TileType {
  Horizontal
  VerticalLeft
  VerticalRight
  Corner
}

fn parse_input(lines: List(String)) -> List(#(Int, Int)) {
  lines
  |> list.filter_map(fn(line) {
    case string.split(line, ",") {
      [x, y] ->
        case int.parse(x), int.parse(y) {
          Ok(a), Ok(b) -> Ok(#(a, b))
          _, _ -> Error(Nil)
        }
      _ -> Error(Nil)
    }
  })
}

fn get_size(p1: #(Int, Int), p2: #(Int, Int)) -> Int {
  let #(x1, y1) = p1
  let #(x2, y2) = p2
  { int.absolute_value(x2 - x1) + 1 } * { int.absolute_value(y2 - y1) + 1 }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let tiles = parse_input(lines)
  tiles
  |> list.index_fold([], fn(acc, tile1, i1) {
    tiles
    |> list.drop(i1 + 1)
    |> list.fold(acc, fn(acc, tile2) { [get_size(tile1, tile2), ..acc] })
  })
  |> list.fold(0, fn(size, acc) { int.max(acc, size) })
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let tiles = parse_input(lines)

  let border =
    [list.last(tiles) |> result.unwrap(#(0, 0)), ..tiles]
    |> list.window_by_2
    |> list.fold(dict.new(), fn(acc, pair) {
      let #(#(x1, y1), #(x2, y2)) = pair
      case x1 == x2, y1 == y2 {
        True, False -> {
          let v_type = case y1 > y2 {
            True -> VerticalRight
            False -> VerticalLeft
          }
          list.range(y1, y2)
          |> list.fold(acc, fn(acc, y) {
            dict.upsert(acc, #(x1, y), fn(v) {
              case v {
                Some(x) -> x
                None -> v_type
              }
            })
          })
        }
        False, True ->
          list.range(x1, x2)
          |> list.fold(acc, fn(acc, x) {
            dict.upsert(acc, #(x, y1), fn(v) {
              case v {
                Some(x) -> x
                None -> Horizontal
              }
            })
          })
        _, _ -> acc
      }
      |> dict.insert(#(x1, y1), Corner)
      |> dict.insert(#(x2, y2), Corner)
    })

  let sorted_border =
    border
    |> dict.to_list
    |> list.sort(fn(a, b) {
      let #(#(x1, y1), _) = a
      let #(#(x2, y2), _) = b
      case int.compare(y1, y2) {
        order.Eq -> int.compare(x1, x2)
        c -> c
      }
    })

  #() |> io.debug("Sorted Border")

  let #(area, _) =
    sorted_border
    |> list.fold(#(set.new(), None), fn(acc, point_tuple) {
      let #(area, prev_type) = acc
      let #(point, point_type) = point_tuple
      case prev_type, point_type {
        _, Horizontal -> #(area |> set.insert(point), Some(point_tuple))
        _, Corner -> #(area |> set.insert(point), Some(point_tuple))
        _, VerticalRight -> #(area |> set.insert(point), Some(point_tuple))
        None, VerticalLeft -> {
          #(acc, point_tuple)
          |> io.debug("Unexpected VerticalLeft at start (None, VerticalLeft)")
          #(area, Some(point_tuple))
        }
        Some(#(#(prev_x, prev_y), prev_type)), VerticalLeft -> {
          let #(x, y) = point
          case prev_y == y, prev_type {
            True, VerticalRight -> {
              let area =
                list.range(prev_x, x)
                |> list.fold(area, fn(area, x) { area |> set.insert(#(x, y)) })
              #(area, None)
            }
            True, Corner -> {
              let area =
                list.range(prev_x, x)
                |> list.fold(area, fn(area, x) { area |> set.insert(#(x, y)) })
              #(area, Some(point_tuple))
            }
            True, _ -> {
              #(#(prev_x, prev_y), prev_type, point, point_type)
              |> io.debug("Unexpected VerticalLeft at start (True, _)")
              #(area, Some(point_tuple))
            }
            False, _ -> {
              #(#(prev_x, prev_y), prev_type, point, point_type)
              |> io.debug("Unexpected VerticalLeft at start (False, _)")
              #(area, Some(point_tuple))
            }
          }
        }
      }
    })

  area |> set.size() |> io.debug("Area size")

  let result =
    tiles
    |> list.index_fold([], fn(acc, tile1, i1) {
      tiles
      |> list.drop(i1 + 1)
      |> list.fold(acc, fn(acc, tile2) {
        [#(tile1, tile2, get_size(tile1, tile2)), ..acc]
      })
    })
    |> list.sort(fn(a, b) {
      let #(_, _, size1) = a
      let #(_, _, size2) = b
      int.compare(size2, size1)
    })
    |> list.find(fn(rect) {
      let #(t1, t2, _) = rect
      let #(x1, y1) = t1
      let #(x2, y2) = t2
      list.range(x1, x2)
      |> list.all(fn(x) {
        list.range(y1, y2)
        |> list.all(fn(y) { set.contains(area, #(x, y)) })
      })
    })

  case result {
    Ok(#(_, _, size)) -> size
    Error(_) -> 0
  }
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(50), Some(24)),
      Expected(0, Some(4_740_155_680), None),
    ],
    run1,
    run2,
    False,
  )
}
