package aoc_2024.aoc_2024_16

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 16

typealias ResultType = Int

typealias Pos = Pair<Int, Int>
typealias Dir = Pair<Int, Int>
typealias PosDir = Pair<Pos, Dir>

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (7036 to 45),
    2 to (11048 to 64),
    0 to (160624 to 692),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var endPosition: Pos = 0 to 0
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            when (c) {
                '#' -> return@mapIndexed null
                'S' ->
                    return@mapIndexed directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }

                'E' -> {
                    endPosition = col to row
                }
            }
            directions.map { ((col to row) to it) to Int.MAX_VALUE }
        }.filterNotNull().flatten()
    }.toMap().toMutableMap()

    while (true) {
        val lowestEntry = map.minByOrNull { it.value } ?: throw RuntimeException("Empty map")
        val (position, direction) = lowestEntry.key
        if (position == endPosition) {
            return lowestEntry.value
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.filter { it != oppositeDirection }
            .map {
                if (it == direction) {
                    return@map ((position.first + it.first to position.second + it.second) to it) to 1
                }
                (position to it) to 1000
            }
            .forEach {
                val oldValue = map[it.first] ?: return@forEach
                val newValue = lowestEntry.value + it.second
                if (newValue < oldValue) {
                    map[it.first] = newValue
                }
            }
        map.remove(lowestEntry.key)
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var endPosition: Pos = 0 to 0
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            when (c) {
                '#' -> return@mapIndexed null
                'S' ->
                    return@mapIndexed directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }

                'E' -> {
                    endPosition = col to row
                }
            }
            directions.map { ((col to row) to it) to Int.MAX_VALUE }
        }.filterNotNull().flatten()
    }.toMap().toMutableMap()

    val bestPrevious = mutableMapOf<PosDir, Set<PosDir>>()

    while (true) {
        val lowestEntry = map.minByOrNull { it.value } ?: throw RuntimeException("Empty map")
        val (position, direction) = lowestEntry.key
        if (position == endPosition) {
            break
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.filter { it != oppositeDirection }
            .map {
                if (it == direction) {
                    return@map ((position.first + it.first to position.second + it.second) to it) to 1
                }
                (position to it) to 1000
            }
            .forEach {
                val oldValue = map[it.first] ?: return@forEach
                val newValue = lowestEntry.value + it.second
                if (newValue < oldValue) {
                    map[it.first] = newValue
                    bestPrevious[it.first] = mutableSetOf(lowestEntry.key)
                } else if (newValue == oldValue) {
                    bestPrevious[it.first] = bestPrevious[it.first]!! + lowestEntry.key
                }
            }
        map.remove(lowestEntry.key)
    }

    fun findWay(posDir: PosDir): Set<Pos> {
        val previous = bestPrevious[posDir] ?: return setOf()
        return previous.fold(setOf()) { acc, position -> acc + posDir.first + findWay(position) }
    }

    return directions.sumOf { findWay(endPosition to it).size }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
