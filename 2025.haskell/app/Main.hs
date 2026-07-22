-- | Advent of Code dispatcher (all years).
--
-- > cabal run aoc -- <year> <day> [dataset]
--
-- @year@ and @day@ select the puzzle; @dataset@ selects the input file
-- (0 = real input, default; 1.. = reference sets). See "AoC" for details.
--
-- To wire up a new day, add it to 'days' below (new-day.sh does this).
module Main (main) where

import AoC (Day, runDay)
import qualified Data.Map.Strict as Map
import System.Environment (getArgs, getProgName)
import System.Exit (exitFailure)
import System.IO (hPutStrLn, stderr)
import Text.Read (readMaybe)

import qualified Y2025.Day01

-- | Registry of solvable days, keyed by @(year, day)@.
days :: Map.Map (Int, Int) Day
days = Map.fromList
  [ ((2025, 1), Y2025.Day01.solve)
  ]

main :: IO ()
main = do
  args <- getArgs
  case args of
    [y, d]       -> dispatch y d "0"
    [y, d, dset] -> dispatch y d dset
    _            -> usage

-- | Parse arguments and run the requested day, or report a helpful error.
dispatch :: String -> String -> String -> IO ()
dispatch yStr dStr dsetStr =
  case (readMaybe yStr, readMaybe dStr, readMaybe dsetStr) of
    (Just y, Just d, Just dataset) ->
      case Map.lookup (y, d) days of
        Just theDay -> runDay dataset theDay
        Nothing     -> die $ "year " ++ show y ++ " day " ++ show d
                              ++ " is not registered (available: "
                              ++ show (Map.keys days) ++ ")"
    (Nothing, _, _) -> die $ "not a year: " ++ yStr
    (_, Nothing, _) -> die $ "not a day number: " ++ dStr
    (_, _, Nothing) -> die $ "not a dataset number: " ++ dsetStr

usage :: IO ()
usage = do
  prog <- getProgName
  die $ "usage: " ++ prog ++ " <year> <day> [dataset]\n"
     ++ "  year    e.g. 2025\n"
     ++ "  day     1..25\n"
     ++ "  dataset 0 = real input (default), 1.. = reference sets"

die :: String -> IO a
die msg = hPutStrLn stderr msg >> exitFailure
