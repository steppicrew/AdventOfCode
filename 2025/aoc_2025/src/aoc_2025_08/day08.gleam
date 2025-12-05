import gleam/list
import gleam/option.{None, Some}
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 8

fn run1(lines: List(String), _: RunEnv) -> Int {
  list.length(lines)
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  list.length(lines)
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(0), Some(0)),
      Expected(0, None, None),
    ],
    run1,
    run2,
    False,
  )
}
