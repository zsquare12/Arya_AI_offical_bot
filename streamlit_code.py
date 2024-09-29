from main import ChatBot
import streamlit as st

bot = ChatBot()
    
st.set_page_config(page_title="Arya AI")
with st.sidebar:
    st.title('Arya-AI (Offical Bot of Arya-Bhatt Hostel)')

def generate_response(input):
    result = bot.rag_chain.invoke(input)
    return result

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, to arya Bhatt"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from my Data Base ."):
            response = generate_response(input) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)