package aoc_2024.aoc_2024_06

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 6

val EXPECTED_RESULTS = listOf(
    1 to (null to null),
    0 to (null to null)
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
