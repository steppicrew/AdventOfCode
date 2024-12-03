package aoc_2024.aoc_2024_03

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 3
const val REF = 0

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val re = "mul\\((\\d+),(\\d+)\\)".toRegex()

    val result = re.findAll(lines.joinToString(""))
        .sumOf { it.groupValues[1].toInt() * it.groupValues[2].toInt() }

    return result
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reDo = "do\\(\\)".toRegex()
    val reDoNot = "don't\\(\\)".toRegex()
    val reMul = "mul\\((\\d+),(\\d+)\\)".toRegex()

    val result = lines.joinToString("")
        .split(reDo)
        .sumOf { doPart ->
            reMul.findAll(doPart.split(reDoNot, 2)[0])
                .sumOf { it.groupValues[1].toInt() * it.groupValues[2].toInt() }
        }

    return result
}

fun main() {
    simpleIO(YEAR, DAY, 1, REF, ::run1)
    simpleIO(YEAR, DAY, 2, REF, ::run2)
}
