document.addEventListener('DOMContentLoaded', function() {
  const chatOutput = document.getElementById('chat-output');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const typingIndicator = document.getElementById('typing-indicator');

  const defaultMessage = 'Hello, I am a helpful AI assistant. How can I assist you today?';

  function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    if (sender === 'user') {
      messageElement.classList.add('user-message');
    } else {
      messageElement.classList.add('bot-message');
    }
  }

  function sendMessage(message, sender = 'user') {
    if (sender === 'user') {
      addMessage('You: ' + message, 'user');
      userInput.value = '';

      // Hide typing indicator
      typingIndicator.style.display = 'none';

      // Send message and URL to backend server
      fetch('http://localhost:5000/generate_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: message, url: window.location.href }), // Include URL in the request
      })
     .then(response => response.json())
     .then(data => {
        addMessage('Bot: ' + data.response, 'bot');
      })
     .catch(error => console.error('Error:', error));
    } else {
      addMessage(message, sender);
    }
  }

  // Send default message when the DOM is loaded
  sendMessage(defaultMessage, 'bot');

  sendBtn.addEventListener('click', () => {
    sendMessage(userInput.value, 'user');
  });

  userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendMessage(userInput.value, 'user');
    }
  });

  userInput.addEventListener('input', () => {
    if (userInput.value.length > 0) {
      typingIndicator.style.display = 'flex';
      typingIndicator.innerHTML = `
        <div class="message user-message">
          <div class="typing-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
        </div>
      `;

      const dots = typingIndicator.querySelectorAll('.dot');
      let index = 0;
      const interval = setInterval(() => {
        dots.forEach(dot => dot.classList.remove('active'));
        dots[index].classList.add('active');
        index = (index + 1) % dots.length;
      }, 500);

      // Clear the interval when the user stops typing
      userInput.addEventListener('blur', () => clearInterval(interval));
    } else {
      typingIndicator.style.display = 'none';
      typingIndicator.innerHTML = '';
    }
  });
});