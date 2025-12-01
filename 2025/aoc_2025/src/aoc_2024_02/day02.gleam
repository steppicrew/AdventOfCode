import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import tools/io
import tools/types.{Expected}

const year = 2024

const day = 2

fn parse_lines(lines: List(String)) -> List(List(Int)) {
  let assert Ok(re) = regexp.from_string("\\s+")

  lines
  |> list.map(fn(s) {
    regexp.split(re, s)
    |> list.filter_map(int.parse)
  })
}

fn descending(l: List(Int)) {
  l
  |> list.window_by_2
  |> list.all(fn(pair) {
    let diff = pair.0 - pair.1
    1 <= diff && diff <= 3
  })
}

fn test_list(l: List(Int)) {
  descending(l) || descending(l |> list.reverse)
}

fn run1(lines: List(String)) -> Int {
  parse_lines(lines)
  |> list.filter(test_list)
  |> list.length
}

fn run2(lines: List(String)) -> Int {
  let test_list_with_one_off = fn(l: List(Int)) {
    test_list(l)
    || {
      list.range(0, list.length(l) - 1)
      |> list.any(fn(idx) {
        test_list(list.append(l |> list.take(idx), l |> list.drop(idx + 1)))
      })
    }
  }

  parse_lines(lines)
  |> list.filter(test_list_with_one_off)
  |> list.length
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(2), Some(4)),
      Expected(0, Some(502), Some(544)),
    ],
    run1,
    run2,
    False,
  )
}
