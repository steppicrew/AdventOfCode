package aoc_2024.aoc_2024_17

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 17

typealias ResultType = String

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    // 1 to ("4,6,3,5,6,3,5,2,1,0" to null),
    // 2 to ("0,1,2" to null),
    // 3 to ("4,2,5,6,7,7,7,7,3,1,0" to null),
    0 to ("3,7,1,7,2,1,0,6,3" to null),
)


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var a = 0
    var b = 0
    var c = 0
    var pc = 0
    var program = listOf<Int>()
    val output = mutableListOf<Int>()

    lines.forEach { line ->
        val matchA = """Register A: (\d+)""".toRegex().matchEntire(line)
        if (matchA != null) {
            a = matchA.groupValues[1].toInt()
        }
        val matchB = """Register B: (\d+)""".toRegex().matchEntire(line)
        if (matchB != null) {
            b = matchB.groupValues[1].toInt()
        }
        val matchC = """Register C: (\d+)""".toRegex().matchEntire(line)
        if (matchC != null) {
            c = matchC.groupValues[1].toInt()
        }
        val matchProgram = """Program: (\d(?:,\d)+)""".toRegex().matchEntire(line)
        if (matchProgram != null) {
            program = matchProgram.groupValues[1].split(",").map(String::toInt)
        }
    }

    fun combo(code: Int): Int {
        return when (code) {
            in 0..3 -> code
            4 -> a
            5 -> b
            6 -> c
            else -> throw RuntimeException("Reserved")
        }
    }

    val opcodes = listOf<(Int) -> Boolean>(
        { a /= 1.shl(combo(it)); true }, // adv
        { b = b xor it; true }, // bxl
        { b = combo(it) % 8; true }, // bst
        {
            if (a != 0) {
                pc = it; false
            } else {
                true
            }
        }, // jnz
        { b = b xor c; true }, // bxc
        { output.add(combo(it) % 8) }, // out
        { b = a / 1.shl(combo(it)); true }, //bdv
        { c = a / 1.shl(combo(it)); true }, //cdv
    )

    while (pc < program.size) {
        val opcode = program[pc]
        val operand = program[pc + 1]
        if (opcodes[opcode](operand)) pc += 2
    }

    return output.joinToString(",")
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var initB = 0L
    var initC = 0L
    var program = listOf<Int>()

    lines.forEach { line ->
        val matchB = """Register B: (\d+)""".toRegex().matchEntire(line)
        if (matchB != null) {
            initB = matchB.groupValues[1].toLong()
        }
        val matchC = """Register C: (\d+)""".toRegex().matchEntire(line)
        if (matchC != null) {
            initC = matchC.groupValues[1].toLong()
        }
        val matchProgram = """Program: (\d(?:,\d)+)""".toRegex().matchEntire(line)
        if (matchProgram != null) {
            program = matchProgram.groupValues[1].split(",").map(String::toInt)
        }
    }

    fun run(initA: Long): Boolean {
        var a = initA
        var b = initB
        var c = initC
        val output = mutableListOf<Int>()
        var pc = 0

        fun combo(code: Int): Long {
            return when (code) {
                in 0..3 -> code.toLong()
                4 -> a
                5 -> b
                6 -> c
                else -> throw RuntimeException("Reserved")
            }
        }

        val opcodes = listOf<(Int) -> Boolean>(
            { a /= 1.shl(combo(it).toInt()); true }, // adv
            { b = b xor it.toLong(); true }, // bxl
            { b = combo(it) % 8; true }, // bst
            {
                if (a != 0L) {
                    pc = it - 2
                    true
                } else {
                    true
                }
            }, // jnz
            { b = b xor c; true }, // bxc
            {
                val outValue = (combo(it) % 8).toInt()
                if (outValue != program[output.size]) {
                    false
                } else {
                    output.add(outValue)
                    true
                }
            }, // out
            { b = a / 1.shl(combo(it).toInt()); true }, //bdv
            { c = a / 1.shl(combo(it).toInt()); true }, //cdv
        )

        while (pc < program.size) {
            val opcode = program[pc]
            val operand = program[pc + 1]
            if (!opcodes[opcode](operand)) break
            pc += 2
        }

        return program == output
    }

    generateSequence(1L) { it + 1 }.forEach {
        if (it % 1_000_000 == 0L) {
            println(it)
        }
        if (run(it)) return it.toString()
    }

    return "empty"
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
