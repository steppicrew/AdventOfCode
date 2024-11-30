package aoc_2024.aoc_2018_02

import aoc_2024.tools.InputOutput

const val year = 2018
const val day = 2
const val ref = 0

fun run1() {
    val io = InputOutput(year, day, 1, ref)
    val lines = io.read()

    var count2 = 0
    var count3 = 0
    for (line in lines) {
        val set = HashMap<String, Int>()
        for (letter in line.split("").filter { it.isNotEmpty() }) {
            set[letter] = (set[letter] ?: 0) + 1
        }
        for (v in set.values) {
            if (v == 2) {
                count2++
                break
            }
        }
        for (v in set.values) {
            if (v == 3) {
                count3++
                break
            }
        }
    }
    val result = count2 * count3
    println(result)
    io.write(result)
}

fun run2() {
    val io = InputOutput(year, day, 2, ref)
    val lines = io.read()

    val letters = lines.map { it.split("") }

    val best_matches = HashMap<Int, String>()

    for (letters1 in letters) {
        var max_match = 0
        var max_letters = ""
        for (letters2 in letters) {
            if (letters1 == letters2) continue

            var count = 0
            var common_result = ""
            for ((letter1, letter2) in letters1.zip(letters2)) {
                if (letter1 == letter2) {
                    count++
                    common_result += letter1
                }
            }
            if (count > max_match) {
                max_match = count
                max_letters = common_result
            }
        }
        best_matches[max_match] = max_letters

    }

    val max_match: Int = best_matches.keys.max()
    val result = best_matches[max_match] ?: ""


    println(result)
    io.write(result)
}

fun main() {
    run1()
    run2()
}
