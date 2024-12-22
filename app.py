import streamlit as st
import requests
import json

CONFIG_FILE = "api_config.json"

# Helper functions to load and save API configurations
def load_api_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_api_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

# Initialize chat history
def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

# Retrieve user input
def get_user_input():
    return st.chat_input("Your message:")

# Setup Streamlit app layout
def setup_app():
    st.set_page_config(page_title="OpenAI-Compatible Chat", page_icon="🤖", layout="wide")
    st.title("OpenAI-Compatible Chat Interface")
    st.subheader("Chat with any OpenAI-compatible API")

# Display chat history in the sidebar
def display_chat_history_in_sidebar():
    st.sidebar.title("Chat History")

    if "messages" in st.session_state and st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.sidebar.markdown(f"**You {i+1}:** {message['content']}")
            elif message["role"] == "assistant":
                st.sidebar.markdown(f"**Assistant {i+1}:** {message['content']}")
    else:
        st.sidebar.markdown("No chat history available.")

# Manage API key, base URL, and model selection dynamically
def manage_api_keys():
    def update_existing_api_config(selected_api, new_api_key_value, new_base_url, new_default_model):
        if selected_api in st.session_state.api_config:
            config = st.session_state.api_config[selected_api]
            if new_api_key_value:
                config['api_key'] = new_api_key_value
            if new_base_url:
                config['base_url'] = new_base_url
            if new_default_model:
                config['default_model'] = new_default_model
            save_api_config(st.session_state.api_config)
            st.success(f"API configuration '{selected_api}' updated successfully!")

    st.sidebar.title("Settings")

    if "api_config" not in st.session_state:
        st.session_state.api_config = load_api_config()

    if "selected_api" not in st.session_state:
        if st.session_state.api_config:
            st.session_state.selected_api = list(st.session_state.api_config.keys())[0]  # Default to the first config

    selected_api = st.sidebar.selectbox("Select an API", list(st.session_state.api_config.keys()), index=0 if "selected_api" not in st.session_state else list(st.session_state.api_config.keys()).index(st.session_state.selected_api))

    if st.sidebar.button("Delete API Configuration"):
        del st.session_state.api_config[selected_api]
        save_api_config(st.session_state.api_config)
        st.success(f"API configuration '{selected_api}' deleted successfully!")
        # st.experimental_rerun()

    new_api_key_name = st.sidebar.text_input("New API Key Name")
    new_api_key_value = st.sidebar.text_input("New API Key Value", value=st.session_state.api_config[selected_api]['api_key'] if selected_api in st.session_state.api_config else "", type="password")
    new_base_url = st.sidebar.text_input("Base URL", value=st.session_state.api_config[selected_api]['base_url'] if selected_api in st.session_state.api_config else "", placeholder="https://api.openai.com/v1")
    

    if st.sidebar.button("Fetch Models"):
        if new_api_key_value and new_base_url:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {new_api_key_value}"
            }
            try:
                response = requests.get(f"{new_base_url}/models", headers=headers)
                if response.status_code == 200:
                    #models = [model for model in response.json().get("data", []) if not model.get("restricted", False)]
                    models = [model for model in response.json().get("data", []) if not model.get("restricted", False) and model.get("id")]

                    st.session_state.models = [model["id"] for model in models]
                    st.success("Models fetched successfully!")
                else:
                    st.error(f"Failed to fetch models: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
        else:
            st.warning("Please provide a valid API key and Base URL to fetch models.")

    new_default_model = st.sidebar.selectbox("Default Model", st.session_state.get("models", ["GPT-4o-mini"] if "GPT-4o-mini" in st.session_state.get("models", []) else ["qwen2.5:0.5b"]))

    if st.sidebar.button("Add or Update API Configuration"):
        if selected_api and (new_api_key_value or new_base_url or new_default_model):
            update_existing_api_config(selected_api, new_api_key_value, new_base_url, new_default_model)
        elif new_api_key_name and new_api_key_value and new_base_url and new_default_model:
            st.session_state.api_config[new_api_key_name] = {
                "api_key": new_api_key_value,
                "base_url": new_base_url,
                "default_model": new_default_model
            }
            save_api_config(st.session_state.api_config)
            st.success(f"API configuration '{new_api_key_name}' added successfully!")
        else:
            st.warning("Please fill in all fields.")

    if not st.session_state.api_config:
        st.sidebar.warning("No API configurations available. Please add one.")
        st.stop()

    st.session_state.selected_api = selected_api
    return st.session_state.api_config[selected_api]

# Send a message to the OpenAI-compatible API
def send_message(api_config, user_input):
    if user_input and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        payload = {
            "model": api_config.get("default_model", "qwen2.5:0.5b"),
            "messages": st.session_state.messages,
            "stream": True
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_config['api_key']}"
        }

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{api_config['base_url']}/chat/completions",
                    json=payload,
                    headers=headers,
                    stream=True
                )

                if response.status_code == 200:
                    reply = ""
                    full_message = ""
                    placeholder = st.empty()
                    for chunk in response.iter_lines():
                        if chunk.strip() == b"data: [DONE]":
                            break
                        try:
                            if chunk.strip().startswith(b"data: "):
                                chunk_data = json.loads(chunk.strip()[6:].decode("utf-8"))
                                if "choices" in chunk_data and chunk_data["choices"]:
                                    reply_chunk = chunk_data["choices"][0]["delta"].get("content", "")
                                    full_message += reply_chunk
                                    placeholder.markdown(f"**Assistant:** {full_message}", unsafe_allow_html=True)
                        except json.JSONDecodeError as e:
                            st.error(f"Failed to decode JSON: {e}")
                            st.write(f"Raw chunk: {chunk}")
                    st.session_state.messages.append({"role": "assistant", "content": full_message})
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")

# Main function to run the app
def main():
    setup_app()
    api_config = manage_api_keys()
    initialize_chat()
    display_chat_history_in_sidebar()

    user_input = get_user_input()
    if user_input:
        send_message(api_config, user_input)

if __name__ == "__main__":
    main()
