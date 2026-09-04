---
name: research
description: Disciplined company research methodology - how to identify a target company, gather reliable facts about it, and structure findings for downstream technical, sector, and report agents.
metadata:
  version: "1.0"
---

# Company Research Methodology

Use this methodology whenever researching a target public company.

## 1. Identify the company precisely

- If given a company name, use `search_symbols` to confirm the ticker,
  exchange, and official name before doing anything else.
- If given a ticker, confirm what company it maps to rather than assuming.
- Note when a name is ambiguous (e.g. multiple listings, similarly named
  companies) and state which one you selected and why.

## 2. Prioritize reliable, relevant information

Focus your research on:

- What the company does (business model, core products/services).
- What industry/sector it operates in.
- How it makes money and who its customers are.
- Notable recent developments that would matter to an investor (only if you
  have a genuine basis for the claim - do not speculate about "recent news"
  you don't actually have).

Skip trivia that doesn't help later analysis (logo history, founding
anecdotes unrelated to the business, etc.).

## 3. Separate verified facts from inference

- Anything sourced directly from a tool call (e.g. `search_symbols` output)
  is a **fact**: state it plainly.
- Anything you are inferring or reasoning about (e.g. "this suggests the
  company is diversifying") must be clearly labeled as **interpretation**,
  not presented as fact.
- Never invent financial figures, dates, or events. If you don't have
  reliable information on something, say so explicitly instead of guessing.

## 4. Structure findings for downstream agents

Downstream agents (technical, sector, report) will consume your output as
context, not read it interactively. Structure your brief with clear
sections so they can extract what they need:

- **Company identity**: name, ticker, exchange.
- **Business model**: what it sells, to whom, how it earns revenue.
- **Industry / sector**: where it competes.
- **Relevant context**: anything else useful for technical or sector
  analysis (e.g. is this a high-growth tech company vs. a mature
  dividend-paying utility - this shapes what "good" technicals/peers look
  like).
- **Sources / data used**: what tool calls or information backed this brief.

Keep it factual and concise - this is a foundation for other agents, not
the final deliverable.
