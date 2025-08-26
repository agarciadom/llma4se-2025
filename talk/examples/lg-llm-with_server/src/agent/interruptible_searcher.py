# from https://github.com/langchain-ai/langchain-mcp-adapters/issues/14
from contextlib import asynccontextmanager

from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.prebuilt.interrupt import ActionRequest, HumanInterrupt, HumanResponse, HumanInterruptConfig
from langgraph.types import interrupt
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0.1,
    timeout=10,
    max_tokens=5_000
)

@asynccontextmanager
async def make_graph():
    client = MultiServerMCPClient(
        {
            "ddg": {
                "command": "uvx",
                "args": ["duckduckgo-mcp-server"],
                "transport": "stdio"
            }
        }
    )

    mcp_tools = await client.get_tools()
    search_tool = next(e for e in mcp_tools if e.name == 'search')
    fetch_tool = next(e for e in mcp_tools if e.name != 'search')

    @tool(
        description=search_tool.description,
        args_schema=search_tool.args_schema
    )
    async def search_with_permission(config: RunnableConfig, **tool_input):
        request = HumanInterrupt(
            action_request=ActionRequest(
                action=search_tool.name,
                args=tool_input
            ),
            config=HumanInterruptConfig(
                allow_ignore=False,
                allow_respond=True,
                allow_edit=False,
                allow_accept=True
            ),
            description="Please review the search request before execution"
        )
        response = interrupt(request)
        if response["type"] == "accept":
            return await search_tool.ainvoke(tool_input, config)
        elif response["type"] == "response":
            return "The user interrupted the search request, and gave this feedback:\n{}".format(response["args"])
        else:
            raise ValueError("Unknown response type {}".format(response["type"]))

    tools = [search_with_permission, fetch_tool]
    llm_with_tools = llm.bind_tools(tools)

    class State(MessagesState):
        # nothing else
        pass

    def call_model(state: State) -> Dict[str, Any]:
        return { "messages": llm_with_tools.invoke(state["messages"]) }

    # Define the graph
    graph = (
        StateGraph(State)
        .add_node(call_model)
        .add_node("tools", ToolNode(tools))
        .add_edge(START, "call_model")
        .add_conditional_edges("call_model", tools_condition)
        .add_edge("tools", "call_model")
        .compile(name="Chatbot with interruptible DDG search")
    )

    yield graph
