# Smolagents examples for LLMA4SE 2025 talk

This is a series of examples for the [smolagents](https://huggingface.co/docs/smolagents/index) framework for the LLMA4SE 2025 summer school.

To run these examples, you will need this initial preparation:

1. Install [uv](https://docs.astral.sh/uv/).
2. Copy `.env.template` to `.env` and fill in your API keys as needed.
3. Build the Docker image for the `04-docker.py` example by running `./build-docker.sh`.

You can then run each example with:

```shell
uv run example.py
```
