from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


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
    .compile(name="Memory-less chatbot")
)

if __name__ == "__main__":
    print("First interaction")
    first_result = graph.invoke(State(messages=[HumanMessage(content="Hello, my name is Antonio!")]))
    for msg in first_result["messages"]:
        msg.pretty_print()

    print("\n---\nSecond interaction")
    second_result = graph.invoke(State(messages=[HumanMessage(content="Do you remember my name?")]))
    for msg in second_result["messages"]:
        msg.pretty_print()
