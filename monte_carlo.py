import numpy as np
import pandas as pd

def run_monte_carlo_simulation(base_ev=1750.0, iterations=10000):
    """
    Executes a 10,000-iteration stochastic Monte Carlo simulation for Enterprise Value.
    Returns the EV array and key percentile metrics (P10, P50, P90).
    """
    np.random.seed(42)
    
    # Stochastic variables: Revenue growth volatility, EBITDA margin spread, WACC fluctuations
    growth_rates = np.random.normal(loc=0.08, scale=0.02, size=iterations)
    ebitda_margins = np.random.normal(loc=0.22, scale=0.03, size=iterations)
    wacc_rates = np.random.normal(loc=0.09, scale=0.01, size=iterations)
    
    # Simulate Enterprise Value distribution based on stochastic cash flow models
    ev_array = base_ev * (1 + growth_rates) * (ebitda_margins / 0.22) / (wacc_rates / 0.09)
    
    p10 = np.percentile(ev_array, 10)
    p50 = np.percentile(ev_array, 50)
    p90 = np.percentile(ev_array, 90)
    
    return ev_array, p10, p50, p90

if __name__ == "_main_":
    print("--- Initializing Standalone Monte Carlo Engine ---")
    evs, p10, p50, p90 = run_monte_carlo_simulation()
    print(f"P10: ${p10:,.2f}M | P50: ${p50:,.2f}M | P90: ${p90:,.2f}M")