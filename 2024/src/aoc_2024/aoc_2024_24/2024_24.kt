package aoc_2024.aoc_2024_24

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 24

typealias ResultType = String

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to ("4" to "no result"),
    2 to ("2024" to "no result"),
    3 to ("9" to "z00,z01,z02,z05"),
    0 to ("51410244478064" to "gst,khg,nhn,tvb,vdc,z12,z21,z33"),
)

typealias Gate = Triple<String, String, String>

fun run1(input: InputData): ResultType {
    val reInitialValues = """(\w+): ([0|1])""".toRegex()
    val reGates = """(\w+) (AND|OR|XOR) (\w+) -> (\w+)""".toRegex()
    val values = input.lines.mapNotNull { line ->
        reInitialValues.matchEntire(line)
    }.associate {
        val (wire, value) = it.destructured
        wire to (value == "1")
    }.toMutableMap()

    val operations = mapOf<String, (Boolean, Boolean) -> Boolean>(
        "AND" to { w1, w2 -> w1 && w2 },
        "OR" to { w1, w2 -> w1 || w2 },
        "XOR" to { w1, w2 -> w1 != w2 },
    )

    fun boolToInt(value: Boolean): Int {
        return if (value) 1 else 0
    }

    val gates = input.lines.mapNotNull { line ->
        reGates.matchEntire(line)
    }.associate {
        val (wire1, operation, wire2, wireOut) = it.destructured
        wireOut to Triple(operation, wire1, wire2)
    }

    fun getValue(name: String): Boolean {
        return values.getOrPut(name) {
            val (operation, wire1, wire2) = gates[name]!!
            operations[operation]!!(getValue(wire1), getValue(wire2))
        }
    }

    val zValues =
        gates.keys.filter { it.startsWith("z") }.sortedDescending()
            .joinToString("") { boolToInt(getValue(it)).toString() }

    return zValues.toULong(2).toString()
}

fun run2(input: InputData): ResultType {
    val reGates = """(\w+) (AND|OR|XOR) (\w+) -> (\w+)""".toRegex()
    val operations = mapOf<String, (Boolean, Boolean) -> Boolean>(
        "AND" to { w1, w2 -> w1 && w2 },
        "OR" to { w1, w2 -> w1 || w2 },
        "XOR" to { w1, w2 -> w1 != w2 },
    )

    fun boolToString(value: Boolean): String {
        return if (value) "1" else "0"
    }

    fun stringToBool(value: String): Boolean {
        return value == "1"
    }

    fun pad(number: Int): String {
        return number.toString().padStart(2, '0')
    }

    val swapCount = if (input.ref > 0) 2 else 4

    val originalGates = input.lines.mapNotNull { line ->
        reGates.matchEntire(line)
    }.associate {
        val (wire1, operation, wire2, wireOut) = it.destructured
        wireOut to Triple(operation, wire1, wire2)
    }

    val maxBits = originalGates.values
        .flatMap { listOf(it.second, it.third) }
        .filter { it.startsWith("x") }
        .toSet().size
    val zBitMask = 1UL.shl(originalGates.keys.count { it.startsWith("z") }) - 1UL

    val verifyOperation: (ULong, ULong) -> ULong = when (input.ref) {
        0 -> { x, y -> x.plus(y).and(zBitMask) }
        3 -> { x, y -> x.and(y).and(zBitMask) }
        else -> return "no result"
    }


    fun wires(wire1: String, wire2: String): Pair<String, String> {
        return if (wire1 > wire2) wire2 to wire1 else wire1 to wire2
    }

    fun numberToInput(number: ULong, prefix: String): List<Pair<String, Boolean>> {
        return number.toString(2).padStart(maxBits, '0').reversed()
            .mapIndexed { index, char -> (prefix + pad(index)) to (char == '1') }
    }

    fun getGates(swap: Set<Pair<String, String>>): Map<String, Gate> {
        val swaps = (swap + swap.map {
            it.second to it.first
        }).toMap()
        return originalGates.map { (output, gate) ->
            output to (originalGates[swaps[output]] ?: gate)
        }.toMap()
    }

    fun getGetDependencies(gates: Map<String, Gate>): (String) -> Set<String> {
        val cache = mutableMapOf<String, Set<String>>()
        fun getDependencies(wire: String, round: Int): Set<String> {
            if (round > 100) throw RuntimeException("Circular dependency")
            return cache.getOrPut(wire) {
                val gate = gates[wire] ?: return@getOrPut setOf()
                val inputs =
                    setOf(gate.second, gate.third).filter { !it.startsWith("x") && !it.startsWith("y") }.toSet()
                inputs + inputs.flatMap { getDependencies(it, round + 1) }
            }
        }
        return { getDependencies(it, 0) }
    }

    val getOriginalDependencies = getGetDependencies(originalGates)

    fun solve(x: ULong, y: ULong, swap: Set<Pair<String, String>>): ULong? {
        val gates = getGates(swap)
        val values = (numberToInput(x, "x") + numberToInput(y, "y"))
            .toMap().toMutableMap()

        val getDependencies = getGetDependencies(gates)

        fun getValue(name: String): Boolean {
            return values.getOrPut(name) {
                val (operation, wire1, wire2) = gates[name]!!

                // Throws an exception if there is a circular dependency
                getDependencies(name)
                operations[operation]!!(getValue(wire1), getValue(wire2))
            }
        }

        try {
            val zValues =
                gates.keys.filter { it.startsWith("z") }.sortedDescending()
                    .joinToString("") { boolToString(getValue(it)) }
            return zValues.toULong(2)
        } catch (e: RuntimeException) {
            return null
        }
    }

    // Create a sequence of x and y values to test
    // Each x and y are set to 00b 01b 11b at each possible bit offset
    fun iterateXY(): Sequence<Triple<ULong, ULong, Int>> = sequence {
        val list01 = sequenceOf(0UL, 1UL)
        val list13 = sequenceOf(1UL, 3UL)

        list01.forEach { x -> list01.forEach { y -> yield(Triple(x, y, 0)) } }

        (1 until maxBits - 1).forEach { shiftBits ->
            list13.map { it.shl(shiftBits) }.forEach { x ->
                list13.map { it.shl(shiftBits) }.forEach { y ->
                    yield(Triple(x, y, shiftBits))
                }
            }
        }
    }

    var swapCandidates: Set<Set<Pair<String, String>>>? = null

    iterateXY().forEach { (x, y, shiftBits) ->
        val zTarget = verifyOperation(x, y)
        val z = solve(x, y, setOf())!!
        if (z == zTarget) return@forEach

        val wrongOutputGates = z.xor(zTarget).toString(2).reversed().mapIndexed { index, bit ->
            index to stringToBool(bit.toString())
        }.filter { it.second }.map { it.first }
        val depends = wrongOutputGates.map { "z" + pad(it) }.map { getOriginalDependencies(it) + it }
        val swaps = depends.flatMapIndexed { index, dependencies1 ->
            depends.drop(index + 1).flatMap { dependencies2 ->
                dependencies1.flatMap { dependency1 ->
                    dependencies2.map { dependency2 ->
                        wires(dependency1, dependency2)
                    }.filter {
                        solve(x, y, setOf(it)) == zTarget
                    }
                }
            }
        }

        // Swaps could be empty if we have more than two outputs to be swapped
        // Skip those and hope to catch them anyway later
        if (swaps.isEmpty()) return@forEach

        if (swapCandidates == null) {
            swapCandidates = swaps.map { setOf(it) }.toSet()
            return@forEach
        }

        swapCandidates = swapCandidates!!.flatMap { previousSwaps ->
            val previouslySwappedWires = previousSwaps
                .fold(setOf<String>()) { acc, swap -> acc + swap.first + swap.second }

            // A swap must be already known or no wire should be part of any previous swap
            swaps.filter { swap ->
                swap in previousSwaps || (
                        swap.first !in previouslySwappedWires &&
                                swap.second !in previouslySwappedWires &&
                                solve(x, y, previousSwaps + swap) == zTarget
                        )
            }.map { previousSwaps + it }
        }.filterNot { it.size > swapCount }.toSet()
        input.log("possible swaps: ${swapCandidates!!.size} (Bits: $shiftBits)")
    }

    return (swapCandidates ?: return "no result")
        // find first matching swapCount that satisfies all tests
        .first { possibleSwap ->
            possibleSwap.size == swapCount &&
                    iterateXY().all { (x, y, _) ->
                        verifyOperation(x, y) == solve(x, y, possibleSwap)
                    }
        }
        // flatten
        .flatMap { listOf(it.first, it.second) }
        // sort
        .sorted()
        // ...and join
        .joinToString(",")
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS, quiet = true)
}
