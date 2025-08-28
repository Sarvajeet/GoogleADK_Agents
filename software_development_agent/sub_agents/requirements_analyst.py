import json
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Requirements Analysis Tools ---

def analyze_openapi_spec(state: dict, file_path: str) -> dict:
    """Analyzes an OpenAPI spec from a file and updates the state.

    Args:
        state: The current session state.
        file_path: The path to the OpenAPI spec file.

    Returns:
        The updated session state.
    """
    try:
        with open(file_path, "r") as f:
            spec_string = f.read()

        spec_dict = json.loads(spec_string)
        project_name = spec_dict.get("info", {}).get("title", "unnamed-project")

        endpoints = list(spec_dict.get("paths", {}).keys())

        state["project_name"] = project_name
        state["endpoints"] = endpoints

        return state
    except Exception as e:
        # It's better to raise the exception and let the caller handle it
        raise e

# --- Agent Definition ---
RequirementsAnalystAgent = LlmAgent(
    name="RequirementsAnalystAgent",
    model="gemini-2.0-flash",
    tools=[analyze_openapi_spec],
    instruction="""You are a requirements analyst agent. Your task is to analyze the user's requirements from an OpenAPI spec file.
    Use the `analyze_openapi_spec` tool to process the requirements.
    The user will provide the path to the OpenAPI spec file.
    """,
    description="An agent that can analyze project requirements from an OpenAPI spec."
)
