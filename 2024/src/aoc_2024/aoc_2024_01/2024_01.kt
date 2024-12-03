package aoc_2024.aoc_2024_01

import aoc_2024.tools.simpleIO
import kotlin.math.abs

const val YEAR = 2024
const val DAY = 1
const val REF = 0

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reSpace = """\s+""".toRegex()

    return lines
        .map { line ->
            line.split(reSpace)
                .let { it[0].toInt() to it[1].toInt() }
        }.unzip()
        .let { it.first.sorted().zip(it.second.sorted()) }
        .sumOf { abs(it.first - it.second) }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reSpace = """\s+""".toRegex()

    return lines
        .map { line ->
            line.split(reSpace)
                .let { it[0].toInt() to it[1].toInt() }
        }.unzip()
        .let { (left, right) -> left to right.groupingBy { it }.eachCount() }
        .let { (left, rightCount) -> left.sumOf { it * rightCount.getOrDefault(it, 0) } }
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
