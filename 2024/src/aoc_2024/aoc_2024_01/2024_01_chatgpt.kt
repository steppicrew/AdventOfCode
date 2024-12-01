package aoc_2024.aoc_2024_01a

import aoc_2024.tools.InputOutput
import kotlin.math.abs

const val year = 2024
const val day = 1
const val ref = 0

fun run1() {
    val io = InputOutput(year, day, 1, ref)
    val lines = io.read()

    // Parse input and split into left and right lists
    val (left, right) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip()

    // Sort both lists and compute the result
    val result = left.sorted().zip(right.sorted())
        .sumOf { (l, r) -> abs(l - r) }

    println(result)
    io.write(result)
}

fun run2() {
    val io = InputOutput(year, day, 2, ref)
    val lines = io.read()

    // Parse input and build left list and right frequency map
    val (left, rightFrequency) = lines.map { line ->
        line.split("\\s+".toRegex()).let { parts -> parts[0].toInt() to parts[1].toInt() }
    }.unzip().let { (left, right) ->
        left to right.groupingBy { it }.eachCount()
    }

    // Compute the result
    val result = left.sumOf { n -> rightFrequency.getOrDefault(n, 0) * n }

    println(result)
    io.write(result)
}

fun main() {
    run1()
    run2()
}
