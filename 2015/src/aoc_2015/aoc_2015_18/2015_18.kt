package aoc_2015.aoc_2015_18

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 18

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (4 to 7),
    0 to (821 to 886)
)

fun run1(input: InputData): ResultType {
    val neighbours = listOf(
        -1 to 0,
        -1 to -1,
        0 to -1,
        1 to -1,
        1 to 0,
        1 to 1,
        0 to 1,
        -1 to 1,
    )

    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char -> (col to row) to (char == '#') }
    }.toMap()

    return (1..100).fold(map) { currentMap, _ ->
        currentMap.mapValues { (position, state) ->
            val neighboursOnCount = neighbours
                .count { neighbourPosition ->
                    (position.first + neighbourPosition.first to position.second + neighbourPosition.second)
                        .let { currentMap[it] ?: false }
                }
            when (state) {
                true -> neighboursOnCount in (2..3)
                false -> neighboursOnCount == 3
            }
        }
    }.values.count { it }
}

fun run2(input: InputData): ResultType {
    val neighbours = listOf(
        -1 to 0,
        -1 to -1,
        0 to -1,
        1 to -1,
        1 to 0,
        1 to 1,
        0 to 1,
        -1 to 1,
    )

    val maxX = input.lines.first().length - 1
    val maxY = input.lines.size - 1

    val corners = setOf(
        0 to 0,
        0 to maxY,
        maxX to 0,
        maxX to maxY,
    )


    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char -> (col to row) to (char == '#') }
    }.plus(
        corners.map { it to true }
    ).toMap()

    return (1..100).fold(map) { currentMap, _ ->
        currentMap.mapValues { (position, state) ->
            if (corners.contains(position)) {
                true
            } else {
                val neighboursOnCount = neighbours
                    .count { neighbourPosition ->
                        (position.first + neighbourPosition.first to position.second + neighbourPosition.second)
                            .let { currentMap[it] ?: false }
                    }
                when (state) {
                    true -> neighboursOnCount in (2..3)
                    false -> neighboursOnCount == 3
                }
            }
        }
    }.values.count { it }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
