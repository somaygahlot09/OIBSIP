const API = "http://127.0.0.1:5000";

// Redirect to login if not logged in
if (!localStorage.getItem("loggedInUser")) {
  window.location.href = "login.html";
}

const micButton = document.getElementById("micButton");
const micCircle = document.getElementById("micCircle");
const chatBox = document.getElementById("chatBox");
const textForm = document.getElementById("textForm");
const textInput = document.getElementById("textInput");
const logoutBtn = document.getElementById("logoutBtn");

let busy = false;

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msg;
}

function setBusy(state) {
  busy = state;
  micCircle.classList.toggle("listening", state);
}

function backendError(err) {
  addMessage("Error: cannot reach backend. Start the Python server (python backend.py).", "jarvis");
  console.error("Backend error:", err);
}

// Voice: the Python backend records from the microphone (speech_recognition)
// and speaks the answer with pyttsx3, so the browser only shows the result.
async function listen() {
  if (busy) return;
  setBusy(true);
  const pending = addMessage("Listening... speak now.", "jarvis");

  try {
    const res = await fetch(`${API}/listen`, { method: "POST" });
    const data = await res.json();
    pending.remove();
    if (data.heard) addMessage(data.heard, "user");
    addMessage(data.reply, "jarvis");
  } catch (err) {
    pending.remove();
    backendError(err);
  } finally {
    setBusy(false);
  }
}

// Typed commands (handy when there's no microphone)
async function sendText(command) {
  if (busy || !command.trim()) return;
  setBusy(true);
  addMessage(command, "user");

  try {
    const res = await fetch(`${API}/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command }),
    });
    const data = await res.json();
    addMessage(data.reply, "jarvis");
  } catch (err) {
    backendError(err);
  } finally {
    setBusy(false);
  }
}

micButton.addEventListener("click", listen);

textForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const command = textInput.value;
  textInput.value = "";
  sendText(command);
});

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
});
