from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage


llm = init_chat_model(
    "gpt-4o-mini",
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
    .compile(name="Memory-less chatbot (with thread ID)")
)

if __name__ == "__main__":
    thread_id = "1"
    config = {"configurable": {"thread_id": thread_id}}
    print("First interaction with thread ID {} and no checkpointing".format(thread_id))
    first_result = graph.invoke(
        State(messages=[HumanMessage(content="Hello, my name is Antonio!")]),
        config=config
    )
    for msg in first_result["messages"]:
        msg.pretty_print()

    print("\n---\nSecond interaction with thread ID {} and no checkpointing".format(thread_id))
    second_result = graph.invoke(
        State(messages=[HumanMessage(content="Do you remember my name?")]),
        config=config
    )
    for msg in second_result["messages"]:
        msg.pretty_print()
