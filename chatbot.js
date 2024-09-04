// chatbot.js
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = text;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        userInput.value = '';
        
        // Simulate bot response
        setTimeout(() => {
            addMessage("Thank you for your message. I'm processing your request.", 'bot');
        }, 1000);
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Initial bot message
addMessage("Welcome to our museum! How can I assist you today?", 'bot');

// Simulating WebSocket connection
function simulateWebSocket() {
    console.log('Simulating WebSocket connection...');
    
    // Simulate incoming messages every 30 seconds
    setInterval(() => {
        addMessage("This is a simulated response from the chatbot.", 'bot');
    }, 30000);
}

simulateWebSocket();