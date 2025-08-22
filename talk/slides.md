% From workflow-based to fully-agentic applications: smolagents and LangGraph
% Antonio Garcia-Dominguez
% LLMA4SE 2025 - September 2nd, 2025

# Introduction

## Who am I?

* Senior Lecturer in Software Engineering at [Department of Computer Science](https://www.york.ac.uk/computer-science/) of the University of York
* Researcher at the [Automated Software Engineering](https://www.york.ac.uk/computer-science/research/groups/automated-software-engineering/) research group
* Work package lead in the [MOSAICO EU project](https://mosaico-project.eu/)

## What is a Language Model?

* Statistical model which predicts the probability of the next token based on previous ones
* Uses mechanisms such as *attention* to focus on key parts of the text and improve its predictive capabilities
* Comes in a range of *parameter sizes*: from Small Language Models that you can run on your own computer, to Large Language Models that may require server-class GPUs to run

## Limitations of a standalone LM

On its own, an LM:

* Can only rely on its own training set to answer prompts
* Can only produce an output, not judge it, or perform tasks on your behalf
* Is limited by its *context window* on how many tokens it can consider at a time

## The ReAct architecture for LMs

In their ICLR 2023 paper, Yao et al. proposed a prompt engineering approach to improve result quality from LMs:

(include figure from paper, with its various options)

## Agents: building on top of LLMs

For the purposes of this presentation, we will use the definition from [LangGraph](https://langchain-ai.github.io/langgraph/agents/overview/):

Agent = LM + tools + prompt

A *tool* is a piece of manually written code that an LM can invoke to retrieve information or perform an action on our behalf.

## LM-based applications come in a spectrum

We can think of LM uses as being between two extremes:

* A fixed workflow with specific steps to follow: more predictable
* An agentic workflow where the LM decides the steps it must take

We will start with the first, and move later to the other extreme.

## Other common augmentations for LMs

* Extending prompt with info from elsewhere (retrieval augmented generation)
* Involving the user in decision-making (human-in-the-loop)
* Allowing LM to ask questions back (multi-turn conversations)
* Managing its short- and long-term memories (avoid exceeding context window)

## How to choose within the spectrum?

* Consider our preference between predictability and flexibility
* Consider our LM's capabilities:
  * We may want to use more prescriptive workflows for SLMs
  * LLMs may have sufficient inference power to drive fully-agentic workflows
* Berkeley hosts a [function calling leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)

# Workflows with LangGraph

## What is LangGraph?

## Implementing states and fixed state transitions

## Managing short-term memories as state

## Using LM-based transitions

## Using tools from LM invocations

## Human-in-the-loop: interrupting for confirmation

# Agentic applications with LangGraph

## The predefined ReAct agent

## Need for observability: LangFuse

## Tradeoffs against predefined workflows

## Reuse from other systems: LangGraph AP

# Agentic applications in Smolagents

## What is Smolagents?

## MultiStepAgent: ReAct in SmolAgents

## CodeAgent: Pythonic tool calling

## Implementing guardrails in tool calls

## Incorporating external tools via MCP

## Using step callbacks to allow human-in-the-loop

## Reuse from other systems: other protocols

# Conclusion

## What we covered

* Items

## Thank you!

Materials available here:

[link text](url to materials)

Contact me:

a.garcia-dominguez AT york.ac.uk

For more information:

https://www-users.york.ac.uk/~agd516/