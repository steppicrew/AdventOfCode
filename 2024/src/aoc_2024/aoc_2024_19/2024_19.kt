package aoc_2024.aoc_2024_19

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 19

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (6L to 16L),
    0 to (340L to 717561822679428L),
)


fun run1(input: InputData): ResultType {
    val patterns = input.lines.first().split(", ").toSet()
    val wantedPatterns = input.lines.drop(2)

    fun findPattern(wanted: String): Boolean {
        if (wanted.isEmpty()) return true
        return patterns.filter { wanted.startsWith(it) }.any { findPattern(wanted.drop(it.length)) }
    }
    return wantedPatterns.count { findPattern(it) }.toLong()
}

fun run2(input: InputData): ResultType {
    val patterns = input.lines.first().split(", ").toSet()
    val wantedPatterns = input.lines.drop(2)

    val cache = mutableMapOf<String, Long>()
    fun findPattern(wanted: String): Long {
        return cache.getOrPut(wanted) {
            if (wanted.isEmpty()) {
                1L
            } else {
                patterns.filter { wanted.startsWith(it) }.sumOf { findPattern(wanted.drop(it.length)) }
            }
        }
    }
    return wantedPatterns.sumOf { findPattern(it) }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
