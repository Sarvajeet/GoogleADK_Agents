import json

from requirements_analyst_agent import analyze_openapi_spec
from project_scaffolder_agent import create_project_structure
from code_generator_agent import generate_code
from test_generator_agent import generate_tests
from documentation_agent import generate_readme
from deployment_agent import generate_dockerfile

print("Testing the Phase 7 pipeline directly...")

# 1. Initialize the state
state = {}

# 2. Call the analyze_openapi_spec tool
state = analyze_openapi_spec(state, "petstore.json")
print(f"State after analyze_openapi_spec: {state}")

# 3. Call the create_project_structure tool
state = create_project_structure(state)
print(f"State after create_project_structure: {state}")

# 4. Call the generate_code tool
state = generate_code(state)
print(f"State after generate_code: {state}")

# 5. Call the generate_tests tool
state = generate_tests(state)
print(f"State after generate_tests: {state}")

# 6. Call the generate_readme tool
state = generate_readme(state)
print(f"State after generate_readme: {state}")

# 7. Call the generate_dockerfile tool
state = generate_dockerfile(state)
print(f"State after generate_dockerfile: {state}")
