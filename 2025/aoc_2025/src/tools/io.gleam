import gleam/float
import gleam/int
import gleam/io
import gleam/list
import gleam/option.{type Option, None, Some}
import gleam/string
import gleam_community/ansi.{bold, green, red, yellow}
import simplifile
import tools/timer
import tools/types.{type ExpectedResult, Expected}

type TestResult {
  Passed
  Failed
  Unchecked
}

pub type RunEnv {
  RunEnv(log: fn(String) -> Nil)
}

fn correct() -> String {
  "✓" |> bold |> green
}

fn failed() -> String {
  "✗" |> bold |> red
}

fn new_result() -> String {
  "?" |> bold |> yellow
}

/// Reads lines from file, skipping comment lines starting with ';'.
fn read_lines(path: String) -> List(String) {
  case simplifile.read(path) {
    Ok(content) ->
      content
      |> string.split("\n")
      |> list.filter(fn(line) {
        !string.starts_with(line, ";") && !string.is_empty(line)
      })
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
  run1: fn(List(String), RunEnv) -> a,
  run2: fn(List(String), RunEnv) -> a,
  quiet: Bool,
) -> Nil {
  let results =
    expected_results
    |> list.flat_map(fn(expected) {
      case expected {
        Expected(ref, exp1, exp2) -> {
          let #(r1, r2) = ref_run(year, day, ref, exp1, exp2, run1, run2, quiet)
          [r1, r2]
        }
      }
    })

  let success = list.count(results, fn(r) { r == Passed })
  let failed = list.count(results, fn(r) { r == Failed })
  let total = list.length(results)

  let color = case success, failed {
    s, _ if s == total -> green
    _, f if f > 0 -> red
    _, _ -> yellow
  }

  io.println(
    "\n"
    <> { "SUMMARY:" |> bold |> color }
    <> " "
    <> string.inspect(success)
    <> "/"
    <> string.inspect(total)
    <> " passed"
    <> {
      case failed {
        0 -> ""
        _ -> " (" <> string.inspect(failed) <> " failed)"
      }
    },
  )
}

fn ref_run(
  year: Int,
  day: Int,
  ref: Int,
  exp1: Option(a),
  exp2: Option(a),
  run1: fn(List(String), RunEnv) -> a,
  run2: fn(List(String), RunEnv) -> a,
  quiet: Bool,
) -> #(TestResult, TestResult) {
  let padded_day = string.pad_start(int.to_string(day), 2, "0")
  let dir = "src/aoc_" <> int.to_string(year) <> "_" <> padded_day
  let #(suffix, label) = case ref {
    0 -> #("", "main")
    _ -> {
      let ref = "ref" <> int.to_string(ref)
      #("_" <> ref, ref)
    }
  }
  let lines = read_lines(dir <> "/input" <> suffix <> ".txt")

  #(
    part_run(dir, label, 1, lines, exp1, run1, suffix, quiet),
    part_run(dir, label, 2, lines, exp2, run2, suffix, quiet),
  )
}

fn create_env(path: String) -> RunEnv {
  case simplifile.is_file(path) {
    Ok(True) -> {
      let _ = simplifile.delete(path)
      Nil
    }
    _ -> Nil
  }

  RunEnv(log: fn(msg) {
    io.println(msg)
    let _ = simplifile.append(path, msg)
    Nil
  })
}

fn part_run(
  dir: String,
  label: String,
  part: Int,
  input: List(String),
  expected: Option(a),
  run: fn(List(String), RunEnv) -> a,
  suffix: String,
  quiet: Bool,
) -> TestResult {
  let result_file =
    dir <> "/result" <> suffix <> "_" <> int.to_string(part) <> ".txt"
  let env = create_env(result_file)
  let #(result, time) = timer.measure_time(fn() { run(input, env) })
  let time_str = format_time(time)
  let result_str = string.inspect(result)

  case quiet {
    True -> Nil
    False -> io.print(label <> "/" <> int.to_string(part) <> ": ")
  }

  case expected {
    Some(exp) if exp == result -> {
      case quiet {
        True -> Nil
        False ->
          io.println(correct() <> " (" <> result_str <> ") in " <> time_str)
      }
      Passed
    }

    Some(exp) -> {
      case quiet {
        True -> Nil
        False -> {
          io.println(failed() <> " in " <> time_str)
          io.println("\tEXPECTED: " <> string.inspect(exp))
          io.println("\tGOT     : " <> result_str)
        }
      }
      Failed
    }

    None -> {
      case quiet {
        True -> Nil
        False ->
          io.println(new_result() <> " (" <> result_str <> ") in " <> time_str)
      }
      let _ = env.log(result_str)
      Unchecked
    }
  }
}

pub fn debug(data: a, label: String, env: Option(RunEnv)) -> a {
  let message = case string.is_empty(label) {
    True -> string.inspect(data)
    False -> label <> " " <> string.inspect(data)
  }
  case env {
    Some(e) -> e.log(message)
    None -> Nil
  }
  data
}

fn format_time(seconds: Float) -> String {
  let ms = { seconds *. 1_000_000.0 |> float.round |> int.to_float } /. 1000.0
  case ms <. 1.0 {
    True -> string.inspect(ms *. 1000.0 |> float.round) <> "µs"
    False ->
      case ms <. 1000.0 {
        True -> string.inspect(ms) <> "ms"
        False ->
          string.inspect({ ms |> float.round |> int.to_float } /. 1000.0) <> "s"
      }
  }
}
