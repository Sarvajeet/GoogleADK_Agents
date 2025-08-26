import os
import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- Load Environment Variables ---
load_dotenv()

# --- Custom File System Tools ---

def create_file(path: str, content: str) -> dict:
    """Creates a new file at the specified path with the given content.

    Args:
        path: The path to the new file.
        content: The content to write to the new file.

    Returns:
        A dictionary with the status of the operation.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return {"status": "success", "message": f"File '{path}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_directory(path: str) -> dict:
    """Creates a new directory at the specified path.

    Args:
        path: The path to the new directory.

    Returns:
        A dictionary with the status of the operation.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return {"status": "success", "message": f"Directory '{path}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Agent Definition ---
file_system_agent = LlmAgent(
    name="file_system_agent",
    model="gemini-2.0-flash",
    tools=[create_file, create_directory],
    instruction="""You are a file system agent. Use the available tools to create files and directories as requested by the user.""",
    description="An agent that can create files and directories."
)

# --- Session and Runner Setup ---
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=file_system_agent,
        app_name="file_system_app",
        session_service=session_service,
    )
    session_id = f"session_{uuid.uuid4()}"
    await session_service.create_session(
        app_name="file_system_app",
        user_id="user_1",
        session_id=session_id,
    )
    return runner, session_id

# --- Agent Interaction Function ---
async def call_agent_async(query, runner, session_id):
    print(f"\n--- Running File System Agent ---")
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

# --- Run Examples ---
async def run_example():
    runner, session_id = await setup_session_and_runner()

    # Trigger create_directory
    await call_agent_async("Create a new directory called 'my_new_project'", runner, session_id)
    # Trigger create_file
    await call_agent_async("Create a file named 'my_new_project/main.py' with the content 'print(\"Hello, World!\")'", runner, session_id)


# --- Execute ---
if __name__ == "__main__":
    print("Executing file system agent example...")
    try:
        asyncio.run(run_example())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("Info: Cannot run asyncio.run from a running event loop (e.g., Jupyter/Colab).")
        else:
            raise e
    print("File system agent example finished.")
