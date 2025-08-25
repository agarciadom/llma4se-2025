from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    timeout=10,
    max_tokens=5_000
)

class State(MessagesState):
    # nothing else
    pass


def call_model(state: State) -> Dict[str, Any]:
    return { "messages": llm.invoke(state["messages"]) }


# Define the graph
graph = (
    StateGraph(State)
    .add_node(call_model)
    .add_edge(START, "call_model")
    .compile(name="Chatbot from LangGraph Server")
)
