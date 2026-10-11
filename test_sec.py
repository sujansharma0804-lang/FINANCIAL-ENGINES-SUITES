import requests

def fetch_sec_data(ticker: str) -> dict:
    """
    Fetches real XBRL financial facts and CIK metadata directly from the official SEC EDGAR API.
    """
    ticker = ticker.strip().upper()
    
    # Mandatory SEC-compliant User-Agent header (AppName Email)
    headers = {
        "User-Agent": "FinancialAnalyticsApp analyst@institutional-suite.com"
    }
    
    # 1. Fetch SEC ticker mapping JSON to resolve CIK
    mapping_url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(mapping_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"SEC API returned status code {response.status_code}")
        
    tickers_data = response.json()
    
    cik_str = None
    title = None
    for item in tickers_data.values():
        if item.get("ticker") == ticker:
            cik_str = str(item.get("cik_str")).zfill(10)
            title = item.get("title")
            break
            
    if not cik_str:
        raise Exception(f"Ticker '{ticker}' not found in SEC directory.")
        
    # 2. Fetch Company Facts (XBRL Data) using the resolved CIK
    facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_str}.json"
    facts_response = requests.get(facts_url, headers=headers)
    
    if facts_response.status_code != 200:
        raise Exception(f"Failed to fetch facts for CIK {cik_str}")
        
    facts_data = facts_response.json()
    
    # 3. Extract core US-GAAP metrics (e.g., Total Assets)
    us_gaap = facts_data.get("facts", {}).get("us-gaap", {})
    
    assets = "N/A"
    if "Assets" in us_gaap:
        units = us_gaap["Assets"].get("units", {})
        usd_units = units.get("USD", [])
        if usd_units:
            latest_val = usd_units[-1].get('val')
            assets = f"${latest_val:,.0f}"

    return {
        "Company Name": title,
        "Ticker": ticker,
        "CIK": cik_str,
        "Entity Name": facts_data.get("entityName"),
        "Total Assets (Latest Filing)": assets,
        "SEC Directory Endpoint": facts_url
    }