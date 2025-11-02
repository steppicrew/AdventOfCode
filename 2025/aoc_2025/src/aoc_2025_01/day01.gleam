import gleam/list
import gleam/option.{None, Some}
import tools/io
import tools/types.{Expected}

pub const year = 2025

pub const day = 1

pub fn run1(lines: List(String)) -> Int {
  list.length(lines)
}

pub fn run2(lines: List(String)) -> Int {
  list.length(lines)
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [Expected(1, Some(0), None), Expected(0, Some(0), None)],
    run1,
    run2,
    False,
  )
}
