#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from new_startup.crew import NewStartup

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Default target for local runs - override by editing these or wiring in
# real CLI args/inputs (e.g. sys.argv, an API request body, etc.).
DEFAULT_INPUTS = {
    'company': 'Apple Inc.',
    'ticker': 'AAPL',
    'current_year': str(datetime.now().year),
}


def run():
    """
    Run the crew.
    """
    try:
        NewStartup().crew().kickoff(inputs=DEFAULT_INPUTS)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        NewStartup().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=DEFAULT_INPUTS)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NewStartup().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        NewStartup().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=DEFAULT_INPUTS)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "company": "",
        "ticker": "",
        "current_year": "",
    }

    try:
        result = NewStartup().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
