import gleam/dict.{type Dict}
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/set.{type Set}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 11

fn parse_lines(lines: List(String)) -> Dict(String, List(String)) {
  lines
  |> list.fold(dict.new(), fn(acc, line) {
    case string.split(line, " ") {
      [] -> acc
      [_] -> acc
      [first, ..destinations] -> {
        let device = string.drop_end(first, 1)
        acc |> dict.insert(device, destinations)
      }
    }
  })
}

fn count_pathes1(
  devices: Dict(String, List(String)),
  device: String,
  seen: Set(String),
) -> Int {
  case set.contains(seen, device) {
    True -> 0
    False -> {
      let seen = set.insert(seen, device)
      case dict.get(devices, device) {
        Ok(destinations) -> {
          destinations
          |> list.map(fn(d) {
            case d {
              "out" -> 1
              _ -> count_pathes1(devices, d, seen)
            }
          })
          |> int.sum
        }
        Error(_) -> 0
      }
    }
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let devices = parse_lines(lines)

  count_pathes1(devices, "you", set.new())
}

// None, FFT, DAC, FFT&DAC
fn count_pathes2(
  devices: Dict(String, List(String)),
  device: String,
  seen: Set(String),
  cache: Dict(String, #(Int, Int, Int, Int)),
) -> #(#(Int, Int, Int, Int), Dict(String, #(Int, Int, Int, Int))) {
  // device |> io.debug("Device")
  case dict.get(cache, device) {
    Ok(counts) -> #(counts, cache)
    _ -> {
      case set.contains(seen, device) {
        True -> #(#(0, 0, 0, 0), cache)
        False -> {
          let seen = set.insert(seen, device)
          case dict.get(devices, device) {
            Ok(destinations) -> {
              destinations
              |> list.fold(#(#(0, 0, 0, 0), cache), fn(acc, device) {
                let #(sums, cache) = acc
                case device {
                  "out" -> #(#(1, 0, 0, 0), cache)
                  _ -> {
                    let #(counts, cache) =
                      count_pathes2(devices, device, seen, cache)
                    let counts = case device {
                      device if device == "fft" -> #(
                        0,
                        counts.0 + counts.1,
                        0,
                        counts.2 + counts.3,
                      )
                      device if device == "dac" -> #(
                        0,
                        0,
                        counts.0 + counts.2,
                        counts.1 + counts.3,
                      )
                      _ -> counts
                    }
                    // #(device, counts)|>io.debug("")
                    let cache = dict.insert(cache, device, counts)

                    let sums = #(
                      sums.0 + counts.0,
                      sums.1 + counts.1,
                      sums.2 + counts.2,
                      sums.3 + counts.3,
                    )

                    #(sums, cache)
                    // |> io.debug("NotOut")
                  }
                }
              })
            }
            Error(_) -> #(#(0, 0, 0, 0), cache)
          }
        }
      }
    }
  }
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let devices = parse_lines(lines)

  let #(counts, _) = count_pathes2(devices, "svr", set.new(), dict.new())
  counts.3
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(5), Some(0)),
      Expected(2, Some(0), Some(2)),
      Expected(0, Some(772), Some(423_227_545_768_872)),
    ],
    run1,
    run2,
    False,
  )
}
