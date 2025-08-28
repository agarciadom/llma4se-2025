import os

from smolagents import OpenAIServerModel, CodeAgent
from smolagents.default_tools import DuckDuckGoSearchTool, VisitWebpageTool

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
)

with CodeAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    max_steps=10,
    executor_type="docker",
    executor_kwargs={
        "build_new_image": False,
        "image_name": "jupyter-kernel-custom"
    }
) as agent:
  agent.run(
      "What are the three most popular first names in France, for boys and girls? "
      + "If you struggle with a specific website, try another.")