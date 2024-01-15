document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.querySelector('#chatInput');
    const sendButton = document.querySelector('#inputSection button');
    const chat = document.querySelector('#chatContent');
    const loader = document.querySelector('.loader-container');

    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }

    function addToChat(input, isBotMessage = false) {
        if (!chat) {
            console.error('Chat element not found!');
            return;
        }

        const messageClass = isBotMessage ? 'botText' : 'userText';
        const messageContainerClass = isBotMessage ? 'message bot-message' : 'message user-message';

        const messageElement = document.createElement('div');
        messageElement.className = messageContainerClass;

        const textElement = document.createElement('div');
        textElement.className = messageClass;
        textElement.textContent = input;

        messageElement.appendChild(textElement);
        chat.appendChild(messageElement);

        // Scroll to the new message
        scrollToBottom(chat);
    }

    function showLoader() {
        loader.style.display = 'flex';
    }

    function hideLoader() {
        loader.style.display = 'none';
    }

    async function sendMessage() {
        const message = inputField.value.trim();
        if (message) {
            addToChat(message); // User message
            inputField.value = '';

            showLoader();


            // setTimeout(() => {
            //     hideLoader();
            //     addToChat("Bot's response to: " + message, true); // Bot message
            // }, 1000); // Adjust the delay as needed

            try {
                // Send data to Flask server
                let response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });
        
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
        
                let data = await response.json();
                hideLoader();
                addToChat(data.reply, true); 

            } catch (error) {
                addToChat("Failed to get response from the server.", true);
                hideLoader();

                console.error("Fetch error: " + error.message);
            }

        }
    }

    sendButton.addEventListener('click', sendMessage);

    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
