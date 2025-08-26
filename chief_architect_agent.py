from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent

from requirements_analyst_agent import RequirementsAnalystAgent
from project_scaffolder_agent import ProjectScaffolderAgent
from code_generator_agent import CodeGeneratorAgent
from test_generator_agent import TestGeneratorAgent

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
        TestGeneratorAgent
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
