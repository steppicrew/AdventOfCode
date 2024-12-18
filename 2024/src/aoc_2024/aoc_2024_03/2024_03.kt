package aoc_2024.aoc_2024_03

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 3

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (161 to 161),
    2 to (161 to 48),
    0 to (160672468 to 84893551)
)

fun run1(input: InputData): ResultType {
    val re = """mul\((\d+),(\d+)\)""".toRegex()

    return input.lines.joinToString("")
        .let { re.findAll(it) }
        .sumOf { match ->
            val (factor1, factor2) = match.destructured
            factor1.toInt() * factor2.toInt()
        }
}

fun run2(input: InputData): ResultType {
    val reDo = """do\(\)""".toRegex()
    val reDoNot = """don't\(\)""".toRegex()
    val reMul = """mul\((\d+),(\d+)\)""".toRegex()

    return input.lines.joinToString("")
        .split(reDo)
        .sumOf { doPart ->
            doPart.split(reDoNot, limit = 2).first()
                .let { reMul.findAll(it) }
                .sumOf { match ->
                    val (factor1, factor2) = match.destructured
                    factor1.toInt() * factor2.toInt()
                }
        }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
