import os

from smolagents import OpenAIServerModel, CodeAgent, MCPClient, Tool
from smolagents.default_tools import VisitWebpageTool
from mcp import StdioServerParameters
from typing import Callable

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
)

server_parameters = StdioServerParameters(
    command='uvx',
    args=['duckduckgo-mcp-server']
)

class UserInputSearch(Tool):
    name = "web_search"
    description = """
    This is a tool that searches the Web for a given query. Before doing the
    search, it will ask the user to confirm the search terms, allowing them
    to tweak the query if desired. It will print the results of the query,
    whether it has been updated or not.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "the search query to be performed (which may be changed by the user)"
        },
        "max_results": {
            "type": "integer",
            "description": "the maximum number of results to be returned (avoid asking for more than 10)"
        }
    }
    output_type = "string"
    base_search: Callable[[str, int], str]

    def __init__(self, base_search: Callable[[str, int], str]):
        super().__init__()
        self.base_search = base_search

    def forward(self, query: str, max_results: int):
        updated_query = input(f"The agent is about to search '{query}'.\nIf this is OK, press Enter, otherwise type the changed query: ")
        if updated_query:
            query = updated_query
            print(f"Updated query to {query}")
        return self.base_search(query=query, max_results=max_results)


try:
    mcp_client = MCPClient(server_parameters)
    tools = mcp_client.get_tools()
    agent = CodeAgent(
        tools=[UserInputSearch(tools[0]), VisitWebpageTool()],
        model=model,
        max_steps=10
    )
    agent.run(
        "What are the three most popular first names in France, for boys and girls? "
        + "If you struggle with a specific website, try another.")
finally:
    mcp_client.disconnect()
