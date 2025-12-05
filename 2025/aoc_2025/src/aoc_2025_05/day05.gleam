import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 5

/// Parses all lines into:
/// - ranges like "10-20"
/// - ingredients like "42"
fn parse_line(lines: List(String)) -> #(List(#(Int, Int)), List(Int)) {
  list.fold(lines, #([], []), fn(acc, line) {
    let #(ranges, ingredients) = acc

    case string.is_empty(line) {
      True ->
        // Ignore empty lines
        acc

      False ->
        // Try range "a-b" first
        case string.split(line, "-") {
          [from_s, to_s] ->
            case int.parse(from_s), int.parse(to_s) {
              Ok(from), Ok(to) ->
                // Cons is cheap, order doesn't matter for us
                #([#(from, to), ..ranges], ingredients)

              _, _ ->
                // Bad line, ignore
                acc
            }

          _ ->
            // Not a range, then try a single integer
            case int.parse(line) {
              Ok(value) -> #(ranges, [value, ..ingredients])

              Error(_) ->
                // Bad line, ignore
                acc
            }
        }
    }
  })
}

/// Merge overlapping / touching ranges into a minimal set of disjoint ranges.
/// Example: [1-3, 2-5, 10-12] -> [1-5, 10-12]
fn merge_ranges(ranges: List(#(Int, Int))) -> List(#(Int, Int)) {
  ranges
  |> list.sort(fn(a, b) {
    let #(a_from, _) = a
    let #(b_from, _) = b
    int.compare(a_from, b_from)
  })
  |> list.fold([], fn(acc, range) {
    case acc {
      [] -> [range]

      [last, ..rest] -> {
        let #(last_from, last_to) = last
        let #(from, to) = range

        case from > last_to {
          // Disjoint: keep both
          True -> [range, last, ..rest]

          // Overlapping / touching: merge them
          False -> [#(last_from, int.max(to, last_to)), ..rest]
        }
      }
    }
  })
}

fn run1(lines: List(String)) -> Int {
  let #(ranges, ingredients) = parse_line(lines)
  let merged = merge_ranges(ranges)

  ingredients
  |> list.filter(fn(ingredient) {
    merged
    |> list.any(fn(range) {
      let #(from, to) = range
      ingredient >= from && ingredient <= to
    })
  })
  |> list.length
}

fn run2(lines: List(String)) -> Int {
  let #(ranges, _) = parse_line(lines)
  let merged = merge_ranges(ranges)

  merged
  |> list.fold(0, fn(count, range) {
    let #(from, to) = range
    // Inclusive range: [from, to]
    count + { to - from + 1 }
  })
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(3), Some(14)),
      Expected(0, Some(756), Some(355_555_479_253_787)),
    ],
    run1,
    run2,
    False,
  )
}
