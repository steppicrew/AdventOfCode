package aoc_2015.aoc_2015_24

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 24

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (99 to null)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val allWeights = lines.map { it.toInt() }.sorted()
    val sum = allWeights.sum()
    val sumThird = sum / 3

    fun findGroups(weights: List<Int>, sum: Int): List<Pair<List<Int>, List<Int>>>? {
        val weightCandidates = weights.filter { it <= sum }
        if (weightCandidates.isEmpty()) {
            return null
        }
        val result = weightCandidates.mapIndexed { index, weight ->
            val remainingWeights = weights.fil
            if (weight == sum) {
                listOf(listOf(weight) to remainingWeights)
            } else {
                findGroups(remainingWeights, sum - weight)?.map {
                    (listOf(weight) + it.first) to it.second
                }
            }
        }.filterNotNull().flatten()
        if (result.isEmpty()) return null
        return result
    }

    val groups1 = findGroups(allWeights, sumThird)

    return lines.count()
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    return lines.count()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
