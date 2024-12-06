package aoc_2024.aoc_2024_00

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 0

// ref to (run1 to run2)
// values may by of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<Int> = listOf(
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
