package aoc_2015.aoc_2015_04

import aoc_2015.tools.simpleIO
import java.security.MessageDigest

const val YEAR = 2015
const val DAY = 4

val EXPECTED_RESULTS = listOf(
    0 to (282749 to 9962624)
)

fun md5Hex(input: String): String {
    val md = MessageDigest.getInstance("MD5")
    val digest = md.digest(input.toByteArray()) // Calculate MD5 hash
    return digest.joinToString("") { "%02x".format(it) } // Convert to hexadecimal format
}

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    for (i in generateSequence(1) { it + 1 }) {
        val md5 = md5Hex(lines[0] + i.toString())
        if (md5.startsWith("00000")) return i
    }
    return 0
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    for (i in generateSequence(1) { it + 1 }) {
        val md5 = md5Hex(lines[0] + i.toString())
        if (md5.startsWith("000000")) return i
    }
    return 0
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
