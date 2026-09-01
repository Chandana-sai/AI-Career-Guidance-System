function sendChatMessage(messageText) {
  const inputEl = document.getElementById("chatInput");
  const msg = messageText || (inputEl ? inputEl.value.trim() : "");
  if (!msg) return;

  const container = document.getElementById("chatMessagesContainer");
  if (!container) return;

  // Append user bubble
  const userBubble = document.createElement("div");
  userBubble.className = "d-flex justify-content-end mb-3";
  userBubble.innerHTML = `<div class="chat-bubble-user shadow-sm">${escapeHtml(msg)}</div>`;
  container.appendChild(userBubble);

  if (inputEl) inputEl.value = "";
  container.scrollTop = container.scrollHeight;

  // Show typing placeholder
  const typingBubble = document.createElement("div");
  typingBubble.id = "typingIndicator";
  typingBubble.className = "d-flex justify-content-start mb-3";
  typingBubble.innerHTML = `<div class="chat-bubble-bot shadow-sm"><i class="bi bi-three-dots"></i> AI Advisor is thinking...</div>`;
  container.appendChild(typingBubble);
  container.scrollTop = container.scrollHeight;

  fetch("/chatbot/api/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken()
    },
    body: JSON.stringify({ message: msg })
  })
    .then(res => res.json())
    .then(data => {
      const typing = document.getElementById("typingIndicator");
      if (typing) typing.remove();

      const botBubble = document.createElement("div");
      botBubble.className = "d-flex justify-content-start mb-3";
      
      // Format markdown-like bold and linebreaks
      let formattedReply = escapeHtml(data.reply)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");

      let chipsHtml = "";
      if (data.suggested_chips && data.suggested_chips.length > 0) {
        chipsHtml = `<div class="d-flex flex-wrap gap-2 mt-2">` +
          data.suggested_chips.map(chip => `<button class="chip-btn" onclick="sendChatMessage(\x27${escapeHtml(chip)}\x27)">${escapeHtml(chip)}</button>`).join("") +
          `</div>`;
      }

      botBubble.innerHTML = `<div class="chat-bubble-bot shadow-sm">
        <div class="fw-semibold text-primary mb-1"><i class="bi bi-robot me-1"></i> AI Career Advisor</div>
        <div>${formattedReply}</div>
        ${chipsHtml}
      </div>`;
      container.appendChild(botBubble);
      container.scrollTop = container.scrollHeight;
    })
    .catch(err => {
      const typing = document.getElementById("typingIndicator");
      if (typing) typing.remove();
      console.error(err);
    });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.innerText = text;
  return div.innerHTML;
}

function getCsrfToken() {
  const cookieValue = document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
  return cookieValue || "";
}
