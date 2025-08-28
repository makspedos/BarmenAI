import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def get_response_from_fastapi(prompt:str):
    response = requests.post("http://localhost:8000/query/prompt/", json={"prompt":prompt})
    data = response.json()
    print(data)
    return data

st.title("Select your drink")

with st.form("prompt_form"):
    prompt = st.text_input("What you want for today, my friend ?")

    submit = st.form_submit_button("Ask")

    if submit:
        model_response, cocktail_response = get_response_from_fastapi(prompt)
        st.write(model_response)
        st.write(cocktail_response)


