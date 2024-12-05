package aoc_2024.aoc_2024_05

import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 5

val EXPECTED_RESULTS = listOf(
    1 to (143 to 123),
    0 to (6498 to 5017)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reRule = """(\d+)\|(\d+)""".toRegex()
    val reOrder = """\d+(?:,\d+)*""".toRegex()

    val orders = lines.filter { line ->
        reOrder.matches(line)
    }
        .map { line ->
            line.split(",").map(String::toInt)
        }

    val allRules = lines.mapNotNull { line ->
        reRule.matchEntire(line)
    }
        .map { match ->
            val (x, y) = match.destructured
            x.toInt() to y.toInt()
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { (_, valueList) -> valueList.toSet() }

    fun getRules(order: List<Int>): Map<Int, Set<Int>> {
        val validNumbers = order.toSet()
        return allRules.filterKeys { validNumbers.contains(it) }.mapValues { validNumbers.intersect(it.value) }
    }

    fun getOrder(order: List<Int>): List<Int> {
        val rules = getRules(order).toMutableMap()
        val pageOrder = mutableListOf<Int>()
        var allLarger = setOf<Int>()
        while (rules.isNotEmpty()) {
            allLarger = rules.values.reduce { acc, set -> acc + set }
            val notInLargerList = rules.keys.filter { !allLarger.contains(it) }
            if (notInLargerList.isEmpty()) {
                println("Error")
                println(pageOrder)
                println(allLarger)
                println(rules)
            }
            val notInLarger = rules.keys.first { !allLarger.contains(it) }
            pageOrder.add(notInLarger)
            rules.remove(notInLarger)
        }
        pageOrder.addAll(allLarger)
        return pageOrder
    }

    fun filterOrders(order: List<Int>): Boolean {
        var remaining = getOrder(order)
        for (n in order) {
            val i = remaining.indexOf(n)
            if (i < 0) {
                return false
            }
            remaining = remaining.subList(i, remaining.size)
        }
        return true
    }

    val validOrders = orders.filter(::filterOrders)
    val result = validOrders.map { order ->
        order[(order.size - 1) / 2]
    }

    return result.sum()
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): Int {
    val reRule = """(\d+)\|(\d+)""".toRegex()
    val reOrder = """\d+(?:,\d+)*""".toRegex()

    val orders = lines.filter { line ->
        reOrder.matches(line)
    }
        .map { line ->
            line.split(",").map(String::toInt)
        }

    val allRules = lines.mapNotNull { line ->
        reRule.matchEntire(line)
    }
        .map { match ->
            val (x, y) = match.destructured
            x.toInt() to y.toInt()
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { (_, valueList) -> valueList.toSet() }

    fun getRules(order: List<Int>): Map<Int, Set<Int>> {
        val validNumbers = order.toSet()
        return allRules.filterKeys { validNumbers.contains(it) }.mapValues { validNumbers.intersect(it.value) }
    }

    fun getOrder(order: List<Int>): List<Int> {
        val rules = getRules(order).toMutableMap()
        val pageOrder = mutableListOf<Int>()
        var allLarger = setOf<Int>()
        while (rules.isNotEmpty()) {
            allLarger = rules.values.reduce { acc, set -> acc + set }
            val notInLargerList = rules.keys.filter { !allLarger.contains(it) }
            if (notInLargerList.isEmpty()) {
                println("Error")
                println(pageOrder)
                println(allLarger)
                println(rules)
            }
            val notInLarger = rules.keys.first { !allLarger.contains(it) }
            pageOrder.add(notInLarger)
            rules.remove(notInLarger)
        }
        pageOrder.addAll(allLarger)
        return pageOrder
    }

    fun filterOrders(order: List<Int>): Boolean {
        var remaining = getOrder(order)
        for (n in order) {
            val i = remaining.indexOf(n)
            if (i < 0) {
                return true
            }
            remaining = remaining.subList(i, remaining.size)
        }
        return false
    }

    val validOrders = orders.filter(::filterOrders)
    val result = validOrders.map { getOrder(it) }.map { order ->
        order[(order.size - 1) / 2]
    }

    return result.sum()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
