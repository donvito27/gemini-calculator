import streamlit as st

# --- App Title ---
st.title("Gemini 3 Flash Profit Calculator")

# --- Initialize Session State ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'net_profit' not in st.session_state:
    st.session_state.net_profit = 0.0
if 'total_revenue' not in st.session_state:
    st.session_state.total_revenue = 0.0
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0
if 'margin' not in st.session_state:
    st.session_state.margin
