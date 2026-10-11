import yfinance as yf
import pandas as pd


def _safe_get(df, labels, default=0):
    """Try multiple possible row labels — yfinance's naming is inconsistent across tickers."""
    if df is None or df.empty:
        return default
    for label in labels:
        if label in df.index:
            val = df.loc[label].iloc[0]
            if pd.notna(val):
                return float(val)
    return default


def calculate_multi_enterprise_value(ticker_symbols):
    results = {}

    for ticker_symbol in ticker_symbols:
        ticker = yf.Ticker(ticker_symbol)

        try:
            info = ticker.info
        except Exception as e:
            print(f"Warning: could not fetch info for {ticker_symbol}: {e}")
            info = {}

        if not info or info.get('marketCap') is None:
            # yfinance's .info endpoint is occasionally flaky — fast_info is a more
            # stable (though less complete) fallback for price/market cap.
            try:
                fast = ticker.fast_info
                info.setdefault('marketCap', getattr(fast, 'market_cap', 0))
                info.setdefault('currentPrice', getattr(fast, 'last_price', 0))
                info.setdefault('sharesOutstanding', getattr(fast, 'shares', 0))
            except Exception:
                pass

        market_cap = info.get('marketCap', 0) or 0
        shares_out = info.get('sharesOutstanding', 0) or 0
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0)) or 0

        balance_sheet = ticker.balance_sheet

        cash = _safe_get(balance_sheet, [
            'Cash And Cash Equivalents', 'Cash Cash Equivalents And Short Term Investments'
        ])

        total_debt = _safe_get(balance_sheet, ['Total Debt'])
        if total_debt == 0:
            long_term_debt = _safe_get(balance_sheet, ['Long Term Debt'])
            current_debt = _safe_get(balance_sheet, ['Current Debt', 'Short Long Term Debt'])
            total_debt = long_term_debt + current_debt

        minority_interest = _safe_get(balance_sheet, ['Minority Interest'])
        preferred_stock = _safe_get(balance_sheet, ['Preferred Stock'])

        enterprise_value = market_cap + total_debt + preferred_stock + minority_interest - cash
        net_debt = total_debt - cash

        if market_cap == 0:
            print(f"Warning: {ticker_symbol} returned no market cap — check ticker or data source.")

        results[ticker_symbol.upper()] = {
            "Share Price ($)": current_price,
            "Shares Outstanding": shares_out,
            "Market Cap": market_cap,
            "(+) Total Debt": total_debt,
            "(+) Preferred Stock": preferred_stock,
            "(+) Minority Interest": minority_interest,
            "(-) Cash & Equivalents": cash,
            "Net Debt": net_debt,
            "Enterprise Value": enterprise_value,
        }

    return pd.DataFrame(results)


def print_ev_bridge(df):
    """Row-aware formatting: price gets 2 decimals, everything else gets thousands separators."""
    print("--- MULTI-COMPANY ENTERPRISE VALUE BRIDGE ---")
    for row_label in df.index:
        row = df.loc[row_label]
        if "Price" in row_label:
            formatted = row.map(lambda x: f"${x:,.2f}")
        elif "Shares Outstanding" in row_label:
            formatted = row.map(lambda x: f"{x:,.0f}")
        else:
            formatted = row.map(lambda x: f"${x:,.0f}")
        print(f"{row_label:<25}", *[f"{v:>18}" for v in formatted])


if  __name__ == "__main__":
    # Non-financial comps only — swap in your actual deal's peer set here.
    df = calculate_multi_enterprise_value(["AAPL", "MSFT", "GOOGL"])
    print_ev_bridge(df)