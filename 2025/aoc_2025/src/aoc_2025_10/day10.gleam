import gleam/dict
import gleam/int
import gleam/list.{Continue, Stop}
import gleam/option.{type Option, None, Some}
import gleam/result
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 10

type Lights =
  String

type ButtonSet =
  List(Int)

type ButtonsSequence =
  List(ButtonSet)

type Joltages =
  List(Int)

fn parse_lines(
  lines: List(String),
) -> List(#(Lights, ButtonsSequence, Joltages)) {
  lines
  |> list.map(fn(line) {
    string.split(line, " ")
    |> list.fold(#("", [], []), fn(acc, part) {
      let #(lights, buttons, joltage) = acc
      let rest = string.slice(part, 1, string.length(part) - 2)
      case string.first(part) {
        Ok("[") -> {
          #(rest, buttons, joltage)
        }
        Ok("(") -> {
          let new_buttons =
            string.split(rest, ",")
            |> list.map(fn(n) { int.parse(n) |> result.unwrap(-1) })
          #(lights, [new_buttons, ..buttons], joltage)
        }
        Ok("{") -> {
          let joltage =
            string.split(rest, ",")
            |> list.map(fn(n) { int.parse(n) |> result.unwrap(-1) })
          #(lights, buttons, joltage)
        }
        _ -> {
          part |> io.debug("Unexpected part")
          acc
        }
      }
    })
  })
}

fn combine_buttons(buttons: ButtonsSequence) -> List(ButtonsSequence) {
  case buttons {
    [] -> []
    [first, ..rest] -> {
      let next_combinations = combine_buttons(rest)
      let combinations =
        next_combinations
        |> list.fold(next_combinations, fn(acc, combi) {
          [[first, ..combi], ..acc]
        })
      [[first], ..combinations]
    }
  }
}

fn press_light_buttons(button_list: ButtonsSequence, max_lights: Int) -> String {
  let lights =
    button_list
    |> list.fold(dict.new(), fn(acc, buttons) {
      buttons
      |> list.fold(acc, fn(acc, button) {
        dict.upsert(acc, button, fn(old) {
          case old {
            Some(b) -> !b
            None -> True
          }
        })
      })
    })
  list.range(max_lights - 1, 0)
  |> list.fold("", fn(acc, i) {
    case dict.get(lights, i) {
      Ok(True) -> "#" <> acc
      _ -> "." <> acc
    }
  })
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let data = parse_lines(lines)

  data
  |> list.map(fn(line) {
    let #(lights, buttons, _) = line
    let result =
      combine_buttons(buttons)
      |> list.sort(fn(a, b) { int.compare(list.length(a), list.length(b)) })
      // |> io.debug("combis")
      |> list.find(fn(combi) {
        let l = press_light_buttons(combi, string.length(lights))
        // #(combi, l) |> io.debug("Lights")
        l == lights
      })
    case result {
      Ok(r) -> list.length(r)
      _ -> 0 |> io.debug("Error")
    }
  })
  // |> io.debug("Result")
  |> int.sum
}

fn parse_lines2(
  lines: List(String),
) -> List(#(Lights, List(#(Int, ButtonSet)), Joltages)) {
  lines
  |> list.map(fn(line) {
    string.split(line, " ")
    |> list.fold(#("", [], []), fn(acc, part) {
      let #(lights, buttons, joltage) = acc
      let rest = string.slice(part, 1, string.length(part) - 2)
      case string.first(part) {
        Ok("[") -> {
          #(rest, buttons, joltage)
        }
        Ok("(") -> {
          let new_buttons =
            string.split(rest, ",")
            |> list.map(fn(n) { int.parse(n) |> result.unwrap(-1) })
          let button_mask =
            new_buttons
            |> list.fold([], fn(acc, button) {
              let len = list.length(acc)
              let acc = case len < button {
                True ->
                  list.range(len, button - 1)
                  |> list.fold(acc, fn(acc, _) { [0, ..acc] })
                False -> acc
              }
              [1, ..acc]
            })
            |> list.reverse
          #(
            lights,
            [#(list.length(new_buttons), button_mask), ..buttons],
            joltage,
          )
        }
        Ok("{") -> {
          let joltage =
            string.split(rest, ",")
            |> list.map(fn(n) { int.parse(n) |> result.unwrap(-1) })
          #(lights, buttons, joltage)
        }
        _ -> {
          part |> io.debug("Unexpected part")
          acc
        }
      }
    })
  })
}

fn get_max_factor(buttons: ButtonSet, joltage: Joltages) -> Int {
  list.zip(buttons, joltage)
  |> list.fold(1000, fn(acc, pair) {
    let #(button, joltage) = pair
    case button {
      0 -> acc
      _ -> int.min(acc, joltage)
    }
  })
}

fn sub_voltage(buttons: ButtonSet, factor: Int, joltage: Joltages) -> Joltages {
  let new_joltage =
    list.zip(buttons, joltage)
    |> list.map(fn(pair) {
      let #(button, joltage) = pair
      joltage - factor * button
    })
  let new_len = list.length(new_joltage)
  case new_len < list.length(joltage) {
    True -> new_joltage |> list.append(joltage |> list.drop(new_len))
    False -> new_joltage
  }
}

fn joltage_empty(joltage: Joltages) -> Bool {
  joltage |> list.all(fn(j) { j == 0 })
}

fn iterate_run2(
  buttons: ButtonsSequence,
  joltage: Joltages,
  old_min: Int,
  env: RunEnv,
) -> Int {
  #(buttons, joltage) |> io.log_debug("iterate2", env)
  case buttons {
    [first, ..rest] -> {
      let max = int.min(get_max_factor(first, joltage), old_min)
      case max {
        max if max < 0 -> 10_000
        0 -> iterate_run2(rest, joltage, old_min, env)
        max ->
          list.range(max, 0)
          |> list.fold(old_min, fn(min, count) {
            let new_joltage = sub_voltage(first, count, joltage)
            let new_min = case joltage_empty(new_joltage) {
              True -> {
                #(buttons, count, joltage) |> io.debug("Found")
                count
              }
              False -> {
                // #(first, rest, count, joltage, new_joltage) |> io.debug("Next")
                iterate_run2(rest, new_joltage, old_min - count, env) + count
              }
            }
            int.min(min, new_min)
          })
      }
    }
    [] -> 10_000
  }
}

fn get_buttons_combinations(
  buttons: ButtonsSequence,
  max: Int,
) -> Result(List(List(#(Int, ButtonSet))), Nil) {
  case buttons, max {
    _, max if max < 0 -> {
      #(buttons, max) |> io.debug("Error1")
      Error(Nil)
    }
    [], max if max > 0 -> {
      // #(buttons, max) |> io.debug("Error2")
      Error(Nil)
    }
    [], _ -> Ok([[]])
    _, max if max == 0 -> Ok([[]])
    [first], max -> Ok([[#(max, first)]])
    [first, ..remaining], 1 -> {
      case get_buttons_combinations(remaining, 1) {
        Ok(other_combis) -> Ok([[#(max, first)], ..other_combis])
        _ -> {
          #(buttons, max) |> io.debug("Error3")
          Error(Nil)
        }
      }
    }
    [first, ..remaining], max -> {
      case get_buttons_combinations(remaining, max) {
        Ok(follow_combis) -> {
          let a =
            list.range(max - 1, 1)
            |> list.fold(follow_combis, fn(acc, i) {
              case get_buttons_combinations(remaining, max - i) {
                Ok(other_combis) ->
                  other_combis
                  |> list.fold(acc, fn(acc, c) { [[#(i, first), ..c], ..acc] })
                _ -> acc
              }
            })
          Ok([[#(max, first)], ..a])
        }
        Error(_) -> {
          #(buttons, max) |> io.debug("Error4")
          Error(Nil)
        }
      }
    }
  }
}

fn min_max_joltage(joltage: Joltages) -> #(Int, Int) {
  joltage
  |> list.fold(#(10_000, 0), fn(min_max, j) {
    let #(min, max) = min_max
    #(int.min(min, j), int.max(max, j))
  })
}

fn iterate_run2a(
  buttons: ButtonsSequence,
  joltage: Joltages,
  max: Option(Int),
  env: RunEnv,
) -> Option(Int) {
  // #(buttons, joltage) |> io.log_debug("iterate2a", env)
  let buttons =
    buttons
    |> list.filter(fn(buttons) {
      list.zip(buttons, joltage)
      |> list.all(fn(p) {
        let #(button, joltage) = p
        button == 0 || joltage > 0
      })
    })
  // #(buttons, joltage) |> io.log_debug("iterate2b", env)

  case buttons {
    [] ->
      case joltage |> list.any(fn(j) { j > 0 }) {
        True -> None
        False -> Some(0)
      }
    _ -> {
      // #(buttons, joltage) |> io.log_debug("iterate2b", env)
      let #(min_joltage, max_joltage) =
        joltage
        |> list.index_fold(#(None, None), fn(acc, joltage, i) {
          case joltage {
            0 -> acc
            j if j < 0 -> {
              joltage |> io.log_debug("Strange joltage", env)
              acc
            }
            _ -> {
              case acc {
                #(None, None) -> #(Some(#(joltage, i)), Some(#(joltage, i)))
                #(Some(#(min_joltage, _)), Some(#(max_joltage, _))) -> {
                  let acc = case min_joltage > joltage {
                    True -> #(Some(#(joltage, i)), acc.1)
                    False -> acc
                  }
                  let acc = case max_joltage < joltage {
                    True -> #(acc.0, Some(#(joltage, i)))
                    False -> acc
                  }
                  acc
                }
                #(_, _) -> acc
              }
            }
          }
        })

      case min_joltage, max_joltage, max {
        None, _, _ -> Some(0)
        _, Some(#(max_joltage, _)), Some(max) if max < max_joltage -> {
          // #(max_joltage, max) |> io.debug("Cancel2")
          None
        }
        Some(#(min_joltage, mj_index)), _, _ -> {
          let possible_buttons =
            buttons
            |> list.fold([], fn(possible_buttons, buttons) {
              case buttons |> list.drop(mj_index) |> list.first {
                Ok(1) -> [buttons, ..possible_buttons]
                _ -> possible_buttons
              }
            })

          case get_buttons_combinations(possible_buttons, min_joltage) {
            Error(_) -> None
            Ok(button_combis) -> {
              let #(possibilities, _) =
                button_combis
                |> list.fold(#([], 1000), fn(acc, combi) {
                  let #(possibilities, max) = acc
                  let joltage =
                    combi
                    |> list.fold(joltage, fn(joltage, button) {
                      let #(button_count, button) = button
                      sub_voltage(button, button_count, joltage)
                    })
                  let #(min_joltage2, max_joltage2) = min_max_joltage(joltage)
                  case min_joltage2, max_joltage2 {
                    // min_j, _ if min_j < 0 -> acc
                    // _, max_j if max_j < max -> #(
                    //   [#(min_joltage, joltage)],
                    //   max_j,
                    // )
                    // _, max_j if max_j == max -> #(
                    //   [#(min_joltage, joltage), ..possibilities],
                    //   max,
                    // )
                    // _, _ -> acc
                    _, _ -> #([#(min_joltage, joltage), ..possibilities], max)
                  }
                })

              // button_combis |> io.debug("Button Combis")
              possibilities
              // |> io.debug("Possibilities")
              |> list.fold(None, fn(min, p) {
                let #(count, joltage) = p
                let min1 = case min {
                  Some(min) -> Some(min - count)
                  None -> None
                }
                case iterate_run2a(buttons, joltage, min1, env), min {
                  Some(c), Some(min) -> {
                    // #(count, c) |> io.debug("Success")
                    Some(int.min(min, count + c))
                  }
                  Some(c), None -> {
                    // #(count, c) |> io.debug("Success")
                    Some(count + c)
                  }
                  None, _ -> {
                    // io.println("None found")
                    min
                  }
                }
              })
            }
          }
        }
      }
    }
  }
}

fn run2(lines: List(String), env: RunEnv) -> Int {
  let data = parse_lines2(lines)
  data
  |> list.index_map(fn(data, i) {
    let #(_, buttons, joltage) = data
    let buttons =
      buttons
      |> list.sort(fn(a, b) { int.compare(b.0, a.0) })
      |> list.map(fn(a) { a.1 })

    let result = iterate_run2a(buttons, joltage, None, env)

    #(i, result) |> io.debug("Result")
    result
  })
  |> list.map(fn(p) {
    case p {
      Some(i) -> i
      None -> 0
    }
  })
  |> int.sum()
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(7), Some(33)),
      // Expected(2, Some(3), None),
      Expected(0, Some(428), None),
    ],
    run1,
    run2,
    False,
  )
}
