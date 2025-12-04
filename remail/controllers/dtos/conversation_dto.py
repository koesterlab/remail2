"""Data Transfer Objects for conversations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ContactDTO:
    """DTO for contact information in conversations."""

    id: int
    first_name: str
    last_name: str
    email: str
    is_known: bool
    type: str  # "business" or "personal"

    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_known": self.is_known,
            "type": self.type,
        }


@dataclass(slots=True)
class ConversationDTO:
    """DTO for conversation information."""

    contacts: list[ContactDTO]
    custom_name: str | None
    type: str  # "conversation" or "group"
    is_favorite: bool

    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            "contacts": [contact.to_dict() for contact in self.contacts],
            "custom_name": self.custom_name,
            "type": self.type,
            "is_favorite": self.is_favorite,
        }

    @classmethod
    def from_service_data(
        cls,
        contacts: list[dict],
        custom_name: str | None,
        conversation_type: str,
        is_favorite: bool,
    ) -> ConversationDTO:
        """
        Create ConversationDTO from service layer data.

        Args:
            contacts: List of contact dictionaries
            custom_name: Custom name for the conversation/group
            conversation_type: Type of conversation ("conversation" or "group")
            is_favorite: Whether conversation is marked as favorite

        Returns:
            ConversationDTO instance
        """
        contact_dtos = [
            ContactDTO(
                id=c["id"],
                first_name=c["first_name"],
                last_name=c["last_name"],
                email=c["email"],
                is_known=c["is_known"],
                type=c["type"],
            )
            for c in contacts
        ]

        return cls(
            contacts=contact_dtos,
            custom_name=custom_name,
            type=conversation_type,
            is_favorite=is_favorite,
        )
