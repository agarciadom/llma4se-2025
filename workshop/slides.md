% Workshop: Development of agentic applications with human-in-the-loop via LangGraph
% Antonio Garcia-Dominguez
% LLMA4SE 2025 - September 2nd, 2025

# Preparation

## Initial dependencies

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman Desktop](https://podman.io/).
* Install [uv](https://github.com/astral-sh/uv)
  * This will be our dependency management tool for Python.
* Install [Ollama](https://ollama.com/download)
  * We will use this to run LLMs locally, while exposing them using an API similar to that of OpenAI's products
  * Once installed, pull an LLM model - some options:
    * `ollama pull gpt-oss:20b`
    * `ollama pull qwen3:4b`
* Clone Github repository with workshop materials

## Testing your environment

For now, try to give some prompts to your LLM using Ollama's desktop client.

If it takes too long to produce an answer, consider an LLM with fewer weights.

# Building a travel planner agent

Work attendees through a LangGraph-powered travel planner agent:

* First iteration can use a fixed workflow: first, we use an LLM to check if they are actually asking about generating a travel plan, and if so, we produce a suggestion directly via the LM
* Second step is to integrate an observability server like LangFuse, so we can always revisit the various calls that were made to the LLM, regardless of where they were made from
* Third step is to add web search to the step that generates the suggestions, to produce more up-to-date information
* Fourth step is to add a way to revise the travel plan based on a suggestion from the user, without every time passing the whole message history to the LLM

# Requirements management agent

In this case, we would work through a more free-form agent that would have tools for building up a set of requirements:

* Create tools for adding, removing, listing, and replacing requirements
* Use the ReAct architecture to let the agent call tools as needed
* Introduce interrupts to confirm/reject proposed tool calls
* As a last exercise, introduce either LlamaIndex MCP 


* Second iteration can incorporate web search in the second step, to find more up-to-date information
* Third iteration can do human-in-the-loop to allow for tweaking the travel plan
* Fourth iteration can simulate the booking and users can allow or stop it
* Fifth iteration


# Observability with LangFuse

# Conclusion

## What we covered

* Items

## Thank you!

Materials available here:

[link text](url to materials)

Contact me:

a.garcia-dominguez AT york.ac.uk
