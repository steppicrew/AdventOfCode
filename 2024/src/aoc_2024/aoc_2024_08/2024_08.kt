package aoc_2024.aoc_2024_08

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import kotlin.math.min

const val YEAR = 2024
const val DAY = 8

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (14 to 34),
    0 to (252 to 839),
)


fun run1(input: InputData): ResultType {
    val maxX = input.lines[0].length
    val maxY = input.lines.size

    val antennas = input.lines
        .flatMapIndexed { row, line ->
            line.mapIndexedNotNull { col, char ->
                if (char == '.') {
                    null
                } else {
                    char to (col to row)
                }
            }
        }
        .groupBy({ it.first }, { it.second })
        .filterValues { it.size > 1 }
        .values

    val antinodes = antennas
        .flatMap { positions ->
            positions.flatMapIndexed { index, position ->
                positions
                    .filterIndexed { i, _ -> i > index }
                    .flatMap { otherPosition ->
                        val distance = position.first - otherPosition.first to position.second - otherPosition.second
                        listOf(
                            position.first + distance.first to position.second + distance.second,
                            position.first - 2 * distance.first to position.second - 2 * distance.second,
                        ).filter { it.first in 0..<maxX && it.second in 0..<maxY }

                    }

            }
        }.toSet()

    return antinodes.size
}

fun run2(input: InputData): ResultType {
    val maxX = input.lines[0].length
    val maxY = input.lines.size

    val antennas = input.lines
        .flatMapIndexed { row, line ->
            line.mapIndexedNotNull { col, char ->
                if (char == '.') {
                    null
                } else {
                    char to (col to row)
                }
            }
        }
        .groupBy({ it.first }, { it.second })
        .filterValues { it.size > 1 }
        .values

    fun normalize(distance: Pair<Int, Int>): Pair<Int, Int> {
        val minValue = min(distance.first, distance.second)
        for (i in minValue downTo 2) {
            if (distance.first % i == 0 && distance.second % i == 0) {
                return distance.first / i to distance.second / i
            }
        }
        return distance
    }

    val antinodes = antennas
        .flatMap { positions ->
            positions.flatMapIndexed { index, position ->
                positions
                    .filterIndexed { i, _ -> i > index }
                    .flatMap { otherPosition ->
                        val distance =
                            normalize(position.first - otherPosition.first to position.second - otherPosition.second)
                        (-maxX..maxX).map {
                            position.first + it * distance.first to position.second + it * distance.second
                        }
                            .filter { it.first in 0..<maxX && it.second in 0..<maxY }

                    }

            }
        }.toSet()

    return antinodes.size
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
