package aoc_2015.aoc_2015_01

import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 1

val EXPECTED_RESULTS = listOf(
    1 to (-1 to 5),
    0 to (280 to 1797)
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    return lines.sumOf { line ->
        line.split("").count { it == "(" }
    } - lines.sumOf { line ->
        line.split("").count { it == ")" }
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    var floor = 0
    var index = 1
    for (line in lines) {
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
