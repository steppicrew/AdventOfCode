package aoc_2024.aoc_2024_12

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 12

typealias ResultType = Int

typealias Pos = Pair<Int, Int>

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (140 to 80),
    2 to (772 to 436),
    3 to (1930 to 1206),
    4 to (692 to 236),
    5 to (1184 to 368),
    0 to (1424472 to 870202),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            (col to row) to c
        }
    }.toMap()

    val directions = sequenceOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    fun getNeighbours(pos: Pos): Sequence<Pos> {
        return directions.map {
            pos.first + it.first to pos.second + it.second
        }
    }

    fun floodFill(startPos: Pos): Set<Pos> {
        val c = map[startPos]!!
        val area = mutableSetOf<Pos>(startPos)
        val todo = ArrayDeque<Pos>(listOf(startPos))
        while (todo.size > 0) {
            val pos = todo.removeFirst()
            val neighbours = getNeighbours(pos).filter {
                map[it] == c && !area.contains(it)
            }
            todo.addAll(neighbours)
            area.addAll(neighbours)
        }
        return area
    }

    fun getPerimeter(area: Set<Pos>): Int {
        val seen = mutableSetOf<Pos>()
        return area.sumOf { pos ->
            val knownNeighboursCount = getNeighbours(pos).filter { seen.contains(it) }.count()
            seen.add(pos)
            4 - 2 * knownNeighboursCount
        }
    }

    val visited = mutableSetOf<Pos>()
    return map.keys.sumOf { pos ->
        if (visited.contains(pos)) {
            0
        } else {
            floodFill(pos)
                .also { visited.addAll(it) }
                .let { it.size * getPerimeter(it) }
        }
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            (col to row) to c
        }
    }.toMap()

    // clockwise
    val directions = sequenceOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    // clockwise, following direction with same index
    val diagonals = (directions + directions.first()).zipWithNext { d1, d2 ->
        d1.first + d2.first to d1.second + d2.second
    }.toList()

    fun getNeighbours(pos: Pos): Sequence<Pos> {
        return directions.map {
            pos.first + it.first to pos.second + it.second
        }
    }

    fun floodFill(startPos: Pos): Set<Pos> {
        val c = map[startPos]!!
        val area = mutableSetOf<Pos>(startPos)
        val todo = ArrayDeque<Pos>(listOf(startPos))
        while (todo.size > 0) {
            val pos = todo.removeFirst()
            val neighbours = getNeighbours(pos).filter {
                map[it] == c && !area.contains(it)
            }
            todo.addAll(neighbours)
            area.addAll(neighbours)
        }
        return area
    }

    fun getDiagonalNeighbours(pos: Pos): List<Pos> {
        return diagonals.map {
            pos.first + it.first to pos.second + it.second
        }
    }

    // Counting corners is the same as counting sides
    fun getCorners(area: Set<Pos>): Int {
        return area.sumOf { pos ->
            val neighbourPairs = getNeighbours(pos)
                .map { area.contains(it) }.toList()
                .let { it + it.first() }
                .zipWithNext()
            val diagonalNeighbours = getDiagonalNeighbours(pos).map { area.contains(it) }

            // Concave corners: two adjacent neighbours exist but not the diagonal in between
            val concaveCorners = neighbourPairs.zip(diagonalNeighbours).count {
                val (positions, diagonal) = it
                positions.first && positions.second && !diagonal
            }

            // Convex corners: two adjacent neighbours are missing
            val convexCorners = neighbourPairs.count {
                !it.first && !it.second
            }

            concaveCorners + convexCorners
        }
    }

    val visited = mutableSetOf<Pos>()
    return map.keys.sumOf { pos ->
        if (visited.contains(pos)) {
            0
        } else {
            floodFill(pos)
                .also { visited.addAll(it) }
                .let { it.size * getCorners(it) }
        }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
