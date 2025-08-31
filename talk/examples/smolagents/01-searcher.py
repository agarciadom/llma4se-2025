import os

from smolagents import OpenAIServerModel, CodeAgent, MCPClient
from smolagents.default_tools import VisitWebpageTool
from mcp import StdioServerParameters

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
)

server_parameters = StdioServerParameters(
    command='uvx',
    args=['duckduckgo-mcp-server']
)

try:
    mcp_client = MCPClient(server_parameters)
    tools = mcp_client.get_tools()
    agent = CodeAgent(
        tools=[tools[0], VisitWebpageTool()],
        model=model,
        max_steps=10
    )
    agent.run(
        "What are the three most popular first names in France, for boys and girls? "
        + "If you struggle with a specific website, try another.\n"
        + "To use the search tool, use always keyword arguments.")
finally:
    mcp_client.disconnect()
