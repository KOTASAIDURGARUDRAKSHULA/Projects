import streamlit as st
from  gpt_code import run_application

st.title("Simple LLM with LangChain and Google Generative AI")

# Create a form to capture the Enter key press
with st.form(key='llm_form'):
    user_input = st.text_input("Enter your prompt:")
    submit_button = st.form_submit_button(label='Generate Response')

# Check if the form is submitted
if submit_button:
    if user_input:
        response = run_application(user_input)
        st.write("Response from Google Generative AI:")
        st.write(response)
    else:
        st.write("Please enter a prompt to generate a response.")