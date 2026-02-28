import streamlit as st

# --- App Title ---
st.title("Gemini 3 Flash Profit Calculator")

# --- 1. INITIALIZE SESSION STATE ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# --- 2. UI Inputs ---
st.header("Business Configuration")

# New Input: Number of users
num_users = st.number_input("Number of Users", min_value=1, value=10, step=1)

# Pricing Structure
st.subheader("Pricing Structure")
sub_price = st.number_input("Monthly Subscription per User ($)", value=20.0)
included_prompts = st.number_input("Included Prompts per User", value=500)
extra_bundle_price = st.number_input("Extra Bundle Price ($)", value=5.0)
extra_bundle_size = st.number_input("Extra Bundle Size (Prompts)", value=100)

# Behavior Scenario
st.subheader("User Behavior Scenario (Average per User)")
actual_prompts_per_user = st.slider("Average Prompts Used per User", 0, 2000, 650)

# New Input: Did they buy extra top-up credits?
st.subheader("Additional Top-Ups")
purchased_topup = st.checkbox("User purchased extra prompt bundles?")

# --- 3. Calculation Logic ---
def calculate_profit():
    # Model Costs (Feb 2026 Gemini 3 Flash Rates)
    # Approx $0.004 per prompt
    cost_per_prompt = (800 * 0.0000005) + (1200 * 0.000003) 

    # Base Metrics
    total_base_revenue = num_users * sub_price
    
    # Extra Revenue Calculation
    extra_revenue = 0
    if purchased_topup and actual_prompts_per_user > included_prompts:
        extra_needed = actual_prompts_per_user - included_prompts
        # Calculate how many bundles they need to purchase
        bundles_needed = (extra_needed // extra_bundle_size) + 1                
        extra_revenue = bundles_needed * extra_bundle_price * num_users

    total_revenue = total_base_revenue + extra_revenue
    
    # Total Cost Calculation
    total_cost = num_users * actual_prompts_per_user * cost_per_prompt
    
    # Financial Summary
    net_profit = total_revenue - total_cost
    margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

    # Save to session state
    st.session_state.net_profit = net_profit
    st.session_state.total_revenue = total_revenue
    st.session_state.total_cost = total_cost
    st.session_state.margin = margin
    st.session_state.calculated = True

# --- 4. Buttons and Display ---
st.button("Calculate Total Profit", on_click=calculate_profit)

if st.session_state.calculated:
    st.write("---")
    st.write(f"### Results for {num_users} Users")
    st.metric("Total Revenue", f"${st.session_state.total_revenue:,.2f}")
    st.metric("Total Google API Cost", f"${st.session_state.total_cost:,.2f}")
    st.metric("Net Profit", f"${st.session_state.net_profit:,.2f}")
    st.metric("Profit Margin", f"{st.session_state.margin:.1f}%")

    if st.session_state.net_profit < 0:
        st.error("Warning: This scenario results in a loss.")
