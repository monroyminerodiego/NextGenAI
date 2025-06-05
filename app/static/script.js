const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const toggleDark = document.getElementById("toggle-dark");
const historyMenu = document.getElementById("chat-history");
const newChatBtn = document.getElementById("new-chat");

document.body.classList.add("dark-mode");

let currentChat = [];
let chatCounter = parseInt(localStorage.getItem("chatCounter")) || 0;

function loadHistory() {
  historyMenu.innerHTML = "";

  // Mostrar Chat actual arriba
  const currentLi = document.createElement("li");
  currentLi.textContent = "Chat actual";
  currentLi.style.fontWeight = "bold";
  currentLi.style.backgroundColor = "#b3d4fc"; // color visual de selección
  currentLi.onclick = () => {
    chatWindow.innerHTML = "";
    currentChat.forEach(entry => renderMessage(entry.text, entry.from));
  };
  historyMenu.appendChild(currentLi);

  // Resto del historial guardado
  for (let i = 1; i <= chatCounter; i++) {
    const chat = JSON.parse(localStorage.getItem(`chat_${i}`));
    const firstMessage = chat?.find(m => m.from !== "system")?.text || `Chat ${i}`;
    const li = document.createElement("li");
    li.textContent = `Chat ${i}: ${firstMessage.slice(0, 20)}...`;
    li.onclick = () => {
      chatWindow.innerHTML = "";
      chat.forEach(entry => renderMessage(entry.text, entry.from));
    };
    historyMenu.appendChild(li);
  }
}


function renderMessage(message, from = "user") {
  const msg = document.createElement("div");
  msg.className = `message ${from}`;
  msg.textContent = message;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function saveChatToHistory() {
  if (currentChat.length > 0) {
    chatCounter++;
    localStorage.setItem("chatCounter", chatCounter);
    localStorage.setItem(`chat_${chatCounter}`, JSON.stringify(currentChat));
    loadHistory();
    currentChat = [];
    chatWindow.innerHTML = "";
  }
}


chatForm.onsubmit = (e) => {
  e.preventDefault();
  const text = chatInput.value;
  if (!text) return;
  renderMessage(text, "user");
  currentChat.push({ text, from: "user" });

  setTimeout(() => {
    const response = "Respuesta simulada de ChatGPT";
    renderMessage(response, "bot");
    currentChat.push({ text: response, from: "bot" });
  }, 500);

  chatInput.value = "";
};

toggleDark.onclick = () => {
  document.body.classList.toggle("dark-mode");
};

newChatBtn.onclick = () => {
  saveChatToHistory();
};

loadHistory();

window.addEventListener("beforeunload", () => {
  for (let i = 1; i <= chatCounter; i++) {
    localStorage.removeItem(`chat_${i}`);
  }
  localStorage.removeItem("chatCounter");
});