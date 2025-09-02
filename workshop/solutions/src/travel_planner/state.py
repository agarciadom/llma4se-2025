from langgraph.graph import MessagesState
from typing_extensions import Annotated


def prefer_new(old_value, new_value):
    return new_value or old_value


class State(MessagesState):
    departure_country: Annotated[str, prefer_new]
    departure_city: Annotated[str, prefer_new]
    destination_country: Annotated[str, prefer_new]
    destination_city: Annotated[str, prefer_new]
    instructions: Annotated[str, prefer_new]
    suggestions: Annotated[str, prefer_new]


def details_known(state: State) -> bool:
    return bool(
        state.get('departure_country') and
        state.get('departure_city') and
        state.get('destination_country') and
        state.get('destination_city')
    )
