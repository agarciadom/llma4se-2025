# Workshop materials

# Talk slides

This folder holds the [Pandoc](https://pandoc.org/)-based slides and materials for the LLMA4SE 2025 talk titled "Development of agentic applications
with human-in-the-loop via LangGraph".

## Building the slides

To build the slides, first install [Pandoc](https://pandoc.org/) and either the inotifytools (on Linux) or fswatch (on Mac/Windows).
You can then run:

```bash
./build.sh
```

## Working on the exercises

The [exercises](./exercises/) folder holds the starting code for a series of exercises to learn about the various features in the [LangGraph](https://langchain-ai.github.io/langgraph/) framework for building agentic applications.

You will need to have the following tools installed to do the exercises:

* [Python](https://www.python.org/) 3.10 or later
* [uv](https://docs.astral.sh/uv/)

The `exercises` and `solutions` folders include an `.env.example` file.
For those examples, you will need to copy `.env.exercises` to `.env` and customise it with your own tokens.

To test your agents, start LangGraph Studio from the `exercises` folder by running these commands:

```bash
cd exercises
uv run langgraph dev
```
