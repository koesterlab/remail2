"""Tests for conversation DTOs."""

from remail.controllers.dto.conversation_dto import ContactDTO, ConversationDTO


class TestContactDTO:
    """Test suite for ContactDTO."""

    def test_create_contact_dto(self):
        """Test creating a ContactDTO."""
        contact = ContactDTO(
            id=1,
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            type="personal",
            is_known=True,
        )

        assert contact.id == 1
        assert contact.email == "test@example.com"
        assert contact.first_name == "John"
        assert contact.last_name == "Doe"
        assert contact.type == "personal"
        assert contact.is_known is True

    def test_contact_dto_to_dict(self):
        """Test converting ContactDTO to dictionary."""
        contact = ContactDTO(
            id=3,
            email="dict@example.com",
            first_name="Jane",
            last_name="Smith",
            type="personal",
            is_known=True,
        )

        result = contact.to_dict()

        assert result == {
            "id": 3,
            "email": "dict@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "type": "personal",
            "is_known": True,
        }


class TestConversationDTO:
    """Test suite for ConversationDTO."""

    def test_create_conversation_dto(self):
        """Test creating a ConversationDTO."""
        contact1 = ContactDTO(
            id=1,
            email="contact1@example.com",
            first_name="John",
            last_name="Doe",
            type="personal",
            is_known=True,
        )
        contact2 = ContactDTO(
            id=2,
            email="contact2@example.com",
            first_name="Jane",
            last_name="Smith",
            type="business",
            is_known=False,
        )

        conversation = ConversationDTO(
            custom_name="Meeting",
            type="conversation",
            contacts=[contact1, contact2],
            is_favorite=True,
        )

        assert conversation.custom_name == "Meeting"
        assert conversation.type == "conversation"
        assert len(conversation.contacts) == 2
        assert conversation.is_favorite is True

    def test_conversation_dto_to_dict(self):
        """Test converting ConversationDTO to dictionary."""
        contact = ContactDTO(
            id=1,
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            type="personal",
            is_known=True,
        )

        conversation = ConversationDTO(
            custom_name="Test Subject",
            type="conversation",
            contacts=[contact],
            is_favorite=True,
        )

        result = conversation.to_dict()

        assert result["custom_name"] == "Test Subject"
        assert result["type"] == "conversation"
        assert result["is_favorite"] is True
        assert len(result["contacts"]) == 1
        assert result["contacts"][0]["email"] == "test@example.com"
        assert result["contacts"][0]["type"] == "personal"

    def test_conversation_dto_from_service_data(self):
        """Test creating ConversationDTO from service data."""
        contacts = [
            {
                "id": 1,
                "email": "contact@example.com",
                "first_name": "Contact",
                "last_name": "Person",
                "type": "personal",
                "is_known": True,
            }
        ]

        conversation = ConversationDTO.from_service_data(
            contacts=contacts,
            custom_name="Service Test",
            conversation_type="conversation",
            is_favorite=True,
        )

        assert conversation.custom_name == "Service Test"
        assert conversation.type == "conversation"
        assert conversation.is_favorite is True
        assert len(conversation.contacts) == 1
        assert conversation.contacts[0].email == "contact@example.com"
        assert isinstance(conversation.contacts[0], ContactDTO)

    def test_conversation_dto_empty_contacts(self):
        """Test ConversationDTO with empty contacts list."""
        conversation = ConversationDTO(
            custom_name="Empty Contacts",
            type="conversation",
            contacts=[],
            is_favorite=False,
        )

        assert len(conversation.contacts) == 0

        result = conversation.to_dict()
        assert result["contacts"] == []
