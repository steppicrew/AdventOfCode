package aoc_2024.tools

import java.io.File
import java.text.NumberFormat
import java.util.*
import kotlin.time.measureTimedValue

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

const val CORRECT = "${green}${bold}✔${reset}"
const val FAILED = "${red}${bold}✗${reset}"
const val NEW_RESULT = "${yellow}${bold}?${reset}"

typealias ExpectedResult<T> = Pair<T?, T?>
typealias ExpectedRefResult<T> = Pair<Int, ExpectedResult<T>>
typealias ExpectedRefResults<T> = List<ExpectedRefResult<T>>

typealias RunType<T> = (List<String>, (String) -> Unit) -> T

val formatter = NumberFormat.getInstance(Locale.GERMAN)!!

fun <T> simpleIO(
    year: Int, day: Int,
    run: Pair<RunType<T>, RunType<T>>,
    expectedResults: ExpectedRefResults<T>,
    quiet: Boolean = false
) {
    fun printResult(result: T): String {
        return "${bold}${result}${reset}"
    }

    fun refRun(ref: Int, expectedResult: ExpectedResult<T>): List<Boolean?> {
        fun partRun(part: Int, run: RunType<T>, expectedResult: T?): Boolean? {
            fun getPath(forResult: Boolean, extension: String): String {
                val paddedDay = day.toString().padStart(2, '0')
                return listOf(
                    "src/aoc_${year}/aoc_${year}_${paddedDay}/${year}_${paddedDay}",
                    (if (ref > 0) "_ref$ref" else ""),
                    (if (forResult) "_$part.result" else ""),
                    ".$extension"
                ).joinToString("")
            }

            val logLines = mutableListOf<String>()
            fun log(line: String) {
                logLines.add("$line\n")
                if (!quiet) println(line)
            }

            val lines = File(getPath(false, "txt"))
                .readLines()
                .filter { !it.startsWith(';') }

            val (result, duration) = measureTimedValue { run(lines, ::log) }
            val time = "${formatter.format(duration.inWholeMilliseconds / 1000.0)}s"

            if (logLines.size > 0) {
                File(getPath(true, "log"))
                    .writeText(logLines.joinToString(""))
            }

            print("${if (ref > 0) "ref${ref}" else "main"}/${part}: ")

            return when (expectedResult) {
                result -> {
                    println("$CORRECT (${printResult(result)}) in $time")
                    true
                }

                null -> {
                    println("$NEW_RESULT (${printResult(result)}) in $time")
                    File(getPath(true, "txt")).writeText(result.toString())
                    null
                }

                else -> {
                    println("$FAILED in $time")
                    println("\tEXPECTED: ${printResult(expectedResult)}")
                    println("\tGOT     : ${printResult(result)}")
                    false
                }
            }
        }

        return listOf(
            partRun(1, run.first, expectedResult.first),
            partRun(2, run.second, expectedResult.second)
        )
    }

    val results = expectedResults.flatMap { expected ->
        refRun(expected.first, expected.second)
    }

    val successCount = results.count { it == true }
    val failedCount = results.count { it == false }
    val expectedCount = 2 * expectedResults.size
    val color = when {
        successCount == expectedCount -> green
        failedCount > 0 -> red
        else -> yellow
    }

    println("${color}PASSED: ${bold}${successCount}/${expectedCount}${reset}")
}
