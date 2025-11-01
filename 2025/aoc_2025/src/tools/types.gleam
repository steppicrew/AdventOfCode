import gleam/option.{type Option}

/// Expected results for a given reference input.
/// 
/// - `ref`: Reference index (0 = main input, >0 = test cases)
/// - `part1` / `part2`: Expected outputs for each puzzle part
///
/// Example:
/// ```gleam
/// [
///   Expected(0, Some(24000), Some(45000)),
///   Expected(1, None, None)  // writes missing results
/// ]
/// ```
pub type ExpectedResult(a) {
  Expected(ref: Int, part1: Option(a), part2: Option(a))
}
