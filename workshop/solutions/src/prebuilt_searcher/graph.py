from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

model = init_chat_model('openai:gpt-4o-mini')
tools = [TavilySearch()]

graph = create_react_agent(
    model=model,
    tools=tools
)
