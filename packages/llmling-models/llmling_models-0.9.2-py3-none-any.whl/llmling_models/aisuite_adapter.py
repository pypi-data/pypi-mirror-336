"""Adapter to use AISuite library models with Pydantic-AI."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import aisuite
from pydantic_ai.messages import (
    ModelMessage,
    ModelResponse,
    ModelResponseStreamEvent,
    SystemPromptPart,
    TextPart,
    UserPromptPart,
)
from pydantic_ai.models import Model, ModelRequestParameters, StreamedResponse
from pydantic_ai.result import Usage


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pydantic_ai.settings import ModelSettings


@dataclass(kw_only=True)
class AISuiteStreamedResponse(StreamedResponse):
    """Stream implementation for AISuite."""

    _timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    """Timestamp of when the response was created."""

    def __post_init__(self):
        """Initialize usage."""
        self._usage = Usage()  # Initialize with empty usage

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        """Not supported yet."""
        msg = "Streaming not supported by AISuite adapter"
        raise NotImplementedError(msg) from None
        # Need to yield even though we raise an error
        # to satisfy the async iterator protocol
        if False:  # pragma: no cover
            yield None  # type: ignore

    @property
    def timestamp(self) -> datetime:
        """Get response timestamp."""
        return self._timestamp

    @property
    def model_name(self) -> str:
        """Get response model_name."""
        return "aisuite"


@dataclass
class AISuiteAdapter(Model):
    """Adapter to use AISuite library models with Pydantic-AI."""

    model: str
    """Model identifier in provider:model format"""

    config: dict[str, dict[str, Any]] = field(default_factory=dict)
    """"Provider configurations."""

    def __post_init__(self):
        """Initialize the client."""
        self._client = aisuite.Client(self.config)

    @property
    def model_name(self) -> str:
        """Return the model name."""
        return self.model

    @property
    def system(self) -> str:
        """Return the system/provider name."""
        return "aisuite"

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, Usage]:
        """Make a request to the model."""
        assert self._client
        formatted_messages = []

        # Convert messages to AISuite format
        for message in messages:
            if isinstance(message, ModelResponse):
                formatted_messages.append({
                    "role": "assistant",
                    "content": str(message.parts[0].content),  # type: ignore
                })
            else:  # ModelRequest
                for part in message.parts:
                    if isinstance(part, SystemPromptPart):
                        formatted_messages.append({
                            "role": "system",
                            "content": part.content,
                        })
                    elif isinstance(part, UserPromptPart):
                        formatted_messages.append({
                            "role": "user",
                            "content": str(part.content),  # TODO: deal with media content
                        })

        # Extract settings
        kwargs = {}
        if model_settings:
            if hasattr(model_settings, "temperature"):
                kwargs["temperature"] = model_settings.temperature  # type: ignore
            if hasattr(model_settings, "max_tokens"):
                kwargs["max_tokens"] = model_settings.max_tokens  # type: ignore

        # Make request to AISuite
        response = self._client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            **kwargs,
        )

        # Extract response content
        content = response.choices[0].message.content

        return ModelResponse(
            parts=[TextPart(content)],
            timestamp=datetime.now(UTC),
        ), Usage()  # AISuite doesn't provide token counts yet

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        """Streaming is not supported yet."""
        msg = "Streaming not supported by AISuite adapter"
        raise NotImplementedError(msg) from None
        # Need to yield even though we raise an error
        # to satisfy the async context manager protocol
        if False:  # pragma: no cover
            yield AISuiteStreamedResponse()


if __name__ == "__main__":
    import asyncio

    from pydantic_ai import Agent

    async def test():
        adapter = AISuiteAdapter(
            model="openai:gpt-4o-mini",
            config={
                "anthropic": {"api_key": "your-api-key"},
            },
        )
        agent: Agent[None, str] = Agent(model=adapter)
        response = await agent.run("Say hello!")
        print(response.data)

    asyncio.run(test())
