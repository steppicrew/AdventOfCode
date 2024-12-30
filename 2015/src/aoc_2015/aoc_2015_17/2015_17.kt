package aoc_2015.aoc_2015_17

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 17

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (null to null)
)

fun run1(input: InputData): ResultType {
    val containers = input.lines.map(String::toInt)

    fun fill(liter: Int, containers: List<Int>): List<List<Int>>? {
        if (liter == 0) {
            return listOf(listOf())
        }
        val containersLeft = containers.filter { it <= liter }
        if (containersLeft.sum() < liter) {
            return null
        }
        return containersLeft.mapIndexedNotNull { index, container ->
            fill(liter - container, containersLeft.drop(index + 1))?.map { listOf(container) + it }
        }.flatten()
    }

    return fill(150, containers)!!.size
}

fun run2(input: InputData): ResultType {
    val containers = input.lines.map(String::toInt)

    fun fill(liter: Int, containers: List<Int>): List<List<Int>>? {
        if (liter == 0) {
            return listOf(listOf())
        }
        val containersLeft = containers.filter { it <= liter }
        if (containersLeft.sum() < liter) {
            return null
        }
        return containersLeft.mapIndexedNotNull { index, container ->
            fill(liter - container, containersLeft.drop(index + 1))?.map { listOf(container) + it }
        }.flatten()
    }

    val combinations = fill(150, containers)!!
    val minCount = combinations.minOf { it.size }
    return combinations.count { it.size == minCount }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
