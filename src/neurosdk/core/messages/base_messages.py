"""
Base message class for all WebSocket messages
"""

from typing import Any, Optional
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseIncoming(DataClassJsonMixin):
    """
    Incoming Message Base Class
    """

    # this needs to be a dictionary, but for inheritance sake we leave it as Any
    command: str
    data: Any | None = None


@dataclass
class BaseOutgoing(DataClassJsonMixin):
    """
    Outcoming Message Base Class
    """

    game: str
    # this needs to be a dictionary, but for inheritance sake we leave it as Any
    data: Any | None
    command: str
