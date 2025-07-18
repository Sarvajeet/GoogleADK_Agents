# Google ADK Agents

This repository contains a collection of agents built using the Google ADK.

## Project Structure

Each agent has its own directory within the `google-adk-agents` directory. The structure of each agent's directory is as follows:

- `main.py`: The main entry point for the agent.
- `agent.py`: The core logic of the agent.
- `tools/`: A directory for any custom tools the agent might need.
- `tests/`: A directory for tests.
    - `test_agent.py`: Tests for the agent logic.

## Adding a New Agent

To add a new agent, simply create a new directory with the same structure as the existing agents. Then, add your agent's code to the appropriate files.

## Running the Agents

### ADK-Based Automated Testing Agent

This agent is built using the Google ADK and is designed to be more flexible and extensible than the original agent. To run this agent, navigate to the `google-adk-agents/adk-automated-testing-agent` directory and run the following command:

```bash
python3 main.py
```

This will start an interactive session with the agent. You can then ask the agent to run tests in a specific directory by typing a message such as "run tests in /path/to/your/project".
