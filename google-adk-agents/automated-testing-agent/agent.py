import os
import unittest

class AutomatedTestingAgent:
    def __init__(self, project_path):
        self.project_path = project_path

    def discover_and_run_tests(self):
        """
        Discovers and runs all tests in the specified project path.
        """
        # Create a TestLoader instance
        loader = unittest.TestLoader()

        # Discover all tests in the project path
        suite = loader.discover(self.project_path)

        # Create a TestResult instance
        result = unittest.TestResult()

        # Run the tests
        suite.run(result)

        return result

    def run(self):
        print(f"Running automated tests for project: {self.project_path}")
        result = self.discover_and_run_tests()

        if result.wasSuccessful():
            print("All tests passed successfully!")
        else:
            print("Some tests failed.")
            for failure in result.failures:
                print(f"FAIL: {failure[0]}")
                print(failure[1])
            for error in result.errors:
                print(f"ERROR: {error[0]}")
                print(error[1])

        print("Automated testing agent finished.")
