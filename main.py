import numpy as np
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

from fra_pricing import fra_payoff, calculate_unhedged_cost, calculate_total_hedged_cost

# 1. On extrait le taux réalisé à 3 mois
settlement_index = int(63)  # 3 mois = ~63 jours de bourse
realized_rates = paths[:, settlement_index]

# 2. Coût total si tu ne couvres pas (tu payes le taux variable)
unhedged_cost = calculate_unhedged_cost(realized_rates, notional, delta)

# 3. Coût total si tu te couvres avec le FRA (tu payes variable + tu reçois FRA)
hedged_cost = calculate_total_hedged_cost(realized_rates, fra_rate, notional, delta)

# 4. Graphe comparatif
import matplotlib.pyplot as plt
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
