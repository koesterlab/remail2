from enum import Enum


class Timezone(str, Enum):
    EUROPE_BERLIN = "europe-berlin"


__all__ = ["Timezone"]
