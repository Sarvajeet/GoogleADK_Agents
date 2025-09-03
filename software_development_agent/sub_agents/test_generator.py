import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Test Generation Tools ---

def generate_tests(state: dict) -> dict:
    """Generates basic unit tests for the application.

    Args:
        state: The current session state.

    Returns:
        The updated session state.
    """
    try:
        if "generate_code_response" in state:
            state = state["generate_code_response"]

        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        tech_stack = state.get("tech_stack", "fastapi")

        if tech_stack == "fastapi":
            generate_fastapi_tests(state)
        elif tech_stack == "springboot":
            generate_springboot_tests(state)
        else:
            raise ValueError(f"Unsupported technology stack: {tech_stack}")

        return state
    except Exception as e:
        raise e

def generate_fastapi_tests(state: dict):
    """Generates FastAPI tests."""
    project_name = state.get("project_name")
    endpoints = state.get("endpoints", [])
    tests_path = os.path.join(project_name, "tests")
    test_main_py_path = os.path.join(tests_path, "test_main.py")

    with open(test_main_py_path, "w") as f:
        f.write('from fastapi.testclient import TestClient\n')
        f.write('from app.main import app\n\n')
        f.write('client = TestClient(app)\n\n')

        for endpoint in endpoints:
            func_name = "test_" + endpoint.replace("/", "_").replace("{", "").replace("}", "")
            f.write(f'def {func_name}():\n')
            if "{" in endpoint:
                test_path = endpoint.replace("{petId}", "123")
            else:
                test_path = endpoint
            f.write(f'    response = client.get("{test_path}")\n')
            f.write(f'    assert response.status_code == 200\n\n')

def generate_springboot_tests(state: dict):
    """Generates Spring Boot tests."""
    project_name = state.get("project_name")
    endpoints = state.get("endpoints", [])
    package_name = "".join(filter(str.isalnum, project_name.lower()))
    app_name = "".join(word.capitalize() for word in package_name.split())

    test_java_path = os.path.join(project_name, "src", "test", "java", "com", "example", package_name)
    test_file_path = os.path.join(test_java_path, f"{app_name}ApplicationTests.java")

    with open(test_file_path, "a") as f:
        f.write("\n")
        for endpoint in endpoints:
            method_name = "test" + "".join(word.capitalize() for word in endpoint.replace("/", " ").replace("{", " ").replace("}", " ").split())
            f.write(f'''
    @Test
    void {method_name}() throws Exception {{
        // TODO: Implement this test
    }}
''')
