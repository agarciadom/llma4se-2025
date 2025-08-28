#!/bin/bash

if ! test -f .env; then
  echo "Please copy .env.template to .env and edit .env with your API keys."
  exit 1
fi

uv run langgraph dev