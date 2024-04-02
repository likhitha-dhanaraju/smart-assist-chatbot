document.addEventListener('DOMContentLoaded', function() {
  const chatOutput = document.getElementById('chat-output');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');

  function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage !== '') {
      addMessage('You: ' + userMessage, 'user');
      userInput.value = '';

      // Send message to backend server
      fetch('http://localhost:5000/generate_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userMessage }),
      })
      .then(response => response.json())
      .then(data => {
        addMessage('Bot: ' + data.response, 'bot');
      })
      .catch(error => console.error('Error:', error));
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });
});
