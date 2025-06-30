from rate_simulation import simulate_libor_paths
from fra_pricing import simulate_fra_pnl
import matplotlib.pyplot as plt

# 1. Simulate interest rate paths
paths = simulate_libor_paths(S0=0.03, mu=0.00, sigma=0.01, T=0.5, dt=1/252, n_paths=1000)

# 2. Define FRA parameters
fra_rate = 0.031  # 3.10%
notional = 1_000_000
delta = 0.25  # 3 months

# 3. Calculate FRA hedge P&L across simulated paths
fra_pnl = simulate_fra_pnl(paths, fra_rate, notional, delta)

# 4. Plot P&L distribution
plt.hist(fra_pnl, bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of FRA Hedge P&L')
plt.xlabel('P&L (€)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
