import gleam/int
import gleam/list
import gleam/option.{None, Some}
import gleam/result
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

fn find_largest_pair(nums: List(Int)) -> Int {
  let first_digit =
    nums
    |> list.take(list.length(nums) - 1)
    |> list.max(int.compare)
    |> result.unwrap(0)
  let first_index =
    nums
    |> list.fold_until(0, fn(i, n) {
      case n == first_digit {
        True -> list.Stop(i)
        False -> list.Continue(i + 1)
      }
    })
  let second_digit =
    nums
    |> list.drop(first_index + 1)
    |> list.max(int.compare)
    |> result.unwrap(0)
  first_digit * 10 + second_digit
}

fn run1(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(find_largest_pair)
  |> int.sum
}

fn find_largest_joltage(nums: List(Int)) -> Int {
  let #(sum, _) =
    list.range(11, 0)
    |> list.fold(#(0, nums), fn(sum_nums, index_left) {
      let #(sum, nums) = sum_nums
      let next_digit =
        nums
        |> list.take(list.length(nums) - index_left)
        |> list.max(int.compare)
        |> result.unwrap(0)
      let index =
        nums
        |> list.fold_until(0, fn(i, n) {
          case n == next_digit {
            True -> list.Stop(i)
            False -> list.Continue(i + 1)
          }
        })
      #(sum * 10 + next_digit, list.drop(nums, index + 1))
    })
  sum
}

fn run2(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.map(find_largest_joltage)
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
