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

# --- Cost Analysis (Feb 2026 Gemini 3 Flash Rates) ---
# Input: $0.50/M tokens | Output: $3.00/M tokens
# Avg prompt: 800 tokens input, 1200 tokens output
cost_per_prompt = (800 * 0.0000005) + (1200 * 0.000003) # Approx $0.004

# --- Financial Calculations ---
base_revenue = sub_price
extra_revenue = 0

if actual_prompts > max_prompts:
    extra_needed = actual_prompts - max_prompts
    # Calculate how many bundles they need to purchase
    bundles_needed = (extra_needed // extra_bundle_size) + 1                
    extra_revenue = bundles_needed * extra_bundle_price

total_revenue = base_revenue + extra_revenue
total_cost = actual_prompts * cost_per_prompt
net_profit = total_revenue - total_cost
margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

# --- Display Results ---
st.write(f"### Analysis for {actual_prompts} Prompts Used
