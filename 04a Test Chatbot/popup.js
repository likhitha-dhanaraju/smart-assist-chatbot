document.addEventListener('DOMContentLoaded', function() {
  const chatOutput = document.getElementById('chat-output')
  const userInput = document.getElementById('user-input')
  const sendBtn = document.getElementById('send-btn')
  const ticontainer = document.getElementsByClassName('ticontainer')

  const defaultMessage = 'Hello, I am a helpful AI assistant. How can I assist you today?'

  function addMessage(message, sender) {
    const messageElement = document.createElement('div')
    messageElement.classList.add('message', sender)
    if (sender === 'bot') {
      messageElement.innerText = message.replace(/chrome-extension:\/\/.+?\//, '').replace('/popup.html', '').replace('Bot: ', '');
    } else {
      messageElement.innerText = message
    }
    chatOutput.appendChild(messageElement)
    chatOutput.scrollTop = chatOutput.scrollHeight

    if (sender === 'user') {
      messageElement.classList.add('user-message')
    } else {
      messageElement.classList.add('bot-message')
    }
  }

  function sendMessage(message, sender = 'user', option = null) {
    if (sender === 'user') {
      addMessage('SmartAssist: ' + message, 'user')
      userInput.value = ''

      // Hide typing indicator
      ticontainer[0].style.display = 'none'

      // Send message and URL to backend server
      fetch('http://localhost:5000/generate_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: message, url: window.location.href, option: option }), // Include URL and option in the request
      })
      .then(response => response.json())
      .then(data => {
        addMessage('Bot: ' + data.response, 'bot')

        // Show options after the first message from the chatbot
        displayOptions()
      })
      .catch(error => console.error('Error:', error))
    } else {
      addMessage(message, sender)
    }
  }

  function displayOptions() {
    const optionsContainer = document.querySelector('.options-container')
    optionsContainer.style.display = 'block'

    const optionButtons = document.querySelectorAll('#option-1, #option-2, #option-3')
    optionButtons.forEach(button => {
      button.addEventListener('click', () => {
        const userChoice = button.innerText
        sendMessage(userChoice, 'user', userChoice) // Pass the selected option to the sendMessage function

        // Hide options
        optionsContainer.style.display = 'none'
      })
    })
  }

  // Send default message when thepage loads
  sendMessage(defaultMessage)

  // Add event listener to the user input field
  userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendMessage(userInput.value)
    }
  })

  // Add event listener to the send button
  sendBtn.addEventListener('click', function() {
    sendMessage(userInput.value)
  })

  // Add event listener to the chat container to show typing indicator
  const chatContainer = document.querySelector('.chat-container')
  chatContainer.addEventListener('input', function() {
    ticontainer[0].style.display = 'block'
  })
})