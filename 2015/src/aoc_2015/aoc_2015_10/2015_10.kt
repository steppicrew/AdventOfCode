package aoc_2015.aoc_2015_10

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 10

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (237746 to 3369156),
    0 to (329356 to 4666278)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reFind = """(\d)\1*""".toRegex()
    return (0..<40).fold(lines[0]) { acc, _ ->
        reFind.findAll(acc).joinToString(separator = "") {
            "${it.value.length}${it.value[0]}"
        }
    }.length
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reFind = """(\d)\1*""".toRegex()
    return (0..<50).fold(lines[0]) { acc, _ ->
        reFind.findAll(acc).joinToString(separator = "") {
            "${it.value.length}${it.value[0]}"
        }
    }.length
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
