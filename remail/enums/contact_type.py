from enum import Enum


class ContactType(Enum):
    BUSINESS = "business"
    PERSONAL = "personal"


__all__ = ["ContactType"]
