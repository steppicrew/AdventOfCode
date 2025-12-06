import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2024

const day = 3

fn get_sum_matches() -> fn(String) -> Int {
  let assert Ok(re_mul) = regexp.from_string("mul\\((\\d{1,3}),(\\d{1,3})\\)")

  fn(text: String) -> Int {
    regexp.scan(re_mul, text)
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
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  lines |> string.join("\n") |> get_sum_matches()
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  lines
  |> string.join("\n")
  |> string.split("do()")
  |> list.map(fn(part) {
    case part |> string.split_once("don't()") {
      Ok(#(before, _)) -> before
      _ -> part
    }
  })
  |> list.map(get_sum_matches())
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
