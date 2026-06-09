"""
LLM Client (OpenRouter)
=======================
Same OpenRouter pattern as Week 1, with one addition: tool_call support.
The client passes tool definitions to the model and returns the raw
response so the agent loop can inspect it for tool calls.
"""

import os
from openai import OpenAI

DEFAULT_MODEL = "openai/gpt-oss-20b:free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMClient:
    """
    Thin wrapper around the OpenRouter API.

    Parameters
    ----------
    api_key : str | None
        OpenRouter API key. Reads from OPENROUTER_API_KEY env var if not provided.
    model : str | None
        Model to use. Reads from OPENROUTER_MODEL env var, then falls back to default.
    """

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key not found. "
                "Set OPENROUTER_API_KEY in your .env file."
            )
        self.model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=OPENROUTER_BASE_URL,
        )

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str = "auto",
    ):
        """
        Send a chat request and return the raw API response.

        The agent loop inspects response.choices[0].message for tool_calls
        or a final text answer.

        Parameters
        ----------
        messages : list[dict]
            Full conversation history in OpenAI message format.
        tools : list[dict] | None
            Tool definitions (JSON schema). If None, no tools are passed.
        tool_choice : str
            "auto" lets the model decide; "none" forces a text response.
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        return self.client.chat.completions.create(**kwargs)

    def __repr__(self):
        return f"LLMClient(model='{self.model}')"
