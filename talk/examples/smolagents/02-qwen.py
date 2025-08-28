from smolagents import LiteLLMModel, CodeAgent
from smolagents.default_tools import WebSearchTool, VisitWebpageTool

# Note: 14B still struggles quite a bit.
# Would want 32B, but won't run on my MacBook
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:14b",
    api_base="http://127.0.0.1:11434",
)

agent = CodeAgent(
    tools=[WebSearchTool(), VisitWebpageTool()],
    model=model,
    max_steps=10
)
agent.run(
    "What are the three most popular first names in France, for boys and girls? "
    + "If you struggle with a specific website, try another."
)