% Workshop: Development of agentic applications with human-in-the-loop via LangGraph
% Antonio Garcia-Dominguez
% LLMA4SE 2025 - September 2nd, 2025<br/> [https://github.com/agarciadom/llma4se-2025](https://github.com/agarciadom/llma4se-2025)

# Preparation

## Software requirements

* [Git](https://git-scm.com/) client for cloning the repo with the materials
* A recent version of Python 3 (v3.10 or newer)
* [uv](https://github.com/astral-sh/uv) Python dependency manager
  * Install using the website's [instructions](https://docs.astral.sh/uv/getting-started/installation/)

## Third-party systems

* We need an OpenAI API key
  * For GPT-4o-mini access
  * To be provided by organizers
* We need a [LangSmith](https://eu.smith.langchain.com/) API key
  * For observability of LM calls
  * Sign up needed (free tier is OK for this workshop)
* We need a [Tavily](https://www.tavily.com/) API key
  * For web search
  * Sign up also needed (1000 queries/month for free)

## LangSmith: signing up

![Login/Signup for LangSmith EU](img/langsmith-login.png){width=50%}

## LangSmith: creating API key

::: columns

::: column

![](img/langsmith-create-token.png)

:::

::: column

* Go to Settings - API Keys
* Create a Personal Access Token (e.g. 30d expiry)
* Save the API key to a safe place for now

:::
:::

## Tavily: signup

* We will use Tavily API for web search
* Sign up to [tavily.com](https://www.tavily.com/)

![Copy API key and save it to a safe place](img/tavily-key.png)

## Cloning the workshop materials

Clone [this Git repository](https://github.com/agarciadom/llma4se-2025) with the materials:

```bash
git clone https://github.com/agarciadom/llma4se-2025.git
```

## Plan for the workshop

::: columns

::: column

![Graph to be built](img/final-graph.png)

:::

::: column

Starting from an empty project, we will:

* Create a prebuilt agent based on the ReAct loop
* Create a workflow-driven travel planner agent (see left)

:::

:::

# Search-enabled ReAct agent: familiarisation with Studio

## What you will do

* Understand the structure of a LangGraph project
* Use the ReAct prebuilt agent to test your setup
* Learn the basic use of the LangGraph Studio

## Development environment

* Open `workshop/exercises` in your IDE:
  * [VS Code](https://code.visualstudio.com/) works but not helpful with imports
  * [PyCharm](https://www.jetbrains.com/pycharm/) works but requires marking `src` as source root, by right-clicking on it and using "Mark Directory As"
* From a terminal inside `workshop/exercises`, download the dependencies with:

```bash
uv sync
```

## Entrypoint: langgraph.json

Open the `langgraph.json` file:

```json
{
  "dependencies": ["."],
  "graphs": {
    "prebuilt_searcher": "./src/prebuilt_searcher/graph.py:graph",
    "travel_planner": "./src/travel_planner/graph.py:graph"
  },
  "env": ".env",
  "image_distro": "wolfi"
}
```

`graphs` lists the agents in this project.<br/>
You do not need to change it.

## Environment variables: .env

* We need to provide our API keys to the agents
* Copy `.env.example` to `.env`
* Customise `.env` with your API keys
  * OpenAI, LangSmith, and Tavily
* Note: in CI environments, we would use secrets rather than `.env`

## Writing the prebuilt_searcher

Edit `src/prebuilt_searcher/graph.py`:

* Create a chat model with `init_chat_model`
  * Facade across all LangChain model providers
  * For example, pass `openai:gpt-4o-mini`
* Set `tools` to a list containing `TavilySearch()`
  * Default settings are fine, but can be customised
* Use `create_react_agent` to produce the graph, providing `model` and `tools`
  * Use keyword arguments, e.g. `model=...`

## Starting the prebuilt_searcher

::: columns

::: column

Use a terminal to run LangGraph Studio:

```bash
uv run langgraph dev
```

Select the `prebuilt_searcher` at the top.
You should see the graph on the right.

:::

::: column

![ReAct-based agent with search](./img/prebuilt_searcher.png){width=1200px}

:::

:::

## Testing the prebuilt_searcher

![](./img/input-state.png){width=80%}

* Studio allows inputs according to an *input schema*
* For a ReAct prebuilt, it is `MessagesState`
* Add a "Human" message and press "Submit", e.g.
  "What is the tallest mountain in Peninsular Spain?"

## ReAct may not use tools

![](./img/prebuilt_searcher-no_tools.png){width=70%}

* In ReAct, it's up to the LM to decide
* If we really want it a source, we should say so!
* Add "Please cite your source" message and Submit

## ReAct decides it needs to search

::: columns

::: column

![](./img/prebuilt_searcher-same_thread_cite.png)

:::

::: columns

* We asked for a citation, so it performs a search
* Response includes links
* Note the "turn 2": it's the same thread so
  full chat history is sent.
* Try creating a new thread and asking in one
  go for info + citations.
:::

:::

## The "Trace" tab

::: columns

::: column

* Click on the "Trace" tab
* You can see every step of the graph for a turn
* You can inspect LM and tool calls
* You can check how many tokens were used and how much it cost

:::

::: column

![](img/trace_tab.png)

:::

:::

## Other things to try

* Try hovering over a step and using "View state"
* You can also re-run a graph from a given point
  * This will create a fork
* You can edit the state at a given point and re-run with that changed state
* You can click on a node and toggle an interrupt before or after
  * Equivalent to a debugging breakpoint

# Travel planner: obtaining trip details

## What we will do

* Suppose you want something more controlled:
  an agent that helps someone plan a trip
* You do not want your users to ask anything they want:
  they should only provide the travel details and then
  sit back
* The first step is to obtain this info:
  * Departure city and country
  * Destintion city and country
* We will use *structured outputs* for this

## Context and state schemas

* We want to be able to configure our agent
  * This can be done with a *context schema*
* User will initially only provide a message, but we need to track internally more info
  * We will specify a *input schema* that is a subset of the *overall schema*

## Writing the context schema

Edit `travel_planner/context.py` to add a `ContextSchema` class:

```python
@dataclass
class ContextSchema:
    model_name: Literal[
        'gpt-4o',
        'gpt-4o-mini'
    ] = 'gpt-4o-mini'
```

We use a `@dataclass` so we can set default values.

## Writing the state schema

Edit `travel_planner/state.py`:

```python
def prefer_new(old_value, new_value):
    return new_value or old_value

class State(MessagesState):
    departure_country: Annotated[str, prefer_new]
    departure_city: Annotated[str, prefer_new]
    destination_country: Annotated[str, prefer_new]
    destination_city: Annotated[str, prefer_new]
```

This is the internal state we will track in the graph.
We need *reducers* to combine old state and updates:
users may not give all the information in one go.

## Graph: chat model

Time to edit `travel_planner/graph.py`.

First, a utility function that creates the chat model:

```python
from langgraph.runtime import get_runtime

def get_chat_model():
  runtime = get_runtime(ContextSchema)
  return init_chat_model(
    model=runtime.context.model_name
  )
```

## Graph: structured output model

We will ask the LLM to extract specific bits of information from natural language.
To do this, we will use a [Pydantic](https://docs.pydantic.dev/latest/) model to describe what we want:

```python
class TripDetails(BaseModel):
    departure_city: Optional[str] = None
    departure_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_country: Optional[str] = None
```

## Graph: starting the node

* We are now ready to write our first graph node
* Nodes take a state and return the updates
* `async` can be better for performance

```python
async def identify_destination(state: State) -> Dict[str, Any]:
    model = get_chat_model()
    model_with_output = model.with_structured_output(TripDetails)
    # ... more to follow ...
```

We set up the chat model to produce structured output, according to the Pydantic model.

## Graph: invoking the LM

We call the LM and get the details from the user query:

```python
output = await model_with_output.ainvoke(
    TRIP_DETAILS_TEMPLATE.format(query=state['messages'][-1].content)
)
location = cast(TripDetails, output)
```

* `await` and `ainvoke` needed as function is `async`
* We need to design a template prompt for the LM
* `cast` tells our IDE the expected type for `location`

## Graph: template prompt

At the top of the file, you could add something like this:

```python
TRIP_DETAILS_TEMPLATE = """
You are a travel planner, and you are trying to find out from the user where they are departing from, and where they want to go.

This is their current query:

<query>
{query}
</query>

Respond with their intended travel details. If they have missed a particular detail, do not try to fill it in yourself.
"""
```

`{query}` will be replaced during the `format` call.

## Graph: returning a dict

Let's return to `identify_destination`.

We need a `dict` with the new info - we will use `model_dump` from Pydantic:

```python
return location.model_dump(
  exclude_none=True,
  exclude_unset=True
)
```

## Graph: populating the graph

Let's create the graph with its first node.

Replace the graph assignment at the bottom with:

```python
graph = (
  StateGraph(State, context_schema=ContextSchema, input_schema=MessagesState)
  .add_node(identify_destination)
  .add_edge(START, "identify_destination")
  .compile()
)
```

## Graph: try it out!

Test the graph now:

* Try telling it only some of the information
* Try multiple interactions on the same thread

You should be able to see the state changes from interaction to interaction.

# Travel planner: validating details

## What we will do

* We need to tell the user what is missing
* We need to tell the user when we have everything
* We will use *conditional edges* for this

## ask_for_details node

* Add a new node called `ask_for_details`
* Here are the first lines - add cases for missing the other details:

```python
def ask_for_details(state: State) -> Dict[str, Any]:
    if state.get('departure_country') is None:
         return {"messages": [AIMessage(content='Which country will you be travelling from?')]}
```

## destination_identified node

* Add a node called `destination_identified`
* Should return an update with a new `AIMessage` that mentions the obtained departure and destination locations

## details_known edge

* We need a function to decide where to go from `identify_destination`
* Write the body of this function, so it returns `True` if there are non-`None` values for the departure and destination keys

```python
def details_known(state: State) -> bool:
  # ... write the body ...
```

## Extending the graph

Add the two new nodes. For the conditional edge:

```python
.add_conditional_edges(
  "identify_destination",
  details_known,
  {
    True: "destination_identified",
    False: "ask_for_details"
  }
)
```

The last argument maps return values to nodes.

## Test the graph!

* Try providing only some of the information now: the graph should ask for what is missing
* Once all the information is available, it will tell you what it understood

# Travel planner: methods of transport

## What we will do

* We have departure and destination locations
* We can now use our own prompt to find out how to
  travel between these
* We can then share this information with the user
* We will use a *subgraph* for this

## Extending the state

* Add an `instructions` field to the graph state
* This will contain the instructions to travel that we will eventually collate into a report

## New node: find_transport

* In this node, we will use a *subgraph*
* We want to do a flexible search loop to find the information,
  without polluting the main graph state
* We will:
  * Use `create_react_agent` for the subgraph
  * Ask the subgraph for suggestions
  * Return the suggestions as an update to the `instructions` state key

## find_transport: invoking agent

If you are using an `async` function:

```python
result = await subgraph_travel_instructions.ainvoke({
  "messages": [HumanMessage(template.format(**state))]
})
```

You'll need to write your own template.
We are using `**state`, so you can use `{departure_city}` in the template, for example.

## find_transport: state update

* The return value of `invoke` / `ainvoke` will be the output state of the graph
* Given it is a `MessagesState` for the most part, you can get the text from the
  final message with:

```python
result['messages'][-1].content
```

## Update and test the graph

* Add the `find_transport` node
* Add an edge from `destination_identified` to `find_transport`
* Try the graph - it should show the instructions, which may
  or may not require some web searches
* Use the Trace view to inspect the LLM calls done by the subgraph

# Travel planner: what to see

## What we will do

* We would also like to suggest things to do at the destination
* To save time, we will run this prompt concurrently with the other one
* We will take advantage of the *super-step* concept in LG graphs

## Adding find_things_to_do

* Add a `suggestions` key to the State
* Add a `find_things_to_do` node which uses a subgraph with a different
  prompt, asking things to see and do, and places to have a meal
* The new node should update the `suggestions` state key

## Extending the graph

* Add the `find_things_to_do` node
* Add an edge from `destination_identified` to `find_things_to_do`
* Note how we have two non-conditional edges with the same source?
* Both will be run concurrently after `destination_identified`:
  * The LG graph runs in *super-steps*
  * Semantics are similar to those of a Petri network,
    based on states being propagated through edges
* Try it out!

## Merging into a report

* Add a new `summary_report` node
* It should use a prompt to take in the instructions and the suggestions,
  and combine it into a single unified report that is returned as an
  update to the `messages` state key
* Add edge from `find_things_to_do` to `summary_report`
* Add edge from `find_transport` to `summary_report`
* Try it out!

# Travel planner: human-in-the-loop

## What we will do

* Before we run the prompts, we may want to confirm with
  the user if we got the trip details right
* We will use *interrupts* for this

## Add a destination_approval node

* Between `identify_destination` and `destination_identified`
* The user will be asked to confirm the trip details

```python
def destination_approval(state: State) -> Command[Literal["destination_identified", "identify_destination"]]:
  # ... rest to come ...
```

* `Command`s are used to route from a node, while also updating the state.

## Interrupting the graph

* We use an interrupt to ask something from the user:

```python
feedback = interrupt({"question": "... question to the user .."})
```

* Populate the string so it mentions the departure and destination details
  to be confirmed by the user

## Routing from feedback

* We will use a simple assumption: if they enter an empty string,
  they accept the details, otherwise we send their feedback to
  `identify_destination`

```python
if not feedback or len(feedback.strip()) == 0:
  return Command(goto="destination_identified")
else:
  return Command(
    goto="identify_destination",
    update={"messages": [HumanMessage(content=feedback)]})
```

## Rewiring the graph

* Add the `destination_approval` node
* Conditional edge from `identify_destination` should go to `destination_approval` when the trip details are known
* Try it out!
  * Once details are available, execution will be interrupted
    and you will be asked for a string
  * Approve with empty string, or give feedback

# Open exercise: TDD

## What to do

* Port the TDD exercise from yesterday to LangGraph
* Use a flow that first produces tests in natural language from
  a spec, then has an interrupt to approve or provide feedback
* You can then have a node for generating the code, then approve or
  give feedback
* Use structured outputs to separate parts

# Conclusion

## What we covered

* Built a simple ReAct-based agent with a search tool
* Built a workflow-based agent dedicated to travel planning, using:
  * Structured outputs
  * Subgraphs with ReAct loops
  * Concurrency within super-steps
  * Human-in-the-loop with interrupts

## Thank you!

Materials available here:

[Github repository](https://github.com/agarciadom/llma4se-2025)

Contact me:

a.garcia-dominguez AT york.ac.uk

More about me:

[Personal website](https://www-users.york.ac.uk/~agd516/)