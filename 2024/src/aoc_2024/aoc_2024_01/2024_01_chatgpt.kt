package aoc_2024.aoc_2024_01a

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO
import kotlin.math.abs

const val YEAR = 2024
const val DAY = 1

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (11 to 31),
    0 to (1889772 to 23228917)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    // Parse input and split into left and right lists
    val (left, right) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip()

    // Sort both lists and compute the result
    val result = left.sorted().zip(right.sorted())
        .sumOf { (l, r) -> abs(l - r) }

    return result
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    // Parse input and build left list and right frequency map
    val (left, rightFrequency) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip().let { (left, right) ->
        left to right.groupingBy { it }.eachCount()
    }

    // Compute the result
    val result = left.sumOf { n -> rightFrequency.getOrDefault(n, 0) * n }

    return result
}

fun main() {
    simpleIO(
        YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS
    )
}
