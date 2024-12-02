package aoc_2024.aoc_2024_02

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 2
const val REF = 0

fun run1(lines: Collection<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {

    fun isSafe(parts: Iterable<Int>): Boolean {
        return parts.zipWithNext { a, b -> b > a && b <= a + 3 }.all { it }
    }

    var result = 0
    for (line in lines) {
        val parts = line.split("\\s+".toRegex()).map { it.toInt() }
        if (isSafe(parts) || isSafe(parts.reversed())) {
            result += 1
        }
    }

    return result
}

fun run2(lines: Collection<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {

    fun glitchCount(parts: Iterable<Int>): Int {
        return parts.zipWithNext { a, b -> b > a && b <= a + 3 }.count { !it }
    }

    fun <T> List<T>.iteratorMissingOne(): Sequence<List<T>> = sequence {
        for (i in indices) {
            yield(this@iteratorMissingOne.filterIndexed { index, _ -> index != i })
        }
    }

    fun isSafe(parts: List<Int>): Boolean {
        val first = glitchCount(parts)
        if (first == 0) return true
        if (first > 2) return false
        for (p in parts.iteratorMissingOne()) {
            if (glitchCount(p) == 0) return true
        }
        return false
    }

    var result = 0
    for (line in lines) {
        val parts = line.split("\\s+".toRegex()).map { it.toInt() }
        if (isSafe(parts) || isSafe(parts.reversed())) {
            result += 1
        }
    }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
