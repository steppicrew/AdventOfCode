package aoc_2015.aoc_2015_11

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 11

typealias ResultType = String

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to ("abcdffaa" to "abcdffbb"),
    2 to ("ghjaabcc" to "ghjbbcdd"),
    0 to ("hxbxxyzz" to "hxcaabcc")
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val forbidden = mapOf('i' to 'j', 'o' to 'p', 'l' to 'm')
    val reDouble = """(\w)\1.*(\w)\2""".toRegex()

    val reSequence = ('a'..'x').joinToString(separator = "|") { "${it}${it.inc()}${it.inc().inc()}" }.toRegex()

    fun inc(value: String): String {
        val digit = value.last()
        if (digit < 'z') {
            val nextDigit = digit.inc()
            return "${value.dropLast(1)}${forbidden[nextDigit] ?: nextDigit}"
        }
        return "${inc(value.dropLast(1))}a"
    }

    var line =
        lines.first().replace("""([iol])(.*)""".toRegex()) { match ->
            "${forbidden[match.groupValues[1].first()]}${"a".repeat(match.groupValues[2].length)}"
        }

    while (true) {
        line = inc(line)
        if (reDouble.containsMatchIn(line) && reSequence.containsMatchIn(line)) {
            break
        }
    }

    return line
}

fun run2(lines: List<String>, log: (String) -> Unit): ResultType {
    return run1(listOf(run1(lines, log)), log)
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
