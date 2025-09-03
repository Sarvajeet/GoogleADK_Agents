import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Custom File System Tools ---

def create_project_structure(state: dict) -> dict:
    """Creates a project structure based on the specified technology stack.

    Args:
        state: The current session state, containing 'project_name' and 'tech_stack'.
    """
    try:
        # The state from the previous tool is nested
        if "analyze_openapi_spec_response" in state:
            state = state["analyze_openapi_spec_response"]

        project_name = state.get("project_name")
        if not project_name:
            raise ValueError("Missing 'project_name' in state.")

        tech_stack = state.get("tech_stack", "fastapi")  # Default to fastapi

        if tech_stack == "fastapi":
            create_fastapi_structure(project_name)
        elif tech_stack == "springboot":
            create_springboot_structure(project_name)
        else:
            raise ValueError(f"Unsupported technology stack: {tech_stack}")

        return state
    except Exception as e:
        raise e

def create_fastapi_structure(project_name: str):
    """Creates a standard FastAPI project structure."""
    base_path = project_name
    app_path = os.path.join(base_path, "app")
    tests_path = os.path.join(base_path, "tests")
    docs_path = os.path.join(base_path, "docs")

    # Create directories
    os.makedirs(app_path, exist_ok=True)
    os.makedirs(tests_path, exist_ok=True)
    os.makedirs(docs_path, exist_ok=True)

    # Create files with content
    with open(os.path.join(app_path, "main.py"), "w") as f:
        f.write('from fastapi import FastAPI\n\n')
        f.write('app = FastAPI()\n\n')

    with open(os.path.join(tests_path, "test_main.py"), "w") as f:
        f.write('# Add tests here\n')

    with open(os.path.join(docs_path, "README.md"), "w") as f:
        f.write(f'# {project_name}\n')

    with open(os.path.join(base_path, ".gitignore"), "w") as f:
        f.write('__pycache__/\n*.pyc\n.env\n.venv\n')

    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write('fastapi\n' + 'uvicorn[standard]\n')


def create_springboot_structure(project_name: str):
    """Creates a standard Spring Boot project structure."""
    base_path = project_name
    # Sanitize project name for package naming
    package_name = "".join(filter(str.isalnum, project_name.lower()))
    app_name = "".join(word.capitalize() for word in package_name.split())

    main_java_path = os.path.join(base_path, "src", "main", "java", "com", "example", package_name)
    main_resources_path = os.path.join(base_path, "src", "main", "resources")
    test_java_path = os.path.join(base_path, "src", "test", "java", "com", "example", package_name)

    # Create directories
    os.makedirs(main_java_path, exist_ok=True)
    os.makedirs(main_resources_path, exist_ok=True)
    os.makedirs(test_java_path, exist_ok=True)

    # Create pom.xml
    with open(os.path.join(base_path, "pom.xml"), "w") as f:
        f.write(f'''<project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>{package_name}</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.7</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>''')

    # Create main application file
    with open(os.path.join(main_java_path, f"{app_name}Application.java"), "w") as f:
        f.write(f'''package com.example.{package_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class {app_name}Application {{
    public static void main(String[] args) {{
        SpringApplication.run({app_name}Application.class, args);
    }}
}}''')

    # Create test application file
    with open(os.path.join(test_java_path, f"{app_name}ApplicationTests.java"), "w") as f:
        f.write(f'''package com.example.{package_name};

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class {app_name}ApplicationTests {{
    @Test
    void contextLoads() {{
    }}
}}''')

    # Create application.properties
    with open(os.path.join(main_resources_path, "application.properties"), "w") as f:
        f.write('') # Empty properties file

    # Create .gitignore
    with open(os.path.join(base_path, ".gitignore"), "w") as f:
        f.write('target/\n.idea/\n*.iml\n')

    # Create README.md
    with open(os.path.join(base_path, "README.md"), "w") as f:
        f.write(f'# {project_name}\n')

