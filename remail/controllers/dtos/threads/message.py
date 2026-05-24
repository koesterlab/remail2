from dataclasses import dataclass, field
from datetime import datetime

from remail.models import Email

from .attachment import AttachmentDTO
from .sender import SenderDTO


@dataclass
class MessageContentDTO:
    body: str
    attachments: list[AttachmentDTO]


@dataclass
class MessageDTO:
    id: int
    sender: SenderDTO
    subject: str
    content: MessageContentDTO
    sent_at: datetime
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None

    @staticmethod
    def from_model(mail: Email):
        return MessageDTO(
            id=mail.id if mail.id else -1,
            sender=SenderDTO(
                id=mail.sender.id,
                first_name=mail.sender.first_name if mail.sender.first_name else "",
                last_name=mail.sender.last_name
                if mail.sender.last_name
                else mail.sender.name
                if mail.sender.name
                else "",
                email=mail.sender.email_address,
            ),
            subject=mail.thread.title,
            content=MessageContentDTO(
                body=mail.body,
                attachments=[
                    AttachmentDTO(
                        file_name=att.filename,
                        file_size=0,
                        file_type="application/octet-stream",
                        url=f"/attachments/{att.id}",
                    )
                    for att in mail.attachments
                ],
            ),
            sent_at=mail.sent_at,
            tags=[t.tag for t in mail.tags],
            due_date=mail.due_date,
        )