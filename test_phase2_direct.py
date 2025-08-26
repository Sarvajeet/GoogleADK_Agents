import json

from requirements_analyst_agent import analyze_requirements
from project_scaffolder_agent import create_project_structure

print("Testing the Phase 2 pipeline directly...")

# 1. Read the requirements.json file
with open("requirements.json", "r") as f:
    requirements_json = f.read()

# 2. Call the analyze_requirements tool
project_name = analyze_requirements(requirements_json)
print(f"Project name from requirements: {project_name}")

# 3. Call the create_project_structure tool
result = create_project_structure(project_name)
print(f"Result from create_project_structure: {result}")
