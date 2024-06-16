# smart-assist-chatbot
SmartAssist: An intelligent chatbot enhancing e-commerce shopping experiences by integrating advanced image-to-text, text QnA, and customer opinion mining models.

Certainly! Below is a GitHub README file based on the provided master's thesis document:

---

# SmartAssist: Enhancing User Shopping on E-commerce Websites

## Overview

**SmartAssist** is an intelligent chatbot browser plugin designed to enhance the online shopping experience on e-commerce websites. Developed using advanced machine learning techniques, the chatbot integrates multiple models to provide features like text-based question answering, customer review summarization, and customized product recommendations. This master's thesis project was completed as part of the MSc Data Analytics and Artificial Intelligence program at EDHEC Business School.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Online shopping has transformed consumer purchasing behaviour, making it more convenient to buy products from home. However, the abundance of choices and information can overwhelm decision-making for customers. SmartAssist aims to simplify this process by providing a user-friendly chatbot that assists with product queries, summarizes customer reviews, and suggests products based on user preferences.

## Features

### 1. Text Question and Answer
The chatbot can answer user queries related to products by understanding and extracting relevant information from product descriptions and reviews.

### 2. Customer Review Summarization
SmartAssist provides a summarized view of customer reviews, highlighting the key sentiments and opinions and helping users make informed decisions without reading numerous reviews.

### 3. Customized Product Suggestions
The chatbot suggests products based on user interactions and preferences, utilizing collaborative and content-based filtering techniques.

## Architecture

The SmartAssist chatbot integrates several advanced technologies:

- **Natural Language Processing (NLP)**: For text-based question answering and review summarization, using models like BERT and GPT.
- **Machine Learning**: For product recommendation, combining collaborative filtering and content-based methods.
- **Web Technologies**: Developed as a browser extension using HTML, CSS, JavaScript, and Python.

![Chatbot Architecture](path_to_architecture_diagram)

## Installation

To install and run SmartAssist locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/smartassist.git
    ```
2. Navigate to the project directory:
    ```bash
    cd smartassist
    ```
3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Build the browser extension and load it into your preferred browser:
    - Follow browser-specific instructions to load unpacked extensions.

## Usage

Once installed, SmartAssist can be activated from the browser toolbar. Users can interact with the chatbot by clicking on the SmartAssist icon and typing their queries or navigating to product pages where the chatbot will provide summarized reviews and product suggestions.

![Chatbot Interface](path_to_interface_image)

## Contributing

We welcome contributions from the community to enhance SmartAssist. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes.
    ```bash
    git commit -m "Description of feature or fix"
    ```
4. Push to the branch.
    ```bash
    git push origin feature-name
    ```
5. Open a pull request and describe your changes.

---

**Author**: Likhitha Dhanaraju  
**Supervisor**: Mario Hernandeztinoco  
**Institution**: EDHEC Business School, MSc Data Analytics and Artificial Intelligence, Class of 2024

**Disclaimer**: "EDHEC Business School does not express approval or disapproval concerning the opinions given in this paper which are the author's sole responsibility."

---

Feel free to reach out for any questions or feedback.
