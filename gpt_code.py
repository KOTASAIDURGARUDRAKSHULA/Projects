# Simple LLM using Langchain with LCEL

import requests
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# get the API key from https://aistudio.google.com/app/apikey
API_KEY = 'AIzaSyBnEVw1GySsiAfwLjifT68vcGqhs-9Vnuc'

def generate_text(prompt):
    endpoint = 'https://generativelanguage.googleapis.com/v1beta2/text:generate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'prompt': prompt,
        'maxTokens': 150  # Adjust this value as needed
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('text', '')
    else:
        return f"Error: {response.status_code} - {response.text}"

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="Generate a response for the following prompt: {user_input}"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=API_KEY
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

def run_application(user_input):
    response = llm_chain.run(user_input)
    return response