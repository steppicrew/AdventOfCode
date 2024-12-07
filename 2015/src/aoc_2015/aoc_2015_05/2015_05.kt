package aoc_2015.aoc_2015_05

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 5

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (2 to 0),
    0 to (255 to 55),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val vowels = setOf('a', 'e', 'i', 'u', 'o')
    val reForbidden = """ab|cd|pq|xy""".toRegex()
    val reTwice = """(\w)\1""".toRegex()
    return lines
        .count { line ->
            line.count {
                vowels.contains(it)
            } >= 3 &&
                    !reForbidden.containsMatchIn(line) &&
                    reTwice.containsMatchIn(line)
        }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reRepeat1 = """(\w\w).*\1""".toRegex()
    val reRepeat2 = """(\w).\1""".toRegex()

    return lines
        .count { line ->
            reRepeat1.containsMatchIn(line) && reRepeat2.containsMatchIn(line)
        }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
