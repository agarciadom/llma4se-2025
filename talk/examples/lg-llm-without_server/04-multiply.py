from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

@tool
def multiply(left, right):
    """
    Multiplies the left operand by the right operand, and returns the result.
    """
    return left * right


llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0.1,
    timeout=10,
    max_tokens=5_000
)
tools = [multiply]
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
    .compile(
        name="Chatbot with multiply tool",
        checkpointer=InMemorySaver())
)

if __name__ == "__main__":
    thread_id = "1"
    config = {"configurable": {"thread_id": thread_id}}
    first_result = graph.invoke(
        State(messages=[HumanMessage(content="What is the result of 40 times 3?")]),
        config=config
    )
    for msg in first_result["messages"]:
        msg.pretty_print()

    second_result = graph.invoke(
        State(messages=[HumanMessage(content="Multiply that by 6")]),
        config=config
    )
    for msg in second_result["messages"]:
        msg.pretty_print()
