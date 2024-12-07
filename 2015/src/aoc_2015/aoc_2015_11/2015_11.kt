package aoc_2015.aoc_2015_11

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 11

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (null to null)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    return lines.count()
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    return lines.count()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
