from enum import Enum


class FontSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


__all__ = ["FontSize"]
