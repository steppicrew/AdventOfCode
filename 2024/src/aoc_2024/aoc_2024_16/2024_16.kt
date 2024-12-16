package aoc_2024.aoc_2024_16

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 16

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (7036 to 45),
    2 to (11048 to 64),
    0 to (160624 to 692),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var endPosition: Pair<Int, Int> = 0 to 0
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            when (c) {
                '.' -> directions.map { ((col to row) to it) to Int.MAX_VALUE }
                'S' -> {
                    directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }
                }

                'E' -> {
                    endPosition = col to row
                    directions.map { ((col to row) to it) to Int.MAX_VALUE }
                }

                else -> null
            }
        }.filterNotNull().flatten()
    }.toMap().toMutableMap()

    while (true) {
        val lowestEntry = map.minByOrNull { it.value } ?: return 0
        val (position, direction) = lowestEntry.key
        if (position == endPosition) {
            return lowestEntry.value
        }
        directions.filter { it != -it.first to -it.second }
            .map {
                if (it == direction) {
                    ((position.first + it.first to position.second + it.second) to it) to 1
                } else {
                    (position to it) to 1000
                }
            }.filter { map.contains(it.first) }
            .forEach {
                val oldValue = map[it.first]!!
                val newValue = lowestEntry.value + it.second
                if (newValue < oldValue) {
                    map[it.first] = newValue
                }
            }
        map.remove(lowestEntry.key)
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var endPosition: Pair<Int, Int> = 0 to 0
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            when (c) {
                '.' -> directions.map { ((col to row) to it) to Int.MAX_VALUE }
                'S' ->
                    directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }

                'E' -> {
                    endPosition = col to row
                    directions.map { ((col to row) to it) to Int.MAX_VALUE }
                }

                else -> null
            }
        }.filterNotNull().flatten()
    }.toMap().toMutableMap()

    val bestPrevious =
        mutableMapOf<Pair<Pair<Int, Int>, Pair<Int, Int>>, MutableSet<Pair<Pair<Int, Int>, Pair<Int, Int>>>>()

    while (true) {
        val lowestEntry = map.minByOrNull { it.value } ?: return 0
        val (position, direction) = lowestEntry.key
        if (position == endPosition) {
            break
        }
        directions.filter { it != -it.first to -it.second }
            .map {
                if (it == direction) {
                    ((position.first + it.first to position.second + it.second) to it) to 1
                } else {
                    (position to it) to 1000
                }
            }.filter { map.contains(it.first) }
            .forEach {
                val oldValue = map[it.first]!!
                val newValue = lowestEntry.value + it.second
                if (newValue < oldValue) {
                    map[it.first] = newValue
                    bestPrevious[it.first] = mutableSetOf(lowestEntry.key)
                } else if (newValue == oldValue) {
                    bestPrevious[it.first]!!.add(lowestEntry.key)
                }
            }
        map.remove(lowestEntry.key)
    }

    fun findWay(pos: Pair<Pair<Int, Int>, Pair<Int, Int>>): Set<Pair<Int, Int>> {
        val previous = bestPrevious[pos] ?: return setOf()
        return previous.fold(setOf()) { acc, position -> acc + pos.first + findWay(position) }
    }

    return directions.sumOf { findWay(endPosition to it).size }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
