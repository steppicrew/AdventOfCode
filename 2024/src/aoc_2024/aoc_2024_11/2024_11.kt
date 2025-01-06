package aoc_2024.aoc_2024_11

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 11

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (55312L to 65601038650482L),
    0 to (224529L to 266820198587914L),
)


fun run1(input: InputData): ResultType {
    val numbers = input.lines.single().split(" ")

    fun blink(number: String, i: Int): Long {
        if (i == 0) {
            return 1L
        }
        val nextI = i - 1
        return when {
            number == "0" -> blink("1", nextI)
            number.length.and(1) == 0 -> {
                val l2 = number.length / 2
                blink(number.dropLast(l2), nextI) + blink(number.drop(l2).toLong().toString(), nextI)
            }

            else -> blink((number.toLong() * 2024).toString(), nextI)
        }
    }

    return numbers.sumOf { blink(it, 25) }
}

fun run2(input: InputData): ResultType {
    val numbers = input.lines.single().split(" ")

    val cache = mutableMapOf<Pair<String, Int>, Long>()
    fun blink(number: String, i: Int): Long {
        return cache.getOrPut(number to i, {
            if (i == 0) {
                return@getOrPut 1L
            }
            val nextI = i - 1
            when {
                number == "0" -> blink("1", nextI)
                number.length.and(1) == 0 -> {
                    val l2 = number.length / 2
                    blink(number.dropLast(l2), nextI) + blink(number.drop(l2).toLong().toString(), nextI)
                }

                else -> blink((number.toLong() * 2024).toString(), nextI)
            }
        })
    }

    return numbers.sumOf { blink(it, 75) }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
