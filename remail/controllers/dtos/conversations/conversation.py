from dataclasses import dataclass
from typing import List

from remail.controllers.dtos.conversations import ContactDTO
from remail.controllers.dtos.threads.thread import ThreadDTO


@dataclass
class ConversationDTO:
    contacts: List[ContactDTO]
    threads: List[ThreadDTO]
    is_favorite: bool
    customName: str|None
