package aoc_2015.aoc_2015_12

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 12

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (0 to 0),
    0 to (191164 to 87842)
)

fun run1(input: InputData): ResultType {
    val reNumber = """-?\d+""".toRegex()

    return reNumber.findAll(input.lines.first()).sumOf { it.value.toInt() }
}

fun run2(input: InputData): ResultType {
    val reNumber = """-?\d+""".toRegex()

    val reObject = """\{([^{}]+)}""".toRegex()
    val reRed = """:"red"""".toRegex()

    fun replace(value: String): String {
        return value.replace(reObject) { match ->
            if (reRed.containsMatchIn(match.value)) {
                ""
            } else {
                "(${match.groupValues[1]})"
            }
        }
    }

    var line = input.lines.first()
    while (true) {
        val nextLine = replace(line)
        if (line == nextLine) {
            break
        }
        line = nextLine
    }

    return reNumber.findAll(line).sumOf { it.value.toInt() }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
