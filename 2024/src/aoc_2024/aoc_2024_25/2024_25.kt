package aoc_2024.aoc_2024_25

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 25

typealias ResultType = Int

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (3 to null),
    0 to (null to null),
)


fun run1(input: InputData): ResultType {
    val keyLocks = input.lines.chunked(8).mapNotNull { chunk ->
        val first = chunk.firstOrNull() ?: return@mapNotNull null
        first.mapIndexed { col, _ ->
            chunk.filter { it.isNotEmpty() }.map { it[col] }
                .count { it == first[col] } * (if (first[0] == '#') 1 else -1)
        }
    }
    val keys = keyLocks.filter { it.first() < 0 }
    val locks = keyLocks.filter { it.first() > 0 }

    return keys.sumOf { key ->
        locks.count { lock ->
            lock.zip(key).all { it.first + it.second <= 0 }
        }
    }
}

fun run2(input: InputData): ResultType {
    val keyLocks = input.lines.chunked(8).mapNotNull { chunk ->
        val first = chunk.firstOrNull() ?: return@mapNotNull null
        first.mapIndexed { col, _ ->
            chunk.filter { it.isNotEmpty() }.map { it[col] }
                .count { it == first[col] } * (if (first[0] == '#') 1 else -1)
        }
    }
    val keys = keyLocks.filter { it.first() < 0 }
    val locks = keyLocks.filter { it.first() > 0 }

    return keys.sumOf { key ->
        locks.count { lock ->
            lock.zip(key).all { it.first + it.second <= 0 }
        }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
