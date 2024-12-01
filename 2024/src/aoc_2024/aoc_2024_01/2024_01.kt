package aoc_2024.aoc_2024_01

import aoc_2024.tools.InputOutput
import kotlin.math.abs

const val year = 2024
const val day = 1
const val ref = 0

fun run1() {
    val io = InputOutput(year, day, 1, ref)
    val lines = io.read()
    var result = 0
    val left:MutableList<Int> = mutableListOf()
    val right:MutableList<Int> = mutableListOf()
    for (line in lines) {
        val parts = line.split("\\s+".toRegex())
        left.add(parts[0].toInt())
        right.add(parts[1].toInt())
    }
    left.sort()
    right.sort()
    for (a in left.zip(right)) {
        result+= abs(a.first-a.second)
    }
    println(result)
    io.write(result)
}

fun run2() {
    val io = InputOutput(year, day, 2, ref)
    val lines = io.read()
    var result = 0

    val left:MutableList<Int> = mutableListOf()
    val right: MutableMap<Int, Int> = mutableMapOf()
    for (line in lines) {
        val parts = line.split("\\s+".toRegex())
        left.add(parts[0].toInt())
        val r = parts[1].toInt()
        right[r] = right.getOrDefault(r, 0) + 1
    }

    for (n in left) {
        result+= right.getOrDefault(n, 0)*n
    }

    println(result)
    io.write(result)
}

fun main() {
    run1()
    run2()
}
