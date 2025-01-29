from neurosdk.core.action.neuro_action import NeuroAction
from enum import Enum
from typing import Callable, Any


class ActionGroupError(BaseException):
    pass


class ActionGroupState(Enum):
    BUILDING = 0
    REGISTERED = 1
    FORCED = 2
    ENDED = 3


# TODO: use a factory pattern, actually
class ActionGroup:
    def __init__(self) -> None:
        self._actions: list[NeuroAction] = []
        self._state = ActionGroupState.BUILDING

        self._context_enabled = False
        self._context_message = ""
        self._context_silent = False

        self._force_enabled = False
        self._force_query = ""
        self._force_state = ""
        self._force_ephemeral_context = False

    @property
    def actions(self):
        return self._actions

    @property
    def force_states(self) -> dict[str, Any]:
        return {
            "force_enabled": self._force_enabled,
            "force_query": self._force_query,
            "force_state": self._force_state,
            "force_ephemeral_context": self._force_ephemeral_context,
        }

    @property
    def context_states(self) -> dict[str, Any]:
        return {
            "context_enabled": self._context_enabled,
            "context_message": self._context_message,
            "context_silent": self._context_silent,
        }

    def set_registered(self):
        self.guard_state(ActionGroupState.BUILDING)
        self._state = ActionGroupState.REGISTERED

    def set_ended(self):
        self._state = ActionGroupState.ENDED

    def set_force(
        self, query: str, state: str | None, ephemeral_context: bool = False
    ) -> None:
        self.guard_state(ActionGroupState.BUILDING)

        self._force_enabled = True
        self._force_query = query
        self._force_state = state
        self._force_ephemeral_context = ephemeral_context

    def set_context(self, message: str, silent: bool = False) -> None:
        self._context_enabled = True
        self._context_message = message
        self._context_silent = silent

    def add_action(self, action: NeuroAction) -> None:
        self.guard_state(ActionGroupState.BUILDING)

        if action.can_be_used():
            self.actions.append(action)

    def guard_state(self, expected_state: ActionGroupState):
        if self._state == expected_state:
            return
        raise ActionGroupError(
            f"Expected State: {expected_state}, Current State: {self._state}"
        )
