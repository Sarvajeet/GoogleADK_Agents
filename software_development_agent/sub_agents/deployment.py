import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Deployment Tools ---

def generate_dockerfile(state: dict) -> dict:
    """Generates a Dockerfile for the project.

    Args:
        state: The current session state.

    Returns:
        The updated session state.
    """
    try:
        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        dockerfile_path = os.path.join(project_name, "Dockerfile")

        with open(dockerfile_path, "w") as f:
            f.write("FROM python:3.9-slim\n\n")
            f.write("WORKDIR /app\n\n")
            f.write("COPY requirements.txt requirements.txt\n")
            f.write("RUN pip install --no-cache-dir -r requirements.txt\n\n")
            f.write("COPY ./app /app\n\n")
            f.write('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]\n')

        return state
    except Exception as e:
        raise e

# --- Agent Definition ---
DeploymentAgent = LlmAgent(
    name="DeploymentAgent",
    model="gemini-2.5-flash",
    tools=[generate_dockerfile],
    instruction="""You are a deployment agent. Your task is to generate a Dockerfile for the project.
    Use the `generate_dockerfile` tool to generate the Dockerfile.
    """,
    description="An agent that can generate a Dockerfile."
)
