package aoc_2024.aoc_2024_23

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 23

typealias ResultType = String

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to ("7" to "co,de,ka,ta"),
    0 to ("1156" to "bx,cx,dr,dx,is,jg,km,kt,li,lt,nh,uf,um"),
)


fun run1(input: InputData): ResultType {
    val pairs = input.lines.map {
        val pair = it.split("-").sorted()
        pair.first() to pair.last()
    }

    val firsts = pairs.groupBy({ it.first }, { it.second }).mapValues { it.value.toSet() }
    val triplets = mutableSetOf<Triple<String, String, String>>()

    firsts.forEach { (first, connectedTo) ->
        connectedTo.forEach inner@{ second ->
            val f = firsts[second] ?: return@inner
            val common = f.intersect(connectedTo)
            if (common.isNotEmpty()) {
                common.forEach {
                    triplets.add(Triple(first, second, it))
                }
            }
        }
    }

    return triplets
        .count { it.first.startsWith("t") || it.second.startsWith("t") || it.third.startsWith("t") }
        .toString()
}

fun run2(input: InputData): ResultType {
    val nodeNeighbours = mutableMapOf<String, Set<String>>()
    input.lines.forEach {
        val pair = it.split("-")
        val first = pair.first()
        val second = pair.last()
        nodeNeighbours[first] = (nodeNeighbours[first] ?: setOf()) + second
        nodeNeighbours[second] = (nodeNeighbours[second] ?: setOf()) + first
    }

    val fullyConnectedSubgraphs = nodeNeighbours.map { (node, neighbours) ->
        val subgraph = mutableSetOf(node)
        neighbours.forEach { neighbour ->
            if (nodeNeighbours[neighbour]!!.containsAll(subgraph)) {
                subgraph.add(neighbour)
            }
        }
        subgraph.toSet()
    }.toSet()

    return fullyConnectedSubgraphs.maxBy { it.size }.toList().sorted().joinToString(",")
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
