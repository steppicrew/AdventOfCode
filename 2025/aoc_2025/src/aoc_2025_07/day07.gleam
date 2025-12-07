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
  let splitter =
    lines
    |> list.index_fold([], fn(acc, line, y) {
      string.to_graphemes(line)
      |> list.index_fold(acc, fn(acc, char, x) {
        case char {
          "^" -> [#(x, y), ..acc]
          _ -> acc
        }
      })
    })
    |> set.from_list

  let start_position = case list.first(lines) {
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

  #(splitter, start_position, list.length(lines))
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
      let y = y + 1
      let position = #(x, y)

      let #(positions, seen_splitters, count) = case
        y < len_y,
        set.contains(seen_splitters, position)
      {
        // inside grid, not yet seen as splitter impact
        True, False ->
          case set.contains(splitters, position) {
            // splitter: branch left+right, mark seen, count+1
            True -> #(
              [#(x - 1, y), #(x + 1, y), ..rest],
              set.insert(seen_splitters, position),
              count + 1,
            )

            // empty: just move straight down
            False -> #([position, ..rest], seen_splitters, count)
          }

        // out of grid OR already seen: drop this path
        _, _ -> #(rest, seen_splitters, count)
      }
      fall_down1(splitters, len_y, positions, seen_splitters, count)
    }
    [] -> count
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start_position, len_y) = parse_lines(lines)

  fall_down1(splitters, len_y, [start_position], set.new(), 0)
}

fn fall_down2(
  splitters: Set(#(Int, Int)),
  len_y: Int,
  position: #(Int, Int),
  seen_pathes: Dict(#(Int, Int), Int),
) -> #(Int, Dict(#(Int, Int), Int)) {
  let #(x, y) = position
  let y = y + 1
  let position = #(x, y)

  case y < len_y, dict.get(seen_pathes, position) {
    // already computed from here
    True, Ok(cached) -> #(cached, seen_pathes)

    // inside grid, not cached yet
    True, Error(_) ->
      case set.contains(splitters, position) {
        // splitter: branch left/right and cache result for this splitter
        True -> {
          let #(count1, seen_pathes) =
            fall_down2(splitters, len_y, #(x - 1, y), seen_pathes)
          let #(count2, seen_pathes) =
            fall_down2(splitters, len_y, #(x + 1, y), seen_pathes)
          let count = count1 + count2

          #(count, dict.insert(seen_pathes, position, count))
        }

        // empty: fall straight down, no cache needed
        False -> fall_down2(splitters, len_y, position, seen_pathes)
      }

    // out of grid bottom: one path finished
    False, _ -> #(1, seen_pathes)
  }
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let #(splitters, start_position, len_y) = parse_lines(lines)

  let #(count, _) = fall_down2(splitters, len_y, start_position, dict.new())
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
