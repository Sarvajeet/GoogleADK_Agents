from dotenv import load_dotenv

from google.adk.agents import LlmAgent

from .sub_agents.requirements_analyst import analyze_openapi_spec
from .sub_agents.project_scaffolder import create_project_structure
from .sub_agents.code_generator import generate_code
from .sub_agents.test_generator import generate_tests
from .sub_agents.documentation import generate_readme
from .sub_agents.deployment import generate_dockerfile

# --- Load Environment Variables ---
load_dotenv()

# --- Agent Definition ---
ChiefArchitectAgent = LlmAgent(
    name="ChiefArchitectAgent",
    model="gemini-2.5-flash",
    tools=[
        analyze_openapi_spec,
        create_project_structure,
        generate_code,
        generate_tests,
        generate_readme,
        generate_dockerfile,
    ],
    instruction="""You are the Chief Architect agent. Your task is to orchestrate the development of a new software project.
    The user will provide the requirements for the project, including the technology stack (e.g., fastapi or springboot) and the path to the OpenAPI spec file.
    You must call all the tools in the correct order in a single turn.
    After calling all the tools, you must provide a summary of the work done as the final response.
    The tools must be called in the following order:
    1. `analyze_openapi_spec`
    2. `create_project_structure`
    3. `generate_code`
    4. `generate_tests`
    5. `generate_readme`
    6. `generate_dockerfile`
    """,
    description="An agent that orchestrates the software development process."
)
