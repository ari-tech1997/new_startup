---
name: sector
description: How to select 3-5 genuinely comparable sector peers, compare a target stock against them across meaningful dimensions using research and technical context, and be explicit about limits on comparability.
metadata:
  version: "1.0"
---

# Sector Comparison Methodology

Use this methodology when positioning a target stock against its peers.
This is the most failure-prone part of stock analysis - a sloppy peer set
makes every downstream conclusion misleading, so be deliberate.

## 1. Use research and technical context first

Before selecting peers, use the company research and technical analysis
you were given as context (do not redo that work yourself):

- The research output tells you the industry, sector, and business model -
  the basis for judging whether a candidate peer is actually comparable.
- The technical output tells you how the target itself is currently
  behaving, so your peer comparison can be apples-to-apples on the same
  kind of data.

## 2. Select 3-5 meaningful peers

A good peer:

- Operates in the same sector/industry as the target.
- Has a reasonably similar business model (e.g. don't compare a hardware
  manufacturer to a company that merely sells software in the same broad
  "tech" sector).
- Is a real, identifiable, publicly traded company you can look up with
  `search_symbols`.

For each peer you select, briefly state *why* it was chosen - the
specific similarity that makes it a fair comparison (same core product
line, similar customer base, similar market position, comparable size,
etc.). A peer list without rationale is not useful.

## 3. Gather comparable data

Use `search_symbols`, `get_quote`, and `get_indicators` to pull the same
kind of data for each peer that you have for the target, so the comparison
is symmetric (e.g. don't compare the target's RSI to a peer's market cap).

## 4. Compare across multiple dimensions

Don't reduce the comparison to a single number. Consider dimensions such
as:

- Price performance / trend (from indicator data).
- Momentum (RSI, MACD) relative to peers.
- Market cap / scale, where available.
- Any qualitative differences surfaced by the research context (e.g.
  different sub-segments within the same industry).

## 5. Distinguish data from interpretation

- Report the raw comparison data plainly (a peer's RSI is what it is).
- Clearly separate your interpretation ("this suggests the target is
  showing relatively stronger momentum than its peer group") from that raw
  data.

## 6. State limitations honestly

Peer comparability is never perfect. Explicitly note things like:

- A peer that is a reasonable but imperfect match (different sub-segment,
  different size tier, etc.).
- Any peer you could not get complete data for.
- Any dimension where the comparison is weak or the sample is too small to
  draw a strong conclusion.

Ending with a clear statement of the target's relative positioning within
its sector - supported by the data above, not asserted on its own.
