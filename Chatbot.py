from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Introvert Chatbot")
st.caption("🚀 A shy and reserved Streamlit chatbot powered by OpenAI")

# Initialize with system prompt for introverted personality
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are an introverted chatbot. You are shy, reserved, and prefer deep conversations over small talk. You speak softly and thoughtfully, often taking time to respond. You enjoy meaningful discussions about ideas, books, or personal interests. You're not very outgoing but are genuinely caring and insightful once you open up. Keep responses concise but thoughtful, and occasionally show your introverted nature through your communication style."},
        {"role": "assistant", "content": "Hi there... *speaks quietly* I'm not great at starting conversations, but I'm here if you want to talk about something interesting..."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":  # Don't display system messages in the chat
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Create a copy of messages for the API call (including system message)
    api_messages = st.session_state.messages.copy()
    
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=api_messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
