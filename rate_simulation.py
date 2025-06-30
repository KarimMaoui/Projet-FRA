import numpy as np
import matplotlib.pyplot as plt

def simulate_libor_paths(S0=0.04, mu=0.00, sigma=0.02, T=1, dt=1/252, n_paths=1000):
    """
    Simulates LIBOR forward paths using a Geometric Brownian Motion (GBM) model.

    Parameters:
        S0 (float): Initial interest rate (e.g., 3% = 0.03)
        mu (float): Drift term
        sigma (float): Volatility of interest rates
        T (float): Time horizon in years
        dt (float): Time step (in years, e.g. 1/252 for daily steps)
        n_paths (int): Number of paths to simulate

    Returns:
        numpy.ndarray: Simulated rate paths (shape: n_paths x n_steps)
    """
    n_steps = int(T / dt)
    rates = np.zeros((n_paths, n_steps))
    rates[:, 0] = S0

    for t in range(1, n_steps):
        Z = np.random.normal(0, 1, n_paths)
        rates[:, t] = rates[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    return rates

# Example: plot a few simulated paths
if __name__ == "__main__":
    paths = simulate_libor_paths()
    for i in range(10):
        plt.plot(paths[i], lw=1)
    plt.title("Simulated LIBOR Paths")
    plt.xlabel("Time steps (days)")
    plt.ylabel("Rate")
    plt.grid(True)
    plt.show()

