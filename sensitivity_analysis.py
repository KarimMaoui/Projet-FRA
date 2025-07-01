from rate_simulation import simulate_libor_paths
from fra_pricing import simulate_fra_pnl
import numpy as np

def run_fra_scenario(S0, sigma, T_fra, fra_rate, notional=1_000_000, delta=0.25, n_paths=1000):
    """
    Run a FRA hedging scenario and return average and std of P&L.

    Parameters:
        S0 (float): Initial rate
        sigma (float): Rate volatility
        T_fra (float): Time until FRA starts (years)
        fra_rate (float): Fixed rate in FRA
        notional, delta: Contract terms
    """
    # Simulate paths
    T_total = T_fra + delta
    dt = 1/252
    paths = simulate_libor_paths(S0=S0, sigma=sigma, T=T_total, dt=dt, n_paths=n_paths)

    # Settlement index
    settlement_index = int(T_fra / dt)
    realized_rates = paths[:, settlement_index]

    # Payoffs
    payoffs = simulate_fra_pnl(paths, fra_rate, notional, delta)
    return np.mean(payoffs), np.std(payoffs)
