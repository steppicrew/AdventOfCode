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

/**
 * Ref4:
 *  adv 3   a = a >> 3
 *  out a   out a % 8
 *  jnz 0                       => We need at most 6 bit values for regA
 *
 * Main:
 *  bst 4   b = a % 8           0<=b<=7
 *  bxl 2   b = b xor 2         0<=b<=7
 *  cdv 5   c = a / 2^b         c = a >> b
 *  bxl 3   b = b xor 3         0<=b<=7
 *  bxc 3   b = b xor c
 *  out 5   out b % 8
 *  adv 3   a = a / 8           => We need at most 10 bit values for regA
 *  jnz 0
 *
 */


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
     Result depends only on register A (regA)
     Ref4: Result is calculated from bit 3 through 5 only
     Main: Result is calculated from the lowest 3 bit of a and three of bits 0 through 9
     Next result is calculated from last (regA >> 3) until regA == 0

     Idea: We build a cache, where we use all possible values for regA (6 bit for ref4, 10 bit for main)
            and map each possible result to a list of all regA inputs
           We start with the last expected result (last program triplet) and regA == 0 and search for every
            regA input with (regA input >> 3)&bitMask == (regA output)&bitMask
            bitMask is number of bits from above - 3
           We search recursive until we get the fist program triplet
           We take the minimum of all results
     */

    var initB = 0UL
    var initC = 0UL
    var program = listOf<Int>()

    lines.forEach { line ->
        val matchB = """Register B: (\d+)""".toRegex().matchEntire(line)
        if (matchB != null) {
            initB = matchB.groupValues[1].toULong()
        }
        val matchC = """Register C: (\d+)""".toRegex().matchEntire(line)
        if (matchC != null) {
            initC = matchC.groupValues[1].toULong()
        }
        val matchProgram = """Program: (\d(?:,\d)+)""".toRegex().matchEntire(line)
        if (matchProgram != null) {
            program = matchProgram.groupValues[1].split(",").map(String::toInt)
        }
    }

    // same as above but return result on "out"
    fun run(initA: ULong): ULong {
        var pc = 0
        var a = initA
        var b = initB
        var c = initC

        fun combo(code: UInt): ULong {
            return when (code) {
                in 0U..3U -> code.toULong()
                4U -> a
                5U -> b
                6U -> c
                else -> throw RuntimeException("Reserved")
            }
        }

        val opcodes = listOf<(UInt) -> ULong?>(
            { a /= 1UL.shl(combo(it).toInt()); null }, // adv
            { b = b xor it.toULong(); null }, // bxl
            { b = combo(it).and(7UL); null }, // bst
            {
                if (a != 0UL) {
                    pc = it.toInt() - 2
                }
                null
            }, // jnz
            { b = b xor c; null }, // bxc
            { combo(it).and(7UL) }, // out
            { b = a / 1UL.shl(combo(it).toInt()); null }, //bdv
            { c = a / 1UL.shl(combo(it).toInt()); null }, //cdv
        )

        while (true) {
            val opcode = program[pc]
            val operand = program[pc + 1]
            val result = opcodes[opcode](operand.toUInt())
            if (result != null) return result
            pc += 2
        }
    }

    val bit = if (program.size == 6) 6 else 10
    val bitMask = 1UL.shl(bit) - 1UL
    val bitMaskA = bitMask.shr(3)
    // println("Bitmask: ${bitMask.toString(8)}($bitMask)")

    // result to list of aIn
    val resultMap = (0UL..bitMask).asSequence()
        .map {
            run(it) to it
        }
        .groupBy({ it.first }, { it.second })

    fun findMatch(a: ULong, program: List<Int>): ULong? {
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
