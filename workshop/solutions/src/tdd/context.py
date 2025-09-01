from dataclasses import dataclass
from typing import Literal, TypedDict

@dataclass
class ContextSchema:
    model_name: Literal[
        'gpt-4o',
        'gpt-4o-mini'
    ] = 'gpt-4o-mini'
