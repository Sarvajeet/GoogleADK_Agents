from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent

from .sub_agents.requirements_analyst import RequirementsAnalystAgent
from .sub_agents.project_scaffolder import ProjectScaffolderAgent
from .sub_agents.code_generator import CodeGeneratorAgent
from .sub_agents.test_generator import TestGeneratorAgent
from .sub_agents.documentation import DocumentationAgent
from .sub_agents.deployment import DeploymentAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Agent Definition ---

# Define the sequential pipeline
pipeline = SequentialAgent(
    name="DevelopmentPipeline",
    sub_agents=[
        RequirementsAnalystAgent,
        ProjectScaffolderAgent,
        CodeGeneratorAgent,
        TestGeneratorAgent,
        DocumentationAgent,
        DeploymentAgent
    ]
)

# Define the Chief Architect Agent
ChiefArchitectAgent = LlmAgent(
    name="ChiefArchitectAgent",
    model="gemini-2.0-flash",
    sub_agents=[pipeline],
    instruction="""You are the Chief Architect agent. Your task is to orchestrate the development of a new software project.
    You will use the 'DevelopmentPipeline' to manage the development process.
    The user will provide the requirements for the project.
    """,
    description="An agent that orchestrates the software development process."
)
