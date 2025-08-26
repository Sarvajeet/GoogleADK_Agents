import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- Load Environment Variables ---
load_dotenv()

# --- Agent Definitions ---

# Agent A will generate a topic
agent_a = LlmAgent(
    name="TopicGenerator",
    model="gemini-2.0-flash",
    instruction="Generate a random, interesting topic.",
    output_key="topic"  # Save the output to session.state['topic']
)

# Agent B will write a short paragraph about the topic from Agent A
agent_b = LlmAgent(
    name="ParagraphWriter",
    model="gemini-2.0-flash",
    instruction="Write a short paragraph about the topic: {topic}.",
    output_key="paragraph" # Save the output to session.state['paragraph']
)

# --- Sequential Agent to orchestrate the pipeline ---
pipeline = SequentialAgent(
    name="WritingPipeline",
    sub_agents=[agent_a, agent_b]
)

# --- Session and Runner Setup ---
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=pipeline,
        app_name="multi_agent_app",
        session_service=session_service,
    )
    session_id = f"session_{uuid.uuid4()}"
    await session_service.create_session(
        app_name="multi_agent_app",
        user_id="user_1",
        session_id=session_id,
    )
    return runner, session_id

# --- Agent Interaction Function ---
async def call_agent_async(query, runner, session_id):
    print(f"\n--- Running Multi-Agent System ---")
    print(f"Query: {query}")

    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not provide a final text response."
    try:
        async for event in runner.run_async(
            user_id="user_1", session_id=session_id, new_message=content
            ):
            if event.get_function_calls():
                call = event.get_function_calls()[0]
                print(f"  Agent Action: Called function '{call.name}' with args {call.args}")
            elif event.get_function_responses():
                response = event.get_function_responses()[0]
                print(f"  Agent Action: Received response for '{response.name}'")
            elif event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text.strip()

        print(f"Agent Final Response: {final_response_text}")

    except Exception as e:
        print(f"An error occurred during agent run: {e}")
        import traceback
        traceback.print_exc()
    print("-" * 30)

# --- Run Example ---
async def run_example():
    runner, session_id = await setup_session_and_runner()
    await call_agent_async("Start the writing pipeline.", runner, session_id)


# --- Execute ---
if __name__ == "__main__":
    print("Executing multi-agent system example...")
    try:
        asyncio.run(run_example())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("Info: Cannot run asyncio.run from a running event loop (e.g., Jupyter/Colab).")
        else:
            raise e
    print("Multi-agent system example finished.")
