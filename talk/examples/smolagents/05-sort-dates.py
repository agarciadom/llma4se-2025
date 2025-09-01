import os

from dotenv import load_dotenv
from smolagents import OpenAIServerModel, CodeAgent
from smolagents.default_tools import DuckDuckGoSearchTool, VisitWebpageTool

load_dotenv()

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
)

with CodeAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    max_steps=10
) as agent:
  agent.run(
    """
    I have these dates:

    * 28 January 2023
    * 2025/11/06
    * February 23rd, 2024

    Sort them from earliest to oldest, and format them as YYYY/MM/DD.
    """)