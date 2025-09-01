import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom File System Tools ---

def create_project_structure(state: dict) -> None:
    """Creates a standard FastAPI project structure.

    Args:
        state: The current session state.

    Returns:
        The updated session state.
    """
    try:
        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        base_path = project_name
        app_path = os.path.join(base_path, "app")
        tests_path = os.path.join(base_path, "tests")
        docs_path = os.path.join(base_path, "docs")

        # Create directories
        os.makedirs(app_path, exist_ok=True)
        os.makedirs(tests_path, exist_ok=True)
        os.makedirs(docs_path, exist_ok=True)

        # Create files with content
        # app/main.py
        with open(os.path.join(app_path, "main.py"), "w") as f:
            f.write('from fastapi import FastAPI\n\n')
            f.write('app = FastAPI()\n\n')

        # tests/test_main.py
        with open(os.path.join(tests_path, "test_main.py"), "w") as f:
            f.write('# Add tests here\n')

        # docs/README.md
        with open(os.path.join(docs_path, "README.md"), "w") as f:
            f.write(f'# {project_name}\n')

        # .gitignore
        with open(os.path.join(base_path, ".gitignore"), "w") as f:
            f.write('__pycache__/\n')
            f.write('*.pyc\n')
            f.write('.env\n')
            f.write('.venv\n')

        # requirements.txt
        with open(os.path.join(base_path, "requirements.txt"), "w") as f:
            f.write('fastapi\n')
            f.write('uvicorn[standard]\n')

        #return state
    except Exception as e:
        raise e

# --- Agent Definition ---
ProjectScaffolderAgent = LlmAgent(
    name="ProjectScaffolderAgent",
    model="gemini-2.5-flash",
    tools=[create_project_structure],
    instruction="""You are a project scaffolder agent. Your task is to create a new project structure depending on technology stack.
       Use the `create_project_structure` tool to do this.""",
    description="An agent that can scaffold a new software project."
)
