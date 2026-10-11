import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_monte_carlo_simulation_advanced(iterations=10000, base_fcf=100.0, volatility=0.20):
    """
    Executes an institutional stochastic DCF simulation across multiple economic vectors.
    """
    growth_rate_mean, growth_rate_std = 0.05, volatility * 0.1
    wacc_mean, wacc_std = 0.09, volatility * 0.08
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

    # Package parameter vectors for the sensitivity matrix
    sim_data = pd.DataFrame({
        'Growth': sim_growth * 100,
        'WACC': sim_wacc * 100,
        'EV': ev_array
    })

    return ev_array, sim_data, p10, p50, p90

def plot_advanced_monte_carlo_charts(ev_array, sim_data, p10, p50, p90, base_target):
    """
    Renders a 3-panel institutional matplotlib dashboard.
    """
    sns.set_theme(style="darkgrid")
    plt.rcParams['font.sans-serif'] = 'Segoe UI'
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5))

    # Panel 1: Probability Density Histogram & Confidence Intervals
    sns.histplot(ev_array, kde=True, ax=ax1, color='#1f77b4', bins=50, stat="density", alpha=0.6)
    ax1.axvline(p10, color='#d62728', linestyle='--', linewidth=1.5, label=f'P10 Bear: ${p10:,.0f}M')
    ax1.axvline(p50, color='#2ca02c', linestyle='-', linewidth=2, label=f'P50 Median: ${p50:,.0f}M')
    ax1.axvline(p90, color='#ff7f0e', linestyle='--', linewidth=1.5, label=f'P90 Bull: ${p90:,.0f}M')
    ax1.axvline(base_target, color='black', linestyle=':', linewidth=1.5, label=f'Base Target: ${base_target:,.0f}M')
    ax1.set_title('1. EV Distribution & Confidence Intervals', fontsize=10, fontweight='bold', pad=10)
    ax1.set_xlabel('Enterprise Value ($M)', fontsize=9)
    ax1.set_ylabel('Density', fontsize=9)
    ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8)

    # Panel 2: Cumulative Distribution Function (CDF)
    sns.ecdfplot(ev_array, ax=ax2, color='#2b2b2b', linewidth=2)
    ax2.axhline(0.50, color='#2ca02c', linestyle=':', alpha=0.7)
    ax2.axvline(p50, color='#2ca02c', linestyle=':', alpha=0.7, label=f'50% Probability Threshold')
    ax2.axvline(base_target, color='black', linestyle=':', linewidth=1.5, label=f'Base Target')
    ax2.set_title('2. Cumulative Distribution Function (CDF)', fontsize=10, fontweight='bold', pad=10)
    ax2.set_xlabel('Enterprise Value ($M)', fontsize=9)
    ax2.set_ylabel('Cumulative Probability', fontsize=9)
    ax2.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8)

    # Panel 3: WACC vs Growth Sensitivity Scatter Heatmap
    sample_data = sim_data.sample(n=1500, random_state=42)
    sc = ax3.scatter(sample_data['WACC'], sample_data['Growth'], c=sample_data['EV'], cmap='viridis', alpha=0.75, s=18, edgecolor='none')
    cbar = fig.colorbar(sc, ax=ax3)
    cbar.set_label('Enterprise Value ($M)', fontsize=9)
    ax3.set_title('3. WACC vs. Growth Sensitivity Matrix', fontsize=10, fontweight='bold', pad=10)
    ax3.set_xlabel('WACC (%)', fontsize=9)
    ax3.set_ylabel('Growth Rate (%)', fontsize=9)

    plt.tight_layout()
    return fig