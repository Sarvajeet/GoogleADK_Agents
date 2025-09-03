import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom Code Generation Tools ---

def generate_code(state: dict) -> dict:
    """Generates source code based on the specified technology stack."""
    try:
        if "create_project_structure_response" in state:
            state = state["create_project_structure_response"]

        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        tech_stack = state.get("tech_stack", "fastapi")

        if tech_stack == "fastapi":
            generate_fastapi_code(state)
        elif tech_stack == "springboot":
            generate_springboot_code(state)
        else:
            raise ValueError(f"Unsupported technology stack: {tech_stack}")

        return state
    except Exception as e:
        raise e

def generate_fastapi_code(state: dict):
    """Generates FastAPI code."""
    project_name = state.get("project_name")
    endpoints = state.get("endpoints", [])
    app_path = os.path.join(project_name, "app")
    main_py_path = os.path.join(app_path, "main.py")

    with open(main_py_path, "a") as f:
        for endpoint in endpoints:
            fastapi_path = endpoint.replace("{", "{").replace("}", "}")
            func_name = endpoint.replace("/", "_").replace("{", "").replace("}", "")
            f.write(f'@app.get("{fastapi_path}")\n')
            f.write(f'def {func_name}():\n')
            f.write(f'    return {{"message": "This is the {endpoint} endpoint"}}\n\n')

def generate_springboot_code(state: dict):
    """Generates Spring Boot code."""
    project_name = state.get("project_name")
    endpoints = state.get("endpoints", [])
    package_name = "".join(filter(str.isalnum, project_name.lower()))
    app_name = "".join(word.capitalize() for word in package_name.split())

    controller_path = os.path.join(project_name, "src", "main", "java", "com", "example", package_name)
    controller_file_path = os.path.join(controller_path, f"{app_name}Controller.java")

    with open(controller_file_path, "w") as f:
        f.write(f'''package com.example.{package_name};

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class {app_name}Controller {{
''')
        for endpoint in endpoints:
            method_name = endpoint.replace("/", "_").replace("{", "").replace("}", "")
            f.write(f'''
    @GetMapping("{endpoint}")
    public String {method_name}() {{
        return "This is the {endpoint} endpoint";
    }}
''')
        f.write('\n}\n')
