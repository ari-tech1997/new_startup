"""Market-data lookups backing the MCP tools.

Uses `yfinance` (a wrapper around Yahoo Finance's public, no-API-key
endpoints) so the project stays runnable without paid infrastructure or
secrets. Every function returns a plain, JSON-serializable dict and never
raises: bad symbols and upstream/network failures are caught and reported
back as {"error": "..."} so a single failed lookup can't crash the crew.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd
import yfinance as yf


def _round(value: Any, digits: int = 2) -> float | None:
    """Round a numeric value, passing through None/NaN as None."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return round(float(value), digits)


def search_symbols(query: str, max_results: int = 5) -> dict[str, Any]:
    """Resolve a company name or partial ticker into candidate stock symbols.

    Args:
        query: Company name or ticker text to search for.
        max_results: Maximum number of matches to return.

    Returns:
        {"query": ..., "results": [{"symbol", "name", "exchange", "type",
        "sector", "industry"}, ...]} or {"query": ..., "error": ...}.
    """
    query = (query or "").strip()
    if not query:
        return {"query": query, "error": "A non-empty search query is required."}

    try:
        search = yf.Search(query, max_results=max_results)
        quotes = search.quotes or []
    except Exception as exc:  # noqa: BLE001 - upstream lookup, never crash the crew
        return {"query": query, "error": f"Symbol search failed: {exc}"}

    results = [
        {
            "symbol": q.get("symbol"),
            "name": q.get("longname") or q.get("shortname"),
            "exchange": q.get("exchDisp") or q.get("exchange"),
            "type": q.get("typeDisp") or q.get("quoteType"),
            "sector": q.get("sector"),
            "industry": q.get("industry"),
        }
        for q in quotes
        if q.get("symbol")
    ]

    if not results:
        return {"query": query, "results": [], "error": "No matching symbols found."}

    return {"query": query, "results": results}


def get_quote(symbol: str) -> dict[str, Any]:
    """Retrieve current/recent market quote data for a ticker.

    Args:
        symbol: Ticker symbol, e.g. "AAPL".

    Returns:
        A structured quote dict, or {"symbol": ..., "error": ...} if the
        symbol is invalid or upstream data is unavailable.
    """
    symbol = (symbol or "").strip().upper()
    if not symbol:
        return {"symbol": symbol, "error": "A ticker symbol is required."}

    try:
        info = yf.Ticker(symbol).fast_info
        price = info.get("lastPrice")
    except Exception as exc:  # noqa: BLE001
        return {"symbol": symbol, "error": f"Could not retrieve quote: {exc}"}

    if price is None:
        return {"symbol": symbol, "error": f"'{symbol}' does not look like a valid ticker."}

    previous_close = info.get("previousClose")
    change = price - previous_close if previous_close else None
    percent_change = (change / previous_close * 100) if change is not None and previous_close else None

    return {
        "symbol": symbol,
        "price": _round(price),
        "previous_close": _round(previous_close),
        "change": _round(change),
        "percent_change": _round(percent_change),
        "open": _round(info.get("open")),
        "day_high": _round(info.get("dayHigh")),
        "day_low": _round(info.get("dayLow")),
        "year_high": _round(info.get("yearHigh")),
        "year_low": _round(info.get("yearLow")),
        "volume": info.get("lastVolume"),
        "market_cap": info.get("marketCap"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "Yahoo Finance (via yfinance)",
    }


def get_indicators(symbol: str, period: str = "6mo") -> dict[str, Any]:
    """Retrieve/calculate technical indicators for a ticker from price history.

    Args:
        symbol: Ticker symbol, e.g. "AAPL".
        period: Lookback window for the underlying price history
            (e.g. "3mo", "6mo", "1y"). Defaults to "6mo".

    Returns:
        A dict of indicator values computed from real historical prices, or
        {"symbol": ..., "error": ...} if the symbol/data is unavailable.
    """
    symbol = (symbol or "").strip().upper()
    if not symbol:
        return {"symbol": symbol, "error": "A ticker symbol is required."}

    try:
        history = yf.Ticker(symbol).history(period=period)
    except Exception as exc:  # noqa: BLE001
        return {"symbol": symbol, "error": f"Could not retrieve price history: {exc}"}

    if history.empty:
        return {"symbol": symbol, "error": f"No price history found for '{symbol}'."}

    close = history["Close"].dropna()
    if len(close) < 15:
        return {
            "symbol": symbol,
            "error": f"Not enough price history ({len(close)} days) to compute indicators.",
        }

    # Simple/exponential moving averages
    sma_20 = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
    sma_50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None

    # RSI(14), Wilder-style
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi_14 = (100 - (100 / (1 + rs))).iloc[-1]

    # MACD(12, 26, 9)
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "symbol": symbol,
        "period": period,
        "data_points": len(close),
        "last_close": _round(close.iloc[-1]),
        "last_date": close.index[-1].date().isoformat(),
        "sma_20": _round(sma_20),
        "sma_50": _round(sma_50),
        "rsi_14": _round(rsi_14),
        "macd": {
            "macd": _round(macd_line.iloc[-1]),
            "signal": _round(signal_line.iloc[-1]),
            "histogram": _round(histogram.iloc[-1]),
        },
        "52_week_high": _round(close.max()),
        "52_week_low": _round(close.min()),
        "source": "Yahoo Finance (via yfinance)",
    }
