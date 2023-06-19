###################################################################################################
##################### OPTIMISATION ################################################################
###################################################################################################
# Function to find the optimal lookback_period
def optimize_lookback_period(dataset, min_lookback, max_lookback, step):
    best_pnl = -float('inf')  # Initialize best PnL to negative infinity
    best_lookback = None  # Initialize best lookback_period to None

    # Iterate through lookback_period values with the given step
    for lookback in range(min_lookback, max_lookback + 1, step):
        pnl = trading_strategy(dataset, lookback)[0]  # Compute PnL using the current lookback_period

        # If the current lookback_period's PnL is better than the best PnL found so far, update the best PnL and lookback_period
        if pnl > best_pnl:
            best_pnl = pnl
            best_lookback = lookback

    return best_lookback, best_pnl

# Define dataset, minimum lookback period, maximum lookback period, and step value
dataset = merged_data_1  # Replace with relevant dataset
min_lookback = 10
max_lookback = 60
step = 5

# Find the optimal lookback_period and its corresponding PnL
optimal_lookback, optimal_pnl = optimize_lookback_period(dataset, min_lookback, max_lookback, step)

# Print the results
print(f"Optimal lookback period: {optimal_lookback} with PnL of {optimal_pnl}")

