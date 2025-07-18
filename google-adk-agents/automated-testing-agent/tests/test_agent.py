import unittest
from unittest.mock import patch
from io import StringIO
from ..agent import AutomatedTestingAgent

class TestAutomatedTestingAgent(unittest.TestCase):

    def test_run(self):
        # Create an instance of the agent
        agent = AutomatedTestingAgent(".")

        # Redirect stdout to capture the output of the run method
        with patch('sys.stdout', new=StringIO()) as fake_out:
            agent.run()
            output = fake_out.getvalue().strip()

        # Check that the output is what we expect
        self.assertEqual(output, "Running automated testing agent...\nAutomated testing agent finished.")

if __name__ == '__main__':
    unittest.main()
