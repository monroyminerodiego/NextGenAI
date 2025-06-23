// =============== VARIABLES ===============
let currentChatId = null;
let chats = {};
let messageHistory = [];
const MAX_CHATS = 10;
const MAX_MESSAGE_LENGTH = 4000;

// =============== DOM ELEMENTS ===============
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const newChatBtn = document.getElementById('newChatBtn');
const clearChatBtn = document.getElementById('clearChatBtn');
const chatList = document.getElementById('chatList');
const storageInfo = document.getElementById('storageInfo');
const welcomeMessage = document.getElementById('welcomeMessage');
const messages = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const charCount = document.getElementById('charCount');
const warningModal = document.getElementById('warningModal');
const modalClose = document.getElementById('modalClose');
const modalOk = document.getElementById('modalOk');

// =============== INITIALIZATION ===============
document.addEventListener('DOMContentLoaded', function() {
    loadChatsFromStorage();
    updateStorageInfo();
    initializeEventListeners();
    autoResizeTextarea();
});

// =============== EVENT LISTENERS ===============
function initializeEventListeners() {
    // Sidebar toggle
    mobileMenuBtn.addEventListener('click', toggleSidebar);
    sidebarToggle.addEventListener('click', toggleSidebar);
    
    // New chat
    newChatBtn.addEventListener('click', createNewChat);
    
    // Clear chat
    clearChatBtn.addEventListener('click', clearCurrentChat);
    
    // Send message
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', handleKeyPress);
    messageInput.addEventListener('input', handleInputChange);
    
    // Modal
    modalClose.addEventListener('click', closeModal);
    modalOk.addEventListener('click', closeModal);
    warningModal.addEventListener('click', function(e) {
        if (e.target === warningModal) {
            closeModal();
        }
    });
    
    // Close sidebar on outside click (mobile)
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && 
            sidebar.classList.contains('open') && 
            !sidebar.contains(e.target) && 
            !mobileMenuBtn.contains(e.target)) {
            closeSidebar();
        }
    });
}

// =============== SIDEBAR FUNCTIONS ===============
function toggleSidebar() {
    sidebar.classList.toggle('open');
}

function closeSidebar() {
    sidebar.classList.remove('open');
}

// =============== CHAT MANAGEMENT ===============
function createNewChat() {
    const chatId = generateChatId();
    const chatTitle = 'Nueva conversación';
    
    // Check if we need to remove old chats
    const chatIds = Object.keys(chats);
    if (chatIds.length >= MAX_CHATS) {
        // Remove oldest chat
        const oldestChatId = chatIds.reduce((oldest, chatId) => {
            return chats[chatId].createdAt < chats[oldest].createdAt ? chatId : oldest;
        });
        delete chats[oldestChatId];
    }
    
    // Create new chat
    chats[chatId] = {
        id: chatId,
        title: chatTitle,
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now()
    };
    
    currentChatId = chatId;
    messageHistory = [];
    
    renderChatList();
    clearMessagesDisplay();
    showWelcomeMessage();
    updateStorageInfo();
    saveChatsToStorage();
    closeSidebar();
}

function loadChat(chatId) {
    if (!chats[chatId]) return;
    
    currentChatId = chatId;
    messageHistory = [...chats[chatId].messages];
    
    renderMessages();
    hideWelcomeMessage();
    renderChatList();
    closeSidebar();
}

function clearCurrentChat() {
    if (!currentChatId) return;
    
    chats[currentChatId].messages = [];
    messageHistory = [];
    
    clearMessagesDisplay();
    showWelcomeMessage();
    saveChatsToStorage();
}

function deleteChat(chatId) {
    if (!chats[chatId]) return;
    
    delete chats[chatId];
    
    if (currentChatId === chatId) {
        currentChatId = null;
        messageHistory = [];
        clearMessagesDisplay();
        showWelcomeMessage();
    }
    
    renderChatList();
    updateStorageInfo();
    saveChatsToStorage();
}

// =============== MESSAGE FUNCTIONS ===============
function sendMessage() {
    const text = messageInput.value.trim();
    
    if (!text) return;
    
    if (text.length > MAX_MESSAGE_LENGTH) {
        showWarningModal();
        return;
    }
    
    // Create chat if doesn't exist
    if (!currentChatId) {
        createNewChat();
    }
    
    // Add user message
    const userMessage = {
        id: generateMessageId(),
        type: 'user',
        content: text,
        timestamp: Date.now()
    };
    
    addMessage(userMessage);
    messageInput.value = '';
    updateCharCount();
    autoResizeTextarea();
    updateSendButton();
    
    // Hide welcome message
    hideWelcomeMessage();
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate bot response
    setTimeout(() => {
        hideTypingIndicator();
        const botResponse = generateBotResponse(text);
        const botMessage = {
            id: generateMessageId(),
            type: 'bot',
            content: botResponse,
            timestamp: Date.now()
        };
        addMessage(botMessage);
    }, 1000 + Math.random() * 2000);
}

function addMessage(message) {
    messageHistory.push(message);
    
    if (currentChatId && chats[currentChatId]) {
        chats[currentChatId].messages.push(message);
        chats[currentChatId].updatedAt = Date.now();
        
        // Update chat title if it's the first message
        if (chats[currentChatId].messages.length === 1 && message.type === 'user') {
            chats[currentChatId].title = message.content.substring(0, 50) + (message.content.length > 50 ? '...' : '');
        }
    }
    
    renderMessage(message);
    saveChatsToStorage();
    renderChatList();
    scrollToBottom();
}

function renderMessages() {
    clearMessagesDisplay();
    messageHistory.forEach(message => {
        renderMessage(message);
    });
    scrollToBottom();
}

function renderMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${message.type}`;
    messageElement.innerHTML = `
        <div class="message-avatar">
            ${message.type === 'user' ? '<i class="ti ti-user"></i>' : '🦩'}
        </div>
        <div class="message-content">
            ${message.content}
            <div class="message-time">${formatTime(message.timestamp)}</div>
        </div>
    `;
    
    messages.appendChild(messageElement);
}

function clearMessagesDisplay() {
    messages.innerHTML = '';
}

function showTypingIndicator() {
    const typingElement = document.createElement('div');
    typingElement.className = 'message bot';
    typingElement.id = 'typing-indicator';
    typingElement.innerHTML = `
        <div class="message-avatar">🦩</div>
        <div class="typing-indicator">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messages.appendChild(typingElement);
    scrollToBottom();
}

function hideTypingIndicator() {
    const typingElement = document.getElementById('typing-indicator');
    if (typingElement) {
        typingElement.remove();
    }
}

function generateBotResponse(userMessage) {
    const responses = [
        "¡Hola! Soy Flami, tu asistente IA. Estoy aquí para ayudarte con lo que necesites.",
        "Esa es una excelente pregunta. Como Flami, puedo ayudarte con una amplia variedad de temas.",
        "Me parece muy interesante lo que me comentas. ¿Podrías darme más detalles?",
        "Como tu asistente virtual Flami, haré mi mejor esfuerzo para darte una respuesta útil.",
        "¡Perfecto! Me encanta poder ayudarte. ¿Hay algo específico en lo que pueda asistirte?",
        "Entiendo tu consulta. Permíteme ayudarte con eso de la mejor manera posible.",
        "¡Qué buena pregunta! Como Flami, siempre estoy dispuesto a aprender y ayudar.",
        "Me alegra que hayas decidido consultar conmigo. ¿En qué más puedo ayudarte?",
        "Esa información es muy valiosa. ¿Te gustaría que profundice en algún aspecto específico?",
        "Como tu flamingo asistente, estoy aquí para hacer tu día más productivo y agradable."
    ];
    
    // Simple keyword-based responses
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('hola') || lowerMessage.includes('hey') || lowerMessage.includes('buenos')) {
        return "¡Hola! 🦩 Soy Flami, tu asistente personal. ¿En qué puedo ayudarte hoy?";
    }
    
    if (lowerMessage.includes('ayuda') || lowerMessage.includes('help')) {
        return "¡Por supuesto! Estoy aquí para ayudarte. Puedes preguntarme sobre cualquier tema y haré mi mejor esfuerzo para darte una respuesta útil. ¿Qué necesitas saber?";
    }
    
    if (lowerMessage.includes('gracias') || lowerMessage.includes('thanks')) {
        return "¡De nada! Me hace muy feliz poder ayudarte. Si tienes más preguntas, no dudes en preguntarme. 😊";
    }
    
    if (lowerMessage.includes('flami') || lowerMessage.includes('flamingo')) {
        return "¡Así es! Soy Flami, tu flamingo asistente virtual. Mi color favorito es el morado y estoy aquí para hacer tu experiencia lo más agradable posible. 🦩💜";
    }
    
    if (lowerMessage.includes('adiós') || lowerMessage.includes('bye') || lowerMessage.includes('hasta luego')) {
        return "¡Hasta pronto! Ha sido un placer ayudarte. Recuerda que siempre puedes volver cuando necesites algo. ¡Cuídate! 🦩✨";
    }
    
    // Random response for other messages
    return responses[Math.floor(Math.random() * responses.length)];
}

// =============== INPUT HANDLING ===============
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function handleInputChange() {
    updateCharCount();
    autoResizeTextarea();
    updateSendButton();
}

function updateCharCount() {
    const length = messageInput.value.length;
    charCount.textContent = `${length}/${MAX_MESSAGE_LENGTH}`;
    
    // Update char count styling
    charCount.className = 'char-count';
    if (length > MAX_MESSAGE_LENGTH * 0.8) {
        charCount.classList.add('warning');
    }
    if (length > MAX_MESSAGE_LENGTH * 0.95) {
        charCount.classList.remove('warning');
        charCount.classList.add('danger');
    }
}

function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    const withinLimit = messageInput.value.length <= MAX_MESSAGE_LENGTH;
    sendBtn.disabled = !hasText || !withinLimit;
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// =============== UI FUNCTIONS ===============
function showWelcomeMessage() {
    welcomeMessage.style.display = 'flex';
}

function hideWelcomeMessage() {
    welcomeMessage.style.display = 'none';
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showWarningModal() {
    warningModal.classList.add('show');
}

function closeModal() {
    warningModal.classList.remove('show');
}

// =============== CHAT LIST RENDERING ===============
function renderChatList() {
    chatList.innerHTML = '';
    
    const sortedChats = Object.values(chats).sort((a, b) => b.updatedAt - a.updatedAt);
    
    sortedChats.forEach(chat => {
        const chatElement = document.createElement('div');
        chatElement.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
        chatElement.innerHTML = `
            <div class="chat-item-content">
                <div class="chat-item-title">${chat.title}</div>
                <div class="chat-item-time">${formatTime(chat.updatedAt)}</div>
            </div>
            <button class="chat-item-delete" onclick="deleteChat('${chat.id}')" title="Eliminar conversación">
                <i class="ti ti-trash"></i>
            </button>
        `;
        
        chatElement.addEventListener('click', (e) => {
            if (!e.target.closest('.chat-item-delete')) {
                loadChat(chat.id);
            }
        });
        
        chatList.appendChild(chatElement);
    });
}

function updateStorageInfo() {
    const chatCount = Object.keys(chats).length;
    storageInfo.textContent = `${chatCount}/${MAX_CHATS} conversaciones`;
}

// =============== STORAGE FUNCTIONS ===============
function saveChatsToStorage() {
    try {
        // Using in-memory storage only for Claude environment
        // In a real environment, you would use localStorage:
        // localStorage.setItem('flami_chats', JSON.stringify(chats));
        // localStorage.setItem('flami_current_chat', currentChatId);
        console.log('Chats saved to memory storage');
    } catch (error) {
        console.error('Error saving chats:', error);
    }
}

function loadChatsFromStorage() {
    try {
        // Using in-memory storage only for Claude environment
        // In a real environment, you would use localStorage:
        // const savedChats = localStorage.getItem('flami_chats');
        // const savedCurrentChat = localStorage.getItem('flami_current_chat');
        
        // if (savedChats) {
        //     chats = JSON.parse(savedChats);
        // }
        // if (savedCurrentChat && chats[savedCurrentChat]) {
        //     currentChatId = savedCurrentChat;
        //     messageHistory = [...chats[currentChatId].messages];
        //     renderMessages();
        //     hideWelcomeMessage();
        // }
        
        renderChatList();
        console.log('Chats loaded from memory storage');
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

// =============== UTILITY FUNCTIONS ===============
function generateChatId() {
    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 1) {
        return 'Hace un momento';
    } else if (diffInHours < 24) {
        return `Hace ${Math.floor(diffInHours)} hora${Math.floor(diffInHours) > 1 ? 's' : ''}`;
    } else if (diffInHours < 24 * 7) {
        const days = Math.floor(diffInHours / 24);
        return `Hace ${days} día${days > 1 ? 's' : ''}`;
    } else {
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short'
        });
    }
}

// =============== GLOBAL FUNCTIONS ===============
// Make deleteChat available globally for onclick handlers
window.deleteChat = deleteChat;