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



from fra_pricing import fra_payoff, calculate_unhedged_cost, calculate_total_hedged_cost

# 1. On extrait le taux réalisé à 3 mois
settlement_index = int(63)  # 3 mois = ~63 jours de bourse
realized_rates = paths[:, settlement_index]

# 2. Coût total si tu ne couvres pas (tu payes le taux variable)
unhedged_cost = calculate_unhedged_cost(realized_rates, notional, delta)

# 3. Coût total si tu te couvres avec le FRA (tu payes variable + tu reçois FRA)
hedged_cost = calculate_total_hedged_cost(realized_rates, fra_rate, notional, delta)

fig, axs = plt.subplots(2, 1, figsize=(10,10))


# Graphique 1 : FRA payoff
axs[0].hist(fra_pnl, bins=50, color='skyblue', edgecolor='black')
axs[0].set_title('Distribution of FRA Hedge P&L')
axs[0].set_xlabel('P&L (€)')
axs[0].set_ylabel('Frequency')
axs[0].grid(True)


# Graphique 2 : Hedged vs Unhedged
axs[1].hist(unhedged_cost, bins=50, alpha=0.6, label='Unhedged cost', color='red')
axs[1].hist(hedged_cost, bins=50, alpha=0.6, label='Hedged cost (FRA)', color='green')
axs[1].axvline(x=np.mean(unhedged_cost), color='red', linestyle='--')
axs[1].axvline(x=np.mean(hedged_cost), color='green', linestyle='--')
axs[1].set_title('Cashflow Exposure: Hedged vs Unhedged (3M Floating Rate Liability)')
axs[1].set_xlabel('€ Cash Outflow')
axs[1].set_ylabel('Frequency')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()

