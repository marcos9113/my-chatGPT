// script.js

// Login Form Handling
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const password = document.getElementById('password').value;
        if (password === 'yourPassword') { // Replace 'yourPassword' with the actual password
            window.location.href = 'chat.html';
        } else {
            alert('Incorrect password!');
        }
    });
}

// Chat Interface Logic
const chatWindow = document.getElementById('chatWindow');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const fileUpload = document.getElementById('fileUpload');

if (sendButton) {
    sendButton.addEventListener('click', function() {
        sendMessage();
    });
}

if (chatInput) {
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

if (fileUpload) {
    fileUpload.addEventListener('change', function() {
        const fileName = this.value.split('\\').pop();
        if (fileName) {
            const label = document.querySelector('.custom-file-label');
            label.textContent = fileName;
            console.log('File selected:', fileName);
            // Here you can handle the file upload, e.g., send it to a server
        }
    });
}

function sendMessage() {
    const message = chatInput.value;
    if (message.trim() !== '') {
        displayMessage('user', message);
        chatInput.value = '';

        // Simulate a bot response (replace with actual bot interaction logic)
        setTimeout(() => {
            displayMessage('bot', 'This is a simulated bot response.');
        }, 500);
    }
}

function displayMessage(type, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(type === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
}