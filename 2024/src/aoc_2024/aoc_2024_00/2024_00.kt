package aoc_2024.aoc_2024_00

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 0
const val REF = 1

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val result = lines.count()
    return result
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val result = lines.count()
    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
