# AdventOfCode 2025.haskell — project guide

Multi-year Advent of Code solutions in Haskell. A single `aoc` executable
dispatches to any year's day against any input set.

## Running

```sh
./run.sh <year> <day> [dataset]     # dataset: 0 = real input (default), 1.. = ref sets
./run.sh 2025 1        # 2025 day 1, real input
./run.sh 2025 1 1      # 2025 day 1, reference set 1
AOC_DEBUG=1 ./run.sh 2025 1 1       # debug messages on stderr
cabal build all
```

`run.sh` wraps `cabal run -v0 aoc -- <year> <day> [dataset]`.

## Adding a day

```sh
./new-day.sh <year> <day>           # e.g. ./new-day.sh 2025 3  or  ./new-day.sh 2026 1
```

`new-day.sh` creates `Y<year>/DayNN.hs` + input files and registers the module
in `x2025-haskell.cabal` (the `days` library), `app/Main.hs` (the dispatcher
map), and — for a brand-new year — `hie.yaml`. Don't wire days up by hand;
use the script so all three stay in sync.

## Layout

```
lib/AoC.hs         shared helpers: input reading, debug, output, parsing (library aoc-lib)
app/Main.hs        dispatcher, keyed by (year, day)                       (executable aoc)
Y<year>/DayNN.hs   one module per day (module Y<year>.DayNN)              (library days)
Y<year>/DayNN_input.txt        real input   (GITIGNORED — personal per account)
Y<year>/DayNN_input_refN.txt   reference sets (committed)
```

Each day exposes `solve :: Day` (built with `AoC.day year dayNo part1 part2`);
inputs sit next to the day's source, filename matching the module (`Day01.hs`
→ `Day01_input.txt`). Multiple reference sets per day are supported.

## Conventions & gotchas

- **Component names:** the helpers library is `aoc-lib` (not `aoc`) — cabal
  forbids a library and executable sharing a name; the executable is `aoc`.
- **Build on Arch Linux:** `cabal.project` forces dynamic linking because
  Arch's system `ghc` ships only `.dyn_hi` interface files. Without it the
  build fails with `Could not find module 'Prelude'`. Don't remove it.
- **Real inputs are gitignored** (`Y*/Day*_input.txt`). Reference sets are
  committed so every day stays runnable after a fresh clone.
- **HLS:** `hie.yaml` maps source paths to cabal components; more specific
  paths must precede the per-year `days` entries. Regenerate carefully — plain
  `gen-hie` mis-orders/over-broadens these.
