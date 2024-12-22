package aoc_2024.aoc_2024_22

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 22

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (37327623L to 24L),
    2 to (37990510L to 23L),
    0 to (13764677935L to 1619L),
)

val prune = 16777216L

fun run1(input: InputData): ResultType {
    val rounds = 2000

    fun generate(seed: Long): Sequence<Long> = generateSequence(seed) { random ->
        (random.shl(6).xor(random) % prune)
            .let { secret ->
                secret.shr(5).xor(secret) % prune
            }.let { secret ->
                secret.shl(11).xor(secret) % prune
            }
    }

    return input.lines.sumOf { line ->
        generate(line.toLong()).elementAt(rounds)
    }
}

fun run2(input: InputData): ResultType {
    val rounds = 2000

    fun generate(seed: Long): Sequence<Long> = generateSequence(seed) { random ->
        (random.shl(6).xor(random) % prune)
            .let { secret ->
                secret.shr(5).xor(secret) % prune
            }.let { secret ->
                secret.shl(11).xor(secret) % prune
            }
    }

    val prices = input.lines.map { line ->
        generate(line.toLong()).take(rounds).map { (it % 10).toInt() }
    }

    val changes = prices.map {
        it.zipWithNext { r1, r2 -> r2 - r1 }
    }

    val sequenceMaps = changes.zip(prices.map { it.toList() })
        .map { (change, price) ->
            val sequenceMap = mutableMapOf<String, Int>()
            change.windowed(4).forEachIndexed { index, window ->
                val key = window.joinToString()
                sequenceMap.putIfAbsent(key, price[index + 4])
            }
            sequenceMap.toMap()
        }

    return sequenceMaps
        .fold(setOf<String>()) { acc, map -> acc + map.keys }
        .maxOf { sequence ->
            sequenceMaps.sumOf { it[sequence] ?: 0 }
        }.toLong()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
