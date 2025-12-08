#!/usr/bin/env bash
# Advent of Code runner for Gleam
# Usage: ./run.sh [day]
# If no day is provided, it runs the current day (based on system date).

set -e

# === Configuration ===
YEAR=2025
SRC_BASE="src"

# Get day argument or current day (UTC to avoid local day rollovers)
if [ -n "$1" ]; then
  DAY=$1
else
  DAY=$(date -u +%-d)
fi

if [ -n "$2" ]; then
  YEAR=$2
fi

# Pad to two digits (01, 02, 03, ...)
PADDED_DAY=$(printf "%02d" "$DAY")
MODULE="aoc_${YEAR}_${PADDED_DAY}"
MAIN_FILE="${SRC_BASE}/${MODULE}/day${PADDED_DAY}.gleam"

# Sanity check
if [ ! -f "$MAIN_FILE" ]; then
  echo "❌ Error: Could not find source file:"
  echo "   ${MAIN_FILE}"
  echo "Make sure day ${DAY} exists (e.g. src/aoc_${YEAR}_${PADDED_DAY}/day${PADDED_DAY}.gleam)"
  exit 1
fi

echo "🎄 Advent of Code ${YEAR} — Day ${DAY}"
echo "▶ Running Gleam module ${MODULE}/day${PADDED_DAY} ..."
echo

gleam run -m "${MODULE}/day${PADDED_DAY}"
