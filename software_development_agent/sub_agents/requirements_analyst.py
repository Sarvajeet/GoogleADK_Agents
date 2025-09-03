import json
import yaml
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Requirements Analysis Tools ---

def analyze_openapi_spec(state: dict, file_path: str, tech_stack: str = "fastapi") -> dict:
    """Analyzes an OpenAPI spec from a file and updates the state.

    Args:
        state: The current session state.
        file_path: The path to the OpenAPI spec file.
        tech_stack: The technology stack to use (e.g., 'fastapi', 'springboot').

    Returns:
        The updated session state.
    """
    try:
        with open(file_path, "r") as f:
            spec_string = f.read()

        if file_path.endswith(".json"):
            spec_dict = json.loads(spec_string)
            OpenAPIToolset(spec_str=spec_string, spec_str_type="json")
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            spec_dict = yaml.safe_load(spec_string)
            OpenAPIToolset(spec_str=spec_string, spec_str_type="yaml")
        else:
            raise ValueError("Unsupported file type. Please use .json, .yaml, or .yml")

        project_name = spec_dict.get("info", {}).get("title", "unnamed-project")
        endpoints = list(spec_dict.get("paths", {}).keys())

        state["project_name"] = project_name
        state["endpoints"] = endpoints
        state["tech_stack"] = tech_stack

        return state
    except Exception as e:
        raise e
