---
name: technical
description: How to read quote data and technical indicators (moving averages, RSI, MACD), combine them into one coherent technical view, and report the actual values behind every claim.
metadata:
  version: "1.0"
---

# Technical Analysis Methodology

Use this methodology when analyzing a stock's price behavior.

## 1. Ground every claim in an actual retrieved value

- Call `get_quote` for current price/change/volume context and
  `get_indicators` for moving averages, RSI, and MACD.
- Never state an indicator's value, trend, or signal without having
  actually retrieved it. If a tool call fails or returns an error, say the
  data was unavailable rather than filling in a plausible-sounding number.

## 2. Interpret each indicator on its own terms

- **Price vs. moving averages**: price above SMA20/SMA50 generally
  suggests an uptrend context; below suggests a downtrend context. A
  shorter MA above a longer MA (e.g. SMA20 > SMA50) suggests improving
  short-term momentum relative to the longer trend.
- **RSI(14)**: below ~30 suggests oversold conditions, above ~70 suggests
  overbought conditions; the 30-70 range is neutral. RSI measures momentum,
  not direction - it does not by itself say "buy" or "sell".
- **MACD**: the MACD line crossing above its signal line suggests
  strengthening upward momentum; crossing below suggests weakening
  momentum. The histogram's sign and size show how strong that gap is.

## 3. Never let one indicator "prove" a conclusion

Indicators frequently disagree (e.g. price above its moving averages while
RSI is falling). Do not cherry-pick the one that supports a tidy story.
Instead:

- Note where indicators agree (higher-confidence signal).
- Note where they disagree, and say so explicitly.
- Describe the overall picture in terms of what the data shows, not a
  prediction of what will happen next.

## 4. Combine into a concise technical view

End with a short synthesis that states, in plain terms:

- The prevailing trend (up / down / range-bound) and what evidence
  supports it.
- The momentum picture (strengthening, weakening, neutral).
- Any notable caveats (e.g. thin data history, conflicting signals).

## 5. Report actual values

Always include the concrete numbers you used (price, SMA20, SMA50, RSI14,
MACD/signal/histogram) alongside your interpretation, so downstream agents
and the reader can verify your reasoning rather than take your word for it.
