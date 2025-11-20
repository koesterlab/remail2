from dataclasses import dataclass
from typing import List

from remail.controllers.dtos.conversations import ContactDTO, ThreadPreviewDTO


@dataclass
class ConversationDTO:
    contacts: List[ContactDTO]
    threads: List[ThreadPreviewDTO]
    is_favorite: bool
    customName: str|None
