from typing import Any, Dict

from langgraph.constants import START
from langgraph.graph import StateGraph
from travel_planner.state import State

# Minimal code to allow LangGraph to run

def node(state: State) -> Dict[str, Any]:
    return {}

# Exercise: replace this with a travel planner
# agent with Tavily tool for search.
graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .compile()
)
