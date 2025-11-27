"""LLM controller for managing LLM operations."""

from __future__ import annotations

from typing import Any

from remail.controllers.dto import LLMResponseDTO
from remail.interfaces.llm.llm_service import LLMService


class LLMController:
    """Controller for LLM operations."""

    def __init__(self):
        """Initialize LLM controller."""

        self.service = LLMService()

    def generate_completion(
        self,
        prompt: str,
        max_tokens: int | None = None,
        temperature: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate text completion from prompt.

        Args:
            prompt: Input prompt for the LLM
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 2.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict with status, message, and structured LLMResponseDTO
        """
        try:
            completion_response = self.service.generate_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs,
            )

            # Extract the completion text
            completion_text = completion_response.completion_text

            # Parse the JSON response into structured DTO
            response_dto = LLMResponseDTO.from_completion_text(completion_text)

            return {
                "status": "success",
                "message": "Completion generated successfully",
                "completion": response_dto.content,
                "thinking": response_dto.thinking,
                "metadata": response_dto.metadata,
                "response_dto": response_dto,
            }

        except ValueError as e:
            return {
                "status": "error",
                "message": f"Failed to parse LLM response: {str(e)}",
                "completion": "",
                "thinking": None,
                "metadata": {},
            }

        except RuntimeError as e:
            return {
                "status": "error",
                "message": str(e),
                "completion": "",
                "thinking": None,
                "metadata": {},
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Completion generation failed: {str(e)}",
                "completion": "",
                "thinking": None,
                "metadata": {},
            }
