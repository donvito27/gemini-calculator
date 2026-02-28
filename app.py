# --- INPUT YOUR NUMBERS HERE ---
sub_price = 20.0        # Price you charge user per month
max_prompts = 500       # Prompts included in subscription
extra_bundle_price = 5.0 # Price for extra prompts
extra_bundle_size = 100  # Prompts in extra bundle

# --- ESTIMATED USAGE ---
actual_prompts = 600    # How many prompts they actually used
# -------------------------------

# Gemini 3 Flash Costs (approximate)
cost_per_prompt = 0.004

# Calculations
base_cost = actual_prompts * cost_per_prompt
extra_revenue = 0

if actual_prompts > max_prompts:
    extra_needed = actual_prompts - max_prompts
    bundles_needed = (extra_needed // extra_bundle_size) + 1
    extra_revenue = bundles_needed * extra_bundle_price

total_revenue = sub_price + extra_revenue
profit = total_revenue - base_cost

print(f"Total Revenue: ${total_revenue:.2f}")
print(f"Google Cost: ${base_cost:.2f}")
print(f"Net Profit: ${profit:.2f}")
