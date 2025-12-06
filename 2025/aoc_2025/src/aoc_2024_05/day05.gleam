import gleam/bool
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/order.{type Order}
import gleam/result
import gleam/set.{type Set}
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2024

const day = 5

fn parse_lines(lines: List(String)) -> #(List(#(Int, Int)), List(List(Int))) {
  let order =
    lines
    |> list.filter_map(fn(line) {
      case line |> string.split("|") |> list.map(int.parse) {
        [Ok(left), Ok(right)] -> Ok(#(left, right))
        _ -> Error(Nil)
      }
    })

  let pages =
    lines
    |> list.filter_map(fn(line) {
      case
        line |> string.trim |> string.split(",") |> list.filter_map(int.parse)
      {
        [_, _, ..] as parts -> Ok(parts)
        _ -> Error(Nil)
      }
    })

  #(order, pages)
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let #(order, pages) = parse_lines(lines)

  let test_page = fn(page: Int, before_pages: List(Int)) -> Bool {
    let next_pages =
      set.from_list(
        order
        |> list.filter_map(fn(order) {
          let #(before, after) = order
          case page == after {
            True -> Ok(before)
            False -> Error(Nil)
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

fn compare(a: Int, b: Int, order: Set(#(Int, Int))) -> Order {
  case set.contains(order, #(a, b)) {
    True -> order.Lt
    False -> {
      case set.contains(order, #(b, a)) {
        True -> order.Gt
        False -> {
          let order_list = set.to_list(order)
          case
            order_list
            |> list.filter(fn(pair) { pair.0 == a })
            |> list.any(fn(pair) {
              let #(_, after) = pair
              case compare(after, b, order) {
                order.Lt -> True
                _ -> False
              }
            })
          {
            True -> order.Lt
            False -> {
              case
                order_list
                |> list.filter(fn(p) { p.1 == a })
                |> list.any(fn(pair) {
                  let #(before, _) = pair
                  case compare(b, before, order) {
                    order.Lt -> True
                    _ -> False
                  }
                })
              {
                True -> order.Gt
                False -> order.Eq
              }
            }
          }
        }
      }
    }
  }
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let #(order, pages) = parse_lines(lines)

  let test_page = fn(page: Int, before_pages: List(Int)) -> Bool {
    let next_pages =
      set.from_list(
        order
        |> list.filter_map(fn(order) {
          let #(before, after) = order
          case page == after {
            True -> Ok(before)
            False -> Error(Nil)
          }
        }),
      )
    before_pages
    |> list.any(fn(page) { next_pages |> set.contains(page) })
    |> bool.negate
  }

  let sort_fn = fn(order: Set(#(Int, Int))) {
    fn(a, b) { compare(a, b, order) }
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
