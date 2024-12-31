package aoc_2024.aoc_2024_04

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 4

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (18 to 9),
    0 to (2644 to 1952)
)

fun run1(input: InputData): ResultType {
    val field = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (row to col) to char
        }
    }.toMap()

    val directions = listOf(
        1 to 0,
        0 to 1,
        1 to 1,
        1 to -1,
        -1 to 0,
        0 to -1,
        -1 to -1,
        -1 to 1,
    )

    return field.keys.sumOf { position ->
        directions.count { direction ->
            fun getChar(i: Int): Char? {
                return field[position.first + i * direction.first to position.second + i * direction.second]
            }
            getChar(0) == 'X' && getChar(1) == 'M' && getChar(2) == 'A' && getChar(3) == 'S'
        }
    }
}

fun run2(input: InputData): ResultType {
    val field = input.lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (row to col) to char
        }
    }.toMap()

    val directions = listOf(
        1 to 1,
        1 to -1,
        -1 to -1,
        -1 to 1,
    )

    return field.keys.count { position ->
        directions.count { direction ->
            fun getChar(i: Int): Char? {
                return field[position.first + i * direction.first to position.second + i * direction.second]
            }
            getChar(-1) == 'M' && getChar(0) == 'A' && getChar(1) == 'S'
        } == 2
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
