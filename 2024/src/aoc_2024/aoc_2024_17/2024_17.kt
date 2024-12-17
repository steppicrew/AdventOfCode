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
    4 to ("5,7,3,0" to "117440"),
    0 to ("3,7,1,7,2,1,0,6,3" to "37221334433268"),
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
    /*
     Result depends only on register a
     Ref4: Result is calculated from bit 3 through 5 only
     Main: Result is calculated from the lowest 3 bit of a and three of bits 0 through 9
     Next result is calculated from last (register A >> 3) until register A == 0

     Idea: We build a cache, where we use all possible values for register A (6 bit for ref4, 10 bit for main)
            and map each possible result to a list of all register A inputs
           We start with the last expected result (last program triplet) and register A == 0 and search for every
            register A input with (register A input >> 3)&bitMask == (register A output)&bitMask
            bitMask is number of bits from above - 3
           We search recursive until we get the fist program triplet
           We take the minimum of all results
     */

    var program = listOf<UInt>()

    lines.forEach { line ->
        val matchProgram = """Program: (\d(?:,\d)+)""".toRegex().matchEntire(line)
        if (matchProgram != null) {
            program = matchProgram.groupValues[1].split(",").map(String::toUInt)
        }
    }

    // Short version of main's program
    fun fillCacheMain(a: ULong): ULong {
        val b = a.and(7UL).xor(2UL) // bst 4; bxl 2 => (a % 8) xor 2
        val c = a.shr(b.toInt()) // cdv 5 => c = a >> b
        return b.xor(3UL).xor(c).and(7UL) // bxl 3; bxc 3; out b%8 => ((b xor 3) xor c) % 8
    }

    // Short version of ref 4's program
    fun fillCacheRef4(a: ULong): ULong {
        return a.shr(3).and(7UL) // adv 3; out 4 => a = a/8; out a%8
    }

    val fillCache = if (program.size == 6) ::fillCacheRef4 else ::fillCacheMain

    val bit = if (program.size == 6) 6 else 10
    val bitMask = 1UL.shl(bit) - 1UL
    val bitMaskA = bitMask.shr(3)
    // println("Bitmask: ${bitMask.toString(8)}($bitMask)")

    // result to list of aIn
    val resultMap = (0UL..bitMask).asSequence()
        .map {
            fillCache(it) to it
        }
        .groupBy({ it.first }, { it.second })

    fun findMatch(a: ULong, program: List<UInt>): ULong? {
        if (program.isEmpty()) return a
        val result = program.last().toULong()
        val remainingProgram = program.dropLast(1)

        return resultMap[result]!!
            .filter { aIn ->
                aIn.shr(3).and(bitMaskA) == a.and(bitMaskA)
            }
            .mapNotNull { aIn ->
                findMatch(a.shl(3).or(aIn), remainingProgram) ?: return@mapNotNull null
            }.minOrNull()
    }

    return findMatch(0UL, program)!!.toString()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
