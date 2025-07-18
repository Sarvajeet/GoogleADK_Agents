import unittest
from ..agent import create_agent

class TestAutomatedTestingAgent(unittest.TestCase):
    def test_create_agent(self):
        agent = create_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(len(agent.tools), 1)
        self.assertEqual(agent.tools[0].name, "automated_testing_tool")

if __name__ == "__main__":
    unittest.main()
