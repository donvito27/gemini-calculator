import streamlit as st
import google.generativeai as genai
import sqlite3

# --- 1. Setup ---
st.title("Gemini Profit Service")

# Configure Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in secrets.")
    st.stop()

# --- 2. Database Setup ---
conn = sqlite3.connect('user_usage.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usage 
             (user_id TEXT PRIMARY KEY, prompts_used INTEGER, top_up_limit INTEGER DEFAULT 0)''')
conn.commit()

# --- 3. UI and Logic ---
st.sidebar.header("User Control")
user_id = st.sidebar.text_input("Enter your unique User ID")
MAX_PROMPTS = 500

if user_id:
    # Check current usage
    c.execute('SELECT prompts_used, top_up_limit FROM usage WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    
    prompts_used = data[0] if data else 0
    extra_allowed = data[1] if data else 0
    total_allowed = MAX_PROMPTS + extra_allowed

    st.write(f"### Usage: {prompts_used} / {total_allowed} prompts used")

    prompt = st.text_input("Enter your prompt")

    if st.button("Generate") and prompt:
        if prompts_used < total_allowed:
            # Call API
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.write(response.text)
            
            # Update usage
            new_usage = prompts_used + 1
            c.execute('INSERT OR REPLACE INTO usage (user_id, prompts_used, top_up_limit) VALUES (?, ?, ?)', (user_id, new_usage, extra_allowed))
            conn.commit()
            st.rerun() # Refresh to update count
        else:
            st.error("Usage limit reached. Please purchase more credits.")

    # --- 4. Top-Up Button (Simulating a purchase) ---
    st.write("---")
    st.write("Need more prompts?")
    if st.button("Buy 100 Extra Prompts ($5)"):
        # In a real app, you would process payment here
        new_top_up = extra_allowed + 100
        c.execute('INSERT OR REPLACE INTO usage (user_id, prompts_used, top_up_limit) VALUES (?, ?, ?)', (user_id, prompts_used, new_top_up))
        conn.commit()
        st.success("100 prompts added!")
        st.rerun()

conn.close()
