package aoc_2015.aoc_2015_07

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 7

typealias ResultType = UShort

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (46065.toUShort() to 14134.toUShort())
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reCommands = mapOf(
        """(\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first },
        """(\w+) AND (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first and inputs.second },
        """(\w+) OR (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first or inputs.second },
        """(\w+) LSHIFT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort {
            return (inputs.first.toInt() shl inputs.second.toInt()).toUShort()
        },
        """(\w+) RSHIFT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort {
            return (inputs.first.toInt() shr inputs.second.toInt()).toUShort()
        },
        """NOT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first.inv() },
    )

    val reNumber = """\d+""".toRegex()

    val rules = lines.mapNotNull { line ->
        val command = reCommands.keys.first { it.matches(line) }
        val match = command.matchEntire(line)
        if (match != null) {
            val output = match.groupValues.last()
            val inputs = match.groupValues[1] to (if (match.groupValues.size > 3) match.groupValues[2] else "0")
            output to (inputs to command)
        } else {
            null
        }
    }.toMap()

    val cache = mutableMapOf<String, UShort>()

    fun getOutput(name: String): UShort {
        val cachedResult = cache[name]
        if (cachedResult != null) {
            return cachedResult
        }

        fun getInput(input: String): UShort {
            return if (reNumber.matches(input)) {
                input.toUShort()
            } else {
                getOutput(input)
            }
        }

        val (inputs, command) = rules[name] ?: throw RuntimeException("Rule must not be null ($name)")
        val commandFn = reCommands[command] ?: throw RuntimeException("Unknown command ($command)")
        val result = commandFn(getInput(inputs.first) to getInput(inputs.second))
        cache[name] = result
        return result
    }

    return getOutput("a")
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reCommands = mapOf(
        """(\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first },
        """(\w+) AND (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first and inputs.second },
        """(\w+) OR (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first or inputs.second },
        """(\w+) LSHIFT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort {
            return (inputs.first.toInt() shl inputs.second.toInt()).toUShort()
        },
        """(\w+) RSHIFT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort {
            return (inputs.first.toInt() shr inputs.second.toInt()).toUShort()
        },
        """NOT (\w+) -> (\w+)""".toRegex() to fun(inputs: Pair<UShort, UShort>): UShort { return inputs.first.inv() },
    )

    val reNumber = """\d+""".toRegex()

    val rules = lines.mapNotNull { line ->
        val command = reCommands.keys.first { it.matches(line) }
        val match = command.matchEntire(line)
        if (match != null) {
            val output = match.groupValues.last()
            val inputs = match.groupValues[1] to (if (match.groupValues.size > 3) match.groupValues[2] else "0")
            output to (inputs to command)
        } else {
            null
        }
    }.toMap().toMutableMap()

    val cache = mutableMapOf<String, UShort>()

    fun getOutput(name: String): UShort {
        val cachedResult = cache[name]
        if (cachedResult != null) {
            return cachedResult
        }

        fun getInput(input: String): UShort {
            return if (reNumber.matches(input)) {
                input.toUShort()
            } else {
                getOutput(input)
            }
        }

        val (inputs, command) = rules[name] ?: throw RuntimeException("Rule must not be null ($name)")
        val commandFn = reCommands[command] ?: throw RuntimeException("Unknown command ($command)")
        val result = commandFn(getInput(inputs.first) to getInput(inputs.second))
        cache[name] = result
        return result
    }

    val a = getOutput("a")
    rules["b"] = (a.toString() to "0") to reCommands.keys.first { it.matches("0 -> b") }
    cache.clear()
    return getOutput("a")
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
