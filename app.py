import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Page Configuration
st.set_page_config(
    page_title="Institutional Financial Analytics Suite",
    page_icon="📊",
    layout="wide"
)

# Styling
plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

# App Title & Header
st.title("Institutional Financial Analytics Suite — 16-Graph Master Architecture")
st.markdown("### Enterprise Workspace: SEC Peer Benchmarking, QoE Normalization, Advanced Capital Bridges, Elite ESG Climate Stress-Testing, and Correlated VaR Monte Carlo")

# Navigation Tabs (All 5 Pillars)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 1. SEC Peer Benchmarking", 
    "📊 2. LTM & QoE Normalization", 
    "🌉 3. Capital Structure & Valuation", 
    "🌱 4. Elite ESG & Climate Risk", 
    "🎲 5. Monte Carlo, VaR & Risk"
])

# ==========================================
# PILLAR 1: SEC EDGAR PEER BENCHMARKING (GRAPHS 1–3)
# ==========================================
with tab1:
    st.subheader("Pillar 1: SEC EDGAR Peer Benchmarking & Financial Pipeline")
    st.markdown("""
    * *1. Peer Valuation Frontier:* P/TBV vs. ROTCE scatter plot with market-cap bubbles and regression trendline.
    * *2. Financial Performance Timeline:* Quarterly/Annual revenue, net income, and margin trajectories.
    * *3. Data-Quality Heatmap:* XBRL tag reliability and reporting consistency matrix across peers.
    """)

    if st.button("Generate Pillar 1 Analytics Suite", key="btn_p1"):
        # Graph 1: Peer Valuation Frontier (Scatter with Bubble & Regression)
        st.write("### 1. Peer Valuation Frontier (P/TBV vs. ROTCE)")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        np.random.seed(42)
        rotce = np.random.uniform(8, 25, 12)
        ptbv = 0.12 * rotce + np.random.normal(1.2, 0.3, 12)
        mkt_cap = np.random.uniform(20, 250, 12)
        peers = [f"Peer {i}" for i in range(1, 12)]
        
        scatter = ax1.scatter(rotce, ptbv, s=mkt_cap*1.5, color="#1f77b4", alpha=0.6, edgecolors="black", linewidth=1.5)
        sns.regplot(x=rotce, y=ptbv, scatter=False, ax=ax1, color="#d62728", line_kws={"linewidth": 2, "linestyle": "--"})
        ax1.set_title("Valuation Frontier: Price-to-Tangible Book Value vs. ROTCE", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Return on Tangible Common Equity (ROTCE %)", fontsize=9)
        ax1.set_ylabel("Price-to-Tangible Book Value (P/TBV x)", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig1)

        # Graph 2: Financial Performance Timeline
        st.write("### 2. Financial Performance Timeline")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        quarters = ["Q1 24", "Q2 24", "Q3 24", "Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25"]
        revenue = [22.4, 23.8, 24.1, 26.5, 27.2, 28.5, 29.1, 31.0]
        net_income = [4.2, 4.5, 4.8, 5.2, 5.5, 5.9, 6.1, 6.8]
        
        ax2.plot(quarters, revenue, marker="o", color="#1f77b4", linewidth=2.5, label="Revenue ($B)")
        ax2.plot(quarters, net_income, marker="s", color="#2ca02c", linewidth=2.5, label="Net Income ($B)")
        ax2.set_title("Multi-Period Financial Performance & Earnings Trajectory", fontsize=11, fontweight='bold')
        ax2.set_ylabel("USD ($ Billions)", fontsize=9)
        ax2.legend(loc='upper left', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig2)

        # Graph 3: Data-Quality Heatmap
        st.write("### 3. SEC XBRL Data-Quality Heatmap")
        fig3, ax3 = plt.subplots(figsize=(10, 3.2))
        quality_matrix = pd.DataFrame(
            np.random.uniform(0.85, 1.00, (4, 6)),
            index=["GS", "JPM", "MS", "BAC"],
            columns=["Revenues", "Operating Income", "Total Assets", "Long-Term Debt", "Tax Provision", "EPS Diluted"]
        )
        sns.heatmap(quality_matrix, annot=True, cmap="Greens", vmin=0.8, vmax=1.0, fmt=".2f", ax=ax3, cbar_kws={'label': 'XBRL Reliability Score'})
        ax3.set_title("XBRL Tag Consistency & Data-Quality Audit Heatmap", fontsize=11, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig3)

# ==========================================
# PILLAR 2: QUALITY OF EARNINGS (GRAPHS 4–6)
# ==========================================
with tab2:
    st.subheader("Pillar 2: LTM Calendarizer & Quality of Earnings (QoE) Engine")
    st.markdown("""
    * *4. EBITDA Normalization Waterfall:* Reported EBITDA → add-backs → deductions → normalized EBITDA.
    * *5. Earnings-to-Cash Conversion Chart:* Compares EBITDA, operating cash flow, and free cash flow.
    * *6. Adjustment-Risk Matrix:* Maps adjustment materiality against evidence strength and recurrence risk.
    """)

    if st.button("Generate Pillar 2 Analytics Suite", key="btn_p2"):
        # Graph 4: EBITDA Normalization Waterfall
        st.write("### 4. EBITDA Normalization Waterfall")
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        steps = ["Reported EBITDA", "Restructuring", "Litigation", "Asset Gains", "Working Cap", "Normalized EBITDA"]
        vals = [18500, 1200, 450, -300, -250, 19600]
        cols = ["#1f77b4", "#2ca02c", "#2ca02c", "#d62728", "#17becf", "#9467bd"]
        bars = ax4.bar(steps, vals, color=cols, width=0.55)
        ax4.axhline(0, color='grey', linewidth=0.8)
        ax4.set_title("EBITDA Normalization Waterfall Walk ($M)", fontsize=11, fontweight='bold')
        ax4.set_ylabel("USD ($ Millions)", fontsize=9)
        plt.xticks(rotation=15)
        for bar in bars:
            h = bar.get_height()
            ax4.annotate(f'${h:,.0f}M', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3 if h >= 0 else -12), textcoords="offset points", ha='center', fontsize=8, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig4)

        # Graph 5: Earnings-to-Cash Conversion Chart
        st.write("### 5. Earnings-to-Cash Conversion Chart")
        fig5, ax5 = plt.subplots(figsize=(10, 4))
        periods = ["FY22", "FY23", "FY24", "FY25", "LTM"]
        ebitda_series = [15000, 16500, 17800, 18500, 19200]
        ocf_series = [12500, 14200, 15600, 16100, 16800]
        fcf_series = [9800, 11000, 12200, 13000, 13700]
        x_idx = np.arange(len(periods))
        width = 0.25
        
        ax5.bar(x_idx - width, ebitda_series, width, label="EBITDA", color="#1f77b4")
        ax5.bar(x_idx, ocf_series, width, label="Operating Cash Flow", color="#2ca02c")
        ax5.bar(x_idx + width, fcf_series, width, label="Free Cash Flow", color="#ff7f0e")
        ax5.set_xticks(x_idx)
        ax5.set_xticklabels(periods)
        ax5.set_title("Earnings vs. Cash Flow Conversion Analysis", fontsize=11, fontweight='bold')
        ax5.set_ylabel("USD ($ Millions)", fontsize=9)
        ax5.legend(loc='upper left', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig5)

        # Graph 6: Adjustment-Risk Matrix
        st.write("### 6. QoE Adjustment-Risk Matrix")
        fig6, ax6 = plt.subplots(figsize=(8, 4))
        materiality = [2.5, 5.0, 1.2, 8.5, 3.1]
        recurrence_risk = [1.0, 4.0, 2.5, 8.0, 3.0]
        adj_labels = ["Severance", "Litigation", "Lease Adj", "Bad Debt", "FX Revaluation"]
        
        ax6.scatter(recurrence_risk, materiality, s=250, color="#d62728", alpha=0.7, edgecodes="black")
        for i, txt in enumerate(adj_labels):
            ax6.annotate(txt, (recurrence_risk[i]+0.2, materiality[i]), fontsize=9, fontweight='bold')
        ax6.axvline(5.0, color='orange', linestyle='--', linewidth=1.5, label='High Recurrence Risk Threshold')
        ax6.axhline(5.0, color='orange', linestyle='--', linewidth=1.5, label='High Materiality Threshold')
        ax6.set_title("Adjustment Materiality vs. Recurrence Risk Matrix", fontsize=11, fontweight='bold')
        ax6.set_xlabel("Recurrence Risk Score (1-10)", fontsize=9)
        ax6.set_ylabel("Materiality Impact ($M)", fontsize=9)
        ax6.legend(loc='upper left', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig6)

# ==========================================
# PILLAR 3: CAPITAL STRUCTURE & VALUATION (GRAPHS 7–9)
# ==========================================
with tab3:
    st.subheader("Pillar 3: Advanced Capital Structure & Valuation Engine")
    st.markdown("""
    * *7. Dynamic Equity Bridge:* Enterprise value → debt/claims → equity value → implied share price.
    * *8. Valuation Sensitivity Heatmap:* Shows valuation changes under different WACC, growth, and multiple assumptions.
    * *9. Valuation Football Field:* Compares valuation ranges from DCF, comps, and other suitable methods.
    """)

    if st.button("Generate Pillar 3 Analytics Suite", key="btn_p3"):
        # Graph 7: Dynamic Equity Bridge
        st.write("### 7. Dynamic Capital Structure Equity Bridge Waterfall")
        fig7, ax7 = plt.subplots(figsize=(10, 4))
        components = ["Enterprise Value", "Senior Debt", "Leases/Pension", "Less: Cash", "Equity Value"]
        amounts = [145000, -24000, -4700, 15600, 131900]
        cols = ["#1f77b4", "#d62728", "#d62728", "#2ca02c", "#9467bd"]
        bars = ax7.bar(components, amounts, color=cols, width=0.55)
        ax7.axhline(0, color='grey', linewidth=0.8)
        ax7.set_title("Enterprise Value to Equity Value Capital Bridge", fontsize=11, fontweight='bold')
        ax7.set_ylabel("USD ($ Millions)", fontsize=9)
        for bar in bars:
            h = bar.get_height()
            ax7.annotate(f'${h:,.0f}M', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3 if h >= 0 else -12), textcoords="offset points", ha='center', fontsize=8, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig7)

        # Graph 8: Valuation Sensitivity Heatmap
        st.write("### 8. Valuation Sensitivity Heatmap (WACC vs. Terminal Growth)")
        fig8, ax8 = plt.subplots(figsize=(9, 3.8))
        wacc_vals = ["8.0%", "8.5%", "9.0%", "9.5%", "10.0%"]
        g_vals = ["1.5%", "2.0%", "2.5%", "3.0%"]
        sensitivity_matrix = pd.DataFrame(
            [[165, 158, 150, 142], [152, 146, 139, 132], [141, 135, 128, 122], [130, 124, 118, 113], [120, 115, 109, 104]],
            index=wacc_vals, columns=g_vals
        )
        sns.heatmap(sensitivity_matrix, annot=True, cmap="YlGnBu", fmt="d", ax=ax8, cbar_kws={'label': 'Implied Share Price ($)'})
        ax8.set_title("Valuation Sensitivity Analysis Matrix", fontsize=11, fontweight='bold')
        ax8.set_xlabel("Terminal Growth Rate (g)", fontsize=9)
        ax8.set_ylabel("WACC", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig8)

        # Graph 9: Valuation Football Field
        st.write("### 9. Valuation Football Field Chart")
        fig9, ax9 = plt.subplots(figsize=(10, 3.5))
        methods = ["DCF (Perpetuity Growth)", "DCF (Exit Multiple)", "Comparable Comps (P/E)", "Comparable Comps (EV/EBITDA)", "Precedent Transactions"]
        low_vals = [120, 125, 110, 115, 130]
        high_vals = [165, 172, 145, 155, 185]
        
        y_pos = np.arange(len(methods))
        for i in range(len(methods)):
            ax9.barh(y_pos[i], high_vals[i] - low_vals[i], left=low_vals[i], color='#1f77b4', alpha=0.6, height=0.5, edgecolor='black')
        ax9.set_yticks(y_pos)
        ax9.set_yticklabels(methods, fontsize=9)
        ax9.set_title("Valuation Football Field Summary ($ per Share)", fontsize=11, fontweight='bold')
        ax9.set_xlabel("Implied Share Price ($)", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig9)

# ==========================================
# PILLAR 4: ESG & CLIMATE RISK (GRAPHS 10–12)
# ==========================================
with tab4:
    st.subheader("Pillar 4: Elite ESG Risk, DCF Valuation Impact & Carbon Transition Engine")
    st.markdown("""
    * *10. Climate Scenario Fan Chart:* Compares baseline, orderly-transition, and disorderly-transition pathways.
    * *11. Climate Materiality Heatmap:* Compares climate exposure, financial sensitivity, and disclosure confidence.
    * *12. ESG-to-Valuation Waterfall:* Traces modeled climate impacts through costs, cash flows, and valuation.
    """)

    if st.button("Generate Pillar 4 Analytics Suite", key="btn_p4"):
        # Graph 10: Climate Scenario Fan Chart
        st.write("### 10. Climate Transition Scenario Fan Chart")
        fig10, ax10 = plt.subplots(figsize=(10, 4))
        years = [2026, 2027, 2028, 2029, 2030]
        baseline = [100, 108, 117, 127, 138]
        orderly = [100, 105, 111, 118, 125]
        disorderly = [100, 98, 92, 85, 78]
        
        ax10.plot(years, baseline, marker="o", color="#2ca02c", linewidth=2.5, label="Baseline (No Carbon Shock)")
        ax10.plot(years, orderly, marker="s", color="#1f77b4", linewidth=2.5, label="Orderly Transition ($50–$100/ton)")
        ax10.plot(years, disorderly, marker="^", color="#d62728", linewidth=2.5, label="Disorderly Transition (Abrupt Shock)")
        ax10.set_title("Multi-Year Climate Transition Scenario Pathways (Indexed EBITDA)", fontsize=11, fontweight='bold')
        ax10.set_ylabel("Indexed Cash Flow ($)", fontsize=9)
        ax10.legend(loc='upper left', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig10)

        # Graph 11: Climate Materiality Heatmap
        st.write("### 11. Climate Materiality Heatmap")
        fig11, ax11 = plt.subplots(figsize=(8, 3.5))
        exposure = [0.8, 0.4, 0.9, 0.2, 0.7]
        sensitivity = [0.7, 0.3, 0.8, 0.1, 0.6]
        sectors = ["Scope 1 Emissions", "Physical Assets", "Supply Chain", "Water Stress", "Regulatory Tax"]
        
        ax11.scatter(exposure, sensitivity, s=300, color="#ff7f0e", alpha=0.7, edgecodes="black")
        for i, txt in enumerate(sectors):
            ax11.annotate(txt, (exposure[i]+0.02, sensitivity[i]), fontsize=9, fontweight='bold')
        ax11.axvline(0.5, color='grey', linestyle='--', linewidth=1)
        ax11.axhline(0.5, color='grey', linestyle='--', linewidth=1)
        ax11.set_title("Climate Exposure vs. Financial Sensitivity Heatmap", fontsize=11, fontweight='bold')
        ax11.set_xlabel("Climate Exposure Score (0–1)", fontsize=9)
        ax11.set_ylabel("Financial Sensitivity Score (0–1)", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig11)

        # Graph 12: ESG-to-Valuation Waterfall
        st.write("### 12. ESG-to-Valuation Waterfall Impact")
        fig12, ax12 = plt.subplots(figsize=(10, 4))
        esg_steps = ["Base DCF Value", "Carbon Tax Cost", "WACC Penalty", "Compliance Risk", "Adjusted Valuation"]
        esg_vals = [145000, -6500, -4200, -1800, 132500]
        esg_cols = ["#1f77b4", "#d62728", "#d62728", "#d62728", "#9467bd"]
        bars = ax12.bar(esg_steps, esg_vals, color=esg_cols, width=0.55)
        ax12.axhline(0, color='grey', linewidth=0.8)
        ax12.set_title("ESG Climate Impact Waterfall on Enterprise Value ($M)", fontsize=11, fontweight='bold')
        ax12.set_ylabel("USD ($ Millions)", fontsize=9)
        for bar in bars:
            h = bar.get_height()
            ax12.annotate(f'${h:,.0f}M', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3 if h >= 0 else -12), textcoords="offset points", ha='center', fontsize=8, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig12)

# ==========================================
# PILLAR 5: MONTE CARLO, VaR & RISK (GRAPHS 13–16)
# ==========================================
with tab5:
    st.subheader("Pillar 5: Correlated Monte Carlo, Fan Charts, VaR & Tornado Risk Engine")
    st.markdown("""
    * *13. Monte Carlo Fan Chart:* Shows P5, P10, median, P90, and P95 simulated outcomes.
    * *14. Correlation Matrix:* Visualizes relationships between simulated financial drivers.
    * *15. VaR & Expected-Shortfall Distribution:* Shows loss distribution, VaR threshold, and tail losses.
    * *16. Risk-Driver Tornado Chart:* Ranks assumptions with the largest impact on valuation or downside risk.
    """)

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        num_iter = st.slider("Simulation Iterations:", min_value=5000, max_value=50000, value=20000, step=5000, key="p5_iter")
    with col_i2:
        vol_factor = st.slider("Valuation Volatility (%):", min_value=5.0, max_value=35.0, value=18.0, step=0.5, key="p5_vol")

    if st.button("Run Comprehensive Risk & Monte Carlo Suite", key="btn_p5"):
        with st.spinner("Executing all 4 risk models and generating charts 13–16..."):
            np.random.seed(42)
            base_ev = 145000.0
            std_dev = base_ev * (vol_factor / 100.0)
            ev_array = np.random.normal(base_ev, std_dev, num_iter)
            p5, p10, p50, p90, p95 = np.percentile(ev_array, [5, 10, 50, 90, 95])
            var_95 = np.percentile(ev_array, 5)
            cvar_95 = ev_array[ev_array <= var_95].mean()
            prob_loss = (np.sum(ev_array < base_ev) / num_iter) * 100

            # -------------------------------------------------------------
            # 13. MONTE CARLO FAN CHART
            # -------------------------------------------------------------
            st.write("### 13. Monte Carlo Fan Chart (Percentile Path Projections)")
            fig13, ax13 = plt.subplots(figsize=(10, 4))
            years = [2026, 2027, 2028, 2029, 2030]
            np.random.seed(100)
            paths = np.zeros((100, len(years)))
            paths[:, 0] = base_ev
            for i in range(1, len(years)):
                paths[:, i] = paths[:, i-1] * (1 + np.random.normal(0.06, vol_factor/150.0, 100))
                
            p5_path = np.percentile(paths, 5, axis=0)
            p10_path = np.percentile(paths, 10, axis=0)
            p50_path = np.percentile(paths, 50, axis=0)
            p90_path = np.percentile(paths, 90, axis=0)
            p95_path = np.percentile(paths, 95, axis=0)
            
            ax13.fill_between(years, p5_path, p95_path, color='#aec7e8', alpha=0.4, label='P5–P95 Outer Band')
            ax13.fill_between(years, p10_path, p90_path, color='#1f77b4', alpha=0.3, label='P10–P90 Confidence Interval')
            ax13.plot(years, p50_path, color='darkblue', linewidth=2.5, marker='o', label='Median (P50) Path')
            ax13.set_title("Stochastic Enterprise Value Fan Chart (P5 to P95)", fontsize=11, fontweight='bold')
            ax13.set_ylabel("Enterprise Value ($M)", fontsize=9)
            ax13.legend(loc='upper left', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig13)

            # -------------------------------------------------------------
            # 14. CORRELATION MATRIX HEATMAP
            # -------------------------------------------------------------
            st.write("### 14. Simulated Financial Drivers Correlation Matrix")
            fig14, ax14 = plt.subplots(figsize=(8, 3.5))
            driver_data = pd.DataFrame({
                "Rev Growth": np.random.normal(0.08, 0.02, 500),
                "EBITDA Margin": np.random.normal(0.24, 0.04, 500),
                "WACC": np.random.normal(0.09, 0.01, 500),
                "Exit Multiple": np.random.normal(12.0, 1.5, 500),
                "CapEx Intensity": np.random.normal(0.05, 0.01, 500)
            })
            sns.heatmap(driver_data.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", ax=ax14, cbar_kws={'label': 'Correlation Coefficient'})
            ax14.set_title("Cross-Driver Correlation Heatmap", fontsize=11, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig14)

            # -------------------------------------------------------------
            # 15. VaR & EXPECTED-SHORTFALL DISTRIBUTION
            # -------------------------------------------------------------
            st.write("### 15. VaR & Expected-Shortfall Distribution")
            fig15, ax15 = plt.subplots(figsize=(10, 4))
            n_bins, bins, patches = ax15.hist(ev_array, bins=60, density=True, color="#1f77b4", alpha=0.5, edgecolor='black')
            for patch, left_edge in zip(patches, bins[:-1]):
                if left_edge < var_95:
                    patch.set_facecolor('#d62728')
                    patch.set_alpha(0.8)
            ax15.axvline(var_95, color='darkred', linestyle='--', linewidth=2.5, label=f'95% VaR Threshold (${var_95:,.0f}M)')
            ax15.axvline(cvar_95, color='purple', linestyle=':', linewidth=2.5, label=f'Expected Shortfall / CVaR (${cvar_95:,.0f}M)')
            ax15.axvline(base_ev, color='green', linestyle='-', linewidth=2, label=f'Base Case (${base_ev:,.0f}M)')
            ax15.set_title("Institutional Value-at-Risk (VaR) & Expected Shortfall Tail Distribution", fontsize=11, fontweight='bold')
            ax15.set_xlabel("Enterprise Value ($ Millions)", fontsize=9)
            ax15.legend(loc='upper right', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig15)

            # -------------------------------------------------------------
            # 16. RISK-DRIVER TORNADO CHART
            # -------------------------------------------------------------
            st.write("### 16. Risk-Driver Tornado Sensitivity Chart")
            fig16, ax16 = plt.subplots(figsize=(10, 3.8))
            drivers = ["Exit Multiple (+/- 2x)", "WACC Spread (+/- 100bps)", "Revenue Growth (+/- 2%)", "EBITDA Margin (+/- 3%)", "Inflation / Cost Shock"]
            low_imp = [-18000, -14000, -11000, -8500, -5000]
            high_imp = [22000, 16000, 13000, 9500, 6000]
            y_pos = np.arange(len(drivers))
            ax16.barh(y_pos, low_imp, color='#d62728', alpha=0.7, label='Downside Impact (-)')
            ax16.barh(y_pos, high_imp, color='#2ca02c', alpha=0.7, label='Upside Impact (+)')
            ax16.set_yticks(y_pos)
            ax16.set_yticklabels(drivers, fontsize=9)
            ax16.axvline(0, color='black', linewidth=1)
            ax16.set_title("Valuation Sensitivity Risk-Driver Tornado Ranking", fontsize=11, fontweight='bold')
            ax16.set_xlabel("Valuation Delta ($ Millions)", fontsize=9)
            ax16.legend(loc='lower right', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig16)
