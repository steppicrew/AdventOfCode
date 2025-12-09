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

fn extend(acc: List(#(Int, Int)), x1: Int, x2: Int) -> List(#(Int, Int)) {
  case acc {
    [] -> [#(x1, x2)]
    [last, ..rest] -> {
      let #(last_x1, last_x2) = last
      case x1 <= last_x2 {
        True -> [#(last_x1, x2), ..rest]
        False -> [#(x1, x2), last, ..rest]
      }
    }
  }
}

fn print_ranges(ranges: List(#(Int, List(#(Int, Int))))) {
  ranges
  |> list.each(fn(range) {
    let #(y, ranges) = range
    io.print(y |> int.to_string |> string.pad_start(4, "0") <> ": ")
    ranges
    |> list.fold(0, fn(last_x, range) {
      let #(x1, x2) = range
      case last_x < x1 {
        True -> io.print(string.repeat(" ", x1 - last_x))
        _ -> Nil
      }
      io.print(string.repeat("#", x2 - x1 + 1))
      x2 + 1
    })
    io.println("")
  })
}

fn two_lists_are_equal(a: List(l), b: List(l)) -> Bool {
  case list.length(a) == list.length(b) {
    False -> False
    True ->
      list.zip(a, b)
      |> list.all(fn(pair) {
        let #(x, y) = pair
        x == y
      })
  }
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
    |> list.fold([], fn(acc, border_item) {
      case acc {
        [] -> [[border_item]]
        [[last, ..rest_line], ..rest] -> {
          let #(#(_, last_y), _) = last
          let #(#(_, y), _) = border_item
          case last_y == y {
            True -> [[border_item, last, ..rest_line], ..rest]
            _ -> [[border_item], ..acc]
          }
        }
        _ -> acc
      }
    })
    |> list.map(fn(line) { list.reverse(line) })
    |> list.reverse()

  // sorted_border |> io.debug("Sorted Border")

  let ranges =
    sorted_border
    |> list.map(fn(line) {
      line
      |> list.window_by_2
      |> list.fold(#(0, []), fn(acc, pair) {
        let #(#(#(x1, y), type1), #(#(x2, _), type2)) = pair
        let #(_, acc) = acc
        let acc = case type1, type2 {
          VerticalLeft, VerticalLeft -> {
            pair |> io.debug("Unexpected VerticalLeft, VerticalLeft")
            acc
          }
          Horizontal, VerticalLeft -> {
            pair |> io.debug("Unexpected Horizontal, VerticalRight")
            acc
          }
          VerticalRight, VerticalLeft -> extend(acc, x1, x2)
          Corner, VerticalLeft -> extend(acc, x1, x2)

          VerticalRight, VerticalRight -> {
            pair |> io.debug("Unexpected VerticalRight, VerticalRight")
            acc
          }
          Horizontal, VerticalRight -> {
            pair |> io.debug("Unexpected Horizontal, VerticalRight")
            acc
          }
          VerticalLeft, VerticalRight -> acc
          Corner, VerticalRight -> acc

          Horizontal, Horizontal -> extend(acc, x1, x2)
          Corner, Horizontal -> extend(acc, x1, x2)
          _, Horizontal -> {
            pair |> io.debug("Unexpected _, Horizontal")
            acc
          }

          VerticalLeft, Corner -> {
            case x1 + 1 == x2 {
              True -> extend(acc, x1, x2)
              False -> [#(x2, x2), ..acc]
            }
          }
          VerticalRight, Corner -> extend(acc, x1, x2)
          Horizontal, Corner -> {
            case x1 + 1 == x2 {
              True -> extend(acc, x1, x2)
              False -> {
                pair |> io.debug("Unexpected _, Horizontal")
                acc
              }
            }
          }
          Corner, Corner -> {
            case x1 + 1 == x2 {
              True -> extend(acc, x1, x2)
              False -> [#(x2, x2), ..acc]
            }
          }
        }
        #(y, acc)
      })
    })
    |> list.map(fn(y_ranges) {
      let #(y, ranges) = y_ranges
      #(y, ranges |> list.reverse())
    })

  // ranges |> print_ranges()
  // ranges |> io.debug("Ranges before merge")

  // ranges
  // |> list.each(fn(ranges) {
  //   let #(y, ranges) = ranges
  //   ranges
  //   |> list.window_by_2
  //   |> list.each(fn(pair) {
  //     let #(#(x11, x12), #(x21, x22)) = pair
  //     case x11 > x12 || x21 > x22 || x21 <= x12 {
  //       True -> {
  //         #(y, pair) |> io.debug("Overlapping ranges")
  //         Nil
  //       }
  //       _ -> Nil
  //     }
  //   })
  // })

  let merged_ranges =
    ranges
    |> list.fold([], fn(last_lines, new_line) {
      let #(y, ranges) = new_line
      case last_lines {
        [] -> [#(#(y, y), ranges)]
        [last_line, ..rest] -> {
          let #(#(last_y1, _), last_ranges) = last_line
          case two_lists_are_equal(last_ranges, ranges) {
            True -> [#(#(last_y1, y), ranges), ..rest]
            False -> [#(#(y, y), ranges), last_line, ..rest]
          }
        }
      }
    })
    |> list.reverse()

  // merged_ranges |> list.take(2) |> io.debug("Merged Ranges")

  // ranges |> io.debug("Ranges")
  // #() |> io.debug("Done ranges")

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
      let #(tile1, tile2, _) = rect
      let #(x1, y1) = tile1
      let #(x2, y2) = tile2
      let #(x_min, x_max) = #(int.min(x1, x2), int.max(x1, x2))
      let #(y_min, y_max) = #(int.min(y1, y2), int.max(y1, y2))
      merged_ranges
      |> list.filter(fn(ranges) {
        let #(#(ry1, ry2), _) = ranges
        ry2 >= y_min && ry1 <= y_max
      })
      |> list.all(fn(ranges) {
        let #(_, ranges) = ranges
        ranges
        |> list.any(fn(range) {
          let #(rx1, rx2) = range
          rx1 <= x_min && rx2 >= x_max
        })
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
      Expected(2, Some(70), Some(24)),
      Expected(0, Some(4_740_155_680), Some(1_543_501_936)),
    ],
    run1,
    run2,
    False,
  )
}
