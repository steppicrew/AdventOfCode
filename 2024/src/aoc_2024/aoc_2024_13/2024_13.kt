package aoc_2024.aoc_2024_13

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 13

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (480L to 875318608908L),
    0 to (37128L to 74914228471331L),
)

typealias Pos = Pair<Long, Long>

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val aTokens = 3
    val bTokens = 1

    val reButtonA = """Button A: X\+(\d+), Y\+(\d+)""".toRegex()
    val reButtonB = """Button B: X\+(\d+), Y\+(\d+)""".toRegex()
    val rePrize = """Prize: X=(\d+), Y=(\d+)""".toRegex()

    fun find(a: Pos, b: Pos, result: Pos): Long? {
        val factorA = (result.first * b.second - result.second * b.first) / (a.first * b.second - a.second * b.first)
        val factorB = (result.first - factorA * a.first) / b.first
        return if (result.first == factorA * a.first + factorB * b.first && result.second == factorA * a.second + factorB * b.second) {
            factorA * aTokens + factorB * bTokens
        } else {
            null
        }
    }

    return lines.chunked(4).sumOf { chunk ->
        val aMatch = reButtonA.matchEntire(chunk.first())
        val bMatch = reButtonB.matchEntire(chunk[1])
        val prizeMatch = rePrize.matchEntire(chunk[2])
        if (aMatch == null || bMatch == null || prizeMatch == null) {
            0
        } else {
            val (buttonAX, buttonAY) = aMatch.destructured
            val (buttonBX, buttonBY) = bMatch.destructured
            val (prizeX, prizeY) = prizeMatch.destructured

            find(
                buttonAX.toLong() to buttonAY.toLong(),
                buttonBX.toLong() to buttonBY.toLong(),
                prizeX.toLong() to prizeY.toLong()
            ) ?: 0
        }
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val aTokens = 3
    val bTokens = 1

    val reButtonA = """Button A: X\+(\d+), Y\+(\d+)""".toRegex()
    val reButtonB = """Button B: X\+(\d+), Y\+(\d+)""".toRegex()
    val rePrize = """Prize: X=(\d+), Y=(\d+)""".toRegex()

    fun find(a: Pos, b: Pos, result: Pos): Long? {
        val factorA = (result.first * b.second - result.second * b.first) / (a.first * b.second - a.second * b.first)
        val factorB = (result.first - factorA * a.first) / b.first
        return if (result.first == factorA * a.first + factorB * b.first && result.second == factorA * a.second + factorB * b.second) {
            factorA * aTokens + factorB * bTokens
        } else {
            null
        }
    }

    return lines.chunked(4).sumOf { chunk ->
        val aMatch = reButtonA.matchEntire(chunk.first())
        val bMatch = reButtonB.matchEntire(chunk[1])
        val prizeMatch = rePrize.matchEntire(chunk[2])
        if (aMatch == null || bMatch == null || prizeMatch == null) {
            0
        } else {
            val (buttonAX, buttonAY) = aMatch.destructured
            val (buttonBX, buttonBY) = bMatch.destructured
            val (prizeX, prizeY) = prizeMatch.destructured

            find(
                buttonAX.toLong() to buttonAY.toLong(),
                buttonBX.toLong() to buttonBY.toLong(),
                (10000000000000L + prizeX.toInt()) to (10000000000000L + prizeY.toInt())
            ) ?: 0
        }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
