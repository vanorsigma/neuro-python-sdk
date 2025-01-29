from neurosdk.core.action.action_group import ActionGroup, ActionGroupState
from neurosdk.core.action.neuro_handler import NeuroActionHandler
from neurosdk.core.config import SDKConfig
from enum import Enum


class ManagerState(Enum):
    STATE_INERT = 0
    STATE_READY = 1
    STATE_PRIMED = 2


class Manager:
    """Entrypoint class. All games should keep an instance
    of this throughout the lifetime of the game"""

    def __init__(self, config: SDKConfig):
        self._neuro_action_handler = NeuroActionHandler(config)
        self._active_action_group: ActionGroup | None = None
        self._state = ManagerState.STATE_INERT
        self._config = config

        self._neuro_action_handler.add_on_action_executed(
            self._on_action_executed_callback
        )

    @property
    def neuro_action_handler(self) -> NeuroActionHandler:
        return self._neuro_action_handler

    @property
    def active_action_window(self) -> ActionGroup | None:
        return self._active_action_group

    @property
    def state(self) -> ManagerState:
        return self._state

    def _on_action_executed_callback(self, action_name: str):
        if self._active_action_group is None:
            return

        matches = list(
            filter(
                lambda action: action.get_name() == action_name,
                self._active_action_group.actions,
            )
        )
        if len(matches) > 0:
            self.unregister_active_action_window()

    # TODO: rename
    def instantiate_action_window(self) -> ActionGroup:
        self._active_action_group = ActionGroup()
        return self._active_action_group

    def register_active_action_window(self):
        action_group = self._active_action_group
        action_group.guard_state(ActionGroupState.BUILDING)

        context_states = action_group.context_states
        force_states = action_group.force_states

        if context_states["context_enabled"]:
            self.neuro_action_handler.send_context(
                context_states["context_message"], context_states["context_silent"]
            )
        self.neuro_action_handler.register_actions(action_group.actions)

        if force_states["force_enabled"]:
            self.neuro_action_handler.force_actions(
                action_group.actions,
                force_states["force_query"],
                force_states["force_state"],
                force_states["force_ephemeral_context"],
            )

        action_group.set_registered()
        self._state = ManagerState.STATE_PRIMED

    def unregister_active_action_window(self):
        action_group = self._active_action_group
        self.neuro_action_handler.unregister_actions(action_group.actions)
        action_group.set_ended()
        self._active_action_group = None
        self._state = ManagerState.STATE_READY
