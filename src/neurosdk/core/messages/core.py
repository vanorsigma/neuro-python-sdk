"""
All core messages
"""

from typing import Literal, Optional, Any
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, DataClassJsonMixin, config
from neurosdk.core.messages.base_messages import BaseOutgoing


@dataclass
class Startup(BaseOutgoing):
    """
    Startup action
    """

    data: None = None
    command: Literal["startup"] = "startup"


@dataclass
class ContextData(DataClassJsonMixin):
    """
    Context data
    """

    message: str
    silent: bool


@dataclass
class Context(BaseOutgoing):
    """
    Context
    """

    data: ContextData
    command: Literal["context"] = "context"
