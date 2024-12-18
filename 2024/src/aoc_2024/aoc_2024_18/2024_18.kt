package aoc_2024.aoc_2024_18

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import java.util.*

const val YEAR = 2024
const val DAY = 18

typealias ResultType = String

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to ("22" to "6,1"),
    0 to ("280" to "28,56"),
)


fun run1(input: InputData): ResultType {
    val bytes = input.lines.map { line ->
        val (x, y) = line.split(",").map(String::toInt)
        x to y
    }

    val (maxX, maxY) = if (input.ref > 0) 6 to 6 else 70 to 70
    val count = if (input.ref > 0) 12 else 1024

    val blocked = bytes.take(count).toSet()

    val map = (0..maxX).flatMap { x ->
        (0..maxY).mapNotNull { y ->
            if (blocked.contains(x to y)) {
                null
            } else {
                (x to y) to Int.MAX_VALUE
            }
        }
    }.toMap().toMutableMap()

    val directions = listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)
    val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> map[p1]!! - map[p2]!! }
    map[0 to 0] = 0
    queue.add(0 to 0)
    while (queue.isNotEmpty()) {
        val nextPos = queue.remove()
        val cost = map[nextPos]!!
        if (nextPos == maxX to maxY) {
            return cost.toString()
        }
        directions
            .map { nextPos.first + it.first to nextPos.second + it.second }
            .filter { map.containsKey(it) }
            .forEach {
                val newCost = cost + 1
                if (map[it]!! > newCost) {
                    map[it] = newCost
                    queue.add(it)
                }
            }
    }
    return "0"
}

fun run2(input: InputData): ResultType {
    val bytes = input.lines.map { line ->
        val (x, y) = line.split(",").map(String::toInt)
        x to y
    }

    val (maxX, maxY) = if (input.ref > 0) 6 to 6 else 70 to 70
    val startCount = if (input.ref > 0) 12 else 1024

    val directions = listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    fun navigate(count: Int): Boolean {
        val blocked = bytes.take(count).toSet()

        val map = (0..maxX).flatMap { x ->
            (0..maxY).mapNotNull { y ->
                if (blocked.contains(x to y)) {
                    null
                } else {
                    (x to y) to Int.MAX_VALUE
                }
            }
        }.toMap().toMutableMap()

        val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> map[p1]!! - map[p2]!! }
        map[0 to 0] = 0
        queue.add(0 to 0)

        while (queue.isNotEmpty()) {
            val nextPos = queue.remove()
            val cost = map[nextPos]!!
            if (nextPos == maxX to maxY) {
                return true
            }
            directions
                .map { nextPos.first + it.first to nextPos.second + it.second }
                .filter { map.containsKey(it) }
                .forEach {
                    val newCost = cost + 1
                    if (map[it]!! > newCost) {
                        map[it] = newCost
                        queue.add(it)
                    }
                }
        }
        return false
    }

    var step = if (bytes.size < 100) 16 else 4096
    var count = startCount + step
    while (step > 1) {
        step /= 2
        if (navigate(count)) {
            count += step
        } else {
            count -= step
        }
    }

    val firstBlocker = if (navigate(count)) bytes[count] else bytes[count - 1]
    return "${firstBlocker.first},${firstBlocker.second}"
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
