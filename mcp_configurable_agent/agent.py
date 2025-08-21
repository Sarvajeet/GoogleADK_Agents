import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
FILESYSTEM_MCP_COMMAND = os.environ.get("FILESYSTEM_MCP_COMMAND", "npx")
FILESYSTEM_MCP_ARGS = os.environ.get("FILESYSTEM_MCP_ARGS", '["-y", "@modelcontextprotocol/server-filesystem", "./mcp_configurable_agent/adk_agent_public"]')
MAPS_MCP_COMMAND = os.environ.get("MAPS_MCP_COMMAND", "npx")
MAPS_MCP_ARGS = os.environ.get("MAPS_MCP_ARGS", '["-y", "@modelcontextprotocol/server-google-maps"]')
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set. Please add it to the .env file.")

# Create the filesystem toolset
filesystem_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=FILESYSTEM_MCP_COMMAND,
            args=eval(FILESYSTEM_MCP_ARGS),
        ),
    ),
    tool_filter=['list_directory', 'read_file']
)

# Create the maps toolset
maps_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=MAPS_MCP_COMMAND,
            args=eval(MAPS_MCP_ARGS),
            env={"GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY}
        ),
    ),
    tool_filter=['get_directions', 'find_place_by_id']
)

# Create the root agent
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='mcp_configurable_agent',
    instruction='Help the user with file system operations and mapping tasks. Use the available tools to answer the user\'s questions.',
    tools=[filesystem_toolset, maps_toolset],
)
