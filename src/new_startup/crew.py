import sys
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from mcp import StdioServerParameters


# Project root (this file lives at src/new_startup/crew.py), so skills/ at
# the repo root can be located regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = PROJECT_ROOT / "skills"


def _load_skill(name: str) -> str:
    """Read one agent's SKILL.md as an inline skill string.

    Each agent gets exactly its own skill (not the whole skills/ directory),
    so skills are assigned deliberately rather than being discoverable by
    every agent. See skills/<name>/SKILL.md for the methodology itself -
    this only wires the file to its agent.
    """
    return (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")


@CrewBase
class NewStartup():
    """Multi-agent stock analysis crew."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # MCP server providing search_symbols/get_quote/get_indicators, launched
    # as a subprocess over stdio. `self.get_mcp_tools(...)` (from @CrewBase)
    # starts it on first use and filters its tools by name per agent.
    #
    # Launched via `sys.executable -m ...` (the same interpreter already
    # running this crew) rather than `uv run ...`: a deployed container may
    # not have the `uv` CLI on PATH, and even when it does, `uv run` first
    # re-validates/syncs the project against pyproject.toml/uv.lock (which
    # can hang or fail without network access) and assumes a specific
    # working directory. Invoking the module directly has neither
    # dependency - it only requires `new_startup` to be importable, which
    # it already must be for this crew to be running at all.
    mcp_server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "new_startup.mcp_server.server"],
    )

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'], # type: ignore[index]
            tools=self.get_mcp_tools("search_symbols"),
            skills=[_load_skill("research")],
            verbose=True,
        )

    @agent
    def technical_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_agent'], # type: ignore[index]
            tools=self.get_mcp_tools("get_quote", "get_indicators"),
            skills=[_load_skill("technical")],
            verbose=True,
        )

    @agent
    def sector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sector_agent'], # type: ignore[index]
            tools=self.get_mcp_tools("search_symbols", "get_quote", "get_indicators"),
            skills=[_load_skill("sector")],
            verbose=True,
        )

    @agent
    def report_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_agent'], # type: ignore[index]
            # No market-data tools: this agent synthesizes prior task
            # outputs rather than independently repeating the analysis.
            skills=[_load_skill("report")],
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def technical_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_task'], # type: ignore[index]
        )

    @task
    def sector_task(self) -> Task:
        # context (research_task, technical_task) is declared in tasks.yaml
        # and resolved automatically by @CrewBase.
        return Task(
            config=self.tasks_config['sector_task'], # type: ignore[index]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the sequential stock analysis crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
