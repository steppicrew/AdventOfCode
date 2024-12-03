package aoc_2015.aoc_2015_02

import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 2

val EXPECTED_RESULTS = listOf(
    1 to (58 to 34),
    0 to (1598415 to 3812909)
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    fun getArea(x: Int, y: Int, z: Int): Int {
        return 2 * x * y + 2 * x * z + 2 * y * z + listOf(x, y, z).sorted().let { it[0] * it[1] }
    }

    val reLine = """(\d+)x(\d+)x(\d+)""".toRegex()

    return lines.map { reLine.matchEntire(it) }.filterNotNull().sumOf { match ->
        val (x, y, z) = match.destructured
        getArea(x.toInt(), y.toInt(), z.toInt())
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    fun getRibbon(x: Int, y: Int, z: Int): Int {
        return x * y * z + listOf(x, y, z).sorted().let { 2 * (it[0] + it[1]) }
    }

    val reLine = """(\d+)x(\d+)x(\d+)""".toRegex()

    return lines.map { reLine.matchEntire(it) }.filterNotNull().sumOf { match ->
        val (x, y, z) = match.destructured
        getRibbon(x.toInt(), y.toInt(), z.toInt())
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
