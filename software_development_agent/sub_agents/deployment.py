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
        if "generate_readme_response" in state:
            state = state["generate_readme_response"]

        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        tech_stack = state.get("tech_stack", "fastapi")
        dockerfile_path = os.path.join(project_name, "Dockerfile")

        if tech_stack == "fastapi":
            with open(dockerfile_path, "w") as f:
                f.write("FROM python:3.9-slim\n\n")
                f.write("WORKDIR /app\n\n")
                f.write("COPY requirements.txt requirements.txt\n")
                f.write("RUN pip install --no-cache-dir -r requirements.txt\n\n")
                f.write("COPY ./app /app\n\n")
                f.write('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]\n')
        elif tech_stack == "springboot":
            with open(dockerfile_path, "w") as f:
                f.write("FROM openjdk:17-jdk-slim\n\n")
                f.write("ARG JAR_FILE=target/*.jar\n")
                f.write("COPY ${JAR_FILE} app.jar\n\n")
                f.write('ENTRYPOINT ["java","-jar","/app.jar"]\n')

        return state
    except Exception as e:
        raise e
