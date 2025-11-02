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

  let test_list_ = fn(windowed: List(#(Int, Int))) {
    windowed
    |> list.all(fn(pair) {
      let #(a, b) = pair
      let diff = a - b
      1 <= diff && diff <= 3
    })
  }

  let test_list = fn(l: List(Int)) {
    test_list_(l |> list.window_by_2())
    || test_list_(l |> list.reverse() |> list.window_by_2())
  }

  lines
  |> list.map(fn(s) {
    regexp.split(re, s)
    |> list.filter_map(fn(num_str) {
      case int.parse(num_str) {
        Ok(n) -> Ok(n)
        _ -> Error(Nil)
      }
    })
    |> test_list()
  })
  |> list.filter(fn(b) { b })
  |> list.length()
}

pub fn run2(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("\\s+")

  let test_list_ = fn(l: List(Int)) {
    l
    |> list.window_by_2()
    |> list.all(fn(pair) {
      let #(a, b) = pair
      let diff = a - b
      1 <= diff && diff <= 3
    })
  }

  let test_list__ = fn(l: List(Int)) {
    l |> test_list_() || l |> list.reverse() |> test_list_()
  }

  let test_list = fn(l: List(Int)) {
    case test_list__(l) {
      True -> True
      False -> {
        l
        |> list.index_map(fn(_, idx) { idx })
        |> list.any(fn(idx) {
          test_list__(list.append(l |> list.take(idx), l |> list.drop(idx + 1)))
        })
      }
    }
  }

  lines
  |> list.map(fn(s) {
    regexp.split(re, s)
    |> list.filter_map(fn(num_str) {
      case int.parse(num_str) {
        Ok(n) -> Ok(n)
        _ -> Error(Nil)
      }
    })
    |> test_list()
  })
  |> list.filter(fn(b) { b })
  |> list.length()
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
