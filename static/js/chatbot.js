let currentLanguage = localStorage.getItem("careerMateLang") || "en";
let isListening = false;
let recognition = null;

// Initialize Web Speech Recognition
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    const inputEl = document.getElementById("chatInput");
    if (inputEl) {
      inputEl.value = transcript;
      sendChatMessage(transcript);
    }
    stopVoiceRecognition();
  };

  recognition.onerror = function (event) {
    console.warn("Speech recognition error:", event.error);
    stopVoiceRecognition();
  };

  recognition.onend = function () {
    stopVoiceRecognition();
  };
}

function setChatLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem("careerMateLang", lang);
  
  // Update select dropdowns if present
  document.querySelectorAll(".lang-selector").forEach(el => el.value = lang);
  
  // Update UI headers if element exists
  const langBadge = document.getElementById("activeLangBadge");
  if (langBadge) {
    const labels = { en: "English", te: "?????? (Telugu)", hi: "????? (Hindi)" };
    langBadge.innerText = labels[lang] || "English";
  }
}

function toggleVoiceInput() {
  if (!recognition) {
    alert("Speech recognition is not supported in this browser. Please use Google Chrome, Edge, or a Web Speech-enabled browser.");
    return;
  }

  const micBtn = document.getElementById("micBtn");
  if (!isListening) {
    // Set speech recognition language
    const langCodes = { en: "en-IN", te: "te-IN", hi: "hi-IN" };
    recognition.lang = langCodes[currentLanguage] || "en-US";

    try {
      recognition.start();
      isListening = true;
      if (micBtn) {
        micBtn.classList.add("btn-danger", "pulse-animation");
        micBtn.classList.remove("btn-outline-primary", "btn-light");
      }
    } catch (e) {
      console.error(e);
    }
  } else {
    stopVoiceRecognition();
  }
}

function stopVoiceRecognition() {
  if (recognition && isListening) {
    recognition.stop();
  }
  isListening = false;
  const micBtn = document.getElementById("micBtn");
  if (micBtn) {
    micBtn.classList.remove("btn-danger", "pulse-animation");
    micBtn.classList.add("btn-light");
  }
}

function speakText(text) {
  if (!("speechSynthesis" in window)) {
    alert("Text-to-Speech is not supported in this browser.");
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  // Strip markdown formatting characters
  const cleanText = text.replace(/[\*\_#`]/g, "").replace(/<[^>]*>?/gm, "");
  const utterance = new SpeechSynthesisUtterance(cleanText);

  const langCodes = { en: "en-IN", te: "te-IN", hi: "hi-IN" };
  utterance.lang = langCodes[currentLanguage] || "en-US";
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  window.speechSynthesis.speak(utterance);
}

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
  typingBubble.innerHTML = `<div class="chat-bubble-bot shadow-sm"><i class="bi bi-three-dots"></i> CareerMate is typing...</div>`;
  container.appendChild(typingBubble);
  container.scrollTop = container.scrollHeight;

  fetch("/chatbot/api/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken()
    },
    body: JSON.stringify({ message: msg, language: currentLanguage })
  })
    .then(res => res.json())
    .then(data => {
      const typing = document.getElementById("typingIndicator");
      if (typing) typing.remove();

      const botBubble = document.createElement("div");
      botBubble.className = "d-flex justify-content-start mb-3";
      
      let formattedReply = escapeHtml(data.reply)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");

      let chipsHtml = "";
      if (data.suggested_chips && data.suggested_chips.length > 0) {
        chipsHtml = `<div class="d-flex flex-wrap gap-2 mt-2">` +
          data.suggested_chips.map(chip => `<button class="chip-btn" onclick="sendChatMessage(\x27${escapeHtml(chip)}\x27)">${escapeHtml(chip)}</button>`).join("") +
          `</div>`;
      }

      // Encode for speech button
      const rawTextForSpeech = escapeHtml(data.reply).replace(/\"/g, "&quot;");

      botBubble.innerHTML = `<div class="chat-bubble-bot shadow-sm">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="fw-semibold text-primary"><i class="bi bi-robot me-1"></i> CareerMate Assistant</span>
          <button class="btn btn-sm btn-link text-secondary p-0" title="Listen / ?????? / ?????" onclick="speakText(\x27${rawTextForSpeech}\x27)">
            <i class="bi bi-volume-up-fill fs-5 text-primary"></i>
          </button>
        </div>
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
