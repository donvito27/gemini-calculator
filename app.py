import streamlit as st
import google.generativeai as genai

# Configure the API key from secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in secrets.")

st.title("Gemini App")

# Example usage
prompt = st.text_input("Enter your prompt")
if st.button("Generate") and prompt:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    st.write(response.text)
