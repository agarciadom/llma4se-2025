# from https://github.com/langchain-ai/langchain-mcp-adapters/issues/14
from contextlib import asynccontextmanager

from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
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
    tools = await client.get_tools()
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
        .compile(name="Chatbot with DDG search")
    )

    yield graph
