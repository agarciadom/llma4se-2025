from typing import Literal, cast
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.runtime import get_runtime
from langgraph.types import Command, interrupt
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from pydantic import BaseModel

from tdd.state import State
from tdd.context import ContextSchema


def get_chat_model():
    runtime = get_runtime(context_schema=ContextSchema)
    return init_chat_model(runtime.context.model_name)


class ProgramSpecification(BaseModel):
    programming_language: str
    program_specification: str

class TestSuite(BaseModel):
    test_suite: str
    summary: str

class ProgramCode(BaseModel):
    code: str
    programming_language: str
    explanation: str


PROMPT_GET_SPEC = """"
You are a software developer with knowledge of test-driven development.

Your customer has sent you this request for a program:

<request>
{request}
</request>

Extract the desired programming language and the program specification.
"""

PROMPT_GENERATE_TESTS = """
You are a software developer with knowledge of test-driven development.

You have been given this specification for a program:

<specification>
{spec}
</specification>

Produce a list of test cases in natural language (English). There
should be tests for success scenarios (with expected inputs and outputs),
and tests for failure scenarios (with expected errors).
"""

PROMPT_REFINE_TESTS = """
You are a software developer with knowledge of test-driven development.

You have been given this specification for a program:

<specification>
{spec}
</specification>

You have designed the following test suite:

<test_suite>
{test_suite}
</test_suite>

Your testing lead has provided the following feedback:

<feedback>
{feedback}
</feedback>

Revise your test suite based on the above feedback.
"""

PROMPT_GENERATE_PROGRAM = """"
You are a software developer with knowledge of test-driven development.

You have been given this specification for a program:

<specification>
{spec}
</specification>

You have designed the following test suite:

<test_suite>
{test_suite}
</test_suite>

Write the {programming_language} code for the program
that can pass the above tests.
"""


async def get_program_spec(state: State) -> State:
    model = get_chat_model()
    model_with_output = model.with_structured_output(ProgramSpecification)
    prompt = PROMPT_GET_SPEC.format(request=state['messages'][0].content)

    response = await model_with_output.ainvoke(prompt)
    prog_spec = cast(ProgramSpecification, response)
    return {
        "programming_language": prog_spec.programming_language,
        "spec": prog_spec.program_specification
    }


def is_spec_complete(state: State) -> bool:
    return (
        state.get("programming_language") is not None
        and state.get("spec") is not None
    )


async def generate_tests(state: State) -> State:
    model = get_chat_model()
    model_with_output = model.with_structured_output(TestSuite)
    prompt = PROMPT_GENERATE_TESTS.format(**state)
    response = await model_with_output.ainvoke(prompt)
    new_ts = cast(TestSuite, response)
    return {
        "test_suite": new_ts.test_suite,
        "messages": [AIMessage(content=new_ts.test_suite)]
    }


async def ask_for_spec(state: State) -> State:
    message = (
        "Please indicate the programming language." if state.get("programming_language") else
        "Please provide a description of the program." if state.get("spec") else
        "Please describe the desired program, indicating the programming language."
    )
    return { "messages": [AIMessage(content=message)] }


async def test_refinement(state: State) -> Command[Literal["test_refinement", "generate_program"]]:
    feedback = interrupt({
        "question": "If you are happy with the above tests, enter an empty string. Otherwise, provide feedback:"
    })

    if feedback:
        model = get_chat_model()
        model_with_output = model.with_structured_output(TestSuite)
        prompt = PROMPT_REFINE_TESTS.format(
            feedback=feedback, **state
        )
        response = await model_with_output.ainvoke(prompt)
        new_test_suite = cast(TestSuite, response)
        return Command(
            goto="test_refinement",
            update={
                "test_suite": new_test_suite.test_suite,
                "messages": [AIMessage(content=new_test_suite.test_suite)]
            }
        )
    else:
        return Command(goto="generate_program")


async def generate_program(state: State) -> State:
    model = get_chat_model()
    model_with_output = model.with_structured_output(ProgramCode)
    prompt = PROMPT_GENERATE_PROGRAM.format(**state)

    output = await model_with_output.ainvoke(prompt)
    code = cast(ProgramCode, output)
    return {
        "program": code.code,
        "programming_language": code.programming_language,
        "messages": [AIMessage(content=code.explanation)]
    }


graph = (
    StateGraph(State, input_schema=MessagesState, context_schema=ContextSchema)
    .add_node(get_program_spec)
    .add_node(generate_tests)
    .add_node(ask_for_spec)
    .add_node(test_refinement)
    .add_node(generate_program)
    .add_edge(START, "get_program_spec")
    .add_conditional_edges("get_program_spec", is_spec_complete, {False: "ask_for_spec", True: "generate_tests"})
    .add_edge("generate_tests", "test_refinement")
)
