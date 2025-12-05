import gleam/erlang/process

// Messages the logger process understands
pub type LogMsg {
  Append(String)
  Dump(process.Subject(String))
}

// Handle you keep in your code
pub type Logger {
  Logger(subject: process.Subject(LogMsg))
}

// Internal loop: keeps `buffer` as mutable state
fn logger_loop(subject: process.Subject(LogMsg), buffer: String) -> Nil {
  // Wait forever for the next message on this subject
  let msg = process.receive_forever(subject)

  case msg {
    Append(text) ->
      // Append to in-memory buffer and continue
      logger_loop(subject, buffer <> text <> "\n")

    Dump(reply_subject) -> {
      // Send current buffer back to caller
      process.send(reply_subject, buffer)
      logger_loop(subject, buffer)
    }
  }
}

// Start a new logger with empty buffer
pub fn start() -> Logger {
  let subject = process.new_subject()

  // Spawn the logger process
  let _pid = process.spawn(fn() { logger_loop(subject, "") })

  Logger(subject: subject)
}

// Log a single message into the logger
pub fn log(logger: Logger, msg: String) -> Nil {
  let Logger(subject) = logger
  process.send(subject, Append(msg))
}

// Get the collected output as a String
pub fn collect(logger: Logger) -> String {
  let Logger(subject) = logger

  // Create a one-shot reply subject
  let reply_subject = process.new_subject()

  // Ask logger to send us its buffer
  process.send(subject, Dump(reply_subject))

  // Block until we get the buffer back
  process.receive_forever(reply_subject)
}
