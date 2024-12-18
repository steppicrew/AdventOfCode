package aoc_2024.aoc_2024_14

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 14

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (12 to 3),
    2 to (1 to 0),
    0 to (231852216 to 8159),
)


fun run1(input: InputData): ResultType {
    val reRobot = """p=(\d+),(\d+) v=(-?\d+),(-?\d+)""".toRegex()
    val robots = input.lines.mapNotNull { reRobot.matchEntire(it) }.map { match ->
        val (startPosX, startPosY, speedX, speedY) = match.destructured.toList().map(String::toInt)
        (startPosX to startPosY) to (speedX to speedY)
    }

    val size = if (input.ref > 0) 11 to 7 else 101 to 103

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

    return quadrants.values.reduce { prod, count -> prod * count }
}

fun run2(input: InputData): ResultType {
    val reRobot = """p=(\d+),(\d+) v=(-?\d+),(-?\d+)""".toRegex()
    val robots = input.lines.mapNotNull { reRobot.matchEntire(it) }.map { match ->
        val (startPosX, startPosY, speedX, speedY) = match.destructured.toList().map(String::toInt)
        (startPosX to startPosY) to (speedX to speedY)
    }

    if (input.ref == 2) return 0

    val size = if (input.ref > 0) 11 to 7 else 101 to 103

    val neighbours = sequenceOf(
        1 to 0, 1 to 1, 0 to 1, -1 to 1, -1 to 0, -1 to -1, 0 to -1, 1 to -1
    )

    generateSequence(1) { it + 1 }.forEach { time ->
        val endPositions = robots
            .map { (startPos, speed) ->
                (startPos.first + speed.first * time) % size.first to (startPos.second + speed.second * time) % size.second
            }
            .map { (if (it.first < 0) it.first + size.first else it.first) to (if (it.second < 0) it.second + size.second else it.second) }
            .toSet()

        val connected = endPositions.filter { position ->
            neighbours.count { endPositions.contains(it.first + position.first to it.second + position.second) } > 1
        }

        if (connected.size > input.lines.size / 2) {
            input.log("Time: $time")
            (0..<size.second).asSequence().forEach { line ->
                input.log((0..<size.first).joinToString("") { if (endPositions.contains(it to line)) "#" else " " })
            }
            return time
        }
    }

    return 0
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS, quiet = true)
}
