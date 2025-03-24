"""gptsession.conversation — internal model for session management

This module implements the internal logic and data structures for
managing multiple concurrent conversation sessions with OpenAI's ChatGPT
models.  It handles message history, token estimation for request
truncation, and session-level tracking of total token usage.

It is not intended to be imported directly. All public functions are
re-exported through the top-level `gptsession` package.

Data Structures
---------------

* models (List[Dict]):
    Defines available OpenAI models and their token limits.
    Each entry has:
      {
          "NAME": "<model name>",       # e.g., "gpt-3.5-turbo"
          "TOKENLIMIT": <max tokens>,   # e.g., 4096
          "ENCODER": <tiktoken encoder> # populated during setup()
      }

* conversations (List[Dict]):
    Tracks one conversation per session.
    Each conversation dictionary includes:
      {
          "I": <index>,                 # Unique session index
          "MODEL": <model dict>,        # Current model in use
          "MESSAGES": [                 # Message list sent to OpenAI
              {"role": "system", "content": "..."},
              {"role": "user", "content": "..."},
              {"role": "assistant", "content": "..."},
              ...
          ],
          "TOKENCOUNTS": [...],         # Token counts for each message
          "TRUNCATED": <bool>,          # True if truncation occurred
          "TOKENSSENT": <int>,          # Accumulated prompt sent
          "TOKENSRECEIVED": <int>,      # Accumulated tokens received
          "RECORD": [...],              # Full untruncated message log
      }

* g (Dict):
    Holds module-wide global state:
      {
          "SEL": <currently selected conversation dict>,
          "DEFAULT_MODEL": <default model dict>,
          "CLIENT": <openai.OpenAI instance>
      }

Message Structure Rules
-----------------------

The `MESSAGES` list must follow the expected alternation pattern
required by OpenAI’s chat completions API. It always begins with a
system message:

  message 0: {"role": "system", "content": "..."}
  message 1: {"role": "user", "content": "..."}
  message 2: {"role": "assistant", "content": "..."}
  message 3: {"role": "user", "content": "..."}
  message 4: {"role": "assistant", "content": "..."}
  ...

Each assistant message directly follows its corresponding user message.
The RECORD list mirrors MESSAGES but is never truncated.

Token Counting
--------------

TOKENCOUNTS stores the approximate token count for each message,
calculated using the model’s encoder. These are used to manage
truncation before API calls.  Actual billing token usage is retrieved
from the API’s response and tracked in TOKENSSENT and TOKENSRECEIVED.

"""

import openai
import tiktoken


# WORDS
I = "I"
MODEL = "MODEL"
NAME = "NAME"  # name of model, used with openai & tiktoken
TOKENLIMIT = "TOKENLIMIT"
ENCODER = "ENCODER"
MESSAGES = "MESSAGES"
TOKENCOUNTS = "TOKENCOUNTS"
TRUNCATED = "TRUNCATED"
TOKENSSENT = "TOKENSSENT"
TOKENSRECEIVED = "TOKENSRECEIVED"
RECORD = "RECORD"
TOTAL = "TOTAL"
SEL = "SEL"
DEFAULT_MODEL = "DEFAULT_MODEL"
CLIENT = "CLIENT"


# global data
conversations = []

models = [
    {NAME: "gpt-3.5-turbo",
     TOKENLIMIT: 4096,
     ENCODER: None},  # populated in setup

    {NAME: "gpt-3.5-turbo-16k",
     TOKENLIMIT: 16000,
     ENCODER: None},  # populated in setup

    {NAME: "gpt-4",
     TOKENLIMIT: 8192,
     ENCODER: None},  # populated in setup

    {NAME: "gpt-4-32k",
     TOKENLIMIT: 32768,
     ENCODER: None}  # populated in setup
]

g = {SEL: None,
     DEFAULT_MODEL: models[0],  # gpt-3.5-turbo
     CLIENT: None}  # populated in setup


# functions

def setup(openapi_key):
    """
    Initialize the gptsession module with your OpenAI API key.

    This function must be called before any other session functions.
    It creates an OpenAI client instance and prepares token encoders
    for all supported models.

    Parameters:
        openapi_key (str): Your OpenAI API key as a plain string.

    Example:
        >>> import gptsession
        >>> gptsession.setup(open("mykey.txt").read().strip())
    """
    g[CLIENT] = openai.OpenAI(api_key=openapi_key)
    for D in models:
        D[ENCODER] = tiktoken.encoding_for_model(D[NAME])

def new():
    """
    Create and select a new conversation session.

    This starts a new session with a blank system prompt and assigns
    the default model. The session becomes the current active one.
    The return value is the session index, which can be used with `sel()`.

    Returns:
        int: The index of the newly created session.

    Example:
        >>> import gptsession
        >>> gptsession.setup(open("mykey.txt").read().strip())
        >>> session_id = gptsession.new()
        >>> print("Session index:", session_id)
    """
    i = len(conversations)
    blank_system_message = {"role": "system", "content": ""}
    D = {I: i,
         MODEL: g[DEFAULT_MODEL],
         MESSAGES: [blank_system_message],
         TOKENCOUNTS: [0],
         TRUNCATED: False,
         TOKENSSENT: 0,
         TOKENSRECEIVED: 0,
         RECORD: [blank_system_message]}
    conversations.append(D)
    sel(i)
    return i

def sel(i):
    """
    Select an existing conversation session by index.

    This sets the current active session, allowing subsequent calls to
    `say()`, `system()`, `model()`, etc., to operate on the chosen
    session.

    Parameters:
        i (int): The index of the session to activate,
                 as returned by `new()`.

    Example:
        >>> session_one = gptsession.new()
        >>> gptsession.system("You eat spam.")
        >>> session_two = gptsession.new()
        >>> gptsession.system("You eat eggs.")
        >>> gptsession.sel(session_one)
        >>> gptsession.say("What do you eat?")
    """
    g[SEL] = conversations[i]

def restart():
    """
    Restart the current conversation session.

    This clears all user and assistant messages from the active session,
    but retains the system prompt and current model. It also resets the
    truncation flag and clears the recorded message history, except for
    the system prompt.

    Note:
        This does not reset token usage counters. To do that, call
        `reset_meter()`.

    Example:
        >>> session = gptsession.new()
        >>> gptsession.system("You are a poetic assistant.")
        >>> gptsession.say("Describe the sea.")
        >>> gptsession.restart()  # clears the conversation,
                                    but keeps the system prompt
    """
    del g[SEL][MESSAGES][1:]
    del g[SEL][TOKENCOUNTS][1:]
    g[SEL][TRUNCATED] = False
    del g[SEL][RECORD][1:]

def reset_meter():
    """
    Reset the token usage counters for the current session.

    This sets both TOKENSSENT and TOKENSRECEIVED to zero, allowing you
    to measure token usage from a clean point within the session
    history.

    This does not affect the conversation history or truncation state.

    Example:
        >>> gptsession.reset_meter()
        >>> gptsession.say("Tell me a story.")
        >>> print(gptsession.meter())  # shows token usage since reset
    """
    g[SEL][TOKENSSENT] = 0
    g[SEL][TOKENSRECEIVED] = 0

def meter():
    """
    Return token usage statistics for the current session.
    
    This includes the number of tokens sent in prompts, received in
    completions, and the total combined. These values reflect actual
    usage reported by the OpenAI API and can be used for cost tracking.
    
    Returns:
        dict: A dictionary with keys TOKENSSENT, TOKENSRECEIVED,
              and TOTAL.
    
    Example:
        >>> usage = gptsession.meter()
        >>> print(usage["TOTAL"], "tokens used")
    """
    a = g[SEL][TOKENSSENT]
    b = g[SEL][TOKENSRECEIVED]
    return {TOKENSSENT: a,
            TOKENSRECEIVED: b,
            TOTAL: a+b}

def model(name):
    """
    Set the active model for the current session.

    This changes which ChatGPT model will be used for subsequent
    completions.  The model name must match one of the supported models
    defined during setup.

    Parameters:
        name (str): The name of the model (e.g., "gpt-3.5-turbo").

    Raises:
        IndexError: If the model name is not recognized.

    Notes:
        To view available models, you may do:

            >>> from gptsession.conversation import models
            >>> print([D["NAME"] for D in models])

    Example:
        >>> gptsession.model("gpt-4")
        >>> gptsession.say("What is consciousness?")
    """
    for D in models:
        if D[NAME].upper() == name.upper():
            g[SEL][MODEL] = D
            return
    else:
        raise IndexError("Model not found: "+name)

def _encodelen(s):
    return len(g[SEL][MODEL][ENCODER].encode(s))

def system(prompt):
    """
    Set the system prompt for the current session.

    The system prompt defines the assistant's behavior and tone.
    It is always the first message in a conversation and will remain
    unchanged unless explicitly updated.

    Parameters:
        prompt (str): The system message to guide the assistant's
                      responses.

    Example:
        >>> gptsession.system("You are a patient, thoughtful tutor.")
        >>> gptsession.say("Can you explain recursion?")
    """
    g[SEL][MESSAGES][0]["content"] = prompt
    g[SEL][TOKENCOUNTS][0] = _encodelen(prompt)

def _user(msg):
    """Add a user message to the conversation."""
    D = {"role": "user", "content": msg}
    g[SEL][MESSAGES].append(D)
    g[SEL][TOKENCOUNTS].append(_encodelen(msg))
    g[SEL][RECORD].append(D)

def _assistant(msg):
    """Add an assistant's message to the conversation."""
    D = {"role": "assistant", "content": msg}
    g[SEL][MESSAGES].append(D)
    g[SEL][TOKENCOUNTS].append(_encodelen(msg))
    g[SEL][RECORD].append(D)

def say(msg):
    """
    Send a user message and receive the assistant's reply.

    This appends a user message to the current session, truncates the
    conversation if necessary to fit within the model's token limit, and
    sends the conversation to OpenAI. The assistant's reply is added to
    the conversation and returned as a string.

    Token usage is recorded, and the full message history (prior to
    truncation) is stored in the session record.

    Parameters:
        msg (str): The message to send to the assistant.

    Returns:
        str: The assistant’s reply.

    Example:
        >>> import gptsession as gpt
        >>> gpt.setup(open("mykey.txt").read().strip())
        >>> gpt.new()
        >>> gpt.model("gpt-3.5-turbo")
        >>> gpt.system("You are a wise oracle.")
        >>> reply = gpt.say("What is the meaning of life?")
        >>> print("ChatGPT:", reply)
        >>> if gpt.truncated():
        ...     print("[Note: conversation truncated due to length.]")
    """
    _user(msg)
    trunc()
    
    response = g[CLIENT].chat.completions.create(model=g[SEL][MODEL][NAME],
                                                 messages=g[SEL][MESSAGES])
    
    result = response.choices[0].message.content
    
    _assistant(result)
    
    # Use OpenAI's actual token usage metrics
    g[SEL][TOKENSSENT] += response.usage.prompt_tokens
    g[SEL][TOKENSRECEIVED] += response.usage.completion_tokens
    
    return result

def count():
    """
    Return the current token count of the active session.

    This includes all messages in the session's MESSAGES list—system,
    user, and assistant—plus structural overhead added by the OpenAI
    chat format. This is used to determine whether truncation is needed.

    Note:
        This value is a local estimate, used for control logic.
        Actual billing tokens are reported separately via `meter()`.

    Returns:
        int: Estimated number of tokens in the current conversation.

    Example:
        >>> tokens = gptsession.count()
        >>> print("Estimated tokens:", tokens)
    """
    return sum(g[SEL][TOKENCOUNTS]) + 4*len(g[SEL][MESSAGES])

def trunc():
    """
    Truncate the current session if it exceeds the model's token limit.

    This removes the oldest user–assistant message pairs until the total
    token count is within the active model’s limit. The system prompt
    is never removed. The TRUNCATED flag is set if truncation occurs.

    Returns:
        bool: True if truncation occurred, False otherwise.

    Example:
        >>> if gptsession.trunc():
        ...     print("Session was truncated to stay within token limits.")
    """
    n = count()  # count tokens
    while n > g[SEL][MODEL][TOKENLIMIT]:
        # remove the first (user) message
        assert g[SEL][MESSAGES][1]["role"] == "user"
        g[SEL][MESSAGES].pop(1)
        n -= g[SEL][TOKENCOUNTS].pop(1)
        assert g[SEL][MESSAGES][1]["role"] == "assistant"
        g[SEL][MESSAGES].pop(1)
        n -= g[SEL][TOKENCOUNTS].pop(1)
        g[SEL][TRUNCATED] = True
    return g[SEL][TRUNCATED]

def truncated():
    """
    Check whether the current session has been truncated.

    This reflects whether any messages have been removed due to
    token limits. The flag is cleared when a session is restarted.

    Returns:
        bool: True if truncation has occurred, False otherwise.

    Example:
        >>> if gptsession.truncated():
        ...     print("Some earlier messages were removed.")
    """
    return g[SEL][TRUNCATED]

def record():
    """
    Return the full untruncated message history for the current session.

    This includes all system, user, and assistant messages in order,
    even those that were removed from the active session due to
    truncation.  Useful for logging, reviewing, or replaying a complete
    conversation.

    Returns:
        list: A list of message dictionaries in OpenAI chat format.

    Example:
        >>> history = gptsession.record()
        >>> for msg in history:
        ...     print(f"[{msg['role']}] {msg['content']}")
    """
    return g[SEL][RECORD]

