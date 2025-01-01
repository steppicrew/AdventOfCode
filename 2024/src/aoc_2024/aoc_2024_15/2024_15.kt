package aoc_2024.aoc_2024_15

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 15

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (2028 to 1751),
    2 to (10092 to 9021),
    3 to (908 to 618),
    0 to (1412971 to 1429299),
)


fun run1(input: InputData): ResultType {
    val reMap = """[#.O@]+""".toRegex()
    val reMove = """[<^>v]+""".toRegex()
    val boxes = mutableSetOf<Pair<Int, Int>>()
    var robotPosition = 0 to 0
    val walls = input.lines.filter { reMap.matches(it) }
        .flatMapIndexed { row, line ->
            line.mapIndexedNotNull { col, c ->
                when (c) {
                    '#' -> return@mapIndexedNotNull col to row
                    'O' -> {
                        boxes.add(col to row)
                    }

                    '@' -> {
                        robotPosition = col to row
                    }
                }
                null
            }
        }.toSet()

    val moves = input.lines.filter { reMove.matches(it) }
        .joinToString("")
        .map {
            when (it) {
                '<' -> -1 to 0
                '^' -> 0 to -1
                '>' -> 1 to 0
                'v' -> 0 to 1
                else -> throw RuntimeException("Not possible")
            }
        }

    fun moveBox(pos: Pair<Int, Int>, direction: Pair<Int, Int>): Boolean {
        val nextPos = pos.first + direction.first to pos.second + direction.second
        if (nextPos in walls) return false
        if (nextPos in boxes && !moveBox(nextPos, direction)) return false
        boxes.remove(pos)
        boxes.add(nextPos)
        return true
    }

    moves.forEach { move ->
        val nextPos = robotPosition.first + move.first to robotPosition.second + move.second
        if (nextPos in walls) return@forEach
        if (nextPos !in boxes || moveBox(nextPos, move)) {
            robotPosition = nextPos
        }
    }

    return boxes.sumOf { it.first + 100 * it.second }
}

fun run2(input: InputData): ResultType {
    val reMap = """[#.O@]+""".toRegex()
    val reMove = """[<^>v]+""".toRegex()
    val boxes = mutableSetOf<Pair<Int, Int>>()
    var robotPosition = 0 to 0
    val walls = input.lines.filter { reMap.matches(it) }
        .flatMapIndexed { row, line ->
            line.flatMapIndexed inner@{ col, c ->
                when (c) {
                    '#' -> return@inner listOf(2 * col to row, 2 * col + 1 to row)
                    'O' -> {
                        boxes.add(2 * col to row)
                    }

                    '@' -> {
                        robotPosition = 2 * col to row
                    }
                }
                listOf()
            }
        }.toSet()

    val moves = input.lines.filter { reMove.matches(it) }
        .joinToString("")
        .map {
            when (it) {
                '<' -> -1 to 0
                '^' -> 0 to -1
                '>' -> 1 to 0
                'v' -> 0 to 1
                else -> throw RuntimeException("Not possible")
            }
        }

    fun checkBox(pos: Pair<Int, Int>): Pair<Int, Int>? {
        if (pos in boxes) return pos
        if ((pos.first - 1 to pos.second) in boxes) return pos.first - 1 to pos.second
        return null
    }

    fun moveBox(boxPos: Pair<Int, Int>, direction: Pair<Int, Int>): Set<Pair<Int, Int>>? {
        val nextPos1 = boxPos.first + direction.first to boxPos.second + direction.second
        val nextPos2 = nextPos1.first + 1 to nextPos1.second
        if (nextPos1 in walls || nextPos2 in walls) return null
        val nextBoxes = setOfNotNull(checkBox(nextPos1), checkBox(nextPos2)) - boxPos
        if (nextBoxes.isNotEmpty()) {
            val boxesToMove = nextBoxes.map { moveBox(it, direction) }
            if (null in boxesToMove) return null
            return boxesToMove.fold(setOf(boxPos)) { acc, boxes -> acc + boxes!! }
        }
        return setOf(boxPos)
    }

    moves.forEach { move ->
        val nextPos = robotPosition.first + move.first to robotPosition.second + move.second
        if (nextPos in walls) return@forEach
        val nextBox = checkBox(nextPos)
        if (nextBox != null) {
            val boxesToMove = moveBox(nextBox, move) ?: return@forEach
            boxes.removeAll(boxesToMove)
            boxes.addAll(boxesToMove.map { it.first + move.first to it.second + move.second })
        }
        robotPosition = nextPos
    }

    return boxes.sumOf { it.first + 100 * it.second }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
