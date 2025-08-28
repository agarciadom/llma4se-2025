
from dataclasses import dataclass
from typing import Annotated

from langgraph.graph import MessagesState

def first_value(a, b):
    return a or b


@dataclass
class State(MessagesState):
    departure_country: str = None
    departure_city: str = None
    destination_country: str = None
    destination_city: str = None
    instructions: Annotated[str, first_value] = None
    suggestions: Annotated[str, first_value] = None


def details_known(state: State) -> bool:
    return (
        state.get('departure_country') is not None and
        state.get('departure_city') is not None and
        state.get('destination_country') is not None and
        state.get('destination_city') is not None
    )
