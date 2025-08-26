import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Test Generation Tools ---

def generate_tests(state: dict) -> dict:
    """Generates basic unit tests for the FastAPI application.

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

        tests_path = os.path.join(project_name, "tests")
        test_main_py_path = os.path.join(tests_path, "test_main.py")

        with open(test_main_py_path, "w") as f:
            f.write('from fastapi.testclient import TestClient\n')
            f.write('from app.main import app\n\n')
            f.write('client = TestClient(app)\n\n')

            for endpoint in endpoints:
                # A simple mapping from OpenAPI path to test function name
                func_name = "test_" + endpoint.replace("/", "_").replace("{", "").replace("}", "")
                # A simple test for each endpoint
                f.write(f'def {func_name}():\n')
                # A very basic test that just checks for a 200 status code
                # This will need to be improved in a future phase
                if "{" in endpoint:
                    # a simple way to handle path parameters
                    test_path = endpoint.replace("{petId}", "123")
                else:
                    test_path = endpoint
                f.write(f'    response = client.get("{test_path}")\n')
                f.write(f'    assert response.status_code == 200\n\n')

        return state
    except Exception as e:
        raise e

# --- Agent Definition ---
TestGeneratorAgent = LlmAgent(
    name="TestGeneratorAgent",
    model="gemini-2.0-flash",
    tools=[generate_tests],
    instruction="""You are a test generator agent. Your task is to generate unit tests for the project.
    Use the `generate_tests` tool to generate the tests.
    """,
    description="An agent that can generate unit tests."
)
