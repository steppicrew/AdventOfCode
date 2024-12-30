package aoc_2015.aoc_2015_20

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO
import kotlin.math.roundToInt
import kotlin.math.sqrt

const val YEAR = 2015
const val DAY = 20

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (831600 to 884520)
)

fun run1(input: InputData): ResultType {
    val wantedPresents = input.lines.first().toInt()

    fun getDividers(number: Int): Set<Int> {
        return (1..sqrt(number.toFloat()).roundToInt())
            .filter { number % it == 0 }
            .toSet()
            .let { it + it.map { number / it } }
    }

    for (i in generateSequence(1) { it + 1 }) {
        val presents = getDividers(i).sum() * 10
        if (presents >= wantedPresents) return i
    }

    throw RuntimeException("Unreachable code")
}

fun run2(input: InputData): ResultType {
    val wantedPresents = input.lines.first().toInt()

    fun getDividers(number: Int): Set<Int> {
        return (1..sqrt(number.toFloat()).roundToInt())
            .filter { number % it == 0 }
            .toSet()
            .let { it + it.map { number / it } }
            .filter { number / it <= 50 }
            .toSet()
    }

    for (i in generateSequence(1) { it + 1 }) {
        val presents = getDividers(i).sum() * 11
        if (presents >= wantedPresents) return i
    }

    throw RuntimeException("Unreachable code")
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
