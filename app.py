import streamlit as st

# --- App Title ---
st.title("Gemini 3 Flash Profit Calculator")

# --- 1. INITIALIZE SESSION STATE ---
# This fixes the AttributeError: 'st.session_state has no attribute margin'
if 'margin' not in st.session_state:
    st.session_state.margin = 0.0
if 'net_profit' not in st.session_state:
    st.session_state.net_profit = 0.0
if 'total_revenue' not in st.session_state:
    st.session_state.total_revenue = 0.0
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# --- 2. UI Inputs ---
st.header("Configure Your Offer")
sub_price = st.number_input("Monthly Subscription ($)", value=20.0)
max_prompts = st.number_input("Included Prompts", value=500)
actual_prompts = st.slider("Actual Prompts Used by User", 0, 2000, 650)

# --- 3. Calculation Logic ---
def calculate_profit():
    # Model Costs (Feb 2026 Gemini 3 Flash Rates)
    # Approx $0.004 per prompt
    cost_per_prompt = (800 * 0.0000005) + (1200 * 0.000003) 

    # Financial Calculations
    total_cost = actual_prompts * cost_per_prompt
    net_profit = sub_price - total_cost
    margin = (net_profit / sub_price) * 100 if sub_price > 0 else 0

    # Save to session state
    st.session_state.net_profit = net_profit
    st.session_state.total_revenue = sub_price
    st.session_state.total_cost = total_cost
    st.session_state.margin = margin
    st.session_state.calculated = True

# --- 4. Buttons and Display ---
st.button("Calculate Profit", on_click=calculate_profit)

if st.session_state.calculated:
    st.write("---")
    st.write(f"### Results for {actual_prompts} Prompts Used")
    st.metric("Subscription Revenue", f"${st.session_state.total_revenue:,.2f}")
    st.metric("Google API Cost", f"${st.session_state.total_cost:,.2f}")
    st.metric("Net Profit", f"${st.session_state.net_profit:,.2f}")
    st.metric("Profit Margin", f"{st.session_state.margin:.1f}%")

    if st.session_state.net_profit < 0:
        st.error("Warning: This scenario results in a loss.")
