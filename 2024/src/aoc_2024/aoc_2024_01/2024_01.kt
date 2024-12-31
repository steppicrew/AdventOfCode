package aoc_2024.aoc_2024_01

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import kotlin.math.abs

const val YEAR = 2024
const val DAY = 1

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (11 to 31),
    0 to (1889772 to 23228917)
)


fun run1(input: InputData): ResultType {
    val reSpace = """\s+""".toRegex()

    return input.lines
        .map { line ->
            line.split(reSpace)
                .let { it.first().toInt() to it.last().toInt() }
        }.unzip()
        .let { it.first.sorted().zip(it.second.sorted()) }
        .sumOf { abs(it.first - it.second) }
}

fun run2(input: InputData): ResultType {
    val reSpace = """\s+""".toRegex()

    return input.lines
        .map { line ->
            line.split(reSpace)
                .let { it.first().toInt() to it.last().toInt() }
        }.unzip()
        .let { (left, right) -> left to right.groupingBy { it }.eachCount() }
        .let { (left, rightCount) -> left.sumOf { it * (rightCount[it] ?: 0) } }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
