import gleam/int

@external(erlang, "erlang", "monotonic_time")
fn monotonic_time_native(unit: Int) -> Int

pub fn measure_time(fun: fn() -> a) -> #(a, Float) {
  // microsecond = 1_000_000
  let start = monotonic_time_native(1_000_000)
  let result = fun()
  let stop = monotonic_time_native(1_000_000)
  let duration_microseconds = stop - start
  #(result, int.to_float(duration_microseconds) /. 1_000_000.0)
}
