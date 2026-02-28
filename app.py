import streamlit as st

# --- App Title ---
st.title("Gemini 3 Flash Profit Calculator")

# --- Sidebar Inputs for Business Model ---
st.sidebar.header("Pricing Structure")
sub_price = st.sidebar.number_input("Monthly Subscription ($)", value=20.0)
max_prompts = st.sidebar.number_input("Included Prompts", value=500)
extra_bundle_price = st.sidebar.number_input("Extra Bundle Price ($)", value=5.0)
extra_bundle_size = st.sidebar.number_input("Extra Bundle Size (Prompts)", value=100)

st.sidebar.header("User Behavior Scenario")
actual_prompts = st.sidebar.slider("Actual Prompts Used by User", 0, 2000, 650)

# --- Cost
