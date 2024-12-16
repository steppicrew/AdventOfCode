package aoc_2024.aoc_2024_16

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO
import java.util.*

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
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val costMap = mutableMapOf<PosDir, Int>()
    val navigationQueue = PriorityQueue<PosDir> { pd1, pd2 -> costMap[pd1]!! - costMap[pd2]!! }
    var endPosition: Pos = 0 to 0
    costMap.putAll(lines.flatMapIndexed { row, line ->
        line.flatMapIndexed inner@{ col, c ->
            when (c) {
                '#' -> return@inner listOf()
                'S' -> {
                    navigationQueue.add((col to row) to (1 to 0))
                    return@inner directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }
                }

                'E' -> {
                    endPosition = col to row
                }
            }
            directions.map { ((col to row) to it) to Int.MAX_VALUE }
        }
    })

    while (navigationQueue.size > 0) {
        val (position, direction) = navigationQueue.remove()
        val value = costMap[position to direction]!!
        if (position == endPosition) {
            return value
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.filter { it != oppositeDirection }
            .map {
                if (it == direction) {
                    ((position.first + it.first to position.second + it.second) to it) to 1
                } else {
                    (position to it) to 1000
                }
            }
            .forEach {
                val oldValue = costMap[it.first] ?: return@forEach
                val newValue = value + it.second
                if (newValue < oldValue) {
                    costMap[it.first] = newValue
                    navigationQueue.add(it.first)
                }
            }
    }
    throw RuntimeException("Empty map")
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val costMap = mutableMapOf<PosDir, Int>()
    val navigationQueue = PriorityQueue<PosDir> { pd1, pd2 -> costMap[pd1]!! - costMap[pd2]!! }
    var endPosition: Pos = 0 to 0
    costMap.putAll(lines.flatMapIndexed { row, line ->
        line.flatMapIndexed inner@{ col, c ->
            when (c) {
                '#' -> return@inner listOf()
                'S' -> {
                    navigationQueue.add((col to row) to (1 to 0))
                    return@inner directions.map { ((col to row) to it) to if (it == 1 to 0) 0 else Int.MAX_VALUE }
                }

                'E' -> {
                    endPosition = col to row
                }
            }
            directions.map { ((col to row) to it) to Int.MAX_VALUE }
        }
    })

    val bestPrevious = mutableMapOf<PosDir, Set<PosDir>>()

    while (navigationQueue.size > 0) {
        val (position, direction) = navigationQueue.remove()
        val value = costMap[position to direction]!!
        if (position == endPosition) {
            break
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.filter { it != oppositeDirection }
            .map {
                if (it == direction) {
                    ((position.first + it.first to position.second + it.second) to it) to 1
                } else {
                    (position to it) to 1000
                }
            }
            .forEach {
                val oldValue = costMap[it.first] ?: return@forEach
                val newValue = value + it.second
                if (newValue > oldValue) return@forEach
                if (newValue < oldValue) {
                    costMap[it.first] = newValue
                    bestPrevious[it.first] = mutableSetOf(position to direction)
                } else {
                    bestPrevious[it.first] = bestPrevious[it.first]!! + (position to direction)
                }
                navigationQueue.add(it.first)
            }
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
