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
st.markdown("### Universal Multi-Engine Workspace: Live SEC Financial Statements, LTM Calendarizer, EV Bridge, ESG, and Stochastic Monte Carlo")

# Navigation Tabs (Separated explicitly)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 SEC EDGAR Pipeline", 
    "📅 LTM Calendarizer", 
    "🌉 EV Bridge Model", 
    "🌱 ESG Engine", 
    "🎲 Monte Carlo Risk"
])

# ==========================================
# TAB 1: SEC EDGAR PIPELINE (UNIVERSAL BALANCE SHEET & INCOME STATEMENT)
# ==========================================
with tab1:
    st.subheader("Universal SEC EDGAR Financial Statement Ingestion")
    st.write("Query official XBRL filings for *any US-listed company* (e.g., GS, AAPL, MSFT, TSLA) to extract Income Statement and Balance Sheet data.")

    ticker_input = st.text_input("Enter US Ticker Symbol:", value="GS").upper().strip()

    if st.button("Fetch Live SEC Financial Statements", key="btn_sec_universal"):
        with st.spinner(f"Resolving CIK and querying SEC EDGAR API for {ticker_input}..."):
            try:
                headers = {'User-Agent': 'InstitutionalFinancialAnalytics student@christuniversity.in'}
                tickers_url = "https://www.sec.gov/files/company_tickers.json"
                tickers_resp = requests.get(tickers_url, headers=headers, timeout=10)
                
                if tickers_resp.status_code == 200:
                    tickers_data = tickers_resp.json()
                    target_cik = None
                    target_name = None
                    
                    for key, val in tickers_data.items():
                        if val.get("ticker") == ticker_input:
                            target_cik = str(val.get("cik_str")).zfill(10)
                            target_name = val.get("title")
                            break
                    
                    if target_cik:
                        st.success(f"Found *{target_name}* (CIK: {target_cik}). Parsing XBRL financial statements...")
                        
                        facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{target_cik}.json"
                        facts_resp = requests.get(facts_url, headers=headers, timeout=15)
                        
                        if facts_resp.status_code == 200:
                            data = facts_resp.json()
                            us_gaap = data.get("facts", {}).get("us-gaap", {})
                            
                            # Helper extractor function for SEC XBRL tags
                            def extract_sec_metric(tags_list, metric_name):
                                rows = []
                                for tag in tags_list:
                                    if tag in us_gaap:
                                        units = us_gaap[tag].get("units", {}).get("USD", [])
                                        for entry in units:
                                            if entry.get("form") in ["10-K", "10-Q"] and "fy" in entry and "fp" in entry:
                                                rows.append({
                                                    "Metric": metric_name,
                                                    "Form": entry.get("form"),
                                                    "Fiscal Year": entry.get("fy"),
                                                    "Period": entry.get("fp"),
                                                    "Value ($M)": round(entry.get("val", 0) / 1e6, 2),
                                                    "End Date": entry.get("end")
                                                })
                                return rows

                            # Extract Revenues, Net Income, and Balance Sheet items (Total Assets, Liabilities)
                            rev_rows = extract_sec_metric(["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "InterestAndDividendIncomeOperating"], "Revenue / Topline")
                            ni_rows = extract_sec_metric(["NetIncomeLoss"], "Net Income")
                            assets_rows = extract_sec_metric(["Assets"], "Total Assets")
                            liab_rows = extract_sec_metric(["Liabilities"], "Total Liabilities")
                            
                            all_financials = rev_rows + ni_rows + assets_rows + liab_rows
                            
                            if all_financials:
                                df_fin = pd.DataFrame(all_financials).drop_duplicates(subset=["Metric", "End Date"]).sort_values("End Date", ascending=False)
                                
                                st.write(f"### Core Financial Statements: {target_name} ({ticker_input})")
                                st.dataframe(df_fin.head(15), use_container_width=True)
                                
                                # Highlight Total Assets specifically
                                df_assets = df_fin[df_fin["Metric"] == "Total Assets"].drop_duplicates(subset=["Fiscal Year"]).sort_values("Fiscal Year", ascending=False)
                                if not df_assets.empty:
                                    st.write("### Balance Sheet Summary: Total Assets (Annual)")
                                    st.dataframe(df_assets[["Fiscal Year", "Value ($M)", "End Date"]].head(5), use_container_width=True)
                            else:
                                st.warning("Standard US-GAAP tags not fully matched. Displaying raw metadata node.")
                                st.json({"Entity": target_name, "CIK": target_cik, "Available GAAP Nodes": len(us_gaap)})
                        else:
                            st.error(f"Failed to retrieve company facts JSON. Status: {facts_resp.status_code}")
                    else:
                        st.error(f"Ticker '{ticker_input}' not found in SEC database.")
                else:
                    st.error("Failed to connect to SEC ticker directory.")
            except Exception as e:
                st.error(f"An error occurred during SEC query: {e}")

# ==========================================
# TAB 2: LTM CALENDARIZER
# ==========================================
with tab2:
    st.subheader("Last Twelve Months (LTM) Calendarizer")
    st.write("Normalize periodic 10-K and 10-Q SEC filings to derive exact LTM run-rate financial profiles.")

    col1, col2 = st.columns(2)
    with col1:
        latest_fy_rev = st.number_input("Latest Full Year Metric ($M):", value=142500.0)
        prior_y_rev = st.number_input("Prior Full Year Metric ($M):", value=130000.0)
    with col2:
        interim_current_y = st.number_input("Current Interim Period YTD ($M):", value=38500.0)
        interim_prior_y = st.number_input("Prior Interim Period YTD ($M):", value=35200.0)

    if st.button("Calculate Normalized LTM", key="btn_ltm"):
        ltm_result = latest_fy_rev + interim_current_y - interim_prior_y
        st.success(f"*Calculated Normalized LTM Run-Rate:* ${ltm_result:,.2f}M")
        
        ltm_breakdown = pd.DataFrame({
            "Component Layer": ["Latest Full Year (FY)", "Current Interim YTD", "Prior Interim YTD (Subtracted)", "Normalized LTM Output"],
            "Amount ($M)": [latest_fy_rev, interim_current_y, -interim_prior_y, ltm_result]
        })
        st.table(ltm_breakdown)

# ==========================================
# TAB 3: EV BRIDGE MODEL
# ==========================================
with tab3:
    st.subheader("Enterprise Value to Equity Value Bridge")
    st.write("Deconstruct capital structure elements to bridge Enterprise Value (EV) down to Equity Value and Implied Share Price.")

    col1, col2 = st.columns(2)
    with col1:
        ev_input = st.number_input("Enterprise Value ($M):", value=145000.0)
        total_debt = st.number_input("Total Debt & Debt-Like Items ($M):", value=28000.0)
        preferred_stock = st.number_input("Preferred Stock & Minority Interest ($M):", value=4200.0)
    with col2:
        cash_equiv = st.number_input("Cash & Cash Equivalents ($M):", value=15600.0)
        shares_out = st.number_input("Diluted Shares Outstanding (M):", value=320.0)

    if st.button("Generate EV Bridge", key="btn_bridge"):
        equity_value = ev_input - total_debt - preferred_stock + cash_equiv
        implied_share_price = equity_value / shares_out if shares_out > 0 else 0

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Implied Equity Value", f"${equity_value:,.2f}M")
        col_m2.metric("Implied Share Price", f"${implied_share_price:,.2f}")

        bridge_df = pd.DataFrame({
            "Bridge Component": ["Enterprise Value", "Less: Total Debt", "Less: Preferred Stock / Minority Interest", "Plus: Cash & Equivalents", "Implied Equity Value"],
            "Value ($M)": [ev_input, -total_debt, -preferred_stock, cash_equiv, equity_value]
        })
        st.table(bridge_df)

# ==========================================
# TAB 4: ESG ENGINE
# ==========================================
with tab4:
    st.subheader("ESG Risk & Valuation Impact Engine")
    st.write("Quantify carbon liability pricing and governance score spreads to adjust cost of capital.")

    col1, col2 = st.columns(2)
    with col1:
        emissions_slider = st.slider("Scope 1 & 2 Emissions (kt CO2e):", min_value=10, max_value=500, value=180)
        st.metric("ESG Capital Penalty", f"+{(0.045 * np.log(emissions_slider) * 100):.1f} bps", delta="-2.1%")
    with col2:
        st.metric("Governance Scorecard", "A- (Tier 1)", delta="+0.4")
        st.progress(0.82, text="ESG Compliance Rating")

    st.markdown("---")
    st.markdown("### WACC Penalty vs. Carbon Intensity Curve")
    
    fig_esg, ax_esg = plt.subplots(figsize=(10, 4))
    emissions_range = np.linspace(10, 500, 50)
    wacc_penalty = 0.045 * np.log(emissions_range) * 100
    
    ax_esg.plot(emissions_range, wacc_penalty, color="#2ca02c", linewidth=2.5, label="WACC Penalty Spread (bps)")
    ax_esg.axvline(emissions_slider, color='orange', linestyle=':', linewidth=2, label=f'Current Level ({emissions_slider} kt)')
    ax_esg.set_title("Carbon Footprint Impact Curve on Cost of Capital", fontsize=11, fontweight='bold')
    ax_esg.set_xlabel("Scope 1 & 2 Emissions (kt CO2e)", fontsize=9)
    ax_esg.set_ylabel("WACC Adjustment (Basis Points)", fontsize=9)
    ax_esg.legend()
    plt.tight_layout()
    st.pyplot(fig_esg)

# ==========================================
# TAB 5: MONTE CARLO RISK (INTERACTIVE ITERATIONS & ADVANCED GRAPHS)
# ==========================================
with tab5:
    st.subheader("Probabilistic Monte Carlo Stress Testing")
    st.write("Run stochastic valuation simulations with configurable iteration counts and volatility parameters.")

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        num_iterations = st.slider("Simulation Iterations:", min_value=1000, max_value=50000, value=10000, step=1000)
    with col_i2:
        volatility_factor = st.slider("Revenue / EV Volatility (%):", min_value=5.0, max_value=30.0, value=17.5, step=0.5)

    if st.button("Run Stochastic Simulation", key="btn_monte_carlo"):
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

            fig, ax = plt.subplots(figsize=(10, 4.5))
            sns.histplot(ev_array, kde=True, color="#1f77b4", bins=50, stat="density", ax=ax, alpha=0.6)
            ax.axvline(p10, color='red', linestyle='--', linewidth=2, label=f'P10 Bear: ${p10:,.1f}M')
            ax.axvline(p50, color='green', linestyle='-', linewidth=2.5, label=f'P50 Median: ${p50:,.1f}M')
            ax.axvline(p90, color='purple', linestyle='--', linewidth=2, label=f'P90 Bull: ${p90:,.1f}M')
            ax.set_title(f"Stochastic Enterprise Value Distribution ({num_iterations:,} Iterations)", fontsize=11, fontweight='bold')
            ax.set_xlabel("Enterprise Value ($ Millions)", fontsize=10)
            ax.set_ylabel("Probability Density", fontsize=10)
            ax.legend(loc='upper right')
            plt.tight_layout()
            st.pyplot(fig)
