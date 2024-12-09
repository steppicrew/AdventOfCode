package aoc_2015.aoc_2015_22

import aoc_2015.tools.ExpectedRefResults
import aoc_2015.tools.simpleIO

const val YEAR = 2015
const val DAY = 22

typealias ResultType = Int

val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    0 to (1824 to 1937)
)

class Magic(
    val name: String,
    val cost: Int,
    val duration: Int = 1,
    val addMana: Int = 0,
    val instantHeal: Int = 0,
    val armor: Int = 0,
    val damage: Int = 0,
    val instantDamage: Int = 0
) {
    override fun toString(): String {
        return name
    }
}

val allMagics = listOf(
    Magic(name = "Magic Missile", duration = 0, cost = 53, instantDamage = 4),
    Magic(name = "Drain", duration = 0, cost = 73, instantHeal = 2, instantDamage = 2),
    Magic(name = "Shield", cost = 113, duration = 6, armor = 7),
    Magic(name = "Poison", cost = 173, duration = 6, damage = 3),
    Magic(name = "Recharge", cost = 229, duration = 5, addMana = 101),
)

class Player(
    private var hit: Int,
    private val armor: Int = 0,
    private val damage: Int = 0,
    private var mana: Int = 0,
) {
    private var magic: Map<Magic, Int> = mapOf()
    private var totalManaLoss: Int = 0
    private var roundArmor: Int = armor

    fun newRound(opponent: Player) {
        if (lost || opponent.lost) {
            return
        }
        mana += magic.keys.sumOf { it.addMana }
        roundArmor = armor + magic.keys.sumOf { it.armor }
        opponent.hit -= magic.keys.sumOf { it.damage }
        magic = magic.mapValues { it.value - 1 }.filterValues { it > 0 }
    }

    fun decHit(opponent: Player) {
        if (lost || opponent.lost) {
            return
        }
        hit -= 1
    }

    fun clone(): Player {
        val player = Player(hit = hit, armor = armor, damage = damage, mana = mana)
        player.totalManaLoss = totalManaLoss
        player.magic = magic
        player.roundArmor = roundArmor
        return player
    }

    fun getAllowedMagics(): List<Magic> {
        return allMagics.filter { it.cost <= mana && !magic.containsKey(it) }
    }

    fun addMagic(newMagic: Magic, opponent: Player) {
        if (lost || opponent.lost) {
            return
        }
        mana -= newMagic.cost
        totalManaLoss += newMagic.cost
        opponent.hit -= newMagic.instantDamage
        hit += newMagic.instantHeal

        if (newMagic.duration > 0) {
            magic = magic.plus(newMagic to newMagic.duration)
        }
    }

    fun hitBy(opponent: Player) {
        if (lost || opponent.lost) {
            return
        }
        hit -= maxOf(1, opponent.damage - roundArmor)
    }

    val lost: Boolean
        get() = hit <= 0

    fun getTotalManaLoss(): Int {
        return totalManaLoss
    }

}

fun run1(
    @Suppress("UNUSED_PARAMETER") lines: List<String>,
    @Suppress("UNUSED_PARAMETER") log: (String) -> Unit
): ResultType {
    val me = Player(50, mana = 500)
    val boss = Player(71, damage = 10)

    fun play(me: Player, boss: Player, round: Int): Int? {
        me.newRound(boss)
        if (boss.lost) {
            return me.getTotalManaLoss()
        }
        return me.getAllowedMagics()
            .mapNotNull { magic ->
                val meClone = me.clone()
                val bossClone = boss.clone()
                meClone.addMagic(magic, bossClone)
                meClone.newRound(bossClone)
                meClone.hitBy(bossClone)
                when {
                    meClone.lost -> null
                    bossClone.lost -> meClone.getTotalManaLoss()
                    else -> play(meClone, bossClone, round + 1)
                }
            }.minOrNull()
    }

    return play(me, boss, 1)!!
}

fun run2(
    @Suppress("UNUSED_PARAMETER") lines: List<String>,
    @Suppress("UNUSED_PARAMETER") log: (String) -> Unit
): ResultType {
    val me = Player(50, mana = 500)
    val boss = Player(71, damage = 10)

    fun play(me: Player, boss: Player, round: Int): Int? {
        me.decHit(boss)
        if (me.lost) {
            return null
        }
        me.newRound(boss)
        if (boss.lost) {
            return me.getTotalManaLoss()
        }
        return me.getAllowedMagics()
            .mapNotNull { magic ->
                val meClone = me.clone()
                val bossClone = boss.clone()
                meClone.addMagic(magic, bossClone)
                meClone.newRound(bossClone)
                meClone.hitBy(bossClone)
                when {
                    meClone.lost -> null
                    bossClone.lost -> meClone.getTotalManaLoss()
                    else -> play(meClone, bossClone, round + 1)
                }
            }.minOrNull()
    }

    return play(me, boss, 1) ?: 0
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
