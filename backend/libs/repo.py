from abc import ABC
from typing import Any


class Repository(ABC):
    session: Any

    def __init__(self, session: Any):
        self.session = session