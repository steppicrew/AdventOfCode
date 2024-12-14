package aoc_2024.aoc_2024_14

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 14

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    // 2 to (null to null),
    1 to (12 to null),
    0 to (231852216 to 8159),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reRobot = """p=(\d+),(\d+) v=(-?\d+),(-?\d+)""".toRegex()
    val robots = lines.mapNotNull { reRobot.matchEntire(it) }.map { match ->
        val (startPosX, startPosY, speedX, speedY) = match.destructured.toList().map(String::toInt)
        (startPosX to startPosY) to (speedX to speedY)
    }

    // val size = 11 to 7
    val size = 101 to 103

    val time = 100

    val endPositions = robots
        .map { (startPos, speed) ->
            (startPos.first + speed.first * time) % size.first to (startPos.second + speed.second * time) % size.second
        }
        .map { (if (it.first < 0) it.first + size.first else it.first) to (if (it.second < 0) it.second + size.second else it.second) }
        .groupingBy { it }.eachCount().filterValues { it > 0 }

    val quadrantBorder = (size.first) / 2 to (size.second) / 2

    val quadrants = endPositions
        .filter { (position, _) -> position.first != quadrantBorder.first && position.second != quadrantBorder.second }
        .map { (position, count) ->
            ((if (position.first < quadrantBorder.first) 0 else 1) to (if (position.second < quadrantBorder.second) 0 else 1)) to count
        }.groupBy({ it.first }, { it.second }).mapValues { it.value.sum() }

    println("$quadrantBorder -> $quadrants")

    return quadrants.values.reduce { prod, count -> prod * count }
}

fun run2(lines: List<String>, log: (String) -> Unit): ResultType {
    val reRobot = """p=(\d+),(\d+) v=(-?\d+),(-?\d+)""".toRegex()
    val robots = lines.mapNotNull { reRobot.matchEntire(it) }.map { match ->
        val (startPosX, startPosY, speedX, speedY) = match.destructured.toList().map(String::toInt)
        (startPosX to startPosY) to (speedX to speedY)
    }

    // val size = 11 to 7
    val size = 101 to 103

    val neighbours = sequenceOf(
        1 to 0, 1 to 1, 0 to 1, -1 to 1, -1 to 0, -1 to -1, 0 to -1, 1 to -1
    )

    (1..100000).asSequence().forEach { time ->
        val endPositions = robots
            .map { (startPos, speed) ->
                (startPos.first + speed.first * time) % size.first to (startPos.second + speed.second * time) % size.second
            }
            .map { (if (it.first < 0) it.first + size.first else it.first) to (if (it.second < 0) it.second + size.second else it.second) }
            .toSet()

        val connected = endPositions.filter { position ->
            neighbours.any { endPositions.contains(it.first + position.first to it.second + position.second) }
        }

        if (connected.size > lines.size / 2) {
            log("Time: $time")
            (0..<size.second).asSequence().forEach { line ->
                log((0..<size.first).joinToString("") { if (endPositions.contains(it to line)) "#" else " " })
            }
        }
    }

    return 0
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
