from typing import TypedDict, Any, Dict

from langgraph.constants import START
from langgraph.graph import StateGraph

# Minimal code to allow LangGraph to run

class State(TypedDict):
    pass

def node(state: State) -> Dict[str, Any]:
    return {}

# Exercise: replace this with a prebuilt React
# agent with Tavily tool for search.
graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .compile()
)
