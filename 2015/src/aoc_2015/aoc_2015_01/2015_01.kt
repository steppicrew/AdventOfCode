package aoc_2015.aoc_2015_01

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 1

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (-1 to 5),
    0 to (280 to 1797)
)


fun run1(input: InputData): ResultType {
    return input.lines.sumOf { line ->
        line.split("").count { it == "(" }
    } - input.lines.sumOf { line ->
        line.split("").count { it == ")" }
    }
}

fun run2(input: InputData): ResultType {
    var floor = 0
    var index = 1
    for (line in input.lines) {
        for (char in line) {
            if (char == '(') {
                floor++
            } else if (char == ')') {
                floor--
            }
            if (floor == -1) return index
            index++
        }
    }
    return 0
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
