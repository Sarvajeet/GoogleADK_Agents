from agent import create_agent

def main():
    agent = create_agent()
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        response = agent.run(query)
        print(f"Agent: {response.output}")

if __name__ == "__main__":
    main()
