package aoc_2024.aoc_2024_01

import aoc_2024.tools.simpleIO
import kotlin.math.abs

const val YEAR = 2024
const val DAY = 1
const val REF = 0

fun run1(lines: Collection<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    var result = 0
    val left: MutableList<Int> = mutableListOf()
    val right: MutableList<Int> = mutableListOf()
    for (line in lines) {
        val parts = line.split("\\s+".toRegex())
        left.add(parts[0].toInt())
        right.add(parts[1].toInt())
    }
    left.sort()
    right.sort()
    for (a in left.zip(right)) {
        result += abs(a.first - a.second)
    }
    return result
}

fun run2(lines: Collection<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    var result = 0

    val left: MutableList<Int> = mutableListOf()
    val right: MutableMap<Int, Int> = mutableMapOf()
    for (line in lines) {
        val parts = line.split("\\s+".toRegex())
        left.add(parts[0].toInt())
        val r = parts[1].toInt()
        right[r] = right.getOrDefault(r, 0) + 1
    }

    for (n in left) {
        result += right.getOrDefault(n, 0) * n
    }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
