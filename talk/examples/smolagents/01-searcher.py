import os

from smolagents import OpenAIServerModel, CodeAgent, MCPClient
from mcp import StdioServerParameters

model = OpenAIServerModel(
    model_id="gpt-4o",
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
        tools=tools,
        model=model,
        max_steps=10
    )
    agent.run(
        "What are the three most popular first names in France, for boys and girls? "
        + "If you struggle with a specific website, try another.")
finally:
    mcp_client.disconnect()
