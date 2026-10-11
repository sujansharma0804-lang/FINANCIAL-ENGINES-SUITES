"""
Phase 1, Step 2: LTM Calendarizer & Quarterly Standardizer
==========================================================

Builds Last-Twelve-Months (LTM) revenue and EBITDA for a peer group from
quarterly income statements, so comps are measured on a like-for-like basis
regardless of fiscal year-end.

Design principles
-----------------
* Fail loudly, not silently: a missing line item yields NaN, never a fake 0.
* Integrity checks: exactly four consecutive quarters are required.
* Transparency: every output row records which line item and period it used.
* Honest labelling: EBITDA is only reported as EBITDA. If it must be derived,
  the derivation is flagged in ebitda_basis.

Usage
-----
    python ltm_standardizer.py AAPL MSFT GOOGL
    python ltm_standardizer.py AAPL MSFT --csv ltm.csv -v
"""



import argparse
import logging
import sys
from dataclasses import asdict, dataclass
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd
import yfinance as yf

logger = logging.getLogger("calendarizer")

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
N_QUARTERS = 4
MAX_QUARTER_GAP_DAYS = 120  # ~one quarter plus a tolerance for 52/53-week calendars
UNIT = 1_000_000  # report in millions

REVENUE_LABELS: tuple[str, ...] = ("Total Revenue", "Operating Revenue")
EBITDA_LABELS: tuple[str, ...] = ("EBITDA", "Normalized EBITDA")
OPERATING_INCOME_LABELS: tuple[str, ...] = ("Operating Income", "Total Operating Income As Reported")
DA_LABELS: tuple[str, ...] = (
    "Reconciled Depreciation",
    "Depreciation And Amortization In Income Statement",
    "Depreciation Amortization Depletion",
)


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class LTMResult:
    ticker: str
    currency: Optional[str]
    latest_quarter: pd.Timestamp
    quarters_used: int
    ltm_revenue_mm: float
    ltm_ebitda_mm: float
    ebitda_margin: float
    revenue_basis: str
    ebitda_basis: str


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _prepare_quarters(q_financials: pd.DataFrame) -> pd.DataFrame:
    """Sort columns newest-first and keep the latest N quarters."""
    df = q_financials.copy()
    df.columns = pd.to_datetime(df.columns)
    df = df.sort_index(axis=1, ascending=False)
    return df.iloc[:, :N_QUARTERS]


def _quarters_are_consecutive(columns: pd.DatetimeIndex) -> bool:
    """True if no gap between adjacent period-ends exceeds the tolerance."""
    gaps = -np.diff(columns.values.astype("datetime64[D]").astype(int))
    return bool((gaps <= MAX_QUARTER_GAP_DAYS).all())


def _ltm_sum(quarters: pd.DataFrame, labels: Iterable[str]) -> tuple[float, Optional[str]]:
    """
    Sum the first available line item that has a value in every quarter.
    Returns (NaN, None) if none qualifies, so gaps never masquerade as zeros.
    """
    for label in labels:
        if label in quarters.index:
            row = quarters.loc[label]
            if row.notna().all():
                return float(row.sum()), label
            logger.debug("'%s' has missing quarters; trying next label.", label)
    return float("nan"), None


def _derive_ebitda(quarters: pd.DataFrame) -> tuple[float, str]:
    """Reported EBITDA, else Operating Income + D&A, else NaN."""
    ebitda, label = _ltm_sum(quarters, EBITDA_LABELS)
    if label:
        return ebitda, label

    op_inc, op_label = _ltm_sum(quarters, OPERATING_INCOME_LABELS)
    da, da_label = _ltm_sum(quarters, DA_LABELS)
    if op_label and da_label:
        return op_inc + da, f"Derived: {op_label} + {da_label}"

    return float("nan"), "Unavailable"


def _get_currency(ticker: yf.Ticker) -> Optional[str]:
    try:
        return ticker.get_info().get("financialCurrency")
    except Exception:  # network/schema issues must not break the pipeline
        return None


# --------------------------------------------------------------------------- #
# Core logic
# --------------------------------------------------------------------------- #
def compute_ltm(symbol: str) -> Optional[LTMResult]:
    """Compute LTM metrics for one ticker, or None if data is unusable."""
    symbol = symbol.strip().upper()
    ticker = yf.Ticker(symbol)

    try:
        raw = ticker.quarterly_financials
    except Exception as exc:
        logger.warning("%s: fetch failed (%s)", symbol, exc)
        return None

    if raw is None or raw.empty:
        logger.warning("%s: no quarterly financials returned", symbol)
        return None

    quarters = _prepare_quarters(raw)

    if quarters.shape[1] < N_QUARTERS:
        logger.warning("%s: only %d quarters available (need %d)", symbol, quarters.shape[1], N_QUARTERS)
        return None

    if not _quarters_are_consecutive(quarters.columns):
        logger.warning("%s: quarters are not consecutive; LTM would be distorted", symbol)
        return None

    revenue, rev_label = _ltm_sum(quarters, REVENUE_LABELS)
    ebitda, ebitda_basis = _derive_ebitda(quarters)

    if rev_label is None:
        logger.warning("%s: revenue line item missing or incomplete", symbol)
        return None

    margin = ebitda / revenue if revenue and not np.isnan(ebitda) else float("nan")

    return LTMResult(
        ticker=symbol,
        currency=_get_currency(ticker),
        latest_quarter=quarters.columns[0],
        quarters_used=quarters.shape[1],
        ltm_revenue_mm=revenue / UNIT,
        ltm_ebitda_mm=ebitda / UNIT if not np.isnan(ebitda) else float("nan"),
        ebitda_margin=margin,
        revenue_basis=rev_label,
        ebitda_basis=ebitda_basis,
    )


def calculate_ltm_financials(ticker_symbols: Sequence[str]) -> pd.DataFrame:
    """Return a DataFrame (one row per ticker) of standardized LTM figures."""
    results = [r for s in ticker_symbols if (r := compute_ltm(s)) is not None]
    if not results:
        return pd.DataFrame()
    return pd.DataFrame([asdict(r) for r in results]).set_index("ticker")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Standardized LTM revenue & EBITDA for a peer group.")
    p.add_argument("tickers", nargs="*", default=["AAPL", "MSFT", "GOOGL"], help="Ticker symbols")
    p.add_argument("--csv", metavar="PATH", help="Also write results to CSV")
    p.add_argument("-v", "--verbose", action="store_true", help="Debug logging")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s | %(message)s",
    )

    df = calculate_ltm_financials(args.tickers)
    if df.empty:
        print("No usable LTM data was produced.", file=sys.stderr)
        return 1

    display = df.copy()
    display["ebitda_margin"] = display["ebitda_margin"].map(lambda x: f"{x:.1%}" if pd.notna(x) else "n/a")
    display["latest_quarter"] = display["latest_quarter"].dt.strftime("%Y-%m-%d")

    print("--- STANDARDIZED LTM FINANCIALS (millions, reporting currency) ---")
    print(display.to_string(float_format=lambda v: f"{v:,.1f}"))

    if args.csv:
        df.to_csv(args.csv)
        print(f"\nSaved to {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())