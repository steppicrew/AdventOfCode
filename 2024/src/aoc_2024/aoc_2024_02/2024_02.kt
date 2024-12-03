package aoc_2024.aoc_2024_02

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 2

val EXPECTED_RESULTS = listOf(
    1 to (2 to 4),
    0 to (502 to 544)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reSpace = """\s+""".toRegex()

    fun isSafe(parts: Iterable<Int>): Boolean {
        return parts.zipWithNext { a, b -> b > a && b <= a + 3 }.all { it }
    }

    return lines.count { line ->
        line.split(reSpace).map(String::toInt).let { isSafe(it) || isSafe(it.reversed()) }
    }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reSpace = """\s+""".toRegex()

    fun countGlitches(parts: List<Int>): Int {
        return parts.zipWithNext { a, b -> b > a && b <= a + 3 }.count { !it }
    }

    fun removeOne(parts: List<Int>): Sequence<List<Int>> {
        return parts.indices.asSequence().map { parts.filterIndexed { index, _ -> it != index } }
    }

    fun isSafe(parts: List<Int>): Boolean {
        val glitches = countGlitches(parts)
        if (glitches == 0) return true
        if (glitches > 2) return false
        return removeOne(parts).any { countGlitches(it) == 0 }
    }

    return lines.count { line ->
        line.split(reSpace).map(String::toInt).let { isSafe(it) || isSafe(it.reversed()) }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
