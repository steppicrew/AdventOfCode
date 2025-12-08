import gleam/dict.{type Dict}
import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/set
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 8

fn parse_input(lines: List(String)) -> List(#(Int, Int, Int)) {
  lines
  |> list.filter_map(fn(line) {
    case line |> string.split(",") |> list.map(int.parse) {
      [Ok(x), Ok(y), Ok(z)] -> Ok(#(x, y, z))
      _ -> Error(Nil)
    }
  })
}

fn distance(j1: #(Int, Int, Int), j2: #(Int, Int, Int)) -> Int {
  let #(x1, y1, z1) = j1
  let #(x2, y2, z2) = j2
  let dx = x1 - x2
  let dy = y1 - y2
  let dz = z1 - z2
  dx * dx + dy * dy + dz * dz
}

fn all_distances(
  junktions: List(#(Int, Int, Int)),
) -> Dict(Int, #(#(Int, Int, Int), #(Int, Int, Int))) {
  junktions
  |> list.index_fold(dict.new(), fn(acc, j1, i1) {
    junktions
    |> list.drop(i1 + 1)
    |> list.fold(acc, fn(acc, j2) {
      case dict.has_key(acc, distance(j1, j2)) {
        True -> {
          #(j1, j2) |> io.debug("Duplicate distance found")
          Nil
        }
        False -> Nil
      }
      dict.insert(acc, distance(j1, j2), #(j1, j2))
    })
  })
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let junctions = parse_input(lines)
  let distance_map = all_distances(junctions)
  let distances = dict.keys(distance_map) |> list.sort(int.compare)

  let max_connections = case list.length(lines) {
    20 -> 10
    _ -> 1000
  }

  let circuits =
    distances
    |> list.take(max_connections)
    |> list.fold([], fn(circuits, distance) {
      let circuits = case dict.get(distance_map, distance) {
        Ok(#(j1, j2)) -> {
          case
            circuits
            |> list.filter(fn(circuit) { set.contains(circuit, j1) }),
            circuits
            |> list.filter(fn(circuit) { set.contains(circuit, j2) })
          {
            [c1], [c2] ->
              case c1 == c2 {
                True -> circuits
                False -> {
                  let c = set.union(c1, c2)
                  [
                    c,
                    ..list.filter(circuits, fn(circuit) {
                      circuit != c1 && circuit != c2
                    })
                  ]
                }
              }
            [c1], [] -> [
              c1 |> set.insert(j2),
              ..list.filter(circuits, fn(circuit) { circuit != c1 })
            ]
            [], [c2] -> [
              c2 |> set.insert(j1),
              ..list.filter(circuits, fn(circuit) { circuit != c2 })
            ]
            [], [] -> [set.from_list([j1, j2]), ..circuits]
            _, _ -> circuits |> io.debug("Not merging circuits")
          }
        }
        _ -> circuits
      }

      circuits
    })

  circuits
  |> list.map(fn(circuit) { set.size(circuit) })
  |> list.sort(fn(a, b) { int.compare(b, a) })
  |> list.take(3)
  |> int.product
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let junctions = parse_input(lines)
  let len_junctions = list.length(junctions)
  let distance_map = all_distances(junctions)
  let distances = dict.keys(distance_map) |> list.sort(int.compare)

  let #(last_two, _) =
    distances
    |> list.fold_until(
      #(#(#(0, 0, 0), #(0, 0, 0)), []),
      fn(last_circuits, distance) {
        let #(_, circuits) = last_circuits
        let #(last_two, circuits) = case dict.get(distance_map, distance) {
          Ok(#(j1, j2)) -> {
            let last_two = #(j1, j2)
            case
              circuits
              |> list.filter(fn(circuit) { set.contains(circuit, j1) }),
              circuits
              |> list.filter(fn(circuit) { set.contains(circuit, j2) })
            {
              [c1], [c2] ->
                case c1 == c2 {
                  True -> #(last_two, circuits)
                  False -> {
                    let c = set.union(c1, c2)
                    #(last_two, [
                      c,
                      ..list.filter(circuits, fn(circuit) {
                        circuit != c1 && circuit != c2
                      })
                    ])
                  }
                }
              [c1], [] -> #(last_two, [
                c1 |> set.insert(j2),
                ..list.filter(circuits, fn(circuit) { circuit != c1 })
              ])
              [], [c2] -> #(last_two, [
                c2 |> set.insert(j1),
                ..list.filter(circuits, fn(circuit) { circuit != c2 })
              ])
              [], [] -> #(last_two, [set.from_list([j1, j2]), ..circuits])
              _, _ -> last_circuits |> io.debug("Not merging circuits")
            }
          }
          _ -> last_circuits
        }

        let result = #(last_two, circuits)

        case list.length(circuits) {
          1 ->
            case list.first(circuits) {
              Ok(first) ->
                case set.size(first) == len_junctions {
                  True -> list.Stop(result)
                  False -> list.Continue(result)
                }
              _ -> list.Continue(result)
            }

          _ -> list.Continue(result)
        }
      },
    )

  let #(j1, j2) = last_two
  j1.0 * j2.0
}

pub fn main() {
  io.simple_io(
    year,
    day,
    [
      Expected(1, Some(40), Some(25_272)),
      Expected(0, Some(175_500), Some(6_934_702_555)),
    ],
    run1,
    run2,
    False,
  )
}
