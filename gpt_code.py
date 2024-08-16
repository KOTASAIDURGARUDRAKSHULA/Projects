import streamlit as st 
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Get the API key from the secrets
google_api_key = st.secrets["google_api_key"]

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="Generate a response for the following prompt: {user_input}"
)

# Pass the google_api_key as a named parameter
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

def run_application(user_input):
    response = llm_chain.run(user_input)
    return response

# Streamlit UI
st.title("Simple LLM using LangChain with LCEL")
user_input = st.text_input("Enter your prompt:")

if user_input:
    response = run_application(user_input)
    st.write(response)
