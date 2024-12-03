package aoc_2024.aoc_2024_02

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 2
const val REF = 0

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reSpace = """\s+""".toRegex()

    fun isSafe(parts: Iterable<Int>): Boolean {
        return parts.zipWithNext { a, b -> b > a && b <= a + 3 }.all { it }
    }

    val result = lines.count { line ->
        line.split(reSpace).map(String::toInt).let { isSafe(it) || isSafe(it.reversed()) }
    }

    return result
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

    val result = lines.count { line ->
        line.split(reSpace).map(String::toInt).let { isSafe(it) || isSafe(it.reversed()) }
    }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
