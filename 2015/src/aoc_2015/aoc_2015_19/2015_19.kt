package aoc_2015.aoc_2015_19

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.InputData
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 19

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (4 to 3),
    2 to (7 to 6),
    0 to (535 to 212)
)

fun run1(input: InputData): ResultType {
    val reReplacement = """(\w+) => (\w+)""".toRegex()
    val reInput = """\w+""".toRegex()

    val replacements = input.lines
        .mapNotNull { reReplacement.matchEntire(it) }
        .map { match ->
            val (from, to) = match.destructured
            from to to
        }

    val input = input.lines.first { reInput.matches(it) }

    return replacements.flatMap { (from, to) ->
        from.toRegex().findAll(input).map { match ->
            val range = match.range
            "${input.substring(0, range.first)}${to}${input.substring(range.last + 1)}"
        }
    }.toSet().size
}

fun run2(input: InputData): ResultType {
    val reReplacement = """(\w+) => (\w+)""".toRegex()
    val reInput = """\w+""".toRegex()

    val allReplacements = input.lines
        .mapNotNull { reReplacement.matchEntire(it) }
        .map { match ->
            val (from, to) = match.destructured
            from to to
        }

    val replacements = allReplacements.filter { it.first != "e" }
    val eReplacements = allReplacements.filter { it.first == "e" }.map { it.second }.toSet()

    val startMolecule = input.lines.first { reInput.matches(it) }

    fun getCounts(molecule: String, replacement: Pair<String, String>): Pair<Int, String> {
        return molecule.replace(replacement.second, ".").count { it == '.' } to molecule.replace(
            replacement.second,
            replacement.first
        )
    }

    fun getCounts2(
        molecule: String,
        replacement1: Pair<String, String>,
        replacement2: Pair<String, String>
    ): Pair<Int, String> {
        val value1 = getCounts(molecule, replacement1)
        val value2 = getCounts(value1.second, replacement2)
        return (value1.first + value2.first) to value2.second
    }

    fun replace(molecule: String): Int {
        if (eReplacements.contains(molecule)) {
            return 1
        } else {
            val replacementCandidates = replacements.filter { molecule.contains(it.second) }
                .sortedByDescending { it.second.length }

            fun getResult(candidates: List<Pair<String, String>>): Int {
                val result = candidates.map { replacement ->
                    val (count, restMolecule) = getCounts(molecule, replacement)
                    replace(restMolecule) + count
                }.filter { it > 0 }
                return if (result.isEmpty()) 0 else result.min()
            }

            // Test if there is any candidate that can be used with any other candidate in any order
            if (replacementCandidates.size > 1) {
                for (firstCandidate in replacementCandidates) {
                    if (replacementCandidates.filter { it.second == firstCandidate.second }
                            .all {
                                getCounts2(molecule, it, firstCandidate) == getCounts2(
                                    molecule,
                                    firstCandidate,
                                    it
                                )
                            }
                    ) {
                        return getResult(listOf(firstCandidate))
                    }
                }
            }
            return getResult(replacementCandidates)
        }
    }

    return replace(startMolecule)
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
