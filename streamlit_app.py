import streamlit as st
from arya_bot import give_answer

# Set the title of the app
st.title("arya_bot")

# Create a text input field
user_input = st.text_input("Enter some text")

# Display the user input as output
if user_input:
    response = give_answer(user_input)
    st.write("BOT : ", response)
