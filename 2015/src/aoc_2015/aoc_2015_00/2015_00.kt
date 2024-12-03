package aoc_2015.aoc_2015_00

import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 0

val EXPECTED_RESULTS = listOf(
    0 to (0 to 0)
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    return lines.count()
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    return lines.count()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
