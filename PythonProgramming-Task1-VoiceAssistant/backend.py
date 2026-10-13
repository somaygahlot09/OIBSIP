import ast
import datetime
import operator
import queue
import random
import re
import string
import threading
import webbrowser
from urllib.parse import quote_plus
import subprocess
import sys

import pyttsx3
import speech_recognition as sr
from flask import Flask, jsonify, request
from flask_cors import CORS

import musiclibrary
from database import create_db, login_user, register_user

app = Flask(__name__)
CORS(app)
create_db()


# ------------------------------------------------------------------
# TEXT-TO-SPEECH (pyttsx3) - every reply Jarvis gives is spoken.
# One background thread owns the engine, so Flask requests never block
# on speech and pyttsx3 is never touched from two threads at once.
# ------------------------------------------------------------------
_speech_queue = queue.Queue()


_TTS_CODE = (
    "import sys, pyttsx3\n"
    "e = pyttsx3.init()\n"
    "v = e.getProperty('voices')\n"
    "if len(v) > 1: e.setProperty('voice', v[1].id)\n"
    "e.setProperty('rate', 170)\n"
    "e.setProperty('volume', 1.0)\n"
    "e.say(sys.argv[1])\n"
    "e.runAndWait()\n"
)


def _speech_worker():
    while True:
        text = _speech_queue.get()
        try:
            # a fresh process per sentence, so pyttsx3 never gets stuck
            subprocess.run([sys.executable, "-c", _TTS_CODE, text], timeout=60)
        except Exception as e:
            print("Speech Error:", e)
        finally:
            _speech_queue.task_done()
            


threading.Thread(target=_speech_worker, daemon=True).start()


def speak(text):
    """Print and queue text for pyttsx3 to say out loud."""
    print(f"JARVIS: {text}")
    _speech_queue.put(text)


# ------------------------------------------------------------------
# SKILLS
# ------------------------------------------------------------------
def has_word(command, *words):
    """True if any of the words appears as a whole word in the command."""
    return any(re.search(rf"\b{re.escape(w)}\b", command) for w in words)


def greet():
    return random.choice([
        "Hello! I am Jarvis, at your service. How can I help you today?",
        "Hi there! Jarvis online and ready.",
        "Hello! What can I do for you?",
    ])


def tell_time_and_date(command):
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %d %B %Y")

    wants_time = has_word(command, "time")
    wants_date = has_word(command, "date", "today")

    if wants_time and wants_date:
        return f"It is {time_str} on {date_str}."
    if wants_date:
        return f"Today is {date_str}."
    return f"The current time is {time_str}."


def web_search(command):
    """Open the browser with a search for the topic the user spoke."""
    match = re.search(
        r"\b(?:search(?:\s+(?:the\s+web|google|on\s+google))?(?:\s+for)?|look\s+up|google)\s+(.+)",
        command,
    )
    topic = match.group(1).strip(" .?!") if match else ""
    if not topic:
        return "What should I search for? Try saying: search for, followed by your topic."

    webbrowser.open(f"https://www.google.com/search?q={quote_plus(topic)}")
    return f"Searching the web for {topic}"


# Safe calculator: only + - * / % and brackets, no eval()
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculate_expression(command):
    """Understands '12 plus 8', '5 times 3', '(2+3)*4' and similar."""
    spoken = {
        r"\bplus\b": "+",
        r"\bminus\b": "-",
        r"\b(?:times|multiplied by)\b": "*",
        r"\b(?:divided by|over)\b": "/",
    }
    for pattern, symbol in spoken.items():
        command = re.sub(pattern, symbol, command)

    expression = re.sub(r"[^0-9+\-*/%().]", "", command)
    if not re.search(r"\d", expression):
        return "Sorry, I couldn't find any numbers to calculate."
    try:
        result = _safe_eval(ast.parse(expression, mode="eval"))
        if isinstance(result, float):
            result = int(result) if result.is_integer() else round(result, 4)
        return f"The answer is {result}"
    except ZeroDivisionError:
        return "I can't divide by zero."
    except Exception as e:
        print("Calc Error:", e)
        return "Sorry, I couldn't calculate that."


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.SystemRandom().choice(characters) for _ in range(length))
    return f"Here is your secure password: {password}"


def detect_mood(command):
    mood_responses = {
        "happy": [
            "That's great to hear! Keep smiling, it suits you.",
            "Wonderful! Let's make today even better.",
            "Nice! I'm glad you're in a good mood.",
        ],
        "sad": [
            "I'm sorry to hear that. Remember, you're stronger than you think.",
            "It's okay to feel sad sometimes. Do you want me to play something relaxing?",
            "I'm here for you. Want me to play your favorite song?",
        ],
        "tired": [
            "You should take a short break or get some rest.",
            "You've been working hard. Let's slow down a bit.",
            "How about I play some calming music for you?",
        ],
        "angry": [
            "Take a deep breath. You'll feel better in a moment.",
            "Let's focus on something positive.",
            "Maybe a bit of music could help you relax?",
        ],
        "bored": [
            "Hmm, sounds like you need some entertainment. Should I open YouTube?",
            "Let's shake things up a little! Want to play a song?",
            "Boredom won't stand a chance when I'm around.",
        ],
    }
    for mood, responses in mood_responses.items():
        if has_word(command, mood):
            return random.choice(responses)
    return None


def play_music():
    try:
        return f"Playing {musiclibrary.play_random()}"
    except Exception as e:
        print("Music Error:", e)
        return "Sorry, I couldn't play any song right now."


# ------------------------------------------------------------------
# COMMAND ROUTER - shared by typed commands and voice commands
# ------------------------------------------------------------------
def handle_command(command):
    command = command.lower().strip()

    # Web search first, so "search for time zones" isn't mistaken for "time"
    if has_word(command, "search", "google") and "open google" not in command or "look up" in command:
        return web_search(command)

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"
    if "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram"
    if "open chatgpt" in command:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT"

    if has_word(command, "time", "date", "today"):
        return tell_time_and_date(command)

    if has_word(command, "hello", "hi", "hey"):
        return greet()

    if "calculate" in command or ("what is" in command and re.search(r"\d", command)):
        return calculate_expression(command)

    if "generate password" in command or "make password" in command:
        return generate_password()

    if "play music" in command or "play song" in command:
        return play_music()

    mood_reply = detect_mood(command)
    if mood_reply:
        return mood_reply

    return ("Sorry, I didn't understand that. Try saying hello, asking the time or date, "
            "or saying: search for, followed by a topic.")


# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Please provide both username and password"}), 400

    if register_user(username, password):
        return jsonify({"message": "Registration successful"})
    return jsonify({"error": "Username already exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Please provide both username and password"}), 400

    if login_user(username, password):
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/process", methods=["POST"])
def process():
    """Typed commands from the text box."""
    data = request.get_json() or {}
    command = data.get("command", "")
    reply = handle_command(command) if command.strip() else "I didn't receive a command."
    speak(reply)
    return jsonify({"heard": command, "reply": reply})


def _retry_reply(message):
    """Graceful error: Jarvis says (and returns) a friendly 'please repeat'."""
    speak(message)
    return jsonify({"heard": None, "reply": message, "ok": False})


@app.route("/listen", methods=["POST"])
def listen():
    """Capture voice from the microphone with speech_recognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        heard = recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        return _retry_reply("I didn't hear anything. Please try again.")
    except sr.UnknownValueError:
        return _retry_reply("Sorry, I couldn't understand that. Could you please repeat?")
    except sr.RequestError:
        return _retry_reply("I can't reach the speech service. Please check your internet connection.")
    except (OSError, AttributeError):
        return _retry_reply("I can't access a microphone. Please check it and that PyAudio is installed.")

    reply = handle_command(heard)
    speak(reply)
    return jsonify({"heard": heard, "reply": reply, "ok": True})


if __name__ == "__main__":
    # use_reloader=False keeps a single speech thread / microphone owner
    app.run(debug=True, use_reloader=False)
