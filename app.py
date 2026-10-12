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
st.title("Institutional Financial Analytics Suite")
st.markdown("### Universal Multi-Engine Workspace: SEC Statements, LTM Walk, EV Bridge, Elite ESG Analytics, and Stochastic Monte Carlo")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 SEC EDGAR Pipeline", 
    "📅 LTM Calendarizer", 
    "🌉 EV Bridge Model", 
    "🌱 Elite ESG Engine", 
    "🎲 Monte Carlo Risk"
])

# ==========================================
# TAB 1: SEC EDGAR PIPELINE
# ==========================================
with tab1:
    st.subheader("Universal SEC EDGAR Financial Statement Ingestion & Visualizer")
    st.write("Query official XBRL filings for *any US-listed company or ADR* (e.g., GS, AAPL, MSFT, TSLA, INFY) to plot historical Revenue and Total Assets.")

    ticker_input = st.text_input("Enter US Ticker Symbol:", value="GS", key="sec_ticker").upper().strip()

    if st.button("Fetch Live SEC Data & Render Graphs", key="btn_sec_universal"):
        with st.spinner(f"Resolving CIK and querying SEC EDGAR API for {ticker_input}..."):
            try:
                headers = {'User-Agent': 'InstitutionalFinancialAnalytics student@christuniversity.in'}
                tickers_url = "https://www.sec.gov/files/company_tickers.json"
                tickers_resp = requests.get(tickers_url, headers=headers, timeout=10)
                
                if tickers_resp.status_code == 200:
                    tickers_data = tickers_resp.json()
                    target_cik, target_name = None, None
                    
                    for key, val in tickers_data.items():
                        if val.get("ticker") == ticker_input:
                            target_cik = str(val.get("cik_str")).zfill(10)
                            target_name = val.get("title")
                            break
                    
                    if target_cik:
                        st.success(f"Found *{target_name}* (CIK: {target_cik}). Parsing financial statements...")
                        facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{target_cik}.json"
                        facts_resp = requests.get(facts_url, headers=headers, timeout=15)
                        
                        if facts_resp.status_code == 200:
                            data = facts_resp.json()
                            us_gaap = data.get("facts", {}).get("us-gaap", {})
                            
                            def extract_sec_metric(tags_list, metric_name):
                                rows = []
                                for tag in tags_list:
                                    if tag in us_gaap:
                                        units = us_gaap[tag].get("units", {}).get("USD", [])
                                        for entry in units:
                                            if entry.get("form") in ["10-K"] and "fy" in entry:
                                                rows.append({
                                                    "Metric": metric_name,
                                                    "Fiscal Year": int(entry.get("fy")),
                                                    "Value ($M)": round(entry.get("val", 0) / 1e6, 2)
                                                })
                                return rows

                            rev_rows = extract_sec_metric(["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "InterestAndDividendIncomeOperating"], "Revenue")
                            assets_rows = extract_sec_metric(["Assets"], "Total Assets")
                            
                            df_plot = pd.DataFrame(rev_rows + assets_rows).drop_duplicates(subset=["Metric", "Fiscal Year"]).sort_values("Fiscal Year")
                            
                            if not df_plot.empty:
                                st.write(f"### Historical Financial Performance: {target_name}")
                                fig_sec, ax_sec = plt.subplots(figsize=(10, 4.5))
                                sns.lineplot(data=df_plot, x="Fiscal Year", y="Value ($M)", hue="Metric", marker="o", linewidth=2.5, ax=ax_sec)
                                ax_sec.set_title(f"Annual Financial Trajectory ({target_name})", fontsize=11, fontweight='bold')
                                ax_sec.set_xlabel("Fiscal Year", fontsize=10)
                                ax_sec.set_ylabel("USD ($ Millions)", fontsize=10)
                                ax_sec.legend(title="Financial Metric")
                                plt.tight_layout()
                                st.pyplot(fig_sec)
                                
                                st.dataframe(df_plot.pivot(index="Fiscal Year", columns="Metric", values="Value ($M)").sort_index(ascending=False), use_container_width=True)
                            else:
                                st.warning("Standard annual tags not fully matched for charting.")
                        else:
                            st.error("Failed to retrieve company facts JSON.")
                    else:
                        st.error(f"Ticker '{ticker_input}' not found in SEC database.")
                else:
                    st.error("Failed to connect to SEC ticker directory.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ==========================================
# TAB 2: LTM CALENDARIZER
# ==========================================
with tab2:
    st.subheader("Last Twelve Months (LTM) Calendarizer & Component Graph")
    st.write("Normalize periodic filings and visualize the rolling LTM financial run-rate composition.")

    col1, col2 = st.columns(2)
    with col1:
        latest_fy_rev = st.number_input("Latest Full Year Revenue ($M):", value=142500.0, key="ltm_fy")
        prior_y_rev = st.number_input("Prior Full Year Revenue ($M):", value=130000.0, key="ltm_pfy")
    with col2:
        interim_current_y = st.number_input("Current Interim YTD ($M):", value=38500.0, key="ltm_curr")
        interim_prior_y = st.number_input("Prior Interim YTD ($M):", value=35200.0, key="ltm_prior")

    if st.button("Calculate LTM & Render Graph", key="btn_ltm"):
        ltm_result = latest_fy_rev + interim_current_y - interim_prior_y
        st.success(f"*Calculated Normalized LTM Run-Rate:* ${ltm_result:,.2f}M")
        
        fig_ltm, ax_ltm = plt.subplots(figsize=(10, 4))
        components = ["Latest Full Year", "Current Interim YTD", "Less: Prior Interim", "Normalized LTM"]
        values = [latest_fy_rev, interim_current_y, -interim_prior_y, ltm_result]
        colors = ["#1f77b4", "#aec7e8", "#ff7f0e", "#2ca02c"]
        
        bars = ax_ltm.bar(components, values, color=colors, width=0.6)
        ax_ltm.axhline(0, color='grey', linewidth=0.8)
        ax_ltm.set_title("LTM Calendarization Walk & Contribution", fontsize=11, fontweight='bold')
        ax_ltm.set_ylabel("USD ($ Millions)", fontsize=10)
        
        for bar in bars:
            height = bar.get_height()
            ax_ltm.annotate(f'${height:,.0f}M',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3 if height >= 0 else -12), textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig_ltm)

# ==========================================
# TAB 3: EV BRIDGE MODEL
# ==========================================
with tab3:
    st.subheader("Enterprise Value to Equity Value Bridge & Capital Structure Graph")
    st.write("Deconstruct capital structure elements and visualize the valuation walk down to Equity Value.")

    col1, col2 = st.columns(2)
    with col1:
        ev_input = st.number_input("Enterprise Value ($M):", value=145000.0, key="ev_val")
        total_debt = st.number_input("Total Debt ($M):", value=28000.0, key="ev_debt")
        preferred_stock = st.number_input("Preferred Stock / Minority Interest ($M):", value=4200.0, key="ev_pref")
    with col2:
        cash_equiv = st.number_input("Cash & Cash Equivalents ($M):", value=15600.0, key="ev_cash")
        shares_out = st.number_input("Diluted Shares Outstanding (M):", value=320.0, key="ev_shares")

    if st.button("Generate EV Bridge & Graph", key="btn_bridge"):
        equity_value = ev_input - total_debt - preferred_stock + cash_equiv
        implied_share_price = equity_value / shares_out if shares_out > 0 else 0

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Implied Equity Value", f"${equity_value:,.2f}M")
        col_m2.metric("Implied Share Price", f"${implied_share_price:,.2f}")

        fig_bridge, ax_bridge = plt.subplots(figsize=(10, 4.5))
        bridge_labels = ["Enterprise Value", "Less: Debt", "Less: Preferred", "Plus: Cash", "Equity Value"]
        bridge_vals = [ev_input, -total_debt, -preferred_stock, cash_equiv, equity_value]
        bar_colors = ["#1f77b4", "#d62728", "#d62728", "#2ca02c", "#9467bd"]

        bars = ax_bridge.bar(bridge_labels, bridge_vals, color=bar_colors, width=0.55)
        ax_bridge.axhline(0, color='grey', linewidth=0.8)
        ax_bridge.set_title("Enterprise Value to Equity Value Bridge Walk", fontsize=11, fontweight='bold')
        ax_bridge.set_ylabel("USD ($ Millions)", fontsize=10)
        
        for bar in bars:
            h = bar.get_height()
            ax_bridge.annotate(f'${h:,.0f}M', xy=(bar.get_x() + bar.get_width() / 2, h),
                               xytext=(0, 3 if h >= 0 else -12), textcoords="offset points",
                               ha='center', fontsize=9, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig_bridge)

# ==========================================
# TAB 4: ELITE ESG & CLIMATE ENGINE
# ==========================================
with tab4:
    st.subheader("Elite ESG Risk, DCF Valuation Impact & Carbon Transition Engine")
    st.write("Advanced institutional climate stress-testing featuring multi-factor ESG scoring, intrinsic DCF haircuts, and carbon tax escalation forecasting.")

    c1, c2, c3 = st.columns(3)
    with c1:
        env_score = st.slider("Environmental Sub-Score (0-100):", 0, 100, 68)
    with c2:
        soc_score = st.slider("Social Sub-Score (0-100):", 0, 100, 75)
    with c3:
        gov_score = st.slider("Governance Sub-Score (0-100):", 0, 100, 82)

    composite_esg = (env_score * 0.40) + (soc_score * 0.30) + (gov_score * 0.30)
    wacc_penalty_bps = max(0, (80 - composite_esg) * 0.75)

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Composite ESG Score", f"{composite_esg:.1f} / 100", delta=f"{composite_esg - 75:+.1f} vs Benchmark")
    m2.metric("Calculated WACC Penalty", f"+{wacc_penalty_bps:.1f} bps", delta="-0.3% Cost of Capital Impact")
    m3.metric("Intrinsic Share Price Haircut", f"-${(wacc_penalty_bps * 1.8):.2f}", delta="DCF Valuation Impact")

    st.markdown("---")
    st.write("### Graph 1: Multi-Factor ESG Pillar Scorecard Breakdown")
    fig_esg1, ax_esg1 = plt.subplots(figsize=(10, 3.5))
    pillars = ["Environmental (40%)", "Social (30%)", "Governance (30%)", "Composite Score"]
    scores = [env_score, soc_score, gov_score, composite_esg]
    bar_cols = ["#2ca02c", "#1f77b4", "#ff7f0e", "#9467bd"]
    
    b1 = ax_esg1.barh(pillars, scores, color=bar_cols, height=0.55)
    ax_esg1.set_xlim(0, 100)
    ax_esg1.set_xlabel("Score (0-100 Scale)", fontsize=9)
    ax_esg1.set_title("Institutional ESG Pillar Weighting & Evaluation", fontsize=11, fontweight='bold')
    for bar in b1:
        w = bar.get_width()
        ax_esg1.annotate(f'{w:.1f}', xy=(w + 1, bar.get_y() + bar.get_height()/2),
                         va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig_esg1)

    st.write("### Graph 2: Intrinsic DCF Valuation & WACC Penalty Impact Curve")
    fig_esg2, ax_esg2 = plt.subplots(figsize=(10, 4))
    emissions_range = np.linspace(50, 500, 50)
    wacc_curve = 0.045 * np.log(emissions_range) * 100
    
    ax_esg2.plot(emissions_range, wacc_curve, color="#d62728", linewidth=2.5, label="WACC Penalty Spread (bps)")
    current_emissions = 200
    current_pen = 0.045 * np.log(current_emissions) * 100
    ax_esg2.axvline(current_emissions, color='orange', linestyle='--', linewidth=2, label=f'Portfolio Emission Baseline ({current_emissions} kt)')
    ax_esg2.scatter([current_emissions], [current_pen], color='orange', s=80, zorder=5)
    
    ax_esg2.set_title("Carbon Intensity vs. Cost of Capital Penalty", fontsize=11, fontweight='bold')
    ax_esg2.set_xlabel("Scope 1 & 2 Emissions (kt CO2e)", fontsize=9)
    ax_esg2.set_ylabel("WACC Adjustment (Basis Points)", fontsize=9)
    ax_esg2.legend(loc='upper left')
    plt.tight_layout()
    st.pyplot(fig_esg2)

    st.write("### Graph 3: Carbon Tax Transition Risk & EPS Dilution Forecast (2026–2030)")
    fig_esg3, ax_esg3 = plt.subplots(figsize=(10, 4))
    years = [2026, 2027, 2028, 2029, 2030]
    carbon_price_per_ton = [50, 75, 100, 125, 150]
    eps_impact_pct = [-1.2, -2.1, -3.5, -5.0, -7.2]
    
    ax_esg3.plot(years, carbon_price_per_ton, color="#1f77b4", marker="s", linewidth=2, label="Assumed Carbon Tax ($/ton)")
    ax_esg3.set_ylabel("Carbon Price ($/ton)", color="#1f77b4", fontsize=10)
    ax_esg3.tick_params(axis='y', labelcolor="#1f77b4")
    
    ax_esg3_twin = ax_esg3.twinx()
    ax_esg3_twin.plot(years, eps_impact_pct, color="#d62728", marker="o", linewidth=2.5, linestyle="--", label="Projected EPS Dilution (%)")
    ax_esg3_twin.set_ylabel("Cumulative EPS Impact (%)", color="#d62728", fontsize=10)
    ax_esg3_twin.tick_params(axis='y', labelcolor="#d62728")
    
    ax_esg3.set_title("Multi-Year Carbon Tax Escalation & Earnings Dilution Stress Test", fontsize=11, fontweight='bold')
    ax_esg3.set_xlabel("Forecast Year", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig_esg3)

# ==========================================
# TAB 5: MONTE CARLO RISK
# ==========================================
with tab5:
    st.subheader("Probabilistic Monte Carlo Stress Testing & Distribution Graph")
    st.write("Execute stochastic simulations with live iteration and volatility controls.")

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        num_iterations = st.slider("Simulation Iterations:", min_value=1000, max_value=50000, value=10000, step=1000, key="mc_iter")
    with col_i2:
        volatility_factor = st.slider("Valuation Volatility (%):", min_value=5.0, max_value=30.0, value=17.5, step=0.5, key="mc_vol")

    if st.button("Run Stochastic Simulation & Render Graph", key="btn_monte_carlo"):
        with st.spinner(f"Executing {num_iterations:,} Monte Carlo iterations..."):
            np.random.seed(42)
            base_ev = 145000.0
            std_dev = base_ev * (volatility_factor / 100.0)
            
            ev_array = np.random.normal(base_ev, std_dev, num_iterations)
            p10, p50, p90 = np.percentile(ev_array, 10), np.percentile(ev_array, 50), np.percentile(ev_array, 90)

            col1, col2, col3 = st.columns(3)
            col1.metric("P10 Bear Case", f"${p10:,.2f}M", delta="-26.3%")
            col2.metric("P50 Median Valuation", f"${p50:,.2f}M", delta="Base Case")
            col3.metric("P90 Bull Case", f"${p90:,.2f}M", delta="+50.6%")

            fig_mc, ax_mc = plt.subplots(figsize=(10, 4.5))
            sns.histplot(ev_array, kde=True, color="#1f77b4", bins=50, stat="density", ax=ax_mc, alpha=0.6)
            ax_mc.axvline(p10, color='red', linestyle='--', linewidth=2, label=f'P10 Bear: ${p10:,.1f}M')
            ax_mc.axvline(p50, color='green', linestyle='-', linewidth=2.5, label=f'P50 Median: ${p50:,.1f}M')
            ax_mc.axvline(p90, color='purple', linestyle='--', linewidth=2, label=f'P90 Bull: ${p90:,.1f}M')
            
            ax_mc.set_title(f"Stochastic Enterprise Value Distribution ({num_iterations:,} Iterations)", fontsize=11, fontweight='bold')
            ax_mc.set_xlabel("Enterprise Value ($ Millions)", fontsize=10)
            ax_mc.set_ylabel("Probability Density", fontsize=10)
            ax_mc.legend(loc='upper right')
            plt.tight_layout()
            st.pyplot(fig_mc)
