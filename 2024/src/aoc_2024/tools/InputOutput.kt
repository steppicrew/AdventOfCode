package aoc_2024.tools

import java.io.File
import kotlin.system.measureTimeMillis

// const val black = "\u001B[30m"
const val red = "\u001B[31m"
const val green = "\u001B[32m"
const val yellow = "\u001B[33m"
// const val blue = "\u001B[34m"
// const val magenta = "\u001B[35m"
// const val cyan = "\u001B[36m"
// const val white = "\u001B[37m"

// const val bgBlack = "\u001B[40m"
// const val bgRed = "\u001B[41m"
// const val bgGreen = "\u001B[42m"
// const val bgYellow = "\u001B[43m"
// const val bgBlue = "\u001B[44m"
// const val bgMagenta = "\u001B[45m"
// const val bgCyan = "\u001B[46m"
// const val bgWhite = "\u001B[47m"

const val reset = "\u001B[0m"
const val bold = "\u001B[1m"
// const val underline = "\u001B[4m"
// const val reversed = "\u001B[7m"

const val CORRECT = "${green}${bold}CORRECT${reset}"
const val FAILED = "${red}${bold}FAILED${reset}"

fun <T> printResult(result: T): String {
    return "${bold}${result}${reset}"
}

fun <T> simpleIO(
    year: Int, day: Int,
    run: Pair<(List<String>, (String) -> Unit) -> T, (List<String>, (String) -> Unit) -> T>,
    expectedResults: List<Pair<Int, Pair<T?, T?>>>
) {
    fun refRun(ref: Int, expectedResult: Pair<T?, T?>): Int {
        fun singleRun(part: Int, run: (List<String>, (String) -> Unit) -> T, expectedResult: T?): Boolean {
            fun getPath(forResult: Boolean, extension: String): String {
                val day1 = day.toString().padStart(2, '0')
                return (
                        "src/aoc_${year}/aoc_${year}_${day1}/${year}_${day1}"
                                + (if (ref > 0) "_ref$ref" else "")
                                + (if (forResult) "_$part.result" else "")
                                + ".$extension"
                        )
            }

            val logLines = mutableListOf<String>()

            fun log(line: String) {
                logLines.add("$line\n")
                println(line)
            }

            val lines = File(getPath(false, "txt")).readLines().filter { !it.startsWith(';') }

            val result: T
            val time = measureTimeMillis { result = run(lines, ::log) }

            if (logLines.size > 0) {
                File(getPath(true, "log"))
                    .writeText(logLines.joinToString("\n"))
            }

            val refStr = if (ref > 0) "ref${ref}" else "main"
            print("${refStr}/${part}: ")
            if (expectedResult == null) {
                println("NEW RESULT (${printResult(result)}) in ${time}ms")
                File(getPath(true, "txt")).writeText(result.toString())
            } else {
                if (expectedResult == result) {
                    println("$CORRECT (${printResult(result)}) in ${time}ms")
                } else {
                    println("$FAILED in ${time}ms")
                    println("EXPECTED: ${printResult(expectedResult)}")
                    println("GOT     : ${printResult(result)}")
                    return false
                }
            }
            return true
        }

        return listOf(
            singleRun(1, run.first, expectedResult.first),
            singleRun(2, run.second, expectedResult.second)
        ).count { it }
    }

    val successCount = expectedResults.sumOf { expected ->
        refRun(expected.first, expected.second)
    }

    val expectedCount = 2 * expectedResults.size

    val color = if (successCount == expectedCount) green else if (successCount > 0) yellow else red

    println("${color}PASSED: ${bold}${successCount}/${expectedCount}${reset}")
}
