import gleam/dict
import gleam/int
import gleam/list.{Continue, Stop}
import gleam/option.{type Option, None, Some}
import gleam/result
import gleam/set.{type Set}
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

fn sub_button(joltage: Joltages, buttons: ButtonSet, factor: Int) -> Joltages {
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

/// How many times can a button be pressed for this joltage?
fn get_max_button_count(button: ButtonSet, joltage: Joltages) -> Int {
  list.zip(button, joltage)
  |> list.fold(10_000, fn(max, button_joltage) {
    let #(b, j) = button_joltage
    case b {
      1 -> int.min(max, j)
      _ -> max
    }
  })
}

fn empty_joltage(joltage: Joltages) -> Joltages {
  list.map(joltage, fn(_) { 0 })
}

fn joltage_is_empty(joltage: Joltages) -> Bool {
  joltage |> list.all(fn(j) { j == 0 })
}

/// Get all combinations of the button sequeneces
/// max if the nuber of button left
/// Returns all combinations with count for each sequence
/// [[#(2, [..button1]), #(1, [..button2])], [#(1, [..button1]), #(2, [..button2])]]
/// Return Error on error or empty button sequence
fn get_new_joltages(
  buttons: ButtonsSequence,
  joltage: Joltages,
  max_remaining: Int,
) -> Result(List(Joltages), Nil) {
  case buttons {
    // No button -> Return empty list if nothing was requested, Error otherwise
    [] ->
      case max_remaining == 0 {
        True -> Ok([joltage])
        False -> Error(Nil)
      }

    // Single button -> If max possible is larger the requested, return list of one, Error otherwise
    [button] -> {
      let max = get_max_button_count(button, joltage)
      case max >= max_remaining {
        True -> {
          let count = int.max(max, max_remaining)
          Ok([sub_button(joltage, button, count)])
        }
        False -> Error(Nil)
      }
    }
    [button, ..remaining] -> {
      let max = int.min(max_remaining, get_max_button_count(button, joltage))
      Ok(
        list.range(0, max)
        |> list.fold([], fn(acc0, count) {
          let new_joltage = sub_button(joltage, button, count)
          case get_new_joltages(remaining, new_joltage, max_remaining - count) {
            Ok(combis) -> {
              combis
              |> list.fold(acc0, fn(acc, new_joltage) { [new_joltage, ..acc] })
            }
            Error(_) -> acc0
          }
        }),
      )
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

fn get_max_joltage(joltage: Joltages) -> Int {
  joltage |> list.fold(0, fn(max, j) { int.max(max, j) })
}

// Get min/max of joltages greater than 0
fn min_max_joltage0(joltage: Joltages) -> #(Option(Int), Option(Int)) {
  joltage
  |> list.fold(#(None, None), fn(min_max, j) {
    case j {
      0 -> min_max
      _ -> {
        let #(min, max) = min_max
        case min, max {
          Some(min), Some(max) -> #(
            Some(int.min(min, j)),
            Some(int.max(max, j)),
          )
          _, _ -> #(Some(j), Some(j))
        }
      }
    }
  })
}

fn select_min(joltage: Joltages) {
  let selected_joltage_index =
    joltage
    |> list.index_fold(#(10_000, 0), fn(acc, j, i) {
      case j {
        0 -> acc
        j if j < 0 -> {
          j |> io.debug("Strange joltage")
          acc
        }
        _ -> {
          let #(selected, _) = acc
          case selected > j {
            True -> #(j, i)
            False -> acc
          }
        }
      }
    })
  let max_joltage = get_max_joltage(joltage)
  #(selected_joltage_index, max_joltage)
}

fn select_max(joltage: Joltages) {
  let selected_joltage_index =
    joltage
    |> list.index_fold(#(0, 0), fn(acc, j, i) {
      case j {
        0 -> acc
        j if j < 0 -> {
          j |> io.debug("Strange joltage")
          acc
        }
        _ -> {
          let #(selected, _) = acc
          case selected < j {
            True -> #(j, i)
            False -> acc
          }
        }
      }
    })
  #(selected_joltage_index, selected_joltage_index.0)
}

fn select_min_buttons(joltage: Joltages, buttons: ButtonsSequence) {
  let joltage_buttons = count_joltage_buttons(joltage, buttons)

  let #(selected_joltage, _, index) =
    list.zip(joltage, joltage_buttons)
    |> list.index_fold(#(0, 10_000, 0), fn(acc, j_count, i) {
      let #(j, count) = j_count
      case j {
        0 -> acc
        j if j < 0 -> {
          j |> io.debug("Strange joltage")
          acc
        }
        _ -> {
          let #(last_joltage, selected, _) = acc
          case count {
            count if selected > count -> #(j, count, i)
            count if selected == count && j < last_joltage -> #(j, count, i)
            _ -> acc
          }
        }
      }
    })
  #(#(selected_joltage, index), get_max_joltage(joltage))
}

/// Test if for every joltage there is a button
fn test_joltage_buttons(joltage: Joltages, buttons: ButtonsSequence) -> Bool {
  case joltage {
    [] -> True
    [j, ..remaining] -> {
      case j {
        0 ->
          test_joltage_buttons(
            remaining,
            buttons |> list.map(fn(b) { list.drop(b, 1) }),
          )
        _ -> {
          let ok =
            buttons
            |> list.any(fn(button) {
              case button {
                [1, ..] -> True
                _ -> False
              }
            })
          case ok {
            True ->
              test_joltage_buttons(
                remaining,
                buttons |> list.map(fn(b) { list.drop(b, 1) }),
              )
            False -> False
          }
        }
      }
    }
  }
}

/// Find the number of matching buttons for each joltage
fn count_joltage_buttons(
  joltage: Joltages,
  buttons: ButtonsSequence,
) -> List(Int) {
  case joltage {
    [] -> []
    [0, ..remaining] -> [
      100_000,
      ..count_joltage_buttons(
        remaining,
        buttons |> list.map(fn(b) { list.drop(b, 1) }),
      )
    ]
    [_, ..remaining] -> {
      let count =
        buttons
        |> list.count(fn(button) {
          case button {
            [1, ..] -> True
            _ -> False
          }
        })
      let tail =
        count_joltage_buttons(
          remaining,
          buttons |> list.map(fn(b) { list.drop(b, 1) }),
        )
      [count, ..tail]
    }
  }
}

/// Iterate throu buttons
/// buttons: a sequence of buttons
/// joltage: joltages
/// max: abort if count exceeds max
/// env: runtime environment
/// Retuns the smallest number of combinations (or None)
fn iterate_run2(
  buttons: ButtonsSequence,
  joltage: Joltages,
  max_needed: Int,
  env: RunEnv,
) -> Option(Int) {
  // #(buttons, joltage) |> io.log_debug("iterate2a", env)

  // remove all buttons with 1 where joltage is 0
  let buttons =
    buttons
    |> list.filter(fn(buttons) {
      list.zip(buttons, joltage)
      |> list.all(fn(p) {
        let #(button, joltage) = p
        button == 0 || joltage > 0
      })
    })

  let buttons = case test_joltage_buttons(joltage, buttons) {
    True -> buttons
    False -> []
  }

  // #(buttons, joltage) |> io.log_debug("iterate2b", env)

  case buttons {
    // no more buttons left
    [] ->
      case joltage_is_empty(joltage) {
        // Return None if joltage is needed
        False -> None

        // Else: No button needs to be pressed (=0)
        True -> Some(0)
      }

    [only_button] -> {
      // only_button |> io.log_debug("Only button", env)
      let count = get_max_button_count(only_button, joltage)
      case sub_button(joltage, only_button, count) |> joltage_is_empty {
        True -> Some(count)
        False -> None
      }
    }

    // process buttons
    _ -> {
      // #(buttons, joltage) |> io.log_debug("iterate2b", env)

      // Get maxmial joltage and its index

      // let #(selected_joltage_index, max_joltage) = select_min(joltage)
      // let #(selected_joltage_index, max_joltage) = select_max(joltage)
      let #(selected_joltage_index, max_joltage) =
        select_min_buttons(joltage, buttons)
      // |> io.debug("Selected Joltage")

      case selected_joltage_index {
        // If largest joltage is larger the max -> no solution
        _ if max_needed < max_joltage -> {
          // #(max_joltage, max) |> io.debug("Cancel2")
          None
        }

        // try largest joltage
        #(selected_joltage, selected_joltage_index) -> {
          // find all buttons that change that joltage
          let possible_buttons =
            buttons
            |> list.fold([], fn(possible_buttons, button) {
              case button |> list.drop(selected_joltage_index) |> list.first {
                Ok(1) -> [button, ..possible_buttons]
                _ -> possible_buttons
              }
            })

          // get all combinations of those buttons to eliminate that voltage
          case get_new_joltages(possible_buttons, joltage, selected_joltage) {
            Error(_) -> {
              // #(possible_buttons, joltage, min_joltage, min_joltage_index)
              // |> io.debug("This should not happen 2")
              None
            }
            Ok(new_joltages) -> {
              // get new joltages, sorted by lowest remaining joltage

              let cost = selected_joltage

              // button_combis |> io.debug("Button Combis")
              let count =
                new_joltages
                // |> io.debug("Possibilities")
                |> list.fold(max_needed, fn(max, joltage) {
                  case iterate_run2(buttons, joltage, max - cost, env) {
                    Some(c) -> {
                      // #(count, c) |> io.debug("Success")
                      int.min(max, cost + c)
                    }
                    None -> {
                      // io.println("None found")
                      max
                    }
                  }
                })

              Some(count)
            }
          }
        }
      }
    }
  }
}

/// Iterate throu buttons
/// Start with "biggest" button and try max..0
/// buttons: a sequence of buttons
/// joltage: joltages
/// max: abort if count exceeds max
/// env: runtime environment
/// Retuns the smallest number of combinations (or None)
fn iterate_run2a(
  buttons: ButtonsSequence,
  joltage: Joltages,
  max_needed: Int,
  env: RunEnv,
) -> Option(Int) {
  // #(buttons, joltage, max_needed) |> io.log_debug("iterate2a", env)

  // remove all buttons with 1 where joltage is 0
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
    // no more buttons left
    [] ->
      case joltage |> list.any(fn(j) { j != 0 }) {
        // Return None if joltage is needed
        True -> None

        // Else: No button needs to be pressed (=0)
        False -> Some(0)
      }

    [only_button] -> {
      // #(joltage, only_button) |> io.log_debug("Only button", env)
      let max = get_max_button_count(only_button, joltage)
      case sub_button(joltage, only_button, max) |> list.all(fn(j) { j == 0 }) {
        True -> Some(max)
        False -> None
      }
    }

    // process buttons
    [first_button, ..remaining_buttons] -> {
      case get_max_button_count(first_button, joltage) {
        0 -> iterate_run2a(remaining_buttons, joltage, max_needed, env)
        max_count -> {
          let max_needed = int.min(max_needed, joltage |> int.sum)
          list.range(max_count, 0)
          |> list.fold(None, fn(best_count, count) {
            let max = case best_count {
              Some(best_count) -> best_count
              None -> max_needed
            }
            let joltage = sub_button(joltage, first_button, count)
            // #(joltage, first_button, count, max, list.length(remaining_buttons))
            // |> io.log_debug("try this", env)
            case max - count < get_max_joltage(joltage) {
              True -> None
              False -> {
                case
                  iterate_run2a(remaining_buttons, joltage, max - count, env)
                {
                  None -> best_count
                  Some(sub_count) -> {
                    // #(sub_count, count, max)
                    // |> io.log_debug("New best_count", env)
                    Some(int.min(sub_count + count, max))
                  }
                }
              }
            }
          })
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

    // joltage |> io.log_debug("Joltage", env)
    // buttons |> io.log_debug("Sorted buttons", env)

    let result = iterate_run2(buttons, joltage, joltage |> int.sum, env)

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
      Expected(2, Some(3), None),
      // Expected(3, Some(1), None),
      Expected(0, Some(428), Some(16_613)),
    ],
    run1,
    run2,
    False,
  )
}
