package aoc_2024.aoc_2024_09

import aoc_2024.tools.ExpectedRefResults
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


fun run1(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val blocks = ArrayDeque(lines.first().map { it.toString().toInt() })

    var pos = 0
    var checksum = 0L
    var fileIndex = 0

    while (blocks.isNotEmpty()) {
        val frontFileSize = blocks.removeFirst()

        checksum += (pos..<(pos + frontFileSize)).sumOf { it.toLong() * fileIndex }
        fileIndex++
        pos += frontFileSize

        if (blocks.isEmpty()) break

        var gap = blocks.removeFirst()
        while (gap > 0 && blocks.isNotEmpty()) {
            val lastFileIndex = fileIndex + blocks.size / 2
            val lastFileSize = blocks.removeLast()

            val usedBlocks = minOf(gap, lastFileSize)
            checksum += (pos until (pos + usedBlocks)).sumOf { it.toLong() * lastFileIndex }
            pos += usedBlocks
            gap -= lastFileSize

            if (gap < 0) {
                // Add remaining file
                blocks.addLast(lastFileSize - usedBlocks)
            } else if (blocks.isNotEmpty()) {
                blocks.removeLast()
            }
        }
    }
    return checksum
}

fun run2(lines: List<String>, @Suppress("UNUSED_PARAMETER") log: (String) -> Unit): ResultType {
    val files = ArrayDeque<Pair<Int, Pair<Int, Int>>>()
    val gaps = ArrayDeque<Pair<Int, Int>>()
    lines.first().map { it.toString().toInt() }.foldIndexed(0) { index, pos, size ->
        if (index % 2 == 0) {
            files.addLast(index / 2 to (pos to size))
        } else {
            gaps.addLast(pos to size)
        }
        pos + size
    }
    val newFiles = files.reversed().map { file ->
        val matchingGapIndex = gaps.indexOfFirst {
            it.first < file.second.first && it.second >= file.second.second
        }
        if (matchingGapIndex >= 0) {
            val gap = gaps[matchingGapIndex]
            gaps[matchingGapIndex] = (gap.first + file.second.second) to (gap.second - file.second.second)
            file.first to (gap.first to file.second.second)
        } else {
            file
        }
    }
    return newFiles.fold(0L) { checksum, file ->
        val (index, fileStat) = file
        val (start, size) = fileStat
        checksum + (start until (start + size)).sumOf { it.toLong() * index }
    }
}

fun main() {
    simpleIO(YEAR, DAY, ::run1 to ::run2, EXPECTED_RESULTS)
}
