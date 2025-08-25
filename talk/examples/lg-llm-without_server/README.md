# LangGraph + OpenAI examples without LangGraph Server

This is a series of examples for the LangGraph APIs, which do not use the LangGraph server.

To run these examples, copy the `.env.template` to `.env` and customise its variables accordingly.

## Need for checkpointing

The `01-start.py` to `03-checkpointer.py` examples cover the need for checkpointing.
To run them, invoke these commands:

```shell
uv run --env-file=.env 01-start.py
uv run --env-file=.env 02-thread.py
uv run --env-file=.env 03-checkpointer.py
```
