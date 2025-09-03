import asyncio
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from software_development_agent import ChiefArchitectAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Session and Runner Setup ---
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=ChiefArchitectAgent,
        app_name="test_app",
        session_service=session_service,
    )
    session_id = "test_session"
    await session_service.create_session(
        app_name="test_app",
        user_id="user_1",
        session_id=session_id,
    )
    return runner, session_id

# --- Agent Interaction Function ---
async def call_agent_async(query, runner, session_id):
    print(f"\n--- Running Test Agent ---")
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
    await call_agent_async("Create a new project based on the 'software_development_agent/petstore.yaml' spec using springboot.", runner, session_id)


# --- Execute ---
if __name__ == "__main__":
    print("Executing test agent runner...")
    try:
        asyncio.run(run_example())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("Info: Cannot run asyncio.run from a running event loop (e.g., Jupyter/Colab).")
        else:
            raise e
    print("Test agent runner finished.")
