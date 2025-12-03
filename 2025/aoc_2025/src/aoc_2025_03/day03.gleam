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

fn find_largest_joltage(nums: List(Int), digits: Int) -> Int {
  let #(sum, _) =
    list.range(digits - 1, 0)
    |> list.fold(#(0, nums), fn(sum_nums, index_left) {
      let #(sum, nums) = sum_nums
      let #(digit, index) =
        nums
        |> list.take(list.length(nums) - index_left)
        |> list.index_fold(#(0, 0), fn(max, n, i) {
          let #(current_max, current_index) = max
          case n > current_max {
            True -> #(n, i)
            False -> #(current_max, current_index)
          }
        })
      #(sum * 10 + digit, list.drop(nums, index + 1))
    })
  sum
}

fn run1(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(fn(nums) { find_largest_joltage(nums, 2) })
  |> int.sum
}

fn run2(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(fn(nums) { find_largest_joltage(nums, 12) })
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
