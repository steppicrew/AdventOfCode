package aoc_2015.aoc_2015_16

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 16

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (40 to 241)
)

fun run1(input: InputData): ResultType {
    val reAunt = """Sue (\d+): (.*)""".toRegex()
    val reProperty = """(\w+): (\d+)""".toRegex()
    val knownProperties = mapOf(
        "children" to 3,
        "cats" to 7,
        "samoyeds" to 2,
        "pomeranians" to 3,
        "akitas" to 0,
        "vizslas" to 0,
        "goldfish" to 5,
        "trees" to 3,
        "cars" to 2,
        "perfumes" to 1,
    )

    return input.lines
        .mapNotNull { reAunt.matchEntire(it) }
        .map { match ->
            val (number, propertiesList) = match.destructured
            val properties = propertiesList
                .split(", ")
                .mapNotNull { reProperty.matchEntire(it) }
                .associate { it.groupValues[1] to it.groupValues[2].toInt() }
            number.toInt() to properties
        }.first { aunt ->
            val properties = aunt.second
            properties.all { property ->
                property.value == knownProperties[property.key]
            }
        }.first
}

fun run2(input: InputData): ResultType {
    val reAunt = """Sue (\d+): (.*)""".toRegex()
    val reProperty = """(\w+): (\d+)""".toRegex()
    val knownProperties = mapOf<String, (Int) -> Boolean>(
        "children" to { it == 3 },
        "cats" to { it > 7 },
        "samoyeds" to { it == 2 },
        "pomeranians" to { it < 3 },
        "akitas" to { it == 0 },
        "vizslas" to { it == 0 },
        "goldfish" to { it < 5 },
        "trees" to { it > 3 },
        "cars" to { it == 2 },
        "perfumes" to { it == 1 },
    )

    return input.lines
        .mapNotNull { reAunt.matchEntire(it) }
        .map { match ->
            val (number, propertiesList) = match.destructured
            val properties = propertiesList
                .split(", ")
                .mapNotNull { reProperty.matchEntire(it) }
                .associate { it.groupValues[1] to it.groupValues[2].toInt() }
            number.toInt() to properties
        }.first { aunt ->
            val properties = aunt.second
            properties.all { property ->
                knownProperties[property.key]!!(property.value)
            }
        }.first
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
