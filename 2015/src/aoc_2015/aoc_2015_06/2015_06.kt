package aoc_2015.aoc_2015_06

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO
import kotlin.math.max

const val YEAR = 2015
const val DAY = 6

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (377891 to 14110788)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = mutableSetOf<Pair<Int, Int>>()

    val reLine = """(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)""".toRegex()

    fun turnOn(xy: Pair<Int, Int>) {
        map.add(xy)
    }

    fun turnOff(xy: Pair<Int, Int>) {
        map.remove(xy)
    }

    fun toggle(xy: Pair<Int, Int>) {
        if (!map.add(xy)) {
            map.remove(xy)
        }
    }

    lines.asSequence()
        .mapNotNull { reLine.matchEntire(it) }
        .forEach { match ->
            val (command, fromX, fromY, toX, toY) = match.destructured
            val fn = when (command) {
                "turn on" -> ::turnOn
                "turn off" -> ::turnOff
                "toggle" -> ::toggle
                else -> throw RuntimeException("This should not happen")
            }
            (fromX.toInt()..toX.toInt()).asSequence().forEach { x ->
                (fromY.toInt()..toY.toInt()).asSequence().forEach { y -> fn(x to y) }
            }
        }
    return map.size
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = mutableMapOf<Pair<Int, Int>, Int>()

    val reLine = """(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)""".toRegex()

    fun turnOn(xy: Pair<Int, Int>) {
        map.compute(xy) { key, oldValue -> (oldValue ?: 0) + 1 }
    }

    fun turnOff(xy: Pair<Int, Int>) {
        map.computeIfPresent(xy) { key, oldValue -> max(oldValue - 1, 0) }
    }

    fun toggle(xy: Pair<Int, Int>) {
        map.compute(xy) { key, oldValue -> (oldValue ?: 0) + 2 }
    }

    lines.asSequence()
        .mapNotNull { reLine.matchEntire(it) }
        .forEach { match ->
            val (command, fromX, fromY, toX, toY) = match.destructured

            val fn = when (command) {
                "turn on" -> ::turnOn
                "turn off" -> ::turnOff
                "toggle" -> ::toggle
                else -> throw RuntimeException("This should not happen")
            }
            (fromX.toInt()..toX.toInt()).asSequence().forEach { x ->
                (fromY.toInt()..toY.toInt()).asSequence().forEach { y -> fn(x to y) }
            }
        }
    return map.values.sum()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
