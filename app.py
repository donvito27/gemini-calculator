import streamlit as st
import google.generativeai as genai
import sqlite3

# --- 1. Setup ---
st.title("Secure AI Service")

# Configure API Key securely
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in settings.")
    st.stop()

# --- 2. Database Setup ---
conn = sqlite3.connect('users.db')
c = conn.cursor()
# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS usage 
             (user_id TEXT PRIMARY KEY, prompts_used INTEGER)''')
conn.commit()

# --- 3. UI and Logic ---
st.sidebar.header("Login")
user_id = st.sidebar.text_input("Enter your Unique User ID")
MAX_PROMPTS = 50

if user_id:
    # Check usage
    c.execute('SELECT prompts_used FROM usage WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    
    # If user is new, add them to database
    if not data:
        c.execute('INSERT INTO usage (user_id, prompts_used) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        current_usage = 0
    else:
        current_usage = data[0]

    st.write(f"### Usage: {current_usage} / {MAX_PROMPTS} prompts used")

    prompt = st.text_input("Enter your prompt")

    if st.button("Generate") and prompt:
        if current_usage < MAX_PROMPTS:
            # Call Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.write(response.text)
            
            # Update usage
            new_usage = current_usage + 1
            c.execute('UPDATE usage SET prompts_used = ? WHERE user_id = ?', (new_usage, user_id))
            conn.commit()
            st.rerun() # Refresh app to update count
        else:
            st.error("Usage limit reached.")

conn.close()
