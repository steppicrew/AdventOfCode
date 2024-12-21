package aoc_2024.aoc_2024_20

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import java.util.*
import kotlin.math.min

const val YEAR = 2024
const val DAY = 20

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (44 to 285),
    // 2 to (6 to null),
    0 to (1378 to 975379),
)


fun run1(input: InputData): ResultType {
    var startPosition = 0 to 0
    var endPosition = 0 to 0
    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                '#' -> return@mapIndexedNotNull null
                'S' -> startPosition = col to row
                'E' -> endPosition = col to row
            }
            col to row
        }
    }.toSet()
    val walls = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                '#' -> col to row
                else -> null
            }
        }
    }.toSet()

    val directions = sequenceOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    fun getGlobalCosts(origin: Pair<Int, Int>): Map<Pair<Int, Int>, Int> {
        val costs = map.associateWith { Int.MAX_VALUE }.toMutableMap()
        val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> costs[p1]!! - costs[p2]!! }
        queue.add(origin)
        costs[origin] = 0
        while (queue.size > 0) {
            val position = queue.remove()
            val newCost = costs[position]!! + 1
            directions.map { position.first + it.first to position.second + it.second }
                .filter { map.contains(it) }
                .forEach {
                    val oldCost = costs[it]!!
                    if (newCost < oldCost) {
                        queue.add(it)
                        costs[it] = newCost
                    }
                }
        }
        return costs
    }

    val globalCostsToEnd = getGlobalCosts(endPosition)
    val globalCostsFromStart = getGlobalCosts(startPosition)

    val time0 = globalCostsToEnd[startPosition]!!
    val minSaving = if (input.ref > 0) 1 else 100

    fun getNeighbours(position: Pair<Int, Int>): Sequence<Pair<Int, Int>> {
        return directions.map { it.first + position.first to it.second + position.second }
    }

    fun pair(positions: Sequence<Pair<Int, Int>>): Sequence<Pair<Pair<Int, Int>, Pair<Int, Int>>> = sequence {
        positions.forEachIndexed { index, p1 ->
            positions.drop(index + 1).forEach {
                yield(p1 to it)
            }
        }
    }


    return walls.sumOf { wall ->
        pair(
            getNeighbours(wall).filter {
                map.contains(it)
            }
        )
            .map {
                min(
                    globalCostsToEnd[it.first]!! + globalCostsFromStart[it.second]!!,
                    globalCostsFromStart[it.first]!! + globalCostsToEnd[it.second]!!
                ) + 2
            }
            .count { it <= time0 - minSaving }
    }
}

fun run2(input: InputData): ResultType {
    val map = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                '#' -> null
                else -> col to row
            }
        }
    }.toSet()
    val startPosition = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                'S' -> col to row
                else -> null
            }
        }
    }.first()
    val endPosition = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                'E' -> col to row
                else -> null
            }
        }
    }.first()
    val walls = input.lines.flatMapIndexed { row, line ->
        line.mapIndexedNotNull { col, c ->
            when (c) {
                '#' -> col to row
                else -> null
            }
        }
    }.toSet()

    val directions = listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    // get the time to reach every point from a start position
    fun getGlobalTimes(origin: Pair<Int, Int>): Pair<Map<Pair<Int, Int>, Int>, Map<Pair<Int, Int>, Pair<Int, Int>>> {
        val times = map.associateWith { Int.MAX_VALUE }.toMutableMap()
        val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> times[p1]!! - times[p2]!! }
        val ways = mutableMapOf<Pair<Int, Int>, Pair<Int, Int>>()
        queue.add(origin)
        times[origin] = 0
        while (queue.isNotEmpty()) {
            val position = queue.remove()
            val newTime = times[position]!! + 1
            directions.map { position.first + it.first to position.second + it.second }
                .filter { map.contains(it) }
                .forEach {
                    val oldBestTime = times[it]!!
                    if (newTime < oldBestTime) {
                        queue.add(it)
                        times[it] = newTime
                        ways[it] = position
                    }
                }
        }
        return times to ways
    }

    val (globalTimesToEnd, wayToEnd) = getGlobalTimes(endPosition)
    val (globalTimesFromStart, _) = getGlobalTimes(startPosition)

    val time0 = globalTimesToEnd[startPosition]!!
    val maxWallTime = 20
    val minSaving = when (input.ref) {
        1 -> 50
        2 -> 1
        else -> 100
    }
    val maxTime = time0 - minSaving

    fun getNeighbours(position: Pair<Int, Int>): List<Pair<Int, Int>> {
        return directions.map { it.first + position.first to it.second + position.second }
    }

    /**
     * Starts from the current position to all possible end points
     * Yields every position on path with low enough time til the end
     */
    fun getWallTunnels(wallStart: Pair<Int, Int>, maxTimeLeft: Int): Sequence<Pair<Pair<Int, Int>, Int>> = sequence {
        val times = mutableMapOf<Pair<Int, Int>, Int>()
        val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> times[p1]!! - times[p2]!! }
        times[wallStart] = 1
        queue.add(wallStart)

        while (queue.isNotEmpty()) {
            val wallEnd = queue.remove()
            val time = times[wallEnd]!!

            val timeToEnd = globalTimesToEnd[wallEnd]
            if (timeToEnd != null && time + timeToEnd <= maxTimeLeft) {
                yield(wallEnd to timeToEnd + time)
            }

            if (time < maxWallTime) {
                val newTime = time + 1
                getNeighbours(wallEnd)
                    .filter { (walls.contains(it) || map.contains(it)) && !times.containsKey(it) }
                    .forEach {
                        times[it] = newTime
                        queue.add(it)
                    }
            }
        }
    }

    var position: Pair<Int, Int>? = startPosition
    val cheats = mutableMapOf<Pair<Pair<Int, Int>, Pair<Int, Int>>, Int>()
    while (position != null) {
        val timeFromStart = globalTimesFromStart[position]!!
        if (timeFromStart > maxTime) break
        getNeighbours(position).filter { walls.contains(it) || map.contains(it) }.forEach { wall ->
            getWallTunnels(wall, maxTime - timeFromStart).forEach { (endPosition, timeLeft) ->
                val key = position!! to endPosition
                val timeSaving = time0 - (timeFromStart + timeLeft)
                if (timeSaving > (cheats[key] ?: 0)) {
                    cheats[key] = timeSaving
                }
            }
        }
        position = wayToEnd[position]
    }

    // println("time0: $time0")
    // println(cheats.values.groupingBy { it }.eachCount())

    return cheats.values.size
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
