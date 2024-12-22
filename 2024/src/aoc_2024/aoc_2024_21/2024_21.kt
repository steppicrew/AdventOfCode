package aoc_2024.aoc_2024_21

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO
import java.util.*

const val YEAR = 2024
const val DAY = 21

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (126384L to 154115708116294L),
    0 to (246990L to 306335137543664L),
)

val codeKeypad = mapOf(
    'A' to (2 to 3),
    '0' to (1 to 3),
    '1' to (0 to 2),
    '2' to (1 to 2),
    '3' to (2 to 2),
    '4' to (0 to 1),
    '5' to (1 to 1),
    '6' to (2 to 1),
    '7' to (0 to 0),
    '8' to (1 to 0),
    '9' to (2 to 0),
)
val directionalKeypad = mapOf(
    'A' to (2 to 0),
    '^' to (1 to 0),
    '<' to (0 to 1),
    'v' to (1 to 1),
    '>' to (2 to 1),
)

fun run1(input: InputData): ResultType {

    val robotStartPositions = mapOf(
        0 to (2 to 3),
        1 to (2 to 0),
        2 to (2 to 0),
    )

    val robotArms = robotStartPositions.toMutableMap()

    fun getKeyPad(robot: Int): Map<Char, Pair<Int, Int>> {
        if (robot == 0) return codeKeypad
        return directionalKeypad
    }

    val directions = listOf((1 to 0) to ">", (0 to 1) to "v", (-1 to 0) to "<", (0 to -1) to "^")

    val navigationCache = mutableMapOf<Pair<Int, Pair<Pair<Int, Int>, Pair<Int, Int>>>, List<String>>()
    fun navigate(robot: Int, start: Pair<Int, Int>, end: Pair<Int, Int>): List<String> {
        return navigationCache.getOrPut(robot to (start to end)) {
            val costs = getKeyPad(robot).values.associateWith { Int.MAX_VALUE }.toMutableMap()
            val ways = mutableMapOf<Pair<Int, Int>, Set<String>>()
            val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> costs[p1]!! - costs[p2]!! }
            queue.add(start)
            costs[start] = 0
            ways[start] = setOf("")
            while (queue.isNotEmpty()) {
                val pos = queue.remove()
                val cost = costs[pos]!!
                val way = ways[pos]!!
                directions.map { (pos.first + it.first.first to pos.second + it.first.second) to it.second }
                    .filter { costs.containsKey(it.first) }
                    .forEach { (nextPos, direction) ->
                        val nextCost = costs[nextPos]!!
                        if (cost + 1 > nextCost) return@forEach
                        if (cost + 1 < nextCost) {
                            costs[nextPos] = cost + 1
                            ways[nextPos] = way.map { it + direction }.toSet()
                            queue.add(nextPos)
                        } else {
                            ways[nextPos] = ways[nextPos]!! + way.map { it + direction }.toSet()
                        }
                    }

            }
            ways[end]!!.toList()
        }
    }

    fun pressButton2(robot: Int, button: Char): List<String> {
        if (robot == 3) return listOf(button.toString())
        val keyPad = getKeyPad(robot)
        val position = robotArms[robot]!!
        val destination = keyPad[button]!!
        val movements = navigate(robot, position, destination).map { it + "A" }
        robotArms[robot] = destination

        fun combine(possibilities: List<List<String>>): List<String> {
            val firstList = possibilities.first()
            if (possibilities.size == 1) return firstList
            return firstList.flatMap { letter ->
                combine(possibilities.drop(1)).map { letter + it }
            }
        }

        return movements.flatMap { movement ->
            val x = combine(movement.map { letter ->
                pressButton2(robot + 1, letter)
            })
            x
        }
    }

    fun pressButton(button: Char): String {
        return pressButton2(0, button).minBy { it.length }
    }

    return input.lines.sumOf { line ->
        line.dropLast(1).toInt() * line.map { pressButton(it) }.joinToString("").length
    }.toLong()
}

fun run2(input: InputData): ResultType {
    val robots = 26

    val robotArms = (0 until robots).map { 'A' }.toMutableList()

    /**
     * I don't know why only this combination works. (except for a and C)
     * Tested combinations ad results:
     * abCdef: 491655470688846
     * aBCdef: 363481568617378
     * aBCDef: 348675369134078
     * aBCDEf: 348675369134078
     * aBCdEf: 306335137543664
     *
     */
    val moves = mapOf(
        ('A' to 'A') to "A",

        ('A' to '<') to "v<<A",             // a!
        // ('A' to '<') to "<v<A",          // A!

        // ('A' to 'v') to "v<A",           // b?
        ('A' to 'v') to "<vA",              // B?

        ('A' to '^') to "<A",
        ('A' to '>') to "vA",

        // ('<' to 'A') to ">^>A",          // c!
        ('<' to 'A') to ">>^A",             // C!

        ('<' to '<') to "A",
        ('<' to 'v') to ">A",
        ('<' to '^') to ">^A",
        ('<' to '>') to ">>A",

        ('v' to 'A') to "^>A",               // d?
        // ('v' to 'A') to ">^A",            // D?

        ('v' to '<') to "<A",
        ('v' to 'v') to "A",
        ('v' to '^') to "^A",
        ('v' to '>') to ">A",
        ('^' to 'A') to ">A",
        ('^' to '<') to "v<A",
        ('^' to 'v') to "vA",
        ('^' to '^') to "A",

        // ('^' to '>') to ">vA",           // e?
        ('^' to '>') to "v>A",              // E?

        ('>' to 'A') to "^A",
        ('>' to '<') to "<<A",
        ('>' to 'v') to "<A",

        ('>' to '^') to "<^A",              // f?
        //('>' to '^') to "^<A",            // F?

        ('>' to '>') to "A",
    )

    val directions = listOf((1 to 0) to ">", (0 to 1) to "v", (-1 to 0) to "<", (0 to -1) to "^")

    val navigationCache = mutableMapOf<Pair<Char, Char>, List<String>>()
    fun navigate(start: Char, end: Char): List<String> {
        return navigationCache.getOrPut(start to end) {
            val costs = codeKeypad.values.associateWith { Int.MAX_VALUE }.toMutableMap()
            val ways = mutableMapOf<Pair<Int, Int>, Set<String>>()
            val queue = PriorityQueue<Pair<Int, Int>> { p1, p2 -> costs[p1]!! - costs[p2]!! }
            val startPos = codeKeypad[start]!!
            queue.add(startPos)
            costs[startPos] = 0
            ways[startPos] = setOf("")
            while (queue.isNotEmpty()) {
                val pos = queue.remove()
                val cost = costs[pos]!! + 1
                val way = ways[pos]!!
                directions.map { (pos.first + it.first.first to pos.second + it.first.second) to it.second }
                    .filter { costs.containsKey(it.first) }
                    .forEach { (nextPos, direction) ->
                        val nextCost = costs[nextPos]!!
                        if (cost > nextCost) return@forEach
                        if (cost < nextCost) {
                            costs[nextPos] = cost
                            ways[nextPos] = way.map { it + direction }.toSet()
                            queue.add(nextPos)
                        } else {
                            ways[nextPos] = ways[nextPos]!! + way.map { it + direction }.toSet()
                        }
                    }

            }
            val endWays = ways[codeKeypad[end]!!]!!.toList()
            endWays
        }
    }

    val directionButtonCache = mutableMapOf<Pair<Int, Pair<Char, Char>>, Long>()
    fun pressDirectionButton(robot: Int, button: Char): Long {
        if (robot == robots) return 1L
        val position = robotArms[robot]
        robotArms[robot] = button
        return directionButtonCache.getOrPut(robot to (position to button)) {
            val movements = moves[position to button] ?: throw RuntimeException("Wrong move: $position to $button")
            movements.sumOf { m ->
                pressDirectionButton(robot + 1, m)
            }
        }
    }

    fun pressCodeButton(button: Char): Long {
        val position = robotArms[0]
        val movements = navigate(position, button).map { it + "A" }
        robotArms[0] = button

        return movements.minOf { movement ->
            movement.sumOf { letter ->
                pressDirectionButton(1, letter)
            }
        }
    }

    return input.lines.sumOf { line ->
        line.dropLast(1).toInt() * line.map { pressCodeButton(it) }.sum()
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
