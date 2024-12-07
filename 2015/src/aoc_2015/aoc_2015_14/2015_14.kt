package aoc_2015.aoc_2015_14

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO
import kotlin.math.min

const val YEAR = 2015
const val DAY = 14

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (2660 to 1564),
    0 to (2640 to 1102)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reSpeed = """\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.""".toRegex()

    val timeTotal = 2503

    return lines
        .mapNotNull { reSpeed.matchEntire(it) }
        .maxOf { match ->
            val (distance, time1, time2) = match.destructured.toList().map(String::toInt)
            val fullCycles = timeTotal / (time1 + time2)
            val fullCyclesTime = fullCycles * (time1 + time2)
            val fullCyclesDistance = fullCycles * time1 * distance
            val timeRemaining = timeTotal - fullCyclesTime
            fullCyclesDistance + min(time1, timeRemaining) * distance
        }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reSpeed = """\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.""".toRegex()

    val timeTotal = 2503

    val speeds = lines
        .mapNotNull { reSpeed.matchEntire(it) }
        .map { match ->
            val (distance, time1, time2) = match.destructured.toList().map(String::toInt)
            (time1 to distance) to time2
        }

    fun getDistances(time: Int): List<Int> {
        return speeds.map { speed ->
            val (time1, distance) = speed.first
            val time2 = speed.second
            val fullCycles = time / (time1 + time2)
            val fullCyclesTime = fullCycles * (time1 + time2)
            val fullCyclesDistance = fullCycles * time1 * distance
            val timeRemaining = time - fullCyclesTime
            fullCyclesDistance + min(time1, timeRemaining) * distance
        }
    }

    fun getPoints(time: Int, oldPoints: List<Int>): List<Int> {
        val distances = getDistances(time)
        val maxDistance = distances.max()
        return distances.zip(oldPoints).map {
            if (it.first == maxDistance) it.second + 1 else it.second
        }
    }

    return (1..timeTotal).fold(speeds.map { 0 }) { points, time ->
        getPoints(time, points)
    }.max()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
