from dataclasses import dataclass

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
    sent_at: str
