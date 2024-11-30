package aoc_2024.aoc_2024_01

import aoc_2024.tools.InputOutput

const val year = 2024
const val day = 1
const val ref = 1

fun run1() {
    val io = InputOutput(year, day, 1, ref)
    val lines = io.read()
    var result = 0
    for (line in lines) {
        val parts = line.split(",\\s*".toRegex())
        for (part in parts) {
            result+= part.toInt()
        }
    }
    println(result)
    io.write(result)
}

fun run2() {
    val io = InputOutput(year, day, 2, ref)
    val lines = io.read()
    var result = 0

    val seen= HashSet<Int>()
    while (true) {
        for (line in lines) {
            seen.add(result)
            result += line.toInt()
            // println("$result, $seen")
            if (seen.contains(result)) {
                break
            }
        }
        if (seen.contains(result)) {
            break
        }
    }
    println(result)
    io.write(result)
}

fun main() {
    run1()
    run2()
}
