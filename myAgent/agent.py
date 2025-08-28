
from google.adk.agents import Agent
from dotenv import load_dotenv
import os


load_dotenv()
#use_vertexai= os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
api_key= 'AIzaSyB45hJrmtn8vH7xTJKzJJuoFm08Bu3V8w4'

root_agent= Agent(
    name='myAgent',
    model="gemini-2.0-flash",
    description="Agent for handsonn",
    instruction="""
   You are a helpful assistance to let user explore"""
)