#!/usr/bin/env bash
# Run an AoC solution.
#
#   ./run.sh <year> <day> [dataset]
#
#   dataset  0 = real input (default)   -> Y<year>/inputs/dayNN_input.txt
#            1.. = reference set N       -> Y<year>/inputs/dayNN_input_refN.txt
#
# Examples:
#   ./run.sh 2025 1 1    # 2025 day 1, reference set 1
#   ./run.sh 2026 1      # 2026 day 1, real input (dataset 0)
#
# Pass AOC_DEBUG=1 in the environment to see debug messages on stderr:
#   AOC_DEBUG=1 ./run.sh 2025 1 1
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <year> <day> [dataset]" >&2
  exit 1
fi

cd "$(dirname "$0")"
exec cabal run -v0 aoc -- "$@"
