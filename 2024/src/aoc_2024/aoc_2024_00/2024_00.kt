package aoc_2024.aoc_2024_00

import aoc_2024.tools.InputOutput

const val year = 2024
const val day = 0
const val ref = 1

fun run1() {
    val io = InputOutput(year, day, 1, ref)
    val lines = io.read()
    val result = 0
    io.log("RESULT: $result")
    io.write(result)
    io.writeLog()
}

fun run2() {
    val io = InputOutput(year, day, 2, ref)
    val lines = io.read()
    val result = 0
    io.log("RESULT: $result")
    io.write(result)
    io.writeLog()
}

fun main() {
    run1()
    run2()
}
