import gleam/bool
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/order.{type Order}
import gleam/result
import gleam/set.{type Set}
import gleam/string
import tools/io
import tools/types.{Expected}

pub const year = 2024

pub const day = 5

pub fn run1(lines: List(String)) -> Int {
  let order =
    lines
    |> list.filter_map(fn(line) {
      case line |> string.split("|") {
        [left, right] ->
          Ok(#(
            int.parse(left) |> result.unwrap(0),
            int.parse(right) |> result.unwrap(0),
          ))
        _ -> Error(Nil)
      }
    })

  let pages =
    lines
    |> list.filter_map(fn(line) {
      case line |> string.trim |> string.split(",") {
        [_, _, ..] as parts ->
          parts
          |> list.try_map(int.parse)
          |> result.map_error(fn(_) { Nil })
        _ -> Error(Nil)
      }
    })

  let test_page = fn(page: Int, before_pages: List(Int)) -> Bool {
    let next_pages =
      set.from_list(
        order
        |> list.filter_map(fn(order) {
          case order.1 {
            after_page if after_page == page -> Ok(order.0)
            _ -> Error(Nil)
          }
        }),
      )
    before_pages
    |> list.any(fn(page) { next_pages |> set.contains(page) })
    |> bool.negate
  }

  pages
  |> list.filter(fn(pages) {
    pages
    |> list.index_map(fn(page, index) { #(index, page) })
    |> list.all(fn(page_index) {
      let #(idx, page) = page_index
      test_page(page, pages |> list.drop(idx))
    })
  })
  |> list.map(fn(pages) {
    pages |> list.drop(list.length(pages) / 2) |> list.first |> result.unwrap(0)
  })
  |> int.sum
}

fn compare(a: Int, b: Int, order: Set(#(Int, Int))) -> Result(Order, Nil) {
  case set.contains(order, #(a, b)) {
    True -> Ok(order.Lt)
    False -> {
      case set.contains(order, #(b, a)) {
        True -> Ok(order.Gt)
        False -> {
          case
            order
            |> set.to_list()
            |> list.filter(fn(pair) { pair.0 == a })
            |> list.any(fn(pair) {
              case compare(pair.1, b, order) {
                Ok(order.Lt) -> True
                _ -> False
              }
            })
          {
            True -> Ok(order.Lt)
            False -> {
              case
                order
                |> set.to_list()
                |> list.filter(fn(p) { p.1 == a })
                |> list.any(fn(pair) {
                  case compare(b, pair.0, order) {
                    Ok(order.Lt) -> True
                    _ -> False
                  }
                })
              {
                True -> Ok(order.Gt)
                False -> Error(Nil)
              }
            }
          }
        }
      }
    }
  }
}

pub fn run2(lines: List(String)) -> Int {
  let order =
    lines
    |> list.filter_map(fn(line) {
      case line |> string.split("|") {
        [left, right] ->
          Ok(#(
            int.parse(left) |> result.unwrap(0),
            int.parse(right) |> result.unwrap(0),
          ))
        _ -> Error(Nil)
      }
    })

  let pages =
    lines
    |> list.filter_map(fn(line) {
      case line |> string.trim |> string.split(",") {
        [_, _, ..] as parts ->
          parts
          |> list.try_map(int.parse)
          |> result.map_error(fn(_) { Nil })
        _ -> Error(Nil)
      }
    })

  let test_page = fn(page: Int, before_pages: List(Int)) -> Bool {
    let next_pages =
      set.from_list(
        order
        |> list.filter_map(fn(order) {
          case order.1 {
            after_page if after_page == page -> Ok(order.0)
            _ -> Error(Nil)
          }
        }),
      )
    before_pages
    |> list.any(fn(page) { next_pages |> set.contains(page) })
    |> bool.negate
  }

  let sort_fn = fn(order: Set(#(Int, Int))) {
    fn(a, b) { compare(a, b, order) |> result.unwrap(order.Eq) }
  }

  pages
  |> list.filter(fn(pages) {
    pages
    |> list.index_map(fn(page, index) { #(index, page) })
    |> list.all(fn(page_index) {
      let #(idx, page) = page_index
      test_page(page, pages |> list.drop(idx))
    })
    |> bool.negate
  })
  |> list.map(fn(pages) {
    let order =
      order
      |> list.filter(fn(o) {
        let #(left, right) = o
        list.contains(pages, left) && list.contains(pages, right)
      })
      |> set.from_list
    pages
    |> list.sort(sort_fn(order))
    |> list.drop(list.length(pages) / 2)
    |> list.first
    |> result.unwrap(0)
  })
  |> int.sum
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(143), Some(123)),
      Expected(0, Some(6498), Some(5017)),
    ],
    run1,
    run2,
    False,
  )
}
