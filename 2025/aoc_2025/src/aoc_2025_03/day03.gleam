import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 3

fn parse_lines(lines: List(String)) -> List(List(Int)) {
  lines
  |> list.map(fn(line) {
    line
    |> string.split("")
    |> list.filter_map(int.parse)
  })
}

fn find_largest_joltage(digits: List(Int), digit_count: Int) -> Int {
  let #(sum, _, _) =
    list.range(digit_count - 1, 0)
    |> list.fold(
      #(0, digits, list.length(digits)),
      fn(sum_digits_len, digits_left) {
        let #(sum, digits, len) = sum_digits_len
        let max_len = len - digits_left
        let #(digit, index) =
          digits
          |> list.index_fold(#(0, 0), fn(max, digit, index) {
            let #(current_max, current_index) = max
            case index < max_len && digit > current_max {
              True -> #(digit, index)
              False -> #(current_max, current_index)
            }
          })
        #(sum * 10 + digit, list.drop(digits, index + 1), len - index - 1)
      },
    )
  sum
}

fn run1(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(fn(digits) { find_largest_joltage(digits, 2) })
  |> int.sum
}

fn run2(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(fn(digits) { find_largest_joltage(digits, 12) })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(357), Some(3_121_910_778_619)),
      Expected(0, Some(17_332), Some(172_516_781_546_707)),
    ],
    run1,
    run2,
    False,
  )
}
