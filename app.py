import streamlit as st

st.title("Gemini API Profit Calculator 2026")

# Sidebar inputs
st.sidebar.header("User Stats")
users = st.sidebar.number_input("Number of Users", value=100)
prompts = st.sidebar.slider("Prompts per User/Month", 10, 1000, 500)
sub_price = st.sidebar.number_input("Your Subscription Price ($)", value=20.0)

# Model selection
model = st.selectbox("Choose Gemini Model", ["3.1 Pro", "3 Flash", "2.5 Flash-Lite"])

# Pricing Logic
prices = {
    "3.1 Pro": {"in": 2.00, "out": 12.00},
    "3 Flash": {"in": 0.50, "out": 3.00},
    "2.5 Flash-Lite": {"in": 0.10, "out": 0.40}
}

# Calculations
cost_per_user = (prompts * 800 / 1_000_000 * prices[model]["in"]) + (prompts * 1200 / 1_000_000 * prices[model]["out"])
total_revenue = users * sub_price
total_cost = cost_per_user * users
profit = total_revenue - total_cost

# Display
st.metric("Estimated Monthly Profit", f"${profit:,.2f}")
st.write(f"Your Google bill will be roughly **${total_cost:,.2f}** per month.")
