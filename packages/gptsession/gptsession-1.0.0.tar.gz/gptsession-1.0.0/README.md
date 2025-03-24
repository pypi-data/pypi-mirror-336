# gptsession

**Simple, stateful conversations with OpenAI's chat models, including truncation and token metering.**

`gptsession` is a lightweight Python module for managing structured, multi-turn conversations with OpenAI’s ChatGPT models. It supports multiple concurrent sessions, automatic token tracking, message truncation, and full conversation recording.

---

## 📦 Installation

```bash
pip install gptsession
```

---

## ✨ Features

- Supports multiple parallel chat sessions
- Token-aware truncation based on model limits
- Tracks actual tokens sent and received
- Maintains full untruncated conversation history
- Clean, minimal API: `setup()`, `say()`, `system()`, `model()`, etc.

---

## 🚀 Quick Start

```python
import gptsession

gptsession.setup(open("mykey.txt").read().strip())
gptsession.new()
gptsession.model("gpt-3.5-turbo")
gptsession.system("You are a helpful assistant.")

reply = gptsession.say("Hello! Can you explain recursion?")
print("ChatGPT:", reply)

if gptsession.truncated():
    print("[Note: Earlier messages were removed to stay within token limits.]")
```

---

## 🔄 Multiple Sessions Example

```python
import gptsession as gpt

gpt.setup(open("mykey.txt").read().strip())

s1 = gpt.new()
gpt.system("You are a bird.")

s2 = gpt.new()
gpt.system("You are a robot.")

gpt.sel(s1)
print(gpt.say("Where do you live?"))

gpt.sel(s2)
print(gpt.say("Where do you live?"))
```

---

## 📄 License

MIT License  
© 2025 Lion Kimbro

---

## 🌐 Project Links

- [Homepage](https://github.com/LionKimbro/gptsession)
- [Bug Tracker](https://github.com/LionKimbro/gptsession/issues)
