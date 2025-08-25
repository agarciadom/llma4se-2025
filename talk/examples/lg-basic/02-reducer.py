from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from operator import add


class State(TypedDict):
    user_name: str
    messages: Annotated[list[str], add]


def hello(state: State) -> State:
    return { "messages": ["Hello {}!".format(state["user_name"])] }


def bye(state: State) -> State:
    return { "messages": ["Bye {}!".format(state["user_name"])] }


builder = StateGraph(State)
builder.add_node("hello", hello)
builder.add_node("bye", bye)
builder.add_edge(START, "hello")
builder.add_edge("hello", "bye")
builder.add_edge("bye", END)

if __name__ == "__main__":
    graph = builder.compile()
    print(graph.invoke(State(user_name="Antonio")))
