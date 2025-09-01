# Talk slides

This folder holds the [Pandoc](https://pandoc.org/)-based slides and examples for the LLMA4SE 2025 talk titled "From workflow-based to fully-agentic applications: smolagents and LangGraph".

## Building the slides

To build the slides, first install [Pandoc](https://pandoc.org/) and either the inotifytools (on Linux) or [fswatch](https://emcrisostomo.github.io/fswatch/) (on Mac/Windows).
You can then run:

```bash
./build.sh
```

## Running the examples

The [examples](./examples) folder contains Python-based projects with the various examples mentioned in the talk.
You will need to have the following tools installed to try them out:

* [Python](https://www.python.org/) 3.10 or later
* [uv](https://docs.astral.sh/uv/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Some of the examples include an `.env.template` file.
For those examples, you will need to copy `.env.template` to `.env` and customise it with your own tokens.
You can then run the example with:

```bash
uv run --env-file .env example.py
```

The `lg-basic` example does not require an `.env` file, so it can be run with just:

```bash
uv run example.py
```