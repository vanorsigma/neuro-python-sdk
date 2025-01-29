from neurosdk.core.action.neuro_action import NeuroAction
from typing import Any
from dataclasses import dataclass


@dataclass
class Option:
    name: str
    description: str
    context: str


class PickOptionAction(NeuroAction):
    def __init__(self, options: list[Option]):
        self._options = options

    def get_name(self) -> str:
        return "Pick an option"

    def get_description(self) -> str:
        return f'Pick an option from the following: {", ".join([option.description for option in self._options])}'

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "choice": {"type": "integer", "description": "The choice made"}
            },
            "required": ["choice"],
        }

    def validate_action(self, data, state) -> None:
        pass

    def execute_action(self) -> None:
        pass
