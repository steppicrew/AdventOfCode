#!/usr/bin/env bash
# Scaffold a new AoC day for a given year:
#   * Y<year>/DayNN.hs                          (module Y<year>.DayNN, `solve :: Day`)
#   * Y<year>/DayNN_input.txt                   (real input, gitignored)
#   * Y<year>/DayNN_input_ref1.txt              (first reference/sample set)
#   * registers Y<year>.DayNN in the `days` library (x2025-haskell.cabal)
#   * registers it in the dispatcher            (app/Main.hs)
#
# Usage: ./new-day.sh <year> <day>
#   ./new-day.sh 2025 2     # sets up 2025 day 2 -> `./run.sh 2025 2`
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <year> <day>" >&2
  exit 1
fi

year=$1
day=$2
nn=$(printf '%02d' "$day")
mod="Y${year}.Day${nn}"          # e.g. Y2025.Day02
qual="Y${year}.Day${nn}"
src="Y${year}/Day${nn}.hs"
input_base="Y${year}/Day${nn}"
cabal_file="x2025-haskell.cabal"
dispatcher="app/Main.hs"

if [[ -e "$src" ]]; then
  echo "error: $src already exists" >&2
  exit 1
fi

# A brand-new year needs its own cradle entry in hie.yaml (the `days` library
# spans one path per year). Detect before we create the directory.
new_year=0
[[ -d "Y${year}" ]] || new_year=1

mkdir -p "Y${year}"

# 1. Day source.
cat > "$src" <<EOF
-- | AoC ${year}, Day ${day}.
module ${mod} (solve) where

import AoC (Day, Solver, day)

part1 :: Solver Int
part1 _input = 0

part2 :: Solver Int
part2 _input = 0

solve :: Day
solve = day ${year} ${day} part1 part2
EOF

# 2. Input files (empty; paste the real puzzle input into the _input one).
touch "${input_base}_input.txt" "${input_base}_input_ref1.txt"

# 3. Register in the `days` library's exposed-modules (after the last Y* line).
awk -v mod="$mod" '
  /^        Y[0-9]+\.Day[0-9][0-9]$/ { lastmod = NR }
  { lines[NR] = $0 }
  END {
    for (i = 1; i <= NR; i++) {
      print lines[i]
      if (i == lastmod) print "        " mod
    }
  }
' "$cabal_file" > "$cabal_file.tmp" && mv "$cabal_file.tmp" "$cabal_file"

# 4. Register in the dispatcher: add a qualified import and a map entry.
awk -v qual="$qual" -v y="$year" -v n="$day" '
  /^import qualified Y[0-9]+\.Day[0-9][0-9]$/ { lastimport = NR }
  /\.solve\)$/ { lastentry = NR }
  { lines[NR] = $0 }
  END {
    for (i = 1; i <= NR; i++) {
      print lines[i]
      if (i == lastimport) print "import qualified " qual
      if (i == lastentry)  print "  , ((" y ", " n "), " qual ".solve)"
    }
  }
' "$dispatcher" > "$dispatcher.tmp" && mv "$dispatcher.tmp" "$dispatcher"

# 5. For a brand-new year, add its cradle entry to hie.yaml so HLS resolves it.
if [[ $new_year -eq 1 ]]; then
  cat >> "hie.yaml" <<EOF

    - path: "./Y${year}"
      component: "x2025-haskell:lib:days"
EOF
  echo "Added Y${year} cradle entry to hie.yaml (new year)."
fi

echo "Created $src and ${input_base}_input{,_ref1}.txt."
echo "Registered ${mod} in $cabal_file and $dispatcher."
echo "Paste your input into ${input_base}_input.txt, then: ./run.sh ${year} ${day}"
