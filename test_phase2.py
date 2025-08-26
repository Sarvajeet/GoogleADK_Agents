import json
from unittest.mock import Mock

from requirements_analyst_agent import analyze_requirements
from project_scaffolder_agent import create_project_structure

print("Testing the Phase 2 pipeline directly...")

# 1. Read the requirements.json file
with open("requirements.json", "r") as f:
    requirements_json = f.read()

# 2. Call the analyze_requirements tool
project_name = analyze_requirements(requirements_json)
print(f"Project name from requirements: {project_name}")

# 3. Create a mock InvocationContext and Session
mock_session = Mock()
state_dict = {"project_name": project_name}
mock_session.state.get.side_effect = lambda key: state_dict.get(key)

mock_context = Mock()
mock_context.session = mock_session

# 4. Call the create_project_structure tool
result = create_project_structure(mock_context)
print(f"Result from create_project_structure: {result}")
