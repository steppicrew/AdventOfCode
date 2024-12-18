package aoc_2024.aoc_2024_09

import aoc_2024.tools.ExpectedRefResults
import aoc_2024.tools.InputData
import aoc_2024.tools.simpleIO

const val YEAR = 2024
const val DAY = 9

typealias ResultType = Long

// ref to (run1 to run2)
// values may be of any type, null is for 'not known' and write result into file
val EXPECTED_RESULTS: ExpectedRefResults<ResultType> = listOf(
    1 to (60L to 132L),
    2 to (1928L to 2858L),
    0 to (6288599492129L to 6321896265143L),
)


fun run1(input: InputData): ResultType {
    val files = ArrayDeque<Pair<Int, Pair<Int, Int>>>()
    val gaps = ArrayDeque<Pair<Int, Int>>()
    input.lines.first().map { it.digitToInt() }.foldIndexed(0) { index, pos, size ->
        if (index % 2 == 0) {
            files.addLast(index / 2 to (pos to size))
        } else {
            gaps.addLast(pos to size)
        }
        pos + size
    }

    val newFiles = files.reversed().flatMap { file ->
        val fileIndex = file.first
        val fileStart = file.second.first
        var fileSize = file.second.second
        val chunks = ArrayDeque<Pair<Int, Pair<Int, Int>>>()
        while (fileSize > 0 && gaps.first().first < fileStart) {
            val (gapStart, gapSize) = gaps.removeFirst()
            if (gapSize >= fileSize) {
                chunks.add(fileIndex to (gapStart to fileSize))
                if (gapSize > fileSize) {
                    gaps.addFirst((gapStart + fileSize) to (gapSize - fileSize))
                }
                fileSize = 0
            } else {
                chunks.add(fileIndex to (gapStart to gapSize))
                fileSize -= gapSize
            }
        }
        if (fileSize > 0) {
            chunks.addLast(fileIndex to (fileStart to fileSize))
        }
        chunks
    }
    return newFiles.sumOf { file ->
        val (index, fileStat) = file
        val (start, size) = fileStat
        (start until (start + size)).sumOf { it.toLong() * index }
    }
}

fun run2(input: InputData): ResultType {
    val files = ArrayDeque<Pair<Int, Pair<Int, Int>>>()
    val gaps = ArrayDeque<Pair<Int, Int>>()
    input.lines.first().map { it.digitToInt() }.foldIndexed(0) { index, pos, size ->
        if (index % 2 == 0) {
            files.addLast(index / 2 to (pos to size))
        } else {
            gaps.addLast(pos to size)
        }
        pos + size
    }
    val newFiles = files.reversed().map { file ->
        val fileIndex = file.first
        val (fileStart, fileSize) = file.second

        val matchingGapIndex = gaps.indexOfFirst {
            it.first < fileStart && it.second >= fileSize
        }
        if (matchingGapIndex >= 0) {
            val gap = gaps[matchingGapIndex]
            gaps[matchingGapIndex] = (gap.first + fileSize) to (gap.second - fileSize)
            fileIndex to (gap.first to fileSize)
        } else {
            file
        }
    }
    return newFiles.sumOf { file ->
        val (index, fileStat) = file
        val (start, size) = fileStat
        (start until (start + size)).sumOf { it.toLong() * index }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
