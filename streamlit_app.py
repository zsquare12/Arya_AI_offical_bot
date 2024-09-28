from main import ChatBot t
import streamlit as st


bot = ChatBot()


st.set_page_config(page_title="ARYA-AI (The AryaBhatt official bot)")
with st.sidebar:
    st.title('ARYA-AI (The AryaBhatt official bot)')

def generate_response(user_input):
    try:
        result = bot.rag_chain.invoke(user_input)
        return result
    except Exception as e:
        return "Sorry, I couldn't process that request."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the AryaBhatt official bot!"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Getting your answer from the database..."):
                response = generate_response(user_input)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
