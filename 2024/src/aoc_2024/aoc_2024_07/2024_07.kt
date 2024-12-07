package aoc_2024.aoc_2024_07

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 7

// ref to (run1 to run2)
// values may by of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ULong> = listOf(
    1 to (3749UL to 11387UL),
    0 to (882304362421UL to 145149066755184UL),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ULong {
    val rePart = """(\d+): ([\d ]+)""".toRegex()
    val equations = lines
        .mapNotNull { rePart.matchEntire(it) }
        .map { match ->
            val (result, operators) = match.destructured
            result.toULong() to operators.split(" ").map(String::toULong)
        }

    fun getResults(operators: MutableList<ULong>): Set<ULong> {
        val operator = operators.removeLast()
        if (operators.isEmpty()) return setOf(operator)
        return getResults(operators.subList(0, operators.size)).flatMap {
            listOf(it + operator, it * operator)
        }.toSet()
    }

    return equations.filter { (result, operators) ->
        getResults(operators.toMutableList()).any { result == it }
    }.sumOf { it.first }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ULong {
    val rePart = """(\d+): ([\d ]+)""".toRegex()
    val equations = lines
        .mapNotNull { rePart.matchEntire(it) }
        .map { match ->
            val (result, operators) = match.destructured
            result.toULong() to operators.split(" ").map(String::toULong)
        }

    fun getResults(operators: MutableList<ULong>): Set<ULong> {
        val operator = operators.removeLast()
        if (operators.isEmpty()) return setOf(operator)
        return getResults(operators.subList(0, operators.size)).flatMap {
            listOf(it + operator, it * operator, (it.toString() + operator.toString()).toULong())
        }.toSet()
    }

    return equations.filter { (result, operators) ->
        getResults(operators.toMutableList()).any { result == it }
    }.sumOf { it.first }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
