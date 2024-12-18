package aoc_2024.aoc_2024_06

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 6

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (41 to 6),
    0 to (5131 to 1784)
)

fun run1(input: InputData): ResultType {
    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char
        }
    }.toMap()
    var position = map.entries.first { it.value == '^' }.key
    var direction = 0 to -1

    val visited = mutableSetOf(position)
    while (map.containsKey(position)) {
        visited.add(position)
        val nextPosition = position.first + direction.first to position.second + direction.second
        if (map.get(nextPosition) == '#') {
            // Rotate direction 90 degrees clockwise
            direction = (-direction.second) to direction.first
            continue
        }
        position = nextPosition
    }
    return visited.size
}

fun run2(input: InputData): ResultType {
    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char
        }
    }.toMap()
    val startPosition = map.entries.first { it.value == '^' }.key

    // Clockwise direction rotation: up, right, down, left
    val directions = listOf(0 to -1, 1 to 0, 0 to 1, -1 to 0)

    fun hasCycle(obstacle: Map.Entry<Pair<Int, Int>, Char>): Boolean {

        var position = startPosition
        var directionIndex = 0

        val visited = mutableSetOf(position to directionIndex)

        while (map.containsKey(position)) {
            val nextPosition =
                position.first + directions[directionIndex].first to
                        position.second + directions[directionIndex].second
            if (map[nextPosition] == '#' || nextPosition == obstacle.key) {
                // Rotate direction clockwise
                directionIndex = (directionIndex + 1) % directions.size
            } else {
                position = nextPosition
                if (!visited.add(position to directionIndex)) {
                    return true // Cycle detected
                }
            }
        }
        return false
    }

    return map.asSequence()
        .filter { it.value == '.' && it.key != startPosition }
        .count(::hasCycle)
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
