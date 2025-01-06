package aoc_2024.aoc_2024_16

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import java.util.*

const val YEAR = 2024
const val DAY = 16

typealias ResultType = Int

typealias Position = Pair<Int, Int>
typealias Direction = Pair<Int, Int>
typealias PositionDirection = Pair<Position, Direction>

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (7036 to 45),
    2 to (11048 to 64),
    0 to (160624 to 692),
)


fun run1(input: InputData): ResultType {
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val costMap = mutableMapOf<PositionDirection, Int>()
    val navigationQueue = PriorityQueue<PositionDirection> { pd1, pd2 -> costMap[pd1]!! - costMap[pd2]!! }
    var endPosition: Position = 0 to 0
    costMap.putAll(input.lines.flatMapIndexed { row, line ->
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

    while (navigationQueue.isNotEmpty()) {
        val positionDirection = navigationQueue.remove()
        val (position, direction) = positionDirection
        val cost = costMap[positionDirection] ?: throw RuntimeException("Missing positionDirection $positionDirection")
        if (position == endPosition) {
            return cost
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.forEach {
            if (it == oppositeDirection) return@forEach
            val (newPositionDirection, newCost) = if (it == direction) {
                ((position.first + it.first to position.second + it.second) to it) to 1
            } else {
                (position to it) to 1000
            }
            val oldBestCost = costMap[newPositionDirection] ?: return@forEach
            val newBestCost = cost + newCost
            if (newBestCost < oldBestCost) {
                costMap[newPositionDirection] = newBestCost
                navigationQueue.add(newPositionDirection)
            }
        }
    }
    throw RuntimeException("Empty queue")
}

fun run2(input: InputData): ResultType {
    val directions = listOf(-1 to 0, 0 to -1, 1 to 0, 0 to 1)
    val costMap = mutableMapOf<PositionDirection, Int>()
    val navigationQueue = PriorityQueue<PositionDirection> { pd1, pd2 -> costMap[pd1]!! - costMap[pd2]!! }
    var endPosition: Position = 0 to 0
    costMap.putAll(input.lines.flatMapIndexed { row, line ->
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

    val bestPrevious = mutableMapOf<PositionDirection, Set<PositionDirection>>()

    while (navigationQueue.isNotEmpty()) {
        val positionDirection = navigationQueue.remove()
        val (position, direction) = positionDirection
        val cost = costMap[positionDirection] ?: throw RuntimeException("Missing positionDirection $positionDirection")
        if (position == endPosition) {
            break
        }
        val oppositeDirection = -direction.first to -direction.second
        directions.forEach {
            if (it == oppositeDirection) return@forEach
            val (newPositionDirection, newCost) = if (it == direction) {
                ((position.first + it.first to position.second + it.second) to it) to 1
            } else {
                (position to it) to 1000
            }
            val oldBestCost = costMap[newPositionDirection] ?: return@forEach
            val newBestCost = cost + newCost
            if (newBestCost > oldBestCost) return@forEach
            if (newBestCost < oldBestCost) {
                costMap[newPositionDirection] = newBestCost
                bestPrevious[newPositionDirection] = setOf(positionDirection)
            } else {
                bestPrevious[newPositionDirection] = bestPrevious[newPositionDirection]!! + positionDirection
            }
            navigationQueue.add(newPositionDirection)
        }
    }

    fun findWays(positionDirection: PositionDirection): Set<Position> {
        val previous = bestPrevious[positionDirection] ?: return setOf()
        return previous.fold(setOf()) { acc, position -> acc + positionDirection.first + findWays(position) }
    }

    return directions.fold(setOf<Position>()) { acc, direction -> acc + findWays(endPosition to direction) }.size
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
