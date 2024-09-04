// login.js
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Here you would typically send this data to your server for authentication
    console.log('Login attempt:', { username, email, password });

    // For this example, we'll just redirect to the chatbot page
    window.location.href = 'chatbot.html';
});