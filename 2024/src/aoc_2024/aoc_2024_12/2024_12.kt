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

    val visited = mutableSetOf<Pos>()

    val directions = listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)

    fun getAllNeighbours(pos: Pos): Sequence<Pos> {
        return directions.asSequence().map {
            pos.first + it.first to pos.second + it.second
        }
    }

    fun floodFill(startPos: Pos): Set<Pos> {
        val c = map[startPos]!!
        val area = mutableSetOf<Pos>(startPos)
        val todo = ArrayDeque<Pos>(listOf(startPos))
        while (todo.size > 0) {
            val pos = todo.removeFirst()
            if (!visited.add(pos)) continue
            val neighbors = getAllNeighbours(pos).filter {
                !visited.contains(it) && map[it] == c
            }
            todo.addAll(neighbors)
            area.addAll(neighbors)
        }
        return area
    }

    fun getPerimeter(area: Set<Pos>): Int {
        val _visited = mutableSetOf<Pos>()
        return area.sumOf { pos ->
            val oldNeighbors = getAllNeighbours(pos).filter { _visited.contains(it) }.toList().size
            _visited.add(pos)
            2 * (2 - oldNeighbors)
        }
    }

    return map.mapNotNull { (pos, _) ->
        if (visited.contains(pos)) {
            null
        } else {
            val area = floodFill(pos)
            area.size * getPerimeter(area)
        }
    }.sum()
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, c ->
            (col to row) to c
        }
    }.toMap()

    val visited = mutableSetOf<Pos>()

    val directions = listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1)
    val diagonals = listOf(1 to 1, -1 to 1, -1 to -1, 1 to -1)

    fun getAllNeighbours(pos: Pos): Sequence<Pos> {
        return directions.asSequence().map {
            pos.first + it.first to pos.second + it.second
        }
    }

    fun floodFill(startPos: Pos): Set<Pos> {
        val c = map[startPos]!!
        val area = mutableSetOf<Pos>(startPos)
        val todo = ArrayDeque<Pos>(listOf(startPos))
        while (todo.size > 0) {
            val pos = todo.removeFirst()
            if (!visited.add(pos)) continue
            val neighbors = getAllNeighbours(pos).filter {
                !visited.contains(it) && map[it] == c
            }
            todo.addAll(neighbors)
            area.addAll(neighbors)
        }
        return area
    }

    fun getDiagonalNeighbours(pos: Pos): List<Pos> {
        return diagonals.map {
            pos.first + it.first to pos.second + it.second
        }
    }

    fun getCorners(area: Set<Pos>): Int {
        return area.sumOf { pos ->
            val neighbours = getAllNeighbours(pos).map { area.contains(it) }.toList().let { it + it.first() }
            val diagonalNeighbours = getDiagonalNeighbours(pos).map { area.contains(it) }

            val innerCorners = neighbours.zipWithNext().zip(diagonalNeighbours).count {
                val (positions, diagonal) = it
                positions.first && positions.second && !diagonal
            }

            val outerCorners = neighbours.zipWithNext().count {
                !it.first && !it.second
            }

            innerCorners + outerCorners
        }
    }

    return map.mapNotNull { (pos, _) ->
        if (visited.contains(pos)) {
            null
        } else {
            val area = floodFill(pos)
            area.size * getCorners(area)
        }
    }.sum()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
