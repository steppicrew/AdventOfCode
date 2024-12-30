package aoc_2015.aoc_2015_25

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 25

typealias ResultType = Long

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (20151125L to 0L),
    5 to (21629792L to 0L),
    15 to (10071777L to 0L),
    16 to (33071741L to 0L),
    19 to (7981243L to 0L),
    0 to (9132360L to 0L)
)

fun run1(input: InputData): ResultType {
    fun generate(): Sequence<Long> = sequence {
        var code = 20151125L
        while (true) {
            yield(code)
            code = code * 252533L % 33554393L
        }
    }

    val codePosition = when (input.ref) {
        1 -> 1 to 1
        5 -> 2 to 2
        15 -> 5 to 1
        16 -> 1 to 6
        19 -> 4 to 3
        0 -> 3075 to 2981
        else -> throw RuntimeException("Unknown position")
    }

    fun getIndex(position: Pair<Int, Int>): Int {
        val (col, row) = position
        return (col + row) * (col + row - 1) / 2 - row
    }

    return generate().drop(getIndex(codePosition)).first()
}

fun run2(
    @Suppress("UNUSED_PARAMETER") input: InputData
): ResultType {
    return 0L
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
