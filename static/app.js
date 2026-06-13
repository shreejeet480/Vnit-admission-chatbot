/* VNIT Admission Assistant — chat frontend */

const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("send");
const suggestionsEl = document.getElementById("suggestions");

const sessionId = crypto.randomUUID();

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
  bubble.textContent = text;
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
      body: JSON.stringify({ message, session_id: sessionId }),
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

inputEl.focus();
