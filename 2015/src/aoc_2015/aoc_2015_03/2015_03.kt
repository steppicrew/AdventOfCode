package aoc_2015.aoc_2015_03

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 3

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (2 to 11),
    0 to (2081 to 2341)
)

fun run1(input: InputData): ResultType {
    var pos = 0 to 0
    val visited = sequenceOf(0 to 0)
        .plus(input.lines[0].map { char ->
            when (char) {
                '<' -> pos.first - 1 to pos.second
                '>' -> pos.first + 1 to pos.second
                '^' -> pos.first to pos.second + 1
                'v' -> pos.first to pos.second - 1
                else -> pos
            }.also {
                pos = it
            }
        }).toSet()
    return visited.count()
}

fun run2(input: InputData): ResultType {
    val bots = mutableListOf(0 to 0, 0 to 0)
    val visited = sequenceOf(0 to 0)
        .plus(input.lines[0].mapIndexed { index, char ->
            val pos = bots[index % 2]
            when (char) {
                '<' -> pos.first - 1 to pos.second
                '>' -> pos.first + 1 to pos.second
                '^' -> pos.first to pos.second + 1
                'v' -> pos.first to pos.second - 1
                else -> pos
            }.also {
                bots[index % 2] = it
            }
        }).toSet()
    return visited.count()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
