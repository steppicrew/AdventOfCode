import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/set
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 8

type Coord =
  #(Int, Int, Int)

type Joint =
  #(Coord, Coord)

fn parse_input(lines: List(String)) -> List(Coord) {
  lines
  |> list.filter_map(fn(line) {
    case line |> string.split(",") {
      [x, y, z] ->
        case int.parse(x), int.parse(y), int.parse(z) {
          Ok(x), Ok(y), Ok(z) -> Ok(#(x, y, z))
          _, _, _ -> Error(Nil)
        }
      _ -> Error(Nil)
    }
  })
}

fn distance(j1: Coord, j2: Coord) -> Int {
  let #(x1, y1, z1) = j1
  let #(x2, y2, z2) = j2
  let dx = x1 - x2
  let dy = y1 - y2
  let dz = z1 - z2
  dx * dx + dy * dy + dz * dz
}

fn get_sorted_connections(junktions: List(Coord)) -> List(Joint) {
  junktions
  |> list.index_fold([], fn(acc, j1, i1) {
    junktions
    |> list.drop(i1 + 1)
    |> list.fold(acc, fn(acc, j2) { [#(#(j1, j2), distance(j1, j2)), ..acc] })
  })
  |> list.sort(fn(a, b) { int.compare(a.1, b.1) })
  |> list.map(fn(connection) { connection.0 })
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let junctions = parse_input(lines)

  let max_connections = case list.length(lines) {
    20 -> 10
    _ -> 1000
  }

  let circuits =
    get_sorted_connections(junctions)
    |> list.take(max_connections)
    |> list.fold([], fn(circuits, connection) {
      let #(j1, j2) = connection
      let circuits = case
        circuits
        |> list.find(fn(circuit) { set.contains(circuit, j1) }),
        circuits
        |> list.find(fn(circuit) { set.contains(circuit, j2) })
      {
        Ok(c1), Ok(c2) ->
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
        Ok(c1), Error(_) -> [
          c1 |> set.insert(j2),
          ..list.filter(circuits, fn(circuit) { circuit != c1 })
        ]
        Error(_), Ok(c2) -> [
          c2 |> set.insert(j1),
          ..list.filter(circuits, fn(circuit) { circuit != c2 })
        ]
        Error(_), Error(_) -> [set.from_list([j1, j2]), ..circuits]
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

  let #(#(#(x1, _, _), #(x2, _, _)), _) =
    get_sorted_connections(junctions)
    |> list.fold_until(
      #(#(#(0, 0, 0), #(0, 0, 0)), []),
      fn(last_circuits, connection) {
        let #(j1, j2) = connection
        let #(_, circuits) = last_circuits
        let #(last_connection_added, circuits) = case
          circuits
          |> list.find(fn(circuit) { set.contains(circuit, j1) }),
          circuits
          |> list.find(fn(circuit) { set.contains(circuit, j2) })
        {
          Ok(c1), Ok(c2) ->
            case c1 == c2 {
              True -> #(connection, circuits)
              False -> {
                let c = set.union(c1, c2)
                #(connection, [
                  c,
                  ..list.filter(circuits, fn(circuit) {
                    circuit != c1 && circuit != c2
                  })
                ])
              }
            }
          Ok(c1), Error(_) -> #(connection, [
            c1 |> set.insert(j2),
            ..list.filter(circuits, fn(circuit) { circuit != c1 })
          ])
          Error(_), Ok(c2) -> #(connection, [
            c2 |> set.insert(j1),
            ..list.filter(circuits, fn(circuit) { circuit != c2 })
          ])
          Error(_), Error(_) -> #(connection, [
            set.from_list([j1, j2]),
            ..circuits
          ])
        }

        let result = #(last_connection_added, circuits)

        case circuits {
          [first] ->
            case set.size(first) == len_junctions {
              True -> list.Stop(result)
              False -> list.Continue(result)
            }

          _ -> list.Continue(result)
        }
      },
    )

  x1 * x2
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
