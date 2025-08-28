% Workshop: Development of agentic applications with human-in-the-loop via LangGraph
% Antonio Garcia-Dominguez
% LLMA4SE 2025 - September 2nd, 2025

# Preparation

## Software requirements

* [Git](https://git-scm.com/) client for cloning the repo with the materials
* A recent version of Python 3 (v3.10 or newer)
* [uv](https://github.com/astral-sh/uv) Python dependency manager
  * Install using the website's [instructions](https://docs.astral.sh/uv/getting-started/installation/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman Desktop](https://podman.io/)
  * For running containers (e.g. MCP servers)

## Third-party systems

* We need an OpenAI API key
  * For GPT-4o-mini access
  * To be provided by organizers
* We need a [LangSmith](https://eu.smith.langchain.com/) API key
  * For observability of LM calls
  * Let's sign up and create an API key

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

## Cloning the workshop materials

Clone [this Git repository](https://github.com/agarciadom/llma4se-2025) with the materials:

```bash
git clone https://github.com/agarciadom/llma4se-2025.git
```

## Testing your environment

Let's try running one of the talk examples.

```bash
cd talk/examples/lg-llm-with_server/
cp .env.template .env
# edit .env with your OpenAI and LangSmith API keys
./run-server.sh
```

Try asking a question to the `searcher` agent. For example: "How far is Madrid from Dusseldorf?".

# Building a travel planner agent

## Outline

Work attendees through a LangGraph-powered travel planner agent:

* First iteration can use a fixed workflow: first, we use an LLM to check if they are actually asking about generating a travel plan, and if so, we produce a suggestion directly via the LM
* Second step is to integrate an observability server like LangFuse, so we can always revisit the various calls that were made to the LLM, regardless of where they were made from
* Third step is to add web search to the step that generates the suggestions, to produce more up-to-date information
* Fourth step is to add a way to revise the travel plan based on a suggestion from the user, without every time passing the whole message history to the LLM

# Requirements management agent

## Outline

In this case, we would work through a more free-form agent that would have tools for building up a set of requirements:

* Create tools for adding, removing, listing, and replacing requirements
* Use the ReAct architecture to let the agent call tools as needed
* Introduce interrupts to confirm/reject proposed tool calls
* As a last exercise, introduce either LlamaIndex MCP 


* Second iteration can incorporate web search in the second step, to find more up-to-date information
* Third iteration can do human-in-the-loop to allow for tweaking the travel plan
* Fourth iteration can simulate the booking and users can allow or stop it
* Fifth iteration


# Conclusion

## What we covered

* Items

## Thank you!

Contact me:

a.garcia-dominguez AT york.ac.uk
