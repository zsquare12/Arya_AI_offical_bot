from main import ChatBot  # Ensure this path is correct
import streamlit as st

# Instantiate the bot
bot = ChatBot()

# Set up the Streamlit page
st.set_page_config(page_title="ARYA-AI (The AryaBhatt official bot)")
with st.sidebar:
    st.title('ARYA-AI (The AryaBhatt official bot)')

# Function to generate response from the bot
def generate_response(user_input):
    try:
        result = bot.rag_chain.invoke(user_input)
        return result
    except Exception as e:
        return "Sorry, I couldn't process that request."

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the AryaBhatt official bot!"}]

# Display the conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate assistant response if the last message is from the user
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Getting your answer from the database..."):
                response = generate_response(user_input)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
