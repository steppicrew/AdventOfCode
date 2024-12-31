package aoc_2024.aoc_2024_07

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 7

typealias ResultType = ULong

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (3749UL to 11387UL),
    0 to (882304362421UL to 145149066755184UL),
)

fun run1(input: InputData): ResultType {
    val rePart = """(\d+): ([\d ]+)""".toRegex()
    val equations = input.lines
        .mapNotNull { rePart.matchEntire(it) }
        .map { match ->
            val (result, operators) = match.destructured
            result.toULong() to operators.split(" ").map(String::toULong)
        }

    fun getResults(operators: List<ULong>): Sequence<ULong> {
        val last = operators.last()
        if (operators.size == 1) return sequenceOf(last)
        return getResults(operators.dropLast(1)).flatMap {
            sequenceOf(it + last, it * last)
        }
    }

    return equations.filter { (result, operators) ->
        result in getResults(operators)
    }.sumOf { it.first }
}

fun run2(input: InputData): ResultType {
    val rePart = """(\d+): ([\d ]+)""".toRegex()
    val equations = input.lines
        .mapNotNull { rePart.matchEntire(it) }
        .map { match ->
            val (result, operators) = match.destructured
            result.toULong() to operators.split(" ").map(String::toULong)
        }

    fun getResults(operators: List<ULong>): Sequence<ULong> {
        val last = operators.last()
        if (operators.size == 1) return sequenceOf(last)
        return getResults(operators.dropLast(1)).flatMap {
            sequenceOf(it + last, it * last, "${it}${last}".toULong())
        }
    }

    return equations.filter { (result, operators) ->
        result in getResults(operators)
    }.sumOf { it.first }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
