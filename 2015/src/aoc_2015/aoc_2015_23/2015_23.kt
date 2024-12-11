package aoc_2015.aoc_2015_23

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 23

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (255 to 334)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var prog = 0

    val registers = mutableMapOf<String, Int>()

    val commands = mapOf<String, (parameter: List<String>) -> Unit>(
        "hlf" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) / 2; prog++ },
        "tpl" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) * 3; prog++ },
        "inc" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) + 1; prog++ },
        "jmp" to { prog += it.first().toInt() },
        "jie" to { if (registers.getOrDefault(it.first(), 0) % 2 == 0) prog += it[1].toInt() else prog++ },
        "jio" to { if (registers.getOrDefault(it.first(), 0) == 1) prog += it[1].toInt() else prog++ },
    )

    val reSpit = """,?\s+""".toRegex()
    val program = lines.map {
        val parts = it.split(reSpit)
        parts.first() to parts.drop(1)
    }

    while (program.indices.contains(prog)) {
        val command = program[prog]
        commands[command.first]!!(command.second)
    }

    return registers["b"]!!
}


fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    var prog = 0

    val registers = mutableMapOf("a" to 1)

    val commands = mapOf<String, (parameter: List<String>) -> Unit>(
        "hlf" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) / 2; prog++ },
        "tpl" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) * 3; prog++ },
        "inc" to { registers[it.first()] = registers.getOrDefault(it.first(), 0) + 1; prog++ },
        "jmp" to { prog += it.first().toInt() },
        "jie" to { if (registers.getOrDefault(it.first(), 0) % 2 == 0) prog += it[1].toInt() else prog++ },
        "jio" to { if (registers.getOrDefault(it.first(), 0) == 1) prog += it[1].toInt() else prog++ },
    )

    val reSpit = """,?\s+""".toRegex()
    val program = lines.map {
        val parts = it.split(reSpit)
        parts.first() to parts.drop(1)
    }

    while (program.indices.contains(prog)) {
        val command = program[prog]
        commands[command.first]!!(command.second)
    }

    return registers["b"]!!
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
