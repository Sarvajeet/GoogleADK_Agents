from adk.agents import LlmAgent
from adk.tools import Tool
import unittest

class AutomatedTestingTool(Tool):
    def __init__(self):
        super().__init__(
            name="automated_testing_tool",
            description="A tool that can run all tests in a given directory.",
        )

    def execute(self, project_path: str) -> str:
        """
        Runs all tests in the specified project path.
        """
        loader = unittest.TestLoader()
        suite = loader.discover(project_path)
        result = unittest.TestResult()
        suite.run(result)

        if result.wasSuccessful():
            return "All tests passed successfully!"
        else:
            failures = ""
            for failure in result.failures:
                failures += f"FAIL: {failure[0]}\n{failure[1]}\n"
            for error in result.errors:
                failures += f"ERROR: {error[0]}\n{error[1]}\n"
            return f"Some tests failed:\n{failures}"

def create_agent():
    return LlmAgent(
        tools=[AutomatedTestingTool()],
    )
