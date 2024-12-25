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

    // Convert Markdown to HTML using the marked library (use parse() for v4.x)
    if (type === 'bot') {
        let htmlContent = marked.parse(message);  // Correct usage of marked for v4.x
        
        // Optionally sanitize the HTML to prevent XSS
        htmlContent = DOMPurify.sanitize(htmlContent);
        
        messageElement.innerHTML = htmlContent;
    } else {
        messageElement.textContent = message;  // Regular text for user
    }

    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
