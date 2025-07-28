import streamlit as st
from openai import OpenAI
from credentials import Gemini_API

def genai_sql_generator():
    st.subheader("🤖 GenAI SQL Query Generator")
    query = st.text_area("Enter your request in plain English:")
    if st.button("Generate SQL"):
        try:
            gemini_model = OpenAI(api_key=Gemini_API, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            message = [
                {"role": "system", "content": "You are an AI assistant. Generate database statements in under 5 lines."},
                {"role": "user", "content": query}
            ]
            response = gemini_model.chat.completions.create(messages=message, model="gemini-2.5-flash")
            sql_query = response.choices[0].message.content
            st.code(sql_query, language="sql")
        except Exception as e:
            st.error(f"Error: {str(e)}")
