% From workflow-based to fully-agentic applications: smolagents and LangGraph
% Antonio Garcia-Dominguez
% LLMA4SE 2025 - September 2nd, 2025

# Introduction

## Who am I?

* Senior Lecturer in Software Engineering at the [Department of Computer Science](https://www.york.ac.uk/computer-science/) of the U. of York
* Researcher at the [Automated Software Engineering](https://www.york.ac.uk/computer-science/research/groups/automated-software-engineering/) research group
* Work package lead in the [MOSAICO EU project](https://mosaico-project.eu/)

## What is a Language Model?

* Statistical model which predicts the probability of the next token based on previous ones
* Uses mechanisms such as *attention* to focus on key parts of the text and improve its predictions
* Comes in a range of *parameter sizes*:
  * From small LMs that you can run locally, 
  * to large LMs that require server-class GPUs

## Standalone LM limitations

On its own, an LM:

* Can only rely on its own training set
* Can only produce an output:
  * Cannot judge its quality
  * Cannot perform tasks on your behalf
* Is limited by its *context window* on how much information it can consider at a time

## From LMs to agents

For the purposes of this presentation, we will use the definition from [LangGraph](https://langchain-ai.github.io/langgraph/agents/overview/):

Agent = LM + tools + prompt

A *tool* is a piece of manually written code that an LM can invoke to retrieve information or perform an action on our behalf.

## LM uses come in a spectrum

We will move between two extremes:

* Fixed workflow: more predictable
* Agentic workflow: LM plans its own steps

We will try both approaches in the workshop.

## Workflow patterns

(revisit workflow patterns from MOSAICO slides?)

## The ReAct architecture

Yao et al. proposed it in [ICLR 2023](https://par.nsf.gov/biblio/10451467)

![ReAct = Reason + Act](img/iclr2023-react.png)

## Choosing within spectrum

* Preference between predictability and flexibility?
* Consider our LM's capabilities:
  * SLMs: may want more prescriptive workflows
  * LLMs may have sufficient inference power to drive fully-agentic workflows
* Berkeley hosts a [function calling leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)

## Other common augmentations

* Extending prompt with info from elsewhere (retrieval augmented generation)
* Involving users in decisions (human-in-the-loop)
* Asking questions back (multi-turn conversations)
* Explicitly managing agent memories

# Workflows with LangGraph

## What is LangGraph?

## Implementing states and fixed state transitions

## Managing short-term memories as state

## Using LM-based transitions

## Using tools from LM invocations

## Predefined agents (ReAct)

## Human-in-the-loop: interrupting for confirmation

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

* Summarise items

## Thank you!

Materials available here:

[Github repository](url to materials)

Contact me:

a.garcia-dominguez AT york.ac.uk

For more information:

[Personal website](https://www-users.york.ac.uk/~agd516/)