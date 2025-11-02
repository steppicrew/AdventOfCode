import gleam/dict
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/result
import tools/io
import tools/types.{Expected}

pub const year = 2024

pub const day = 1

pub fn run1(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("\\s+")

  let #(left, right) =
    lines
    |> list.filter_map(fn(s) {
      case regexp.split(re, s) {
        [left, right, ..] -> {
          case int.parse(left), int.parse(right) {
            Ok(l), Ok(r) -> Ok(#(l, r))
            _, _ -> Error(Nil)
          }
        }
        _ -> Error(Nil)
      }
    })
    |> list.unzip()

  let left = list.sort(left, int.compare)
  let right = list.sort(right, int.compare)
  list.zip(left, right)
  |> list.map(fn(pair) {
    let #(l, r) = pair
    int.absolute_value(r - l)
  })
  |> int.sum()
}

pub fn run2(lines: List(String)) -> Int {
  let assert Ok(re) = regexp.from_string("\\s+")

  let #(left, right) =
    lines
    |> list.filter_map(fn(s) {
      case regexp.split(re, s) {
        [left, right, ..] -> {
          case int.parse(left), int.parse(right) {
            Ok(l), Ok(r) -> Ok(#(l, r))
            _, _ -> Error(Nil)
          }
        }
        _ -> Error(Nil)
      }
    })
    |> list.unzip()

  let counts =
    right
    |> list.fold(dict.new(), fn(counts, n) {
      counts
      |> dict.insert(
        n,
        {
          dict.get(counts, n)
          |> result.unwrap(0)
        }
          + 1,
      )
    })

  left
  |> list.map(fn(n) {
    case counts |> dict.get(n) {
      Ok(count) -> n * count
      _ -> 0
    }
  })
  |> int.sum()
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(11), Some(31)),
      Expected(0, Some(1_889_772), Some(23_228_917)),
    ],
    run1,
    run2,
    False,
  )
}
