import instructor
from typing import Type
from pydantic import BaseModel


class StructuredOutputEnforcer:
    """
    Wraps an OpenAI-compatible LLM client
    and enforces structured Pydantic output.
    """

    def __init__(self, response_model: Type[BaseModel]):
        self.response_model = response_model

    def wrap(self, base_client):
        """
        Patches the base LLM client with Instructor.
        """
        return instructor.patch(base_client)
