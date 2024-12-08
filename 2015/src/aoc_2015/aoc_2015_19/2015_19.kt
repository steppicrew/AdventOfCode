package aoc_2015.aoc_2015_19

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 19

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (4 to null),
    2 to (7 to null),
    // 0 to (535 to null)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reReplacement = """(\w+) => (\w+)""".toRegex()
    val reInput = """\w+""".toRegex()

    val replacements = lines
        .mapNotNull { reReplacement.matchEntire(it) }
        .map { match ->
            val (from, to) = match.destructured
            from to to
        }

    val input = lines.first { reInput.matches(it) }

    return replacements.flatMap { (from, to) ->
        from.toRegex().findAll(input).map { match ->
            val range = match.range
            "${input.substring(0, range.first)}${to}${input.substring(range.last + 1)}"
        }
    }.toSet().size
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    return lines.size
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
