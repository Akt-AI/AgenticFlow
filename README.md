# AgenticFlow
## With OpenAI-Compatible Chat Interface

This is a Streamlit-based chat interface for interacting with any OpenAI-compatible API. It supports managing multiple API configurations, dynamic model selection, and streaming responses.

## Features

- **Dynamic API Configuration**: Add, update, and manage API keys, base URLs, and default models.
- **Streaming Responses**: View responses from the API in real-time.
- **Chat History**: View chat history directly in the sidebar.
- **User-Friendly Interface**: A clean and intuitive UI powered by Streamlit.

---

## Requirements

- Python 3.6 or higher
- Libraries:
  - `streamlit`
  - `requests`
  - `json`

Install the required libraries using:
```bash
pip install streamlit requests
```

---

## How to Use

### Step 1: Setup
Clone the repository and ensure the `api_config.json` file is available in the same directory as the script.

### Step 2: Run the Script
Start the Streamlit app by running:
```bash
streamlit run script_name.py
```

### Step 3: Configure APIs
1. Open the **Settings** section in the sidebar.
2. Add or update API configurations:
   - **API Key Name**: A unique name for the API.
   - **API Key Value**: The actual API key (hidden input).
   - **Base URL**: The endpoint of the API (e.g., `https://api.openai.com/v1`).
   - **Default Model**: The model to use (fetched dynamically from the API).
3. Save configurations, and they will be stored in `api_config.json`.
4. Base urls:
  ``` 
  XAI_BASE_URL="https://api.x.ai/v1"
  GROQ_BASE_URL="https://api.groq.com/openai/v1"
  OLLAMA_BASE_URL="http://localhost:11434/v1"
  OPENAI_BASE_URL="https://api.openai.com/v1/"
```

### Step 4: Start Chatting
1. Enter your message in the chat input box at the bottom of the interface.
2. Responses will be displayed in real-time.

### Step 5: View Chat History
Chat history is displayed in the **Chat History** section of the sidebar.

---

## Script Overview

### Core Functions
1. **API Configuration Management**:
   - Load and save API configurations to `api_config.json`.
   - Manage multiple APIs dynamically.

2. **Chat Functionality**:
   - Initialize chat history.
   - Fetch user inputs.
   - Send messages to the API and handle streaming responses.

3. **UI Setup**:
   - Sidebar for settings and chat history.
   - Main interface for real-time conversation.

4. **API Integration**:
   - Send requests and handle responses from OpenAI-compatible APIs.

---

## Example

After configuring an API and entering a message, the app might look like this:

```
You: Hello!
Assistant: Hi there! How can I assist you today?
```

---

## Troubleshooting

- **API Errors**: Ensure the API key and base URL are correct.
- **Connection Issues**: Check your internet connection and API endpoint status.
- **Missing Configurations**: Add valid configurations in the **Settings** section.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

Inspired by OpenAI's APIs and designed for user-friendly interaction.

Happy Chatting! 🤖
```

This README provides a detailed explanation of the script, including its features, usage instructions, and an overview of its core components. Let me know if you'd like any modifications!
