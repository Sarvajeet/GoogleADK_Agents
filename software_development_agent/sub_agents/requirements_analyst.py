import json
import yaml
from dotenv import load_dotenv
import PyPDF2
import io

from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Requirements Analysis Tools ---

def analyze_requirements_from_pdf(ctx: ToolContext, file_key: str) -> dict:
    """Analyzes requirements from a PDF document and updates the state.

    Args:
        ctx: The tool context.
        file_key: The key of the artifact containing the PDF file.

    Returns:
        The updated session state.
    """
    try:
        pdf_file = ctx.invocation_context.artifact_service.load_artifact(file_key)
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Use the LLM to extract the project name and endpoints
        llm = LlmAgent(
            model="gemini-2.5-flash",
            instruction=f"""You are an expert at analyzing software requirements.
            Given the following text from a PDF document, please extract the project name and a list of API endpoints.
            The project name should be a single string.
            The endpoints should be a list of strings, where each string is an API endpoint (e.g., '/users', '/products/{{product_id}}').
            Return the project name and endpoints in a JSON format.

            Example:
            {{
                "project_name": "My Awesome API",
                "endpoints": ["/users", "/users/{{user_id}}", "/products"]
            }}

            Here is the text from the PDF:
            {text}
            """
        )
        response = llm(text)
        response_dict = json.loads(response)

        ctx.invocation_context.session.state["project_name"] = response_dict.get("project_name", "unnamed-project")
        ctx.invocation_context.session.state["endpoints"] = response_dict.get("endpoints", [])

        return ctx.invocation_context.session.state
    except Exception as e:
        raise e

def analyze_openapi_spec_from_text(ctx: ToolContext, spec_string: str, spec_format: str) -> dict:
    """Analyzes an OpenAPI spec from a string and updates the state.

    Args:
        ctx: The tool context.
        spec_string: The string containing the OpenAPI spec.
        spec_format: The format of the spec, either 'json' or 'yaml'.

    Returns:
        The updated session state.
    """
    try:
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
    model="gemini-2.5-flash",
    tools=[analyze_openapi_spec_from_text, analyze_requirements_from_pdf],
    instruction="""You are a requirements analyst agent. Your task is to analyze the user's requirements from either an OpenAPI spec or a PDF document.

    If the user provides an OpenAPI spec as a string, use the `analyze_openapi_spec_from_text` tool.
    If the user provides a PDF file, use the `analyze_requirements_from_pdf` tool.

    You must decide which tool to use based on the user's input.
    """,
    description="An agent that can analyze project requirements from an OpenAPI spec or a PDF document."
)
