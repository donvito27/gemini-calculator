import streamlit as st
import google.generativeai as genai
import sqlite3

# --- 1. Setup ---
st.title("Secure Gemini Service")

# Configure the API key from secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in secrets.")
    st.stop()

# --- 2. Database Setup for Usage Tracking ---
conn = sqlite3.connect('user_usage.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usage (user_id TEXT PRIMARY KEY, prompts_used INTEGER)''')
conn.commit()

# --- 3. UI and Logic ---
user_id = st.text_input("Enter your unique User ID")
prompt = st.text_input("Enter your prompt")
MAX_PROMPTS = 500

if st.button("Generate") and prompt and user_id:                
    # Check usage
    c.execute('SELECT prompts_used FROM usage WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    
    current_usage = data[0] if data else 0                

    if current_usage < MAX_PROMPTS:
        # Call API
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)
        
        # Update usage
        new_usage = current_usage + 1
        c.execute('INSERT OR REPLACE INTO usage (user_id, prompts_used) VALUES (?, ?)', (user_id, new_usage))
        conn.commit()
        st.write(f"Prompts used: {new_usage}/{MAX_PROMPTS}")
    else:
        st.error("Usage limit reached. Please purchase more credits.")

conn.close()
