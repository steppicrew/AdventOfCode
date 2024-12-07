package aoc_2015.aoc_2015_08

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 8

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (12 to 19),
    0 to (1333 to 2046)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reReplace = """\\x[0-9a-f]{2}|\\\\|\\"""".toRegex()
    return lines.sumOf { line ->
        line.length - line.replace(reReplace, " ").length + 2
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reReplace = """[\\"]""".toRegex()
    return lines.sumOf { line ->
        line.replace(reReplace, "  ").length + 2 - line.length
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
