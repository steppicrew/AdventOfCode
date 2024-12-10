package aoc_2024.aoc_2024_10

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 10

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (36 to 81),
    0 to (796 to 1942),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char.toString().toInt()
        }
    }.toMap()

    val directions = listOf(
        -1 to 0,
        1 to 0,
        0 to -1,
        0 to 1
    )

    fun countHeads(position: Pair<Int, Int>): Set<Pair<Int, Int>> {
        val height = map[position]!!
        if (height == 9) {
            return setOf(position)
        }
        return directions
            .map { (position.first + it.first) to (position.second + it.second) }
            .filter { map[it] == height + 1 }
            .flatMap { countHeads((it)) }.toSet()
    }

    return map.filterValues { it == 0 }.keys.sumOf { countHeads(it).size }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val map = lines.flatMapIndexed { row, line ->
        line.mapIndexed { col, char ->
            (col to row) to char.toString().toInt()
        }
    }.toMap()

    val directions = listOf(
        -1 to 0,
        1 to 0,
        0 to -1,
        0 to 1
    )

    fun countHeads(position: Pair<Int, Int>): Int {
        val height = map[position]!!
        if (height == 9) {
            return 1
        }
        return directions
            .map { (position.first + it.first) to (position.second + it.second) }
            .filter { map[it] == height + 1 }
            .sumOf { countHeads((it)) }
    }

    return map.filterValues { it == 0 }.keys.sumOf { countHeads(it) }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
