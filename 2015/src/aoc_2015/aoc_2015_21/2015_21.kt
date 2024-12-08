package aoc_2015.aoc_2015_21

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO
import kotlin.math.max

const val YEAR = 2015
const val DAY = 21

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (121 to 201)
)

fun playGame(me: Pair<Int, Pair<Int, Int>>, boss: Pair<Int, Pair<Int, Int>>): Boolean {
    val myDamage = max(1, me.second.first - boss.second.second)
    val myHitCount = (boss.first - 1) / myDamage
    val bossDamage = max(1, boss.second.first - me.second.second)
    val bossHitCount = (me.first - 1) / bossDamage
    return myHitCount <= bossHitCount
}

val weapons = listOf(
    8 to (4 to 0),
    10 to (5 to 0),
    25 to (6 to 0),
    40 to (7 to 0),
    74 to (8 to 0)
)

val armors = listOf(
    0 to (0 to 0),
    13 to (0 to 1),
    31 to (0 to 2),
    53 to (0 to 3),
    75 to (0 to 4),
    102 to (0 to 5)
)

val rings = listOf(
    0 to (0 to 0),
    0 to (0 to 0),
    25 to (1 to 0),
    50 to (2 to 0),
    100 to (3 to 0),
    20 to (0 to 1),
    40 to (0 to 2),
    80 to (0 to 3),
)

val boss = 103 to (9 to 2)

fun add(items: List<Pair<Int, Pair<Int, Int>>>): Pair<Int, Int> {
    return items.map { it.second }.reduce { acc, item -> (acc.first + item.first) to (acc.second + item.second) }
}

fun addGold(items: List<Pair<Int, Pair<Int, Int>>>): Int {
    return items.map { it.first }.sum()
}

fun run1(
    @Suppress("UNUSED_PARAMETER") lines: List<String>,
    @Suppress("UNUSED_PARAMETER") log: (String) -> Unit
): ResultType {
    return weapons.flatMap { weapon ->
        armors.flatMap { armor ->
            rings.flatMapIndexed { ring1Index, ring1 ->
                rings.filterIndexed { ring2Index, _ -> ring1Index != ring2Index }
                    .map { ring2 ->
                        val me = 100 to add(listOf(weapon, armor, ring1, ring2))
                        if (playGame(me, boss)) addGold(listOf(weapon, armor, ring1, ring2)) else null
                    }
            }
        }
    }.filterNotNull().min()
}

fun run2(
    @Suppress("UNUSED_PARAMETER") lines: List<String>,
    @Suppress("UNUSED_PARAMETER") log: (String) -> Unit
): ResultType {
    return weapons.flatMap { weapon ->
        armors.flatMap { armor ->
            rings.flatMapIndexed { ring1Index, ring1 ->
                rings.filterIndexed { ring2Index, _ -> ring1Index != ring2Index }
                    .map { ring2 ->
                        val me = 100 to add(listOf(weapon, armor, ring1, ring2))
                        if (playGame(me, boss)) null else addGold(listOf(weapon, armor, ring1, ring2))
                    }
            }
        }
    }.filterNotNull().max()
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
