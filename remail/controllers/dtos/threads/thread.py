from dataclasses import dataclass, field

from remail.controllers.dtos.conversations import ContactDTO, ThreadPreviewDTO
from .message import MessageDTO

@dataclass
class ThreadDTO(ThreadPreviewDTO):
    title: str
    messages: list[MessageDTO]
