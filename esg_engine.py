import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure dark institutional finance theme
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['axes.edgecolor'] = '#444444'
plt.rcParams['axes.linewidth'] = 1.0

print("--- Executing ESG Engine with Institutional Visuals ---")

# Portfolio Data
portfolio_data = [
    {
        "Company": "EcoTech CleanCorp", 
        "Base EV ($M)": 1800.0, "Revenue ($M)": 500.0, 
        "Scope_1": 5.0, "Scope_2": 3.0, "Scope_3": 15.0, 
        "E_Score": 9.2, "S_Score": 8.5, "G_Score": 8.8,
        "Fossil_Asset_Exposure_Pct": 0.0
    },
    {
        "Company": "Global Heavy Ind.", 
        "Base EV ($M)": 3200.0, "Revenue ($M)": 1500.0, 
        "Scope_1": 350.0, "Scope_2": 120.0, "Scope_3": 850.0, 
        "E_Score": 4.1, "S_Score": 5.5, "G_Score": 5.0,
        "Fossil_Asset_Exposure_Pct": 0.45
    },
    {
        "Company": "Apex Logistics", 
        "Base EV ($M)": 1250.0, "Revenue ($M)": 600.0, 
        "Scope_1": 110.0, "Scope_2": 40.0, "Scope_3": 320.0, 
        "E_Score": 6.0, "S_Score": 7.1, "G_Score": 7.5,
        "Fossil_Asset_Exposure_Pct": 0.20
    }
]

esg_results = []
initial_carbon_price = 85.0
carbon_price_cagr = 0.07

for item in portfolio_data:
    company = item["Company"]
    ev = item["Base EV ($M)"]
    rev = item["Revenue ($M)"]
    s1, s2, s3 = item["Scope_1"], item["Scope_2"], item["Scope_3"]
    total_emissions = s1 + s2 + s3
    
    cumulative_carbon_cost = 0
    current_price = initial_carbon_price
    for year in range(1, 6):
        annual_cost = (total_emissions * current_price) / 1000.0
        cumulative_carbon_cost += annual_cost / ((1 + 0.08) ** year)
        current_price *= (1 + carbon_price_cagr)
        
    stranded_asset_impairment = ev * item["Fossil_Asset_Exposure_Pct"] * 0.35
    composite_esg = (item["E_Score"] * 0.4) + (item["S_Score"] * 0.3) + (item["G_Score"] * 0.3)
    
    if composite_esg >= 8.0:
        wacc_spread_bps = -50.0
    elif composite_esg >= 6.0:
        wacc_spread_bps = 0.0
    else:
        wacc_spread_bps = 125.0
        
    climate_adjusted_ev = ev - cumulative_carbon_cost - stranded_asset_impairment
    
    esg_results.append({
        "Company": company,
        "Base EV": ev,
        "Climate EV": round(climate_adjusted_ev, 2),
        "Scope 1": s1,
        "Scope 2": s2,
        "Scope 3": s3,
        "Composite ESG": round(composite_esg, 2),
        "WACC Spread (bps)": wacc_spread_bps
    })

df = pd.DataFrame(esg_results)

# --- RENDERING INSTITUTIONAL GRAPHICAL DASHBOARD ---
fig, axs = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Institutional ESG & Climate Transition Valuation Analytics Suite', fontsize=15, fontweight='bold', color='#ffffff', y=0.98)

# Panel 1: EV Valuation Haircut Comparison
x = np.arange(len(df['Company']))
width = 0.35
axs[0].bar(x - width/2, df['Base EV'], width, label='Base EV ($M)', color='#1f77b4', alpha=0.85)
axs[0].bar(x + width/2, df['Climate EV'], width, label='Climate-Adjusted EV ($M)', color='#d62728', alpha=0.85)
axs[0].set_title('Valuation Haircut: Base vs. Climate EV', fontsize=11, fontweight='bold', pad=10)
axs[0].set_xticks(x)
axs[0].set_xticklabels(df['Company'], rotation=15)
axs[0].set_ylabel('Enterprise Value ($M)', fontsize=10)
axs[0].legend(frameon=True, facecolor='#222222', edgecolor='#444444')
axs[0].grid(axis='y', linestyle=':', alpha=0.4)

# Panel 2: Stacked Carbon Emissions (Scope 1, 2, 3)
axs[1].bar(df['Company'], df['Scope 1'], label='Scope 1 (Direct)', color='#2ca02c')
axs[1].bar(df['Company'], df['Scope 2'], bottom=df['Scope 1'], label='Scope 2 (Energy)', color='#ff7f0e')
axs[1].bar(df['Company'], df['Scope 3'], bottom=df['Scope 1']+df['Scope 2'], label='Scope 3 (Value Chain)', color='#9467bd')
axs[1].set_title('Carbon Footprint Scope Breakdown (kt CO2e)', fontsize=11, fontweight='bold', pad=10)
axs[1].set_xticklabels(df['Company'], rotation=15)
axs[1].set_ylabel('Emissions (kt CO2e)', fontsize=10)
axs[1].legend(frameon=True, facecolor='#222222', edgecolor='#444444')
axs[1].grid(axis='y', linestyle=':', alpha=0.4)

# Panel 3: ESG Score vs WACC Risk Heatmap
heatmap_data = df.set_index('Company')[['Composite ESG', 'WACC Spread (bps)']]
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="vlag", cbar=True, ax=axs[2], linewidths=1, linecolor='#333333')
axs[2].set_title('ESG Rating vs. WACC Risk Spread (bps)', fontsize=11, fontweight='bold', pad=10)
axs[2].set_ylabel('')

plt.tight_layout()
plt.show()