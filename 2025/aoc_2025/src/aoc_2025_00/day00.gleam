import gleam/list
import gleam/option.{None}
import tools/io
import tools/types.{Expected}

pub const year = 2025

pub const day = 0

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
    [Expected(1, None, None), Expected(0, None, None)],
    run1,
    run2,
    False,
  )
}
