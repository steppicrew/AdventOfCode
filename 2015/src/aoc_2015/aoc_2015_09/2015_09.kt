package aoc_2015.aoc_2015_09

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 9

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (605 to 982),
    0 to (141 to 736)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reDistance = """(\w+) to (\w+) = (\d+)""".toRegex()
    val distances = lines
        .mapNotNull { reDistance.matchEntire(it) }
        .flatMap {
            val (location1, location2, distance) = it.destructured
            listOf(location1 to (location2 to distance.toInt()), location2 to (location1 to distance.toInt()))
        }.groupBy { it.first }.mapValues { it.value.map { it.second } }

    fun getDistances(nextStop: String, visited: Set<String>): Int {
        val nextStops = distances[nextStop] ?: throw RuntimeException("This should not happen")
        val nextDistances = nextStops.filter { !visited.contains(it.first) }
        if (nextDistances.isEmpty()) {
            return 0
        }
        val newVisited = visited.plus(nextStop)
        return nextDistances.minOf { getDistances(it.first, newVisited) + it.second }
    }

    return distances.keys.minOf { getDistances(it, setOf(it)) }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reDistance = """(\w+) to (\w+) = (\d+)""".toRegex()
    val distances = lines
        .mapNotNull { reDistance.matchEntire(it) }
        .flatMap {
            val (location1, location2, distance) = it.destructured
            listOf(location1 to (location2 to distance.toInt()), location2 to (location1 to distance.toInt()))
        }.groupBy { it.first }.mapValues { it.value.map { it.second } }

    fun getDistances(nextStop: String, visited: Set<String>): Int {
        val nextStops = distances[nextStop] ?: throw RuntimeException("This should not happen")
        val nextDistances = nextStops.filter { !visited.contains(it.first) }
        if (nextDistances.isEmpty()) {
            return 0
        }
        val newVisited = visited.plus(nextStop)
        return nextDistances.maxOf { getDistances(it.first, newVisited) + it.second }
    }

    return distances.keys.maxOf { getDistances(it, setOf(it)) }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
