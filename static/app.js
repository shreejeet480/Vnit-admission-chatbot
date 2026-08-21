/* VNIT Admission Assistant — chat frontend */

const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("send");
const suggestionsEl = document.getElementById("suggestions");

const sessionId = crypto.randomUUID();
let userName = "";

/* ---------- Minimal Markdown → HTML renderer ----------
   Converts **bold**, bullet lines, and newlines to real HTML,
   so answers show real bold instead of literal ** symbols.     */
function renderMarkdown(text) {
  // Escape HTML first (safety)
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // **bold**  ->  <strong>bold</strong>
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Turn "• item" or "- item" lines into list items
  const lines = html.split("\n");
  let out = "";
  let inList = false;
  for (let line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("•") || trimmed.startsWith("- ")) {
      if (!inList) { out += "<ul>"; inList = true; }
      out += "<li>" + trimmed.replace(/^([•]|- )\s*/, "") + "</li>";
    } else {
      if (inList) { out += "</ul>"; inList = false; }
      out += line + "<br>";
    }
  }
  if (inList) out += "</ul>";
  return out;
}

function addUserMessage(text) {
  const msg = document.createElement("div");
  msg.className = "msg user";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  msg.appendChild(bubble);
  messagesEl.appendChild(msg);
  scrollToBottom();
}

function addBotMessage(text, meta) {
  const msg = document.createElement("div");
  msg.className = "msg bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = renderMarkdown(text);   // render markdown (real bold)
  msg.appendChild(bubble);

  // Signature: ML telemetry strip — intent, confidence, source
  if (meta && meta.intent) {
    const strip = document.createElement("div");
    strip.className = "telemetry";

    const tag = document.createElement("span");
    tag.className = "intent-tag";
    tag.textContent = meta.intent;

    const bar = document.createElement("span");
    bar.className = "conf-bar";
    const fill = document.createElement("span");
    fill.className = "conf-fill";
    fill.style.width = "0%";
    bar.appendChild(fill);

    const pct = document.createElement("span");
    pct.textContent = Math.round((meta.confidence || 0) * 100) + "%";

    const src = document.createElement("span");
    src.className = "source-tag " + (meta.source === "ml" ? "ml" : "rules");
    src.textContent = meta.source === "ml" ? "· ML model" : "· rules fallback";

    strip.append(tag, bar, pct, src);
    msg.appendChild(strip);

    requestAnimationFrame(() => {
      fill.style.width = Math.round((meta.confidence || 0) * 100) + "%";
    });
  }

  messagesEl.appendChild(msg);
  scrollToBottom();
}

function showTyping() {
  const msg = document.createElement("div");
  msg.className = "msg bot";
  msg.id = "typing-msg";
  msg.innerHTML =
    '<div class="bubble"><span class="typing"><span></span><span></span><span></span></span></div>';
  messagesEl.appendChild(msg);
  scrollToBottom();
}

function hideTyping() {
  const t = document.getElementById("typing-msg");
  if (t) t.remove();
}

function renderSuggestions(list) {
  suggestionsEl.innerHTML = "";
  (list || []).slice(0, 4).forEach((s) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = s;
    suggestionsEl.appendChild(chip);
  });
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function send(text) {
  const message = (text || inputEl.value).trim();
  if (!message) return;

  inputEl.value = "";
  addUserMessage(message);
  showTyping();
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId, user_name: userName }),
    });
    const data = await res.json();
    hideTyping();

    if (data.error) {
      addBotMessage("Something went wrong. Try rephrasing your question.");
    } else {
      addBotMessage(data.response, {
        intent: data.intent,
        confidence: data.confidence,
        source: data.intent_source,
      });
      renderSuggestions(data.suggestions);
    }
  } catch (err) {
    hideTyping();
    addBotMessage("Could not reach the server. Check that the app is running and try again.");
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener("click", () => send());
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") send();
});
suggestionsEl.addEventListener("click", (e) => {
  if (e.target.classList.contains("chip")) send(e.target.textContent);
});

/* ---------- Name pop-up before chat starts ---------- */
function startChat(name) {
  userName = name.trim();
  const overlay = document.getElementById("name-overlay");
  if (overlay) overlay.remove();

  const greeting = userName
    ? `🍊 Hello **${userName}**! Welcome to the VNIT Admission Assistant. Ask me anything about programs, eligibility, entrance exams, fees, documents, counselling, or placements.`
    : `🍊 Welcome to the VNIT Admission Assistant. Ask me anything about admissions.`;
  addBotMessage(greeting, null);
  inputEl.focus();
}

function buildNameOverlay() {
  const overlay = document.createElement("div");
  overlay.id = "name-overlay";
  overlay.innerHTML = `
    <div class="name-card">
      <h2>Welcome! 👋</h2>
      <p>What's your name?</p>
      <input type="text" id="name-input" placeholder="Enter your name" autocomplete="off" />
      <button id="name-submit">Start Chatting</button>
    </div>`;
  document.body.appendChild(overlay);

  const nameInput = document.getElementById("name-input");
  const nameSubmit = document.getElementById("name-submit");
  nameInput.focus();

  nameSubmit.addEventListener("click", () => startChat(nameInput.value || ""));
  nameInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") startChat(nameInput.value || "");
  });
}

// Show the name pop-up on load
buildNameOverlay();