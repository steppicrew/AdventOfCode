-- | Shared helpers for Advent of Code, across years.
--
-- Days are dispatched by a single @aoc@ executable:
--
-- > cabal run aoc -- <year> <day> [dataset]
--
-- The optional /dataset/ number selects which input file to read, alongside
-- the day's source in @Y<year>\/@:
--
--   * @0@ (default) — the real puzzle input, @DayNN_input.txt@
--   * @1@, @2@, …   — reference/sample sets, @DayNN_input_refN.txt@
--
-- Each day exposes a 'Day' (see 'day') carrying its year and number; the
-- dispatcher looks it up and runs it with 'runDay'. Set @AOC_DEBUG=1@ to
-- enable 'debug' messages (to stderr).
module AoC
  ( -- * Defining a day
    Day (..)
  , Solver
  , day
    -- * Running a day
  , runDay
    -- * Input reading
  , readInput
  , readLines
  , readInts
  , inputPath
    -- * Debug messages
  , debug
  , debugShow
    -- * Output
  , printPart
    -- * Parsing helpers
  , splitOn
  , wordsBy
  , ints
  , Grid
  , parseGrid
  ) where

import Control.Monad (when)
import Data.Char (isDigit)
import Data.List (foldl')
import qualified Data.List.Split as Split
import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map
import System.CPUTime (getCPUTime)
import System.Environment (lookupEnv)
import System.IO (hPutStrLn, stderr)
import Text.Printf (printf)

-- | A solver takes the raw input file contents and produces an answer that
-- can be shown (an 'Int', 'String', etc.).
type Solver a = String -> a

-- | A day's two solvers plus the year and day it belongs to, packaged so the
-- dispatcher can store them uniformly. The existential 'Show' constraints let
-- each part return whatever type is convenient.
data Day = forall a b. (Show a, Show b) => Day
  { dayYear   :: Int
  , dayNumber :: Int
  , part1     :: Solver a
  , part2     :: Solver b
  }

-- | Build a 'Day' from its year, number, and two solvers.
--
-- > solve :: Day
-- > solve = day 2025 1 part1 part2
day :: (Show a, Show b) => Int -> Int -> Solver a -> Solver b -> Day
day = Day

-- | Read the input for a day\/dataset, run both parts with timing, and print
-- labelled, timed answers. Called by the dispatcher.
runDay :: Int -> Day -> IO ()
runDay dataset (Day y n p1 p2) = do
  input <- readInput y n dataset
  printPart 1 =<< timed (p1 input)
  printPart 2 =<< timed (p2 input)

-- | Run a pure value to WHNF-ish via 'show', returning the shown result and
-- elapsed CPU time in seconds.
timed :: Show a => a -> IO (String, Double)
timed x = do
  start <- getCPUTime
  let s = show x
  end <- s `seq` getCPUTime
  pure (s, fromIntegral (end - start) / 1e12)

-- * Input reading -----------------------------------------------------------

-- | Path to the input file for a year, day, and dataset number. Inputs sit
-- alongside the day's source under @Y<year>\/@.
--
--   * dataset @0@ → @Y2025\/DayNN_input.txt@       (the real input)
--   * dataset @k@ → @Y2025\/DayNN_input_refK.txt@  (reference set @k@)
inputPath :: Int -> Int -> Int -> FilePath
inputPath year dayNo dataset
  | dataset <= 0 = printf "Y%d/Day%02d_input.txt" year dayNo
  | otherwise    = printf "Y%d/Day%02d_input_ref%d.txt" year dayNo dataset

-- | Read the input file for a year, day, and dataset number.
readInput :: Int -> Int -> Int -> IO String
readInput year dayNo dataset = do
  let path = inputPath year dayNo dataset
  debug ("reading input: " ++ path)
  readFile path

-- | Read the input as a list of lines.
readLines :: Int -> Int -> Int -> IO [String]
readLines year dayNo dataset = lines <$> readInput year dayNo dataset

-- | Read the input as a list of integers, one per line.
readInts :: Int -> Int -> Int -> IO [Int]
readInts year dayNo dataset = map read . lines <$> readInput year dayNo dataset

-- * Debug -------------------------------------------------------------------

-- | Print a debug message to stderr when @AOC_DEBUG=1@. Never touches stdout,
-- so it won't corrupt the answer.
debug :: String -> IO ()
debug msg = do
  on <- envFlag "AOC_DEBUG"
  when on $ hPutStrLn stderr ("[debug] " ++ msg)

-- | Like 'debug' but for any 'Show'-able value, with a label.
debugShow :: Show a => String -> a -> IO ()
debugShow label x = debug (label ++ " = " ++ show x)

-- * Output ------------------------------------------------------------------

-- | Print one part's answer to stdout with its timing.
printPart :: Int -> (String, Double) -> IO ()
printPart n (answer, secs) =
  printf "Part %d: %s  (%.3fs)\n" n answer secs

-- * Parsing helpers ---------------------------------------------------------

-- | Split a list on every occurrence of a delimiter sublist, dropping the
-- delimiters. E.g. @splitOn \",\" \"a,b,c\" == [\"a\",\"b\",\"c\"]@.
splitOn :: Eq a => [a] -> [a] -> [[a]]
splitOn = Split.splitOn

-- | Split a list into maximal runs of elements failing the predicate,
-- dropping the separators. Useful for splitting on any whitespace/punctuation.
wordsBy :: (a -> Bool) -> [a] -> [[a]]
wordsBy = Split.wordsBy

-- | Extract every (optionally signed) integer embedded in a string, ignoring
-- all other characters. E.g. @ints \"x=3, y=-7\" == [3,-7]@.
ints :: String -> [Int]
ints [] = []
ints s@(c : cs)
  | c == '-', (d : _) <- cs, isDigit d =
      let (num, rest) = span isDigit cs
       in read (c : num) : ints rest
  | isDigit c =
      let (num, rest) = span isDigit s
       in read num : ints rest
  | otherwise = ints cs

-- | A 2D character grid keyed by @(row, col)@ coordinates (both 0-based).
type Grid = Map (Int, Int) Char

-- | Parse newline-separated text into a 'Grid'. Row 0 is the first line.
parseGrid :: String -> Grid
parseGrid = foldl' addRow Map.empty . zip [0 ..] . lines
  where
    addRow g (r, row) =
      foldl' (\g' (c, ch) -> Map.insert (r, c) ch g') g (zip [0 ..] row)

-- * Internals ---------------------------------------------------------------

-- | True when an environment variable is set to a truthy value (@1@/@true@/@yes@).
envFlag :: String -> IO Bool
envFlag name = do
  mv <- lookupEnv name
  pure $ case mv of
    Just v  -> v `elem` ["1", "true", "yes", "True", "TRUE"]
    Nothing -> False
