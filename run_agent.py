from google.adk.runners import Runner
from chatbot_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.generativeai.types import Content, Part

def main():
    if not root_agent:
        print("Agent not loaded. Exiting.")
        return

    runner = Runner(root_agent)
    print("Agent is running.")

    try:
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(
            app_name=root_agent.name, user_id="user"
        )

        user_message = "hello"
        events = runner.run(
            user_id="user", session_id=session.id, user_content=Content(parts=[Part.from_text(user_message)])
        )

        for event in events:
            print(f"Agent > {event.stringify_content()}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Agent stopped.")
        runner.close()

if __name__ == "__main__":
    main()
