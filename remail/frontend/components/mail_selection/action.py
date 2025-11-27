from dataclasses import dataclass
from typing import Callable

import flet


@dataclass
class Action:
    title: str
    secondary: str
    on_executed: Callable[[], None]
    color: flet.Colors
    icon: flet.Icons