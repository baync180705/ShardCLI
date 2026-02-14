import os
from groq import Groq
from typing import Optional


class GroqLLMClient:
    """
    Groq LLM wrapper with optional structured output enforcement.
    """

    def __init__(
        self,
        system_prompt: str,
        model: str,
        temperature: float ,
        top_p: float,
        api_key: Optional[str] = None,
        structured_output_enforcer=None,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.top_p = top_p

        base_client = Groq(api_key=self.api_key)

        # Apply structured output enforcement if provided
        if structured_output_enforcer:
            self.client = structured_output_enforcer.wrap(base_client)
            self.response_model = structured_output_enforcer.response_model
        else:
            self.client = base_client
            self.response_model = None

    def generate(self, user_prompt: str):
        """
        Generate command from natural language input.
        Returns Pydantic model if structured output is enabled,
        otherwise raw completion response.
        """

        if self.response_model:
            return self.client.chat.completions.create(
                model=self.model,
                response_model=self.response_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                top_p=self.top_p,
            )

        # Fallback: no structured enforcement
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            top_p=self.top_p,
        )

        return completion.choices[0].message.content
