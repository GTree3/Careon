# Adapted from template provided by CloudFlare's Python with Cloudflare Workers and Streamlit tutorial (https://youtu.be/sJQUuN7R8sA?si=JMd0e_YXHArvxioz)

import json

import streamlit as st
from cloudflare import Cloudflare

st.markdown("""
    <style>
        h1 { text-align: center; }
        .stMarkdown a { display: none !important; }
    </style>
    <h1>Customer Support Chat Bot</h1>
""", unsafe_allow_html=True)

# Set Cloudflare API key from Streamlit secrets
client = Cloudflare(api_token=st.secrets["CLOUDFLARE_API_TOKEN"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        # Sends the messages stored in st.session_state.messages to the model
        with client.ai.with_streaming_response.run(
            account_id=st.secrets["CLOUDFLARE_ACCOUNT_ID"],
            model_name="@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ) as response:
            # The response is an EventSource object that looks like so
            # data: {"response": "Hello "}
            # data: {"response": ", "}
            # data: {"response": "World!"}
            # data: [DONE]
            # Creates a token iterator
            def iter_tokens(r):
                for line in r.iter_lines():
                    if line.startswith("data: ") and not line.endswith("[DONE]"):
                        entry = json.loads(line.replace("data: ", ""))
                        yield entry["response"]
            # Shows response bit by bit, as if it's being typed
            completion = st.write_stream(iter_tokens(response))
    st.session_state.messages.append({"role": "assistant", "content": completion})