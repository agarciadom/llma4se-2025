
from typing import Annotated
from langgraph.graph import MessagesState


def prefer_new(old_value, new_value):
    return new_value or old_value


class State(MessagesState):
    spec: Annotated[str, prefer_new]
    test_suite: Annotated[str, prefer_new]
    program: Annotated[str, prefer_new]
    programming_language: Annotated[str, prefer_new]
