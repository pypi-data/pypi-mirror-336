"""gptsession — Simple, stateful conversations with OpenAI's chat models.

This package provides a structured interface for managing multiple
conversation sessions with OpenAI's ChatGPT models. It handles message
history, token accounting, automatic truncation to fit model limits, and
records the full conversation for later inspection.

Main functions:
  setup(api_key)  – Initialize the module with your OpenAI API key
  new()           – Start a new conversation session
  system(prompt)  - Set the system prompt for the current session
  say(message)    – Send a message and receive the assistant’s reply
  model(name)     – Change the active model for a session
  meter()         - Return token usage stats (sent, received, total)
  truncated()     - Check if the session was truncated due to token limits
  record()        – Retrieve the full untruncated message history

Importing the package gives access to all public functions via: `import gptsession`


Example: multiple sessions

  import gptsession as gpt

  gpt.setup(open("mykey.txt").read().strip())

  session_one = gpt.new()
  gpt.system("You are a bird.")

  session_two = gpt.new()
  gpt.system("You are a robot.")

  gpt.sel(session_one)
  gpt.say("Where do you live?")   # ChatGPT replies as a bird

  gpt.sel(session_two)
  gpt.say("Where do you live?")   # ChatGPT replies as a robot


Example: minimal single-session chat client

  import gptsession as gpt

  gpt.setup(open("mykey.txt").read().strip())
  gpt.new()

  while True:
      msg = input("You: ")
      if msg.lower() in ("exit", "quit"):
          break
      print("ChatGPT:", gpt.say(msg))
"""

__version__ = "1.0.0"

from .conversation import (
    setup,
    new,
    sel,
    restart,
    reset_meter,
    meter,
    model,
    system,
    say,
    count,
    trunc,
    truncated,
    record,
)

__all__ = [
    "setup",
    "new",
    "sel",
    "restart",
    "reset_meter",
    "meter",
    "model",
    "system",
    "say",
    "count",
    "trunc",
    "truncated",
    "record",
]
