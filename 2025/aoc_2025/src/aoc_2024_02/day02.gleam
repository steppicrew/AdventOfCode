import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import tools/io
import tools/types.{Expected}

pub const year = 2024

pub const day = 2

pub fn run1(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("\\s+")

  let descending = fn(l: List(Int)) {
    l
    |> list.window_by_2
    |> list.all(fn(pair) {
      let diff = pair.0 - pair.1
      1 <= diff && diff <= 3
    })
  }

  let test_list = fn(l: List(Int)) {
    descending(l) || descending(l |> list.reverse)
  }

  lines
  |> list.filter(fn(s) {
    regexp.split(re, s)
    |> list.filter_map(int.parse)
    |> test_list
  })
  |> list.length
}

pub fn run2(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("\\s+")

  let descending = fn(l: List(Int)) {
    l
    |> list.window_by_2()
    |> list.all(fn(pair) {
      let diff = pair.0 - pair.1
      1 <= diff && diff <= 3
    })
  }

  let test_list = fn(l: List(Int)) {
    l |> descending || l |> list.reverse |> descending
  }

  let test_list_with_one_off = fn(l: List(Int)) {
    test_list(l)
    || {
      list.range(0, list.length(l) - 1)
      |> list.any(fn(idx) {
        test_list(list.append(l |> list.take(idx), l |> list.drop(idx + 1)))
      })
    }
  }

  lines
  |> list.filter(fn(s) {
    regexp.split(re, s)
    |> list.filter_map(int.parse)
    |> test_list_with_one_off
  })
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
