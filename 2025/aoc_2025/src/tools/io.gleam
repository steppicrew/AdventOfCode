import gleam/int
import gleam/io
import gleam/list
import gleam/option.{type Option, None, Some}
import gleam/string
import simplifile
import tools/timer
import tools/types.{type ExpectedResult, Expected}

pub const green = "\u{1B}[32m"

pub const red = "\u{1B}[31m"

pub const yellow = "\u{1B}[33m"

pub const bold = "\u{1B}[1m"

pub const reset = "\u{1B}[0m"

pub const correct = green <> bold <> "✓" <> reset

pub const failed = red <> bold <> "✗" <> reset

pub const new_result = yellow <> bold <> "?" <> reset

/// Reads lines from file, skipping comment lines starting with ';'.
pub fn read_lines(path: String) -> List(String) {
  case simplifile.read(path) {
    Ok(content) ->
      content
      |> string.split("\n")
      |> list.filter(fn(line) { !string.starts_with(line, ";") && line != "" })
    Error(_) -> []
  }
}

/// Run the two parts with automatic input and output management.
/// 
/// - Writes missing result files (`None` in Expected)
/// - Colors output
/// - Shows total summary
/// - Respects quiet mode
pub fn simple_io(
  year: Int,
  day: Int,
  expected_results: List(ExpectedResult(a)),
  run1: fn(List(String)) -> a,
  run2: fn(List(String)) -> a,
  quiet: Bool,
) -> Nil {
  let results =
    expected_results
    |> list.map(fn(expected) {
      case expected {
        Expected(ref, exp1, exp2) ->
          ref_run(year, day, ref, exp1, exp2, run1, run2, quiet)
      }
    })
    |> list.flatten

  let success = list.count(results, fn(r) { r == True })
  let failed = list.count(results, fn(r) { r == False })
  let total = list.length(results)

  let color = case success, failed {
    s, _ if s == total -> green
    _, f if f > 0 -> red
    _, _ -> yellow
  }

  io.println(
    "\n"
    <> color
    <> bold
    <> "SUMMARY"
    <> reset
    <> ": "
    <> string.inspect(success)
    <> "/"
    <> string.inspect(total)
    <> " passed ("
    <> string.inspect(failed)
    <> " failed)",
  )
}

fn ref_run(
  year: Int,
  day: Int,
  ref: Int,
  exp1: Option(a),
  exp2: Option(a),
  run1: fn(List(String)) -> a,
  run2: fn(List(String)) -> a,
  quiet: Bool,
) -> List(Bool) {
  let padded_day = string.pad_start(int.to_string(day), 2, "0")
  let dir = "src/aoc_" <> int.to_string(year) <> "_" <> padded_day
  let suffix = case ref == 0 {
    True -> ""
    False -> "_ref" <> int.to_string(ref)
  }
  let input_path = dir <> "/input" <> suffix <> ".txt"
  let lines = read_lines(input_path)

  let label = case ref == 0 {
    True -> "main"
    False -> "ref" <> int.to_string(ref)
  }

  [
    part_run(dir, label, 1, lines, exp1, run1, suffix, quiet),
    part_run(dir, label, 2, lines, exp2, run2, suffix, quiet),
  ]
}

fn part_run(
  dir: String,
  label: String,
  part: Int,
  input: List(String),
  expected: Option(a),
  run: fn(List(String)) -> a,
  suffix: String,
  quiet: Bool,
) -> Bool {
  let #(result, time) = timer.measure_time(fn() { run(input) })
  let time_str = format_time(time)
  let result_str = string.inspect(result)
  let result_file =
    dir <> "/input" <> suffix <> "_" <> int.to_string(part) <> ".result"

  case quiet {
    True -> Nil
    False -> io.print(label <> "/" <> int.to_string(part) <> ": ")
  }

  case expected {
    Some(exp) if exp == result -> {
      case quiet {
        True -> Nil
        False ->
          io.println(correct <> " (" <> result_str <> ") in " <> time_str)
      }
      True
    }

    None -> {
      case quiet {
        True -> Nil
        False ->
          io.println(new_result <> " (" <> result_str <> ") in " <> time_str)
      }
      let _ = simplifile.write(result_file, result_str)
      True
    }

    Some(_) -> {
      case quiet {
        True -> Nil
        False -> {
          io.println(failed <> " in " <> time_str)
          io.println("\tEXPECTED: " <> string.inspect(expected))
          io.println("\tGOT     : " <> result_str)
        }
      }
      False
    }
  }
}

fn format_time(seconds: Float) -> String {
  let ms = seconds *. 1000.0
  case ms <. 1.0 {
    True -> string.inspect(ms *. 1000.0) <> "µs"
    False ->
      case ms <. 1000.0 {
        True -> string.inspect(ms) <> "ms"
        False -> string.inspect(seconds) <> "s"
      }
  }
}
