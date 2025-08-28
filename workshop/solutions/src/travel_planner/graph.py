from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, cast, Optional, Callable, Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_tavily import TavilySearch
from langgraph.constants import START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command, interrupt
from pydantic import BaseModel

from travel_planner.context import ContextSchema
from travel_planner.state import State, details_known
from langchain.chat_models import init_chat_model

from langgraph.graph import StateGraph
from langgraph.runtime import get_runtime


@dataclass
class TripDetails(BaseModel):
    departure_city: Optional[str] = None
    departure_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_country: Optional[str] = None


TRIP_DETAILS_TEMPLATE = """
You are a travel planner, and you are trying to find out from the user
where they are departing from, and where they want to go.

This is their current query:

<query>
{query}
</query>

Respond with their intended travel details. If they have missed a particular
detail, do not try to fill it in yourself.
"""

TRIP_DETAILS_UPDATE_TEMPLATE = """
Thank you for the new information. Your trip details are:

  * Departure from {departure_city} ({departure_country})
  * Arrival to {destination_city} ({destination_country})

I will search the internet to find you some instructions on how
to get there, and things you can do once you arrive.
"""

TRIP_INSTRUCTIONS_TEMPLATE = """
You are a travel agent. Your customer has told you they want to go
from {departure_city} (in {departure_country}) to {destination_city}
(in {destination_country}). Please give them some recommendations on
how to travel, balancing cost, travel time. You can search on the
internet to find options if you like.
"""

TRIP_THINGS_TO_DO_TEMPLATE = """
You are a travel agent. Your customer has told you they want to go
from {departure_city} from {departure_city} (in {departure_country})
to {destination_city} (in {destination_country}). Please suggest
things to do, things to see, and places to have a meal in the area.
You can search on the internet to find options if you like.
"""

TRIP_SUMMARY_TEMPLATE = """
You are a travel agent. Your customer has told you they want to go
from {departure_city} from {departure_city} (in {departure_country})
to {destination_city} (in {destination_country}).

You have checked how to get there, and have seen these options:

<travel_options>
{instructions}
</travel_options>

You have also considered various things to do and tips to give them:

<things_to_do>
{suggestions}
</things_to_do>

Combine the above pieces of information into a unified report,
and explain it in simple terms to the customer. Do not add anything
outside of the above information to the report. This is your final
interaction with the user: do not offer any follow-up interactions.
"""


def get_chat_model():
    runtime = get_runtime(ContextSchema)
    return init_chat_model(
        model=runtime.context.model_name
    )

async def identify_destination(state: State) -> Dict[str, Any]:
    model = get_chat_model()
    model_with_output = model.with_structured_output(TripDetails)

    output = await model_with_output.ainvoke(
        TRIP_DETAILS_TEMPLATE.format(query=state['messages'][-1].content)
    )
    location = cast(TripDetails, output)

    updates = location.model_dump(exclude_none=True, exclude_unset=True)
    if not location.departure_country and 'departure_country' not in state:
            return {"messages": [AIMessage(content='Which country will you be travelling from?')]} | updates
    elif not location.departure_city and 'departure_city' not in state:
            return {"messages": [AIMessage(content='Which city will you be travelling from?')]} | updates
    elif not location.destination_country and 'destination_country' not in state:
            return {"messages": [AIMessage(content='Which country will you be travelling to?')]} | updates
    elif not location.destination_city and 'destination_city' not in state:
            return {"messages": [AIMessage(content='Which city will you be travelling to?')]} | updates

    if updates:
        return {
            "messages": [
                AIMessage(TRIP_DETAILS_UPDATE_TEMPLATE.format(**(state | updates)))
            ]
        } | updates

    return updates


def destination_approval(state: State) -> Command[Literal["destination_identified", "identify_destination"]]:
    feedback = interrupt({
        "question": "I understand that you wish to travel from {departure_city} in {departure_country} to {destination_city} in {destination_country}. Please confirm with an empty string, or provide feedback otherwise.".format(**state)
    })
    if not feedback or len(feedback.strip()) == 0:
        return Command(goto="destination_identified")
    else:
        return Command(goto="identify_destination",
                       update={
                        "messages": [HumanMessage(content=feedback)]
                       })


# This is just a marker for concurrent branching
def destination_identified(state: State):
    return {}


def subgraph_for_prompt_template(key: str, template: str) -> Callable:
    """
    Creates a ReAct subgraph that runs a prompt by passing the current state
    through a static template.
    Args:
        key (str): The state key where the result will be stored.
        template (str): The static template to use.
    """
    async def call_subgraph(state: State) -> Dict[str, Any]:
        subgraph_travel_instructions = create_react_agent(
            model=get_chat_model(),
            tools=[TavilySearch()]
        )
        result = await subgraph_travel_instructions.ainvoke({
            "messages": [HumanMessage(template.format(**state))]
        })
        return {
            key: result['messages'][-1].content
        }

    return call_subgraph


async def summary_report(state: State) -> Dict[str, Any]:
    model = get_chat_model()
    result = await model.ainvoke([HumanMessage(TRIP_SUMMARY_TEMPLATE.format(**state))])
    return {
        "messages": [result]
    }


graph = (
    StateGraph(State, context_schema=ContextSchema)
    .add_node(identify_destination)
    .add_node("find_travel_instructions", subgraph_for_prompt_template("instructions", TRIP_INSTRUCTIONS_TEMPLATE))
    .add_node("find_things_to_do", subgraph_for_prompt_template("suggestions", TRIP_THINGS_TO_DO_TEMPLATE))
    .add_node(destination_approval)
    .add_node(destination_identified)
    .add_node(summary_report)
    .add_edge(START, "identify_destination")
    .add_conditional_edges("identify_destination", details_known, {False: END, True: "destination_approval"})
    .add_edge("destination_identified", "find_travel_instructions")
    .add_edge("destination_identified", "find_things_to_do")
    .add_edge("find_travel_instructions", "summary_report")
    .add_edge("find_things_to_do", "summary_report")
    .compile(name="Travel Planner")
)
