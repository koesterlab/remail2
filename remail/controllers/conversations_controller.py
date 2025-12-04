"""Conversations controller for managing conversation operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from remail.controllers.dto.conversation_dto import ConversationDTO
from remail.interfaces.email.services.conversation_service import ConversationService

if TYPE_CHECKING:
    pass


class ConversationsController:
    """Controller for conversation operations."""

    def __init__(self):
        """
        Initialize conversations controller.
        """

        self.service = ConversationService()

    def get_conversations(self, user_id: int) -> list[ConversationDTO]:
        """
        Fetch all conversations for the frontend for a specific user.

        Args:
            user_id: User ID to fetch conversations for

        Returns:
            List of ConversationDTO objects with user-specific favorite status
        """

        conversations_data = self.service.get_all_conversations(user_id)

        return [
            ConversationDTO.from_service_data(
                contacts=conv["contacts"],
                custom_name=conv["custom_name"],
                conversation_type=conv["type"],
                is_favorite=conv["is_favorite"],
            )
            for conv in conversations_data
        ]
