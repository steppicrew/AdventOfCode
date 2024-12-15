package aoc_2024.aoc_2024_15

import aoc_2024.tools.ExpectedRefResults
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


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reMap = """[#.O@]+""".toRegex()
    val reMove = """[<^>v]+""".toRegex()
    val boxes = mutableSetOf<Pair<Int, Int>>()
    var robotPosition = 0 to 0
    val walls = lines.filter { reMap.matches(it) }
        .flatMapIndexed { row, line ->
            line.mapIndexedNotNull { col, c ->
                when (c) {
                    '#' -> col to row
                    'O' -> {
                        boxes.add(col to row)
                        null
                    }

                    '@' -> {
                        robotPosition = col to row
                        null
                    }

                    else -> null

                }
            }
        }.toSet()

    val moves = lines.filter { reMove.matches(it) }
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
        if (walls.contains(nextPos)) return false
        if (boxes.contains(nextPos) && !moveBox(nextPos, direction)) return false
        boxes.remove(pos)
        boxes.add(nextPos)
        return true
    }

    for (move in moves) {
        val nextPos = robotPosition.first + move.first to robotPosition.second + move.second
        if (walls.contains(nextPos)) continue
        if (!boxes.contains(nextPos) || moveBox(nextPos, move)) {
            robotPosition = nextPos
        }
    }

    return boxes.sumOf { it.first + 100 * it.second }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reMap = """[#.O@]+""".toRegex()
    val reMove = """[<^>v]+""".toRegex()
    val boxes = mutableSetOf<Pair<Int, Int>>()
    var robotPosition = 0 to 0
    val walls = lines.filter { reMap.matches(it) }
        .flatMapIndexed { row, line ->
            line.flatMapIndexed { col, c ->
                when (c) {
                    '#' -> listOf(2 * col to row, 2 * col + 1 to row)
                    'O' -> {
                        boxes.add(2 * col to row)
                        listOf()
                    }

                    '@' -> {
                        robotPosition = 2 * col to row
                        listOf()
                    }

                    else -> listOf()

                }
            }
        }.toSet()

    val moves = lines.filter { reMove.matches(it) }
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
        if (boxes.contains(pos)) return pos
        if (boxes.contains(pos.first - 1 to pos.second)) return pos.first - 1 to pos.second
        return null
    }

    fun moveBox(boxPos: Pair<Int, Int>, direction: Pair<Int, Int>): Set<Pair<Int, Int>>? {
        val nextPos1 = boxPos.first + direction.first to boxPos.second + direction.second
        val nextPos2 = nextPos1.first + 1 to nextPos1.second
        if (walls.contains(nextPos1) || walls.contains(nextPos2)) return null
        val nextBoxes = listOfNotNull(checkBox(nextPos1), checkBox(nextPos2)).toSet() - boxPos
        if (nextBoxes.isNotEmpty()) {
            val boxesToMove = nextBoxes.map { moveBox(it, direction) }
            if (boxesToMove.contains(null)) return null
            return boxesToMove.fold(setOf(boxPos)) { acc, boxes -> acc + boxes!! }
        }
        return setOf(boxPos)
    }

    for (move in moves) {
        val nextPos = robotPosition.first + move.first to robotPosition.second + move.second
        if (walls.contains(nextPos)) continue
        val nextBox = checkBox(nextPos)
        if (nextBox != null) {
            val boxesToMove = moveBox(nextBox, move) ?: continue
            boxes.removeAll(boxesToMove)
            for (box in boxesToMove) {
                boxes.add(box.first + move.first to box.second + move.second)
            }
        }
        robotPosition = nextPos
    }

    return boxes.sumOf { it.first + 100 * it.second }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
