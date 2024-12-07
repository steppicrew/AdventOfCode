package aoc_2024.aoc_2024_05

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 5

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (143 to 123),
    0 to (6498 to 5017)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reRule = """(\d+)\|(\d+)""".toRegex()
    val reOrder = """\d+(?:,\d+)*""".toRegex()

    val allRules = lines.mapNotNull { line ->
        reRule.matchEntire(line)
    }
        .map { match ->
            val (x, y) = match.destructured
            x.toInt() to y.toInt()
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { (_, valueList) -> valueList.toSet() }

    val orders = lines.filter { line ->
        reOrder.matches(line)
    }
        .map { line ->
            line.split(",").map(String::toInt)
        }

    return orders
        .zip(orders.map { order ->
            // Build correct order
            //  - filter for rule keys contained in current order
            //  - sort by keys not contained in any following key's values
            val orderSet = order.toSet()
            allRules
                .filterKeys { orderSet.contains(it) }
                .asIterable()
                .sortedWith { a, b ->
                    when {
                        a.value.contains(b.key) -> -1
                        b.value.contains(a.key) -> 1
                        else -> 0
                    }
                }
                .map { it.key }
            // We do not need values not contained in left hand rules
            // .plus(orderSet.minus(allRules.keys))
        })
        // Filter for all matching orders
        .filter { (a, b) -> a.zip(b).all { it.first == it.second } }
        .sumOf { it.first[(it.first.size - 1) / 2] }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reRule = """(\d+)\|(\d+)""".toRegex()
    val reOrder = """\d+(?:,\d+)*""".toRegex()

    val allRules = lines.mapNotNull { line ->
        reRule.matchEntire(line)
    }
        .map { match ->
            val (x, y) = match.destructured
            x.toInt() to y.toInt()
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { (_, valueList) -> valueList.toSet() }

    val orders = lines.filter { line ->
        reOrder.matches(line)
    }
        .map { line ->
            line.split(",").map(String::toInt)
        }

    return orders
        .zip(orders.map { order ->
            // Build correct order
            //  - filter for rule keys contained in current order
            //  - sort by keys not contained in any following key's values
            val orderSet = order.toSet()
            allRules
                .filterKeys { orderSet.contains(it) }
                .asIterable()
                .sortedWith { a, b ->
                    when {
                        a.value.contains(b.key) -> -1
                        b.value.contains(a.key) -> 1
                        else -> 0
                    }
                }
                .map { it.key }
            // We do not need values not contained in left hand rules
            // .plus(orderSet.minus(allRules.keys))
        })
        // Filter for all mismatching orders
        .filter { (a, b) -> a.zip(b).any { it.first != it.second } }
        // Find the middle value by *first's* length (first may be longer than second)
        .sumOf { it.second[(it.first.size - 1) / 2] }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
