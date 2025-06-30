import numpy as np

def fra_payoff(realized_rate, fra_rate, notional, delta):
    """
    Calculate the payoff of a FRA given the realized rate.

    Parameters:
        realized_rate (float or array): the rate at settlement
        fra_rate (float): the agreed FRA rate
        notional (float): the notional amount
        delta (float): year fraction (e.g. 0.25 for 3 months)

    Returns:
        float or array: the payoff amount
    """
    payoff = (realized_rate - fra_rate) * notional * delta / (1 + realized_rate * delta)
    return payoff

def simulate_fra_pnl(rate_paths, fra_rate, notional=1_000_000, delta=0.25):
    """
    Compute the P&L of hedging using a FRA over multiple simulated paths.

    Parameters:
        rate_paths (ndarray): simulated LIBOR paths (n_paths x n_steps)
        fra_rate (float): the agreed FRA rate
        notional (float): the notional exposure
        delta (float): the period covered by the FRA

    Returns:
        ndarray: array of FRA payoffs (1 per path)
    """
    # Take the rate at FRA settlement (e.g., 3 months forward = column 63 if dt = 1/252)
    settlement_index = int(63)  # approx 3 months if daily steps
    realized_rates = rate_paths[:, settlement_index]
    payoffs = fra_payoff(realized_rates, fra_rate, notional, delta)
    return payoffs

def calculate_unhedged_cost(realized_rates, notional, delta):
    return realized_rates * notional * delta

def calculate_total_hedged_cost(realized_rates, fra_rate, notional, delta):
    float_cost = calculate_unhedged_cost(realized_rates, notional, delta)
    fra_compensation = fra_payoff(realized_rates, fra_rate, notional, delta)
    return float_cost - fra_compensation
