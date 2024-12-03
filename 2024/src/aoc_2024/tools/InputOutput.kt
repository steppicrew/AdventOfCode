package aoc_2024.tools

import java.io.File
import kotlin.system.measureTimeMillis

fun <T> simpleIO(year: Int, day: Int, part: Int, ref: Int, run: (List<String>, (String) -> Unit) -> T) {
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

    println("RESULT: $result")
    getPath(true, "txt").let { path ->
        println("Writing $path, time: ${time}ms")
        File(path).writeText(result.toString())
    }

    if (logLines.size > 0) {
        File(getPath(true, "log"))
            .writeText(logLines.joinToString("\n"))
    }
}
