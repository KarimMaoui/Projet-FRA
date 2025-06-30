from rate_simulation import simulate_libor_paths
from fra_pricing import calculate_unhedged_cost, calculate_total_hedged_cost
import matplotlib.pyplot as plt
import numpy as np

# 1. Simulate interest rate paths
paths = simulate_libor_paths(S0=0.03, mu=0.00, sigma=0.01, T=0.5, dt=1/252, n_paths=1000)

# 2. FRA parameters
fra_rate = 0.031
notional = 1_000_000
delta = 0.25  # 3 months

# 3. Get realized 3-month rates
settlement_index = int(63)
realized_rates = paths[:, settlement_index]

# 4. Calculate costs
unhedged_cost = calculate_unhedged_cost(realized_rates, notional, delta)
hedged_cost = calculate_total_hedged_cost(realized_rates, fra_rate, notional, delta)

# 5. Plot only the hedged vs unhedged cost distribution
plt.figure(figsize=(10,5))
plt.hist(unhedged_cost, bins=50, alpha=0.6, label='Unhedged cost', color='red')
plt.hist(hedged_cost, bins=50, alpha=0.6, label='Hedged cost (FRA)', color='green')
plt.axvline(x=np.mean(unhedged_cost), color='red', linestyle='--')
plt.axvline(x=np.mean(hedged_cost), color='green', linestyle='--')
plt.title('Cashflow Exposure: Hedged vs Unhedged (3M Floating Rate Liability)')
plt.xlabel('€ Cash Outflow')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

