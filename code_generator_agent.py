import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Code Generation Tools ---

def generate_code(state: dict) -> dict:
    """Generates a FastAPI application with endpoints from the session state.

    Args:
        state: The current session state.

    Returns:
        The updated session state.
    """
    try:
        project_name = state.get("project_name")
        endpoints = state.get("endpoints", [])

        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        app_path = os.path.join(project_name, "app")
        main_py_path = os.path.join(app_path, "main.py")

        with open(main_py_path, "a") as f:
            for endpoint in endpoints:
                # A simple mapping from OpenAPI path to FastAPI path
                fastapi_path = endpoint.replace("{", "{").replace("}", "}")
                f.write(f'@app.get("{fastapi_path}")\n')
                # A simple function name based on the endpoint
                func_name = endpoint.replace("/", "_").replace("{", "").replace("}", "")
                f.write(f'def {func_name}():\n')
                f.write(f'    return {{"message": "This is the {endpoint} endpoint"}}\n\n')

        return state
    except Exception as e:
        raise e

# --- Agent Definition ---
CodeGeneratorAgent = LlmAgent(
    name="CodeGeneratorAgent",
    model="gemini-2.0-flash",
    tools=[generate_code],
    instruction="""You are a code generator agent. Your task is to generate the source code for the project.
    Use the `generate_code` tool to generate the code.
    """,
    description="An agent that can generate source code."
)
