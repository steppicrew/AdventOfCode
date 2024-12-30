package aoc_2015.aoc_2015_13

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 13

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (330 to 286),
    0 to (618 to 601)
)

fun <T> permutationsSequence(list: List<T>): Sequence<List<T>> = sequence {
    if (list.isEmpty()) { // Base case
        yield(emptyList())
        return@sequence
    }

    for (element in list) {
        val remaining = list - element
        for (permutation in permutationsSequence(remaining)) {
            yield(listOf(element) + permutation)
        }
    }
}


fun run1(input: InputData): ResultType {
    val reSentence = """(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).""".toRegex()

    val map = input.lines
        .mapNotNull { reSentence.matchEntire(it) }
        .map { match ->
            val (subject, verb, value, obj) = match.destructured
            subject to (obj to value.toInt().let { if (verb == "gain") it else -it })
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { it.value.toMap() }

    return permutationsSequence(map.keys.toList())
        .maxOf { list ->
            list
                .plus(list.first())
                .zipWithNext()
                .sumOf { map[it.first]!![it.second]!! + map[it.second]!![it.first]!! }
        }
}

fun run2(input: InputData): ResultType {
    val reSentence = """(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).""".toRegex()

    val map = input.lines
        .mapNotNull { reSentence.matchEntire(it) }
        .map { match ->
            val (subject, verb, value, obj) = match.destructured
            subject to (obj to value.toInt().let { if (verb == "gain") it else -it })
        }
        .groupBy({ it.first }, { it.second })
        .mapValues { it.value.toMap().plus("Me" to 0) }
        .let {
            it.plus("Me" to it.keys.associateWith { 0 })
        }

    return permutationsSequence(map.keys.toList())
        .maxOf { list ->
            list.plus(list.first())
                .zipWithNext()
                .sumOf { map[it.first]!![it.second]!! + map[it.second]!![it.first]!! }
        }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
