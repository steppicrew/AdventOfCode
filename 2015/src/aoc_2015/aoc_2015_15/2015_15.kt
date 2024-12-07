package aoc_2015.aoc_2015_15

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO
import kotlin.math.max

const val YEAR = 2015
const val DAY = 15

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (62842880 to 57600000),
    0 to (222870 to 117936)
)

fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reIngredients =
        """\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories -?\d+""".toRegex()

    val scores = lines
        .mapNotNull { reIngredients.matchEntire(it) }
        .map { match ->
            match.destructured.toList().map(String::toInt)
        }

    fun getMixtures(max: Int, ingredientCount: Int): Sequence<List<Int>> = sequence {
        if (ingredientCount == 1) {
            yield(listOf(max))
            return@sequence
        }

        for (spoons in 0..max) {
            for (other in getMixtures(max - spoons, ingredientCount - 1)) {
                yield(listOf(spoons) + other)
            }
        }
    }

    return getMixtures(100, scores.size)
        .maxOf { spoons ->
            spoons
                .zip(scores)
                .map { (spoons, ingredientScores) ->
                    ingredientScores.map { it * spoons }
                }
                .reduce { acc, current ->
                    acc.zip(current).map { it.first + it.second }
                }
                .fold(1) { product, i -> product * max(i, 0) }
        }
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val reIngredients =
        """\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)""".toRegex()

    val scores = lines
        .mapNotNull { reIngredients.matchEntire(it) }
        .map { match ->
            match.destructured.toList().map(String::toInt)
        }

    fun getMixtures(max: Int, ingredientCount: Int): Sequence<List<Int>> = sequence {
        if (ingredientCount == 1) {
            yield(listOf(max))
            return@sequence
        }

        for (spoons in 0..max) {
            for (other in getMixtures(max - spoons, ingredientCount - 1)) {
                yield(listOf(spoons) + other)
            }
        }
    }

    return getMixtures(100, scores.size)
        .map { spoons ->
            spoons
                .zip(scores)
                .map { (spoons, ingredientScores) ->
                    ingredientScores.map { it * spoons }
                }
                .reduce { acc, current ->
                    acc.zip(current).map { it.first + it.second }
                }
        }
        .filter { it.last() == 500 }
        .maxOf {
            it.dropLast(1).fold(1) { product, i -> product * max(i, 0) }
        }

}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
