import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp
import gleam/string
import tools/io
import tools/types.{Expected}

const year = 2025

const day = 2

fn parse_lines(lines: List(String)) -> List(#(Int, Int)) {
  let assert Ok(re) = regexp.from_string("(\\d+)-(\\d+)")
  lines
  |> string.join("")
  |> string.split(",")
  |> list.filter_map(fn(part) {
    case regexp.scan(re, part) {
      [match] ->
        case match.submatches {
          [Some(a), Some(b)] -> {
            case int.parse(a), int.parse(b) {
              Ok(a), Ok(b) -> Ok(#(a, b))
              _, _ -> Error(Nil)
            }
          }
          _ -> Error(Nil)
        }
      _ -> Error(Nil)
    }
  })
}

fn filter_range_sum(
  acc: Int,
  from: Int,
  until: Int,
  filter: fn(Int) -> Bool,
) -> Int {
  case from > until {
    True -> acc
    False -> {
      let acc = case filter(from) {
        True -> acc + from
        False -> acc
      }
      filter_range_sum(acc, from + 1, until, filter)
    }
  }
}

fn check_repeat(s: String, part_size: Int) -> Bool {
  let len = string.length(s)
  let first_part = string.slice(s, 0, part_size)
  list.range(1, len / part_size - 1)
  |> list.all(fn(start) {
    let part = string.slice(s, start * part_size, part_size)
    part == first_part
  })
}

fn check_single_repeat(n: Int) -> Bool {
  let s = int.to_string(n)
  let len = string.length(s)
  case len % 2 {
    0 -> check_repeat(s, len / 2)
    _ -> False
  }
}

fn run1(lines: List(String)) -> Int {
  // let assert Ok(re) = regexp.from_string("^(\\d+)(\\1)$")
  lines
  |> parse_lines
  |> list.map(fn(range) {
    let #(from, until) = range
    // filter_range_sum(0, from, until, fn(n) {
    //   regexp.check(re, int.to_string(n))
    // })
    filter_range_sum(0, from, until, check_single_repeat)
  })
  |> int.sum
}

fn test_any_devisors(last_devisor: Int, n: Int, test_fn: fn(Int) -> Bool) {
  let devisor = last_devisor + 1
  case devisor * devisor {
    x if x > n -> False
    x if x == n -> test_fn(devisor)
    _ -> {
      case n % devisor {
        0 -> {
          case test_fn(devisor) || test_fn(n / devisor) {
            True -> True
            False -> test_any_devisors(devisor, n, test_fn)
          }
        }
        _ -> test_any_devisors(devisor, n, test_fn)
      }
    }
  }
}

fn check_multiple_repeat(n: Int) -> Bool {
  let s = int.to_string(n)
  let len = string.length(s)
  case len > 1 {
    True ->
      check_repeat(s, 1)
      || test_any_devisors(1, len, fn(part_size) { check_repeat(s, part_size) })
    False -> False
  }
}

fn run2(lines: List(String)) -> Int {
  // let assert Ok(re) = regexp.from_string("^(\\d+)(\\1)+$")
  lines
  |> parse_lines
  |> list.map(fn(range) {
    let #(from, until) = range
    // filter_range_sum(0, from, until, fn(n) {
    //   regexp.check(re, int.to_string(n))
    // })
    filter_range_sum(0, from, until, check_multiple_repeat)
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(1_227_775_554), Some(4_174_379_265)),
      Expected(0, Some(31_000_881_061), Some(46_769_308_485)),
    ],
    run1,
    run2,
    False,
  )
}
