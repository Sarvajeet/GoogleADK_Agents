import argparse
from agent import AutomatedTestingAgent

def main():
    parser = argparse.ArgumentParser(description="Automated Testing Agent")
    parser.add_argument("project_path", help="The path to the project to test.")
    args = parser.parse_args()

    agent = AutomatedTestingAgent(args.project_path)
    agent.run()

if __name__ == "__main__":
    main()
