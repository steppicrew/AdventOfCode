package aoc_2024.aoc_2024_01a

import aoc_2024.tools.simpleIO
import kotlin.math.abs

const val YEAR = 2024
const val DAY = 1
const val REF = 0

fun run1(lines: Collection<String>, log:(String)->Unit): Int {
    // Parse input and split into left and right lists
    val (left, right) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip()

    // Sort both lists and compute the result
    val result = left.sorted().zip(right.sorted())
        .sumOf { (l, r) -> abs(l - r) }

    return result
}

fun run2(lines: Collection<String>, log:(String)->Unit): Int {
    // Parse input and build left list and right frequency map
    val (left, rightFrequency) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip().let { (left, right) ->
        left to right.groupingBy { it }.eachCount()
    }

    // Compute the result
    val result = left.sumOf { n -> rightFrequency.getOrDefault(n, 0) * n }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
