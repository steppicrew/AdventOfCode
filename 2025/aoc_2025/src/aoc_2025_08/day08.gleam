import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/set
import gleam/string
import tools/io.{type RunEnv}
import tools/types.{Expected}

const year = 2025

const day = 8

type Joint =
  #(Int, Int, Int)

type Connection =
  #(Joint, Joint)

fn parse_input(lines: List(String)) -> List(Joint) {
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

fn distance(j1: Joint, j2: Joint) -> Int {
  let #(x1, y1, z1) = j1
  let #(x2, y2, z2) = j2
  let dx = x1 - x2
  let dy = y1 - y2
  let dz = z1 - z2
  dx * dx + dy * dy + dz * dz
}

fn get_sorted_connections(junktions: List(Joint)) -> List(Connection) {
  junktions
  |> list.index_fold([], fn(acc, j1, i1) {
    junktions
    |> list.drop(i1 + 1)
    |> list.fold(acc, fn(acc, j2) { [#(#(j1, j2), distance(j1, j2)), ..acc] })
  })
  |> list.sort(fn(a, b) { int.compare(a.1, b.1) })
  |> list.map(fn(connection) { connection.0 })
}

fn join_junctions(
  circuits: List(set.Set(Joint)),
  connection: Connection,
) -> List(set.Set(Joint)) {
  let #(j1, j2) = connection
  case
    circuits
    |> list.find(fn(circuit) { set.contains(circuit, j1) }),
    circuits
    |> list.find(fn(circuit) { set.contains(circuit, j2) })
  {
    // Both joint already in circuits
    Ok(c1), Ok(c2) ->
      case c1 == c2 {
        // Both joints in same circuit
        True -> circuits

        // Both joints in different circuits -> merge circuits
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

    // Only joint 1 already in a circuit -> add joint 2 to it
    Ok(c1), Error(_) -> [
      c1 |> set.insert(j2),
      ..list.filter(circuits, fn(circuit) { circuit != c1 })
    ]

    // Only joint 2 already in a circuit -> add joint 1 to it
    Error(_), Ok(c2) -> [
      c2 |> set.insert(j1),
      ..list.filter(circuits, fn(circuit) { circuit != c2 })
    ]

    // Neither joint in a circuit yet -> create new circuit
    Error(_), Error(_) -> [set.from_list([j1, j2]), ..circuits]
  }
}

fn run1(lines: List(String), _: RunEnv) -> Int {
  let junctions = parse_input(lines)

  let max_connections = case list.length(lines) {
    20 -> 10
    _ -> 1000
  }

  get_sorted_connections(junctions)
  // Only take the first N connections to limit runtime
  |> list.take(max_connections)
  // Build list of circuits
  |> list.fold([], join_junctions)
  // Map to circuit sizes
  |> list.map(fn(circuit) { set.size(circuit) })
  // Sort sizes descending
  |> list.sort(fn(a, b) { int.compare(b, a) })
  // Take the top 3 largest circuits
  |> list.take(3)
  // Multiply their sizes
  |> int.product
}

fn run2(lines: List(String), _: RunEnv) -> Int {
  let junctions = parse_input(lines)
  let junction_count = list.length(junctions)

  // Add connections until all junctions are connected
  // Mutliply the x-values of the last two connections added
  let #(#(x1, _, _), #(x2, _, _), _) =
    get_sorted_connections(junctions)
    |> list.fold_until(#(#(0, 0, 0), #(0, 0, 0), []), fn(acc, connection) {
      let #(_, _, circuits) = acc
      let #(j1, j2) = connection
      let circuits = join_junctions(circuits, connection)

      let acc = #(j1, j2, circuits)

      // If there is only one circuit with all junctions, all junctions are connected
      case circuits {
        [only] ->
          case set.size(only) == junction_count {
            // All junctions are connected
            True -> list.Stop(acc)

            // Not all junctions are connected
            False -> list.Continue(acc)
          }
        _ -> list.Continue(acc)
      }
    })

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
