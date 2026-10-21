# Task 1 - Voice Assistant (J.A.R.V.I.S)

OIBSIP internship, Python Programming track, **Beginner tier**.

A voice assistant with a Python (Flask) backend and a sci-fi web interface. The microphone is captured in Python with `speech_recognition`, and every reply is spoken with `pyttsx3`.

## Beginner-tier checklist

- [x] Capture voice input using `speech_recognition` (microphone)
- [x] Respond to "Hello" with a predefined greeting
- [x] Tell the current time and date on request
- [x] Perform a web search on a user-specified topic (opens browser with the query)
- [x] Graceful error handling: if voice is not understood, ask the user to repeat
- [x] Text-to-speech feedback using `pyttsx3` for all responses

## Extra features

- Login / register system (passwords stored as salted hashes in SQLite)
- Mood detection replies (happy, sad, tired, angry, bored)
- Random music player, password generator, safe calculator
- Open Google, YouTube, Instagram and ChatGPT by voice
- Typed-command box for when no microphone is available

## Tech stack

Python, Flask, Flask-CORS, SpeechRecognition, PyAudio, pyttsx3, SQLite, HTML/CSS/JavaScript

## How to run

1. Use Python 3.12 or 3.13 (PyAudio has no ready-made build for the newest versions).
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the backend:
   ```
   python backend.py
   ```
4. Open `login.html` in your browser, register, log in, and click the microphone.

## Example commands

- "Hello"
- "What's the time?" / "What's the date?"
- "Search for Python tutorials"
- "Calculate 12 plus 8"
- "Play music"
- "I'm feeling tired"

## Files

| File | Purpose |
|------|---------|
| `backend.py` | Flask server: voice capture, command handling, text-to-speech |
| `database.py` | SQLite user storage with hashed passwords |
| `musiclibrary.py` | Song list and player |
| `login.html`, `index.html` | Login page and assistant interface |
| `main.js`, `style.css` | Frontend logic and styling |

## Author

Somay
