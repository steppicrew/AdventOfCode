///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////

import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 3

type Versions {
  Original
  ChatGpt
}

const version = ChatGpt

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

// ChatGPT's O(n) greedy algorithm for finding the largest number by removing digits
// We traverse the digits once from left to right. While doing that we maintain:
// - a list of chosen digits (let’s call it the stack)
// - how many digits we still may drop: to_drop
//
// When we see a new digit d:
// While all of these are true:
//   - We still have drops left (to_drop > 0), and
//   - The stack is not empty, and
//   - The last chosen digit (top of the stack) is less than d
// → we pop that smaller digit from the stack and decrement to_drop.
// This means:
// “If I can remove a smaller digit before this bigger one, the resulting number will be larger.”
//
// After we’ve popped everything we can, we push d onto the stack.
//
// At the end:
//
// We may have pushed all digits, but we may not want all of them.
//
// The stack might be longer than digit_count if we didn’t use all drops — we just keep the first digit_count.

fn fix_stack(digit: Int, stack: List(Int), digits_to_drop: Int) {
  case stack {
    [] -> #(stack, digits_to_drop)
    [last_digit, ..rest] -> {
      case digit > last_digit && digits_to_drop > 0 {
        True -> fix_stack(digit, rest, digits_to_drop - 1)
        False -> #(stack, digits_to_drop)
      }
    }
  }
}

fn find_largest_joltage_chatgpt(digits: List(Int), digit_count: Int) -> Int {
  let #(stack, _) =
    digits
    |> list.fold(
      #([], list.length(digits) - digit_count),
      fn(stack_drop, digit) {
        let #(stack, digits_to_drop) = stack_drop
        let #(stack, digits_to_drop) = fix_stack(digit, stack, digits_to_drop)
        #([digit, ..stack], digits_to_drop)
      },
    )
  stack
  |> list.reverse
  |> list.take(digit_count)
  |> list.fold(0, fn(acc, digit) { acc * 10 + digit })
}

fn run1(lines: List(String)) -> Int {
  let find_joltage = case version {
    Original -> find_largest_joltage
    ChatGpt -> find_largest_joltage_chatgpt
  }
  parse_lines(lines)
  |> list.map(fn(digits) { find_joltage(digits, 2) })
  |> int.sum
}

fn run2(lines: List(String)) -> Int {
  let find_joltage = case version {
    Original -> find_largest_joltage
    ChatGpt -> find_largest_joltage_chatgpt
  }
  parse_lines(lines)
  |> list.map(fn(digits) { find_joltage(digits, 12) })
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
