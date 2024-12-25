// app/js/script.js
const sendButton = document.getElementById('sendButton');
const chatInput = document.getElementById('chatInput');
const chatWindow = document.getElementById('chatWindow');

if (sendButton) {
    sendButton.addEventListener('click', function() {
        sendMessage();
    });
}

function sendMessage() {
    const message = chatInput.value;
    if (message.trim() !== '') {
        displayMessage('user', message);
        chatInput.value = '';

        // Send the message to FastAPI backend to get a response from GPT-4
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            displayMessage('bot', data.response || "Sorry, I didn't get that.");
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('bot', 'An error occurred.');
        });
    }
}

function displayMessage(type, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(type === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
