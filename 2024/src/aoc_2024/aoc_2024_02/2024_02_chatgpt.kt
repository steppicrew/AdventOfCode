package aoc_2024.aoc_2024_02_chatgpt

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 2

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (2 to 4),
    0 to (502 to 544)
)

fun run1(input: InputData): ResultType {

    fun isSafe(parts: List<Int>): Boolean =
        parts.zipWithNext { a, b -> b > a && b <= a + 3 }.all { it }

    val result = input.lines.count { line ->
        val parts = line.split("\\s+".toRegex()).map(String::toInt)
        isSafe(parts) || isSafe(parts.reversed())
    }

    return result
}

fun run2(input: InputData): ResultType {

    fun glitchCount(parts: List<Int>): Int =
        parts.zipWithNext { a, b -> b > a && b <= a + 3 }.count { !it }

    fun List<Int>.variantsWithoutOne(): Sequence<List<Int>> =
        indices.asSequence().map { i -> this.filterIndexed { index, _ -> index != i } }

    fun isSafe(parts: List<Int>): Boolean {
        val initialGlitches = glitchCount(parts)
        if (initialGlitches == 0) return true
        if (initialGlitches > 2) return false
        return parts.variantsWithoutOne().any { glitchCount(it) == 0 }
    }

    val result = input.lines.count { line ->
        val parts = line.split("\\s+".toRegex()).map(String::toInt)
        isSafe(parts) || isSafe(parts.reversed())
    }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
