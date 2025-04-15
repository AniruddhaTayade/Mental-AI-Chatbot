// chatbot.js

document.getElementById('send-button').onclick = function() {
    const userMessage = document.getElementById('user-input').value;
    if (userMessage.trim()) {
        addMessageToChatLog("You: " + userMessage, 'user');
        document.getElementById('user-input').value = '';

        // Send user message to the server
        fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChatLog("Bot: " + data.response, 'bot');
        });
    }
};

function addMessageToChatLog(message, sender) {
    const chatLog = document.getElementById('chat-log');
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.textContent = message;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
}

document.getElementById('close-chat').onclick = function() {
    document.getElementById('chat-container').style.display = 'none'; // Close chat window
};

