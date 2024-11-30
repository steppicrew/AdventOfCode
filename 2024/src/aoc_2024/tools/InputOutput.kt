package aoc_2024.tools

import java.io.File

class InputOutput(private val year: Int, private val day: Int, private val part: Int, private val ref: Int) {

    private var startTime: Long = 0

    private fun getPath(forResult: Boolean): String {
        val day1 = day.toString().padStart(2, '0')
        return (
                "src/aoc_${year}/aoc_${year}_${day1}/${year}_${day1}"
                        + (if (ref > 0) "_ref$ref" else "")
                        + (if (forResult) "_$part.result" else "")
                )
    }


    private val logLines = mutableListOf<String>()

    fun log(line: String) {
        logLines.add("$line\n")
        println(line)
    }

    fun writeLog() {
        val path = getPath(true)
        File("$path.log").writeText(logLines.joinToString(""))
    }

    fun read(): List<String> {
        val path = getPath(false)
        // println("Reading $path")
        startTime = System.currentTimeMillis()
        return File("$path.txt").readLines().filter { !it.startsWith(';') }
    }

    fun write(result: Int) {
        write(result.toString())
    }

    fun write(result: String) {
        val path = getPath(true)
        val elapsedTime = String.format("%.1f", (System.currentTimeMillis() - startTime) / 1000.0)
        println("Writing $path, time: ${elapsedTime}s")
        File("$path.txt").writeText(result)
    }
}