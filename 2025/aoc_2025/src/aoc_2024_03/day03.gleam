import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/string
import tools/io
import tools/types.{Expected}

pub const year = 2024

pub const day = 3

pub fn run1(lines: List(String)) -> Int {
  let text = lines |> string.join("\n")
  let assert Ok(re_mul) = regexp.from_string("mul\\((\\d{1,3}),(\\d{1,3})\\)")

  let matches = regexp.scan(re_mul, text)
  matches
  |> list.map(fn(captures) {
    case captures.submatches {
      [Some(a_str), Some(b_str), ..] -> {
        case int.parse(a_str), int.parse(b_str) {
          Ok(a), Ok(b) -> a * b
          _, _ -> 0
        }
      }
      _ -> 0
    }
  })
  |> int.sum
}

pub fn run2(lines: List(String)) -> Int {
  let assert Ok(re_mul) = regexp.from_string("mul\\((\\d{1,3}),(\\d{1,3})\\)")
  lines
  |> string.join("\n")
  |> string.split("do()")
  |> list.map(fn(part) {
    case part |> string.split_once("don't()") {
      Ok(#(before, _)) -> before
      _ -> part
    }
  })
  |> list.map(fn(text) {
    let matches = regexp.scan(re_mul, text)
    matches
    |> list.map(fn(captures) {
      case captures.submatches {
        [Some(a_str), Some(b_str), ..] -> {
          case int.parse(a_str), int.parse(b_str) {
            Ok(a), Ok(b) -> a * b
            _, _ -> 0
          }
        }
        _ -> 0
      }
    })
    |> int.sum
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(161), Some(161)),
      Expected(2, Some(161), Some(48)),
      Expected(0, Some(160_672_468), Some(84_893_551)),
    ],
    run1,
    run2,
    False,
  )
}
