import json
import yaml
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Requirements Analysis Tools ---

def analyze_openapi_spec(ctx: ToolContext, file_key: str, spec_format: str) -> dict:
    """Analyzes an OpenAPI spec from an artifact and updates the state.

    Args:
        ctx: The tool context.
        file_key: The key of the artifact containing the OpenAPI spec.
        spec_format: The format of the spec, either 'json' or 'yaml'.

    Returns:
        The updated session state.
    """
    try:
        spec_string = ctx.invocation_context.artifact_service.load_artifact(file_key)

        if spec_format == "json":
            spec_dict = json.loads(spec_string)
            OpenAPIToolset(spec_str=spec_string, spec_str_type="json")
        elif spec_format == "yaml":
            spec_dict = yaml.safe_load(spec_string)
            OpenAPIToolset(spec_str=spec_string, spec_str_type="yaml")
        else:
            raise ValueError("Unsupported spec format. Please use 'json' or 'yaml'")

        project_name = spec_dict.get("info", {}).get("title", "unnamed-project")

        endpoints = list(spec_dict.get("paths", {}).keys())

        ctx.invocation_context.session.state["project_name"] = project_name
        ctx.invocation_context.session.state["endpoints"] = endpoints

        return ctx.invocation_context.session.state
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
    The user will provide the file key for the OpenAPI spec and the format of the spec.
    """,
    description="An agent that can analyze project requirements from an OpenAPI spec."
)
