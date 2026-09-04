"""MCP server entry point: exposes market-data tools over stdio.

Run directly with `uv run stock-mcp-server` (see pyproject.toml), or let
`NewStartup.mcp_server_params` in crew.py launch it as a subprocess.

This module only wires tool functions to the MCP protocol; the actual data
fetching/calculation lives in market_data.py.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from new_startup.mcp_server import market_data

mcp = FastMCP("stock-market-data")


@mcp.tool()
def search_symbols(query: str) -> dict[str, Any]:
    """Search/resolve public stock ticker symbols and company identities.

    Args:
        query: Company name or partial ticker to search for (e.g. "Apple").

    Returns:
        Matching ticker symbols with company name, exchange, and sector/
        industry when available.
    """
    return market_data.search_symbols(query)


@mcp.tool()
def get_quote(symbol: str) -> dict[str, Any]:
    """Get current/recent market quote data for a ticker symbol.

    Args:
        symbol: Ticker symbol, e.g. "AAPL".

    Returns:
        Price, change/percent change, open/high/low/previous close, volume,
        and a timestamp, when available from the data source.
    """
    return market_data.get_quote(symbol)


@mcp.tool()
def get_indicators(symbol: str, period: str = "6mo") -> dict[str, Any]:
    """Get technical indicators for a ticker, calculated from real price history.

    Args:
        symbol: Ticker symbol, e.g. "AAPL".
        period: Historical lookback window, e.g. "3mo", "6mo", "1y".

    Returns:
        Moving averages (SMA20/SMA50), RSI(14), and MACD(12,26,9), along with
        the 52-week high/low observed in the requested window.
    """
    return market_data.get_indicators(symbol, period)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
