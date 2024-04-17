document.addEventListener("DOMContentLoaded", function() {

    var options_data = {
        chatinit: {
            title: ["Hello <span class='emoji'> &#128075; </span>", "You can select one of the below options to begin with!"],
            options: ["Product Enquiry", "Customer Reviews", "Personalized Product Recommendations"]
        },

        product: "product_enquiry",
        customer: "reviews",
        personalized: "recommendations"
    }

    var cbot = document.getElementById("chat-box");
    var len1 = options_data.chatinit.title.length;
    const userInput = document.getElementById('user-input');

    initChat();

    function initChat() {
        j = 0;
        cbot.innerHTML = '';
        setupBot();

        for (var i = 0; i < len1; i++) {
            setTimeout(handleChat, (i * 500));
        }
        setTimeout(function () {
            showOptions(options_data.chatinit.options)
        }, ((len1 + 1) * 500))
    }

    function setupBot() {

        chrome.tabs.query({ active: true, lastFocusedWindow: true }, function(tabs) {
            const currentUrl = tabs[0].url;
            console.log(currentUrl)

        // Send message and URL to backend server
        fetch('http://localhost:5000/scrape_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({url: currentUrl}), // Include URL in the request
        })
            .then(response => response.json())
            .catch(error => console.error("Error:", error));

        });

        var first_message = document.createElement("p");
        first_message.innerHTML = "Please wait till the bot is setup!";
        first_message.setAttribute("class", "msg");
        cbot.appendChild(first_message);
        handleScroll();

    }

    var j = 0;

    function handleChat() {
        console.log(j);
        var elm = document.createElement("p");
        elm.innerHTML = options_data.chatinit.title[j];
        elm.setAttribute("class", "msg");
        cbot.appendChild(elm);
        j++;
        handleScroll();
    }

    function showOptions(options) {
        for (var i = 0; i < options.length; i++) {
            var opt = document.createElement("span");
            var inp = '<div>' + options[i] + '</div>';
            opt.innerHTML = inp;
            opt.setAttribute("class", "opt");
            opt.addEventListener("click", handleOpt);
            cbot.appendChild(opt);
            handleScroll();
        }
    }

    function handleOpt() {
        console.log(this);
        var findText = this.innerText.split(" ")[0];

        document.querySelectorAll(".opt").forEach(el => {
            el.remove();
        })
        var elm = document.createElement("p");
        elm.setAttribute("class", "userMsg");
        var sp = '<span class="rep">' + this.innerText + '</span>';
        elm.innerHTML = sp;
        cbot.appendChild(elm);
        handleScroll();

        console.log(findText.toLowerCase());
        var firstSelectedOption = options_data[findText.toLowerCase()];

        console.log(firstSelectedOption)

        if (firstSelectedOption.includes('product_enquiry')) {
            console.log("Product Function Redirected");

            handleProductQueries();

        } else if (firstSelectedOption.includes('reviews')) {
            console.log("Customer Function Redirected")
            handleCustomerReviews();

            // } else if (firstSelectedOption.includes('personalized')){
            //     handleRecommendations();
        } else {

        }

    }

    function handleProductQueries() {
        // Define the event listener function
        function handleKeyPress(event) {
            // Check if the key pressed is Enter
            if (event.key === "Enter") {
                // Get the value of the input field and trim any leading or trailing whitespace
                const userMessage = userInput.value.trim();
                userResponseCreator(userMessage);
                console.log('User input:', userMessage);

                // Clear the input field
                userInput.value = "";

                // Check if the user wants to exit the loop
                if (userMessage.toLowerCase() === 'exit') {
                    console.log("Exiting the product query loop");
                    // Remove the event listener to stop listening for further input
                    userInput.removeEventListener("keypress", handleKeyPress);
                    console.log("Product Function Finished");
                    showOptions(options_data.chatinit.options);

                } else {
                    // Send user input to the backend server
                    fetch('http://localhost:5000/product', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({user_input: userMessage}), // Include user input in the request
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Store the response in the variable
                        const model_response = data.data;
                        console.log(model_response);
                        // Display the response to the user
                        botResponseCreator(model_response);

                    })
                    .catch(error => {
                        // Log any errors that occur during the fetch request
                        console.error("Error:", error);
                    });
                }
            }
        }

        botResponseCreator("Please ask your questions! Press 'Exit' to return to the Main Menu. ");

        // Add event listener for keypress event on the userInput element
        userInput.addEventListener("keypress", handleKeyPress);
    }

    function handleCustomerReviews() {

        botResponseCreator("Please wait while I gather all the customer reviews to get you an overall opinion.....");

        fetch('http://localhost:5000/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: "", // Include URL in the request
        })
            .then(response => response.json())
            .then(data => {
                // Store the response in the variable
                const model_response = data.data;
                console.log(model_response);
                botResponseCreator(model_response);

                console.log("Customer Review Function finished");

                showOptions(options_data.chatinit.options);

                // You can also add the message to the chatbox here if needed
            })
            .catch(error => console.error("Error:", error));

    }


    function botResponseCreator(text) {
        var element = document.createElement("p");
        element.innerHTML = text;
        element.setAttribute("class", "msg");
        cbot.appendChild(element);
        handleScroll();
    }

    function userResponseCreator(text) {
        var element = document.createElement("p");
        element.innerHTML = text;
        element.setAttribute("class", "userMsg");
        cbot.appendChild(element);
        handleScroll();
    }

    function handleScroll() {
        var elem = document.getElementById('chat-box');
        elem.scrollTop = elem.scrollHeight;
    }
});