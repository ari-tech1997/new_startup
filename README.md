# NewStartup Crew - Multi-Agent Stock Analysis

A [crewAI](https://crewai.com) project with four specialized agents that
analyze a public company sequentially: **research → technical analysis →
sector comparison → final report**. Market data (symbol search, quotes,
technical indicators) is served by a dedicated MCP server backed by
[yfinance](https://github.com/ranaroussi/yfinance), so no market-data API
key is required.

## Installation

Ensure you have Python >=3.10 <3.14 installed. This project uses
[UV](https://docs.astral.sh/uv/) for dependency management.

```bash
pip install uv
uv sync
```

Copy `.env.example` to `.env` and add your `OPENAI_API_KEY` (the only
required secret - the market-data MCP server needs no key).

## Running the Project

```bash
crewai run
```

This kicks off the crew for the target set in `src/new_startup/main.py`
(`company` / `ticker`, defaulting to Apple / AAPL) and writes the final
report to `report.md`. The MCP server is launched automatically as a
subprocess by the crew; you don't need to start it separately.

To run the MCP server on its own (e.g. to test tools directly):

```bash
uv run stock-mcp-server
```

## Architecture

```
research_agent   (Company Research Analyst)
      |
      v
technical_agent  (Technical Analysis Specialist)
      |
      v
sector_agent     (Sector Comparison Specialist)  <- context: research + technical
      |
      v
report_agent     (Investment Analysis Report Writer)  <- context: research + technical + sector
```

- **`src/new_startup/config/agents.yaml`** - agent role/goal/backstory.
- **`src/new_startup/config/tasks.yaml`** - task descriptions, expected
  outputs, and `context` dependencies between tasks.
- **`skills/<name>/SKILL.md`** - one behavioral/methodology skill per
  agent (research, technical, sector, report). Skills teach *how* to
  reason; they contain no executable tools.
- **`src/new_startup/mcp_server/`** - the MCP server exposing
  `search_symbols`, `get_quote`, and `get_indicators` as tools, backed by
  `yfinance`.
- **`src/new_startup/crew.py`** - wires agents, tasks, skills, and MCP
  tools together.
- **`src/new_startup/main.py`** - entry point / kickoff inputs.

## Support

For support, questions, or feedback regarding the NewStartup Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
