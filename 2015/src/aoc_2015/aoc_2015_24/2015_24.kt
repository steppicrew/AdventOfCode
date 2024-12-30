package aoc_2015.aoc_2015_24

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 24

typealias ResultType = Long

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (99L to 44L),
    0 to (10439961859L to 72050269L)
)

fun run1(input: InputData): ResultType {
    val allWeights = input.lines.map(String::toInt).sorted().reversed()
    val sum = allWeights.sum()
    val sumThird = sum / 3

    fun findGroups(
        weights: List<Int>,
        sum: Int,
        remainingGroups: Int,
        size: Int = 0
    ): List<Pair<List<Int>, List<Int>>>? {
        if (size > weights.size / remainingGroups) return null
        val weightCandidates = weights.filter { it <= sum }
        if (weightCandidates.isEmpty()) {
            return null
        }
        val result = weightCandidates.mapIndexed { index, weight ->
            val remainingWeights = weights.drop(index + 1)
            if (weight == sum) {
                listOf(listOf(weight) to remainingWeights)
            } else {
                findGroups(remainingWeights, sum - weight, remainingGroups, size + 1)?.map {
                    (listOf(weight) + it.first) to it.second
                }
            }
        }.filterNotNull().flatten()
        if (result.isEmpty()) return null
        return result
    }

    val groups1 = findGroups(allWeights, sumThird, 2)?.filter { (_, remaining) ->
        findGroups(remaining, sumThird, 1) != null
    }?.map { it.first }!!
    val minGroup1Length = groups1.minOf { it.size }
    return groups1.filter { it.size == minGroup1Length }.minOf { it.map(Int::toLong).reduce { prod, i -> prod * i } }
}

fun run2(input: InputData): ResultType {
    val allWeights = input.lines.map(String::toInt).sorted().reversed()
    val sum = allWeights.sum()
    val sumQuarter = sum / 4

    fun findGroups(
        weights: List<Int>,
        sum: Int,
        remainingGroups: Int,
        size: Int = 0
    ): List<Pair<List<Int>, List<Int>>>? {
        if (size > weights.size / remainingGroups) return null
        val weightCandidates = weights.filter { it <= sum }
        if (weightCandidates.isEmpty()) {
            return null
        }
        val result = weightCandidates.mapIndexed { index, weight ->
            val remainingWeights = weights.drop(index + 1)
            if (weight == sum) {
                listOf(listOf(weight) to remainingWeights)
            } else {
                findGroups(remainingWeights, sum - weight, remainingGroups, size + 1)?.map {
                    (listOf(weight) + it.first) to it.second
                }
            }
        }.filterNotNull().flatten()
        if (result.isEmpty()) return null
        return result
    }

    val groups1 = findGroups(allWeights, sumQuarter, 3)?.filter { (_, remaining) ->
        findGroups(remaining, sumQuarter, 2)?.any { (_, remaining) ->
            findGroups(
                remaining,
                sumQuarter,
                1
            ) != null
        } != null
    }?.map { it.first }!!
    val minGroup1Length = groups1.minOf { it.size }
    return groups1.filter { it.size == minGroup1Length }.minOf { it.map(Int::toLong).reduce { prod, i -> prod * i } }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
