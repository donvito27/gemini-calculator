import streamlit as st

# --- App Title ---
st.title("Gemini 3 Flash Profit Calculator")

# --- UI for Business Model ---
with st.form(key='profit_form'):
    st.header("Configure Your Offer")
    sub_price = st.number_input("Monthly Subscription ($)", value=20.0)
    max_prompts = st.number_input("Included Prompts", value=500)
    
    st.header("User Behavior Scenario")
    actual_prompts = st.slider("Actual Prompts Used by User", 0, 2000, 650)
    
    # Submit button is crucial to trigger calculations
    submit_button = st.form_submit_button(label='Calculate Profit')

# --- Cost Analysis & Calculations ---
if submit_button:
    # Model Costs (Feb 2026 Gemini 3 Flash Rates)
    # Approx $0.004 per prompt
    cost_per_prompt = (800 * 0.0000005) + (1200 * 0.000003) 

    # Financial Calculations
    total_cost = actual_prompts * cost_per_prompt
    net_profit = sub_price - total_cost
    margin = (net_profit / sub_price) * 100 if sub_price > 0 else 0

    # --- Display Results ---
    st.write(f"### Results for {actual_prompts} Prompts Used")
    
    # Using st.metric for
