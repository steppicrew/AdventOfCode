# Advent of Code — Haskell (multi-year)

A single `aoc` dispatcher runs any year's day against any input set.

## Layout

```
lib/AoC.hs         shared helpers (input reading, debug, output, parsing)
app/Main.hs        dispatcher: parses <year> <day> [dataset] and runs the day
Y<year>/DayNN.hs   one module per day (module Y<year>.DayNN, exposes solve :: Day)
Y<year>/DayNN_input.txt        real puzzle input   (gitignored — personal)
Y<year>/DayNN_input_refN.txt   reference/sample sets (committed)
```

Each day's inputs sit next to its source, e.g. `Y2025/Day01.hs`,
`Y2025/Day01_input.txt`, `Y2025/Day01_input_ref1.txt`.

## Running

```sh
./run.sh 2025 1        # 2025 day 1, dataset 0 = real input (Y2025/Day01_input.txt)
./run.sh 2025 1 1      # 2025 day 1, dataset 1 = Y2025/Day01_input_ref1.txt
./run.sh 2025 1 2      # 2025 day 1, dataset 2 = Y2025/Day01_input_ref2.txt
./run.sh 2026 1        # 2026 day 1, real input (once day 2026/1 is added)
AOC_DEBUG=1 ./run.sh 2025 1 1   # debug messages to stderr (never stdout)
```

`run.sh` is a thin wrapper over `cabal run -v0 aoc -- <year> <day> [dataset]`.
The **dataset** number selects the input file: `0` (default) is the real
input; `1`, `2`, … are reference sets (multiple per day supported).

## Adding a day

```sh
./new-day.sh 2025 3      # or: ./new-day.sh 2026 1
```

Creates `Y2025/Day03.hs` and its input files, and registers `Y2025.Day03` in
both the `days` library and the dispatcher. Then paste the puzzle input into
`Y2025/Day03_input.txt` and implement `part1` / `part2`.

## AoC helper API (`import AoC`)

- `day :: Int -> Int -> Solver a -> Solver b -> Day` — package a day's year,
  number, and two solvers.
- `Solver a = String -> a` — a part maps raw input to a `Show`-able answer.
- `runDay`, `readInput`, `readLines`, `readInts`, `inputPath` — take
  year + day + dataset numbers.
- `debug` / `debugShow` — stderr messages gated by `AOC_DEBUG`.
- `splitOn` / `wordsBy` / `ints` — string splitting and integer extraction.
- `parseGrid :: String -> Grid` — 2D char map keyed by `(row, col)`.

## Note on the build (Arch Linux)

Arch's system `ghc` ships only dynamic interface files, so the build is
configured for dynamic linking in `cabal.project`. Without it, `cabal build`
fails with `Could not find module 'Prelude'`.
