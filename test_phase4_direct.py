import json
from unittest.mock import Mock

from requirements_analyst_agent import analyze_requirements
from project_scaffolder_agent import create_project_structure
from code_generator_agent import generate_code
from test_generator_agent import generate_tests

print("Testing the Phase 4 pipeline directly...")

# 1. Read the requirements.json file
with open("requirements.json", "r") as f:
    requirements_json = f.read()

# 2. Call the analyze_requirements tool
project_name = analyze_requirements(requirements_json)
print(f"Project name from requirements: {project_name}")

# 3. Call the create_project_structure tool
result = create_project_structure(project_name)
print(f"Result from create_project_structure: {result}")

# 4. Create a mock ToolContext
mock_session = Mock()
state_dict = {"project_name": project_name}
mock_session.state.get.side_effect = lambda key: state_dict.get(key)
mock_context = Mock()
mock_context.invocation_context.session = mock_session

# 5. Call the generate_code tool
result = generate_code(mock_context)
print(f"Result from generate_code: {result}")

# 6. Call the generate_tests tool
result = generate_tests(mock_context)
print(f"Result from generate_tests: {result}")
