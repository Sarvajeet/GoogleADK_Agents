# Software Development Agent using Google ADK

This project is a multi-agent system for software development built with the Google Agent Development Kit (ADK).

## Overview

The system is composed of several specialized agents that work together to take an OpenAPI specification and generate a complete project structure, including:
- Boilerplate API code for a FastAPI application.
- Basic unit tests for the API.
- A `README.md` file.
- A `Dockerfile`.

The agents are orchestrated by a "Chief Architect" agent that manages the development process.

## How to Run

### Using the ADK Web UI

The easiest way to interact with the agent is through the ADK Web UI. To start the web server, run the following command in your terminal:

```bash
adk web software_development_agent
```

This will start a web server, and you can open the provided URL in your browser to interact with the `ChiefArchitectAgent`.

### Using the Runner Script

A `run.py` script is included to demonstrate how to run the agent programmatically. You can run this script with the following command:

```bash
python run.py
```

This script will run the full pipeline and create a new project named "Simple Pet Store API" based on the `software_development_agent/petstore.json` spec.

### Important Note on Authentication

The agent requires authentication with the Google AI API to function correctly when run through the ADK framework. The `run.py` script will fail with an authentication error in an environment where credentials are not configured.
