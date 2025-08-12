from google.adk.agents import Agent

root_agent = Agent(
    name="chatbot_agent",
    model="gemini-2.0-flash",
    description="A simple chatbot that should respond without tools.",
    instruction="You are a helpful chatbot. Please respond to the user.",
    tools=[],
)
