"""
All actions messages
"""

from typing import Literal, Any
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, DataClassJsonMixin, config
from neurosdk.core.messages.base_messages import BaseOutgoing, BaseIncoming


@dataclass
class Action(DataClassJsonMixin):
    """
    Action base class
    """

    name: str
    description: str
    schema_: dict[str, Any] | None = field(
        default=None, metadata=config(field_name="schema")
    )


@dataclass
class RegisterAction(BaseOutgoing):
    """
    Register action
    """

    data: dict[Literal["actions"], list[Action]]
    command: Literal["actions/register"] = "actions/register"


@dataclass
class ReregisterAllActions(BaseOutgoing):
    """
    Re-register action
    """

    data: None = None
    command: Literal["actions/reregister_all"] = "actions/reregister_all"


@dataclass
class UnregisterAction(BaseOutgoing):
    """
    Unregister action
    """

    data: dict[Literal["action_names"], list[str]]
    command: Literal["actions/unregister"] = "actions/unregister"


@dataclass
class ForceActionData(DataClassJsonMixin):
    """
    Force Actions' data field value
    """

    state: str | None
    query: str
    ephemeral_context: bool | None
    action_names: list[str]


@dataclass
class ForceAction(BaseOutgoing):
    """
    Force action
    """

    data: ForceActionData
    command: Literal["actions/force"] = "actions/force"


@dataclass
class ResultActionData(DataClassJsonMixin):
    """
    Result action data
    """

    id: str
    success: bool
    message: str | None


@dataclass
class ResultAction(BaseOutgoing):
    """
    Result action
    """

    data: ResultActionData
    command: Literal["action/result"] = "action/result"


@dataclass
class IncomingActionData(DataClassJsonMixin):
    """
    IncomingAction Data
    """

    id: str
    name: str
    data: str | None


@dataclass
class IncomingAction(BaseIncoming):
    """
    IncomingAction
    """

    data: IncomingActionData
    command: Literal["action"]
