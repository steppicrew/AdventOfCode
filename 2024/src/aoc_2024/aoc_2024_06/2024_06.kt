package aoc_2024.aoc_2024_06

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 6

val EXPECTED_RESULTS = listOf(
    1 to (41 to 6),
    0 to (5131 to 1784)
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char
        }
    }.toMap()
    var pos = map.entries.filter { it.value == '^' }[0].key
    var dir = 0 to -1

    val visited = mutableSetOf(pos)
    while (map.containsKey(pos)) {
        visited.add(pos)
        val nextPos = pos.first + dir.first to pos.second + dir.second
        if (map.getOrDefault(nextPos, ' ') == '#') {
            dir = (-dir.second) to dir.first
            continue
        }
        pos = nextPos
    }
    return visited.size
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char
        }
    }.toMap()
    val startPos = map.entries.filter { it.value == '^' }[0].key

    fun loop(entry: Map.Entry<Pair<Int, Int>, Char>): Pair<Int, Int>? {
        if (entry.value != '.') {
            return null
        }
        val newMap = map.toMutableMap()
        newMap[entry.key] = '#'

        var pos = startPos
        var dir = 0 to -1

        val visited = mutableSetOf(pos to dir)

        while (newMap.containsKey(pos)) {
            val nextPos = pos.first + dir.first to pos.second + dir.second
            if (newMap.getOrDefault(nextPos, ' ') == '#') {
                dir = (-dir.second) to dir.first
                continue
            }
            pos = nextPos
            if (visited.contains(pos to dir)) {
                return entry.key
            }
            visited.add(pos to dir)
        }
        return null
    }

    val obsitcles = map.entries.mapNotNull(::loop)

    return obsitcles.size
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
