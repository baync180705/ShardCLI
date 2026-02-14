from pydantic import BaseModel, Field
from typing import Literal, Optional


class CommandGenerationResult(BaseModel):
    """
    Structured response returned by the LLM
    for terminal command generation.
    """

    command: Optional[str] = Field(
        description="The generated shell command"
    )

    explanation: Optional[str] = Field(
        description="Short explanation of what the command does"
    )

    risk: Literal["low", "medium", "high"] = Field(
        description="Risk classification of the command"
    )

    raw_response: Optional[str] = Field(
        default=None,
        description="Original LLM response if parsing fails"
    )

    note: Optional[str] = Field(
        default=None,
        description="Optional note for the user about execution caveats or limitations"
    )
