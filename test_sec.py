import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional styling for institutional charts
sns.set_theme(style="darkgrid")
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

print("--- Initializing Monte Carlo Engine with Advanced Visualizations ---")

# Simulation parameters
iterations = 10000
base_fcf = 100.0  # Base Year Free Cash Flow ($M)

growth_rate_mean, growth_rate_std = 0.05, 0.015
wacc_mean, wacc_std = 0.09, 0.01
terminal_growth_mean, terminal_growth_std = 0.025, 0.005

np.random.seed(42)

sim_growth = np.random.normal(growth_rate_mean, growth_rate_std, iterations)
sim_wacc = np.random.normal(wacc_mean, wacc_std, iterations)
sim_tg = np.random.normal(terminal_growth_mean, terminal_growth_std, iterations)
sim_wacc = np.maximum(sim_wacc, sim_tg + 0.015)

ev_results = []

for i in range(iterations):
    g = sim_growth[i]
    wacc = sim_wacc[i]
    tg = sim_tg[i]
    
    fcf_stream = [base_fcf * ((1 + g) ** year) for year in range(1, 6)]
    pv_fcf = sum([fcf / ((1 + wacc) ** year) for year, fcf in enumerate(fcf_stream, start=1)])
    terminal_value = (fcf_stream[-1] * (1 + tg)) / (wacc - tg)
    pv_tv = terminal_value / ((1 + wacc) ** 5)
    
    ev_results.append(pv_fcf + pv_tv)

ev_array = np.array(ev_results)
p10 = np.percentile(ev_array, 10)
p50 = np.percentile(ev_array, 50)
p90 = np.percentile(ev_array, 90)

print(f"\nP10: ${p10:,.2f}M | P50: ${p50:,.2f}M | P90: ${p90:,.2f}M")
print("--- Rendering Institutional Valuation Distribution Chart ---")

# Create a high-end dual-panel figure layout
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Probability Density Histogram with Confidence Intervals
sns.histplot(ev_array, kde=True, ax=ax1, color='#1f77b4', bins=50, stat="density", alpha=0.6)
ax1.axvline(p10, color='#d62728', linestyle='--', linewidth=2, label=f'P10 Bear: ${p10:,.0f}M')
ax1.axvline(p50, color='#2ca02c', linestyle='-', linewidth=2.5, label=f'P50 Median: ${p50:,.0f}M')
ax1.axvline(p90, color='#ff7f0e', linestyle='--', linewidth=2, label=f'P90 Bull: ${p90:,.0f}M')
ax1.set_title('Monte Carlo DCF: Enterprise Value Distribution', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Enterprise Value ($M)', fontsize=10)
ax1.set_ylabel('Density', fontsize=10)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

# Panel 2: Cumulative Distribution Function (CDF)
sns.ecdfplot(ev_array, ax=ax2, color='#2b2b2b', linewidth=2.5)
ax2.axhline(0.50, color='#2ca02c', linestyle=':', alpha=0.7)
ax2.axvline(p50, color='#2ca02c', linestyle=':', alpha=0.7, label=f'50% Probability Threshold')
ax2.set_title('Cumulative Distribution Function (CDF)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Enterprise Value ($M)', fontsize=10)
ax2.set_ylabel('Probability', fontsize=10)
ax2.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)