from langgraph.graph import StateGraph, START, END
from random import random
from typing import Literal, TypedDict

class State(TypedDict):
    flip_result: bool
    messages: list[str]

def flip_coin(_: State) -> State:
    return { "flip_result": random() < 0.5 }

def use_flip_result(state: State) -> Literal["flipped_heads", "flipped_tails"]:
    return "flipped_heads" if state["flip_result"] else "flipped_tails"

def flipped_heads(state: State) -> State:
    return { "messages": [ "You flipped heads!" ]}

def flipped_tails(state: State) -> State:
    return { "messages": [ "You flipped tails!" ]}


builder = StateGraph(State)
builder.add_node(flip_coin)
builder.add_node(flipped_heads)
builder.add_node(flipped_tails)
builder.add_edge(START, "flip_coin")
builder.add_conditional_edges("flip_coin", use_flip_result)
builder.add_edge("flipped_heads", END)
builder.add_edge("flipped_tails", END)


if __name__ == "__main__":
    agent = builder.compile()
    print(agent.invoke(State()))
