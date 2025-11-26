from dataclasses import dataclass
from typing import List

from .contact import ContactDTO
from .thread_preview import ThreadPreviewDTO


@dataclass
class ConversationDTO:
    contacts: List[ContactDTO]
    threads: List[ThreadPreviewDTO]
    is_favorite: bool
    customName: str|None
