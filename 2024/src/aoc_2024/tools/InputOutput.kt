package aoc_2024.tools

import java.io.File
import kotlin.system.measureTimeMillis

fun <T>simpleIO(year: Int, day: Int, part: Int, ref: Int, run: (Collection<String>, (String)->Unit) -> T) {
    fun getPath(forResult: Boolean): String {
        val day1 = day.toString().padStart(2, '0')
        return (
                "src/aoc_${year}/aoc_${year}_${day1}/${year}_${day1}"
                        + (if (ref > 0) "_ref$ref" else "")
                        + (if (forResult) "_$part.result" else "")
                )
    }

    val logLines = mutableListOf<String>()

    fun log(line: String) {
        logLines.add("$line\n")
        println(line)
    }

    val lines = run {
        val path = getPath(false)
        // println("Reading $path")
        File("$path.txt").readLines().filter { !it.startsWith(';') }
    }

    val result:T
    val time = measureTimeMillis { result = run(lines, ::log) }

    run {
        println("RESULT: $result")
        val path = getPath(true)
        println("Writing $path, time: ${time}ms")
        File("$path.txt").writeText(result.toString())
    }

    if (logLines.size > 0) {
        val path = getPath(true)
        File("$path.log").writeText(logLines.joinToString(""))
    }
}
