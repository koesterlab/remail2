"""Data class for LLM response with structured JSON format."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LLMResponseDTO:
    """Structured DTO for LLM responses with consistent JSON format."""

    content: str
    thinking: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_completion_text(cls, text: str) -> LLMResponseDTO:
        """
        Parse LLM completion text into structured DTO.

        Expects JSON format:
        {
            "content": "The main response text",
            "thinking": "Optional reasoning or thinking process",
            "metadata": {
                "key": "value"
            }
        }

        Args:
            text: The raw completion text from LLM

        Returns:
            Parsed LLMResponseDTO

        Raises:
            ValueError: If the response cannot be parsed as valid JSON
        """
        try:
            data = json.loads(text)

            return cls(
                content=data.get("content", text),
                thinking=data.get("thinking"),
                metadata=data.get("metadata", {}),
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}") from e

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary."""
        return {
            "content": self.content,
            "thinking": self.thinking,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert DTO to JSON string."""
        return json.dumps(self.to_dict())
