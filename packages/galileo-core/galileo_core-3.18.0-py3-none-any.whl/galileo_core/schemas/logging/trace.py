from typing import Literal, Optional

from pydantic import Field

from galileo_core.schemas.logging.span import (
    Span,  # noqa: F401  # to solve forward reference issues
    StepWithChildSpans,
)
from galileo_core.schemas.logging.step import BaseStep, StepType


class BaseTrace(BaseStep):
    type: Literal[StepType.trace] = Field(default=StepType.trace)
    input: str = Field()
    output: Optional[str] = Field(default=None)


class Trace(BaseTrace, StepWithChildSpans):
    pass
