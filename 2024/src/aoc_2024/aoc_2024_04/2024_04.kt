package aoc_2024.aoc_2024_04

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 4

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (18 to 9),
    0 to (2644 to 1952)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val field = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (row to col) to char
        }
    }.toMap()

    val dirs = listOf(
        1 to 0,
        0 to 1,
        1 to 1,
        1 to -1,
        -1 to 0,
        0 to -1,
        -1 to -1,
        -1 to 1,
    )

    fun testPos(pos: Pair<Int, Int>): Int {
        fun testWord(dir: Pair<Int, Int>): Boolean {
            fun getChar(i: Int): Char? {
                return field[pos.first + i * dir.first to pos.second + i * dir.second]
            }
            return getChar(0) == 'X' && getChar(1) == 'M' && getChar(2) == 'A' && getChar(3) == 'S'
        }
        return dirs.count { testWord(it) }
    }

    return field.keys.sumOf { testPos(it) }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val field = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (row to col) to char
        }
    }.toMap()

    val dirs = listOf(
        1 to 1,
        1 to -1,
        -1 to -1,
        -1 to 1,
    )

    fun testPos(pos: Pair<Int, Int>): Boolean {
        fun testWord(dir: Pair<Int, Int>): Boolean {
            fun getChar(i: Int): Char? {
                return field[pos.first + i * dir.first to pos.second + i * dir.second]
            }
            return getChar(-1) == 'M' && getChar(0) == 'A' && getChar(1) == 'S'
        }
        return dirs.count { testWord(it) } == 2
    }

    return field.keys.count { testPos(it) }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
