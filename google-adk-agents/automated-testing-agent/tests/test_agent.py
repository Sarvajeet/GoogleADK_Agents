import unittest
from unittest.mock import MagicMock, patch
from ..agent import AutomatedTestingAgent

class TestAutomatedTestingAgent(unittest.TestCase):

    @patch('unittest.TestLoader')
    def test_discover_and_run_tests(self, mock_loader):
        # Create a mock suite
        mock_suite = MagicMock()

        # Configure the mock loader to return the mock suite
        mock_loader.return_value.discover.return_value = mock_suite

        # Create an instance of the agent and run the test
        agent = AutomatedTestingAgent("fake/path")
        result = agent.discover_and_run_tests()

        # Check that the loader was called with the correct path
        mock_loader.return_value.discover.assert_called_with("fake/path")

        # Check that the suite's run method was called
        self.assertTrue(mock_suite.run.called)

        # Check that the result is a TestResult instance
        self.assertIsInstance(result, unittest.TestResult)

if __name__ == '__main__':
    unittest.main()
