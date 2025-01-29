import json
import os
import sys

import websocket
import threading
import time
from typing import cast, Callable
from neurosdk.core.action.neuro_action import NeuroAction
from neurosdk.core.config import SDKConfig
from neurosdk.core.messages.action import (
    RegisterAction,
    UnregisterAction,
    IncomingAction,
    ForceActionData,
    ForceAction,
    ResultAction,
    ResultActionData,
)
from neurosdk.core.messages.base_messages import BaseIncoming
from neurosdk.core.messages.core import Context, ContextData


class NeuroActionHandler:
    def __init__(self, config: SDKConfig):
        self._actions: list[NeuroAction] = []
        self._ws: websocket.WebSocket = websocket.create_connection(config.ws_url)
        self._config: SDKConfig = config
        self._thread = threading.Thread(target=self.__run_websocket_forever)
        self._thread.start()
        self._on_action_executed_callbacks: list[Callable[[str], None]] = []
        self._message_condition = threading.Condition()

    def __run_websocket_forever(self):
        while True:
            try:
                if self._ws.connected:
                    message = self._ws.recv()
                    self._on_ws_message(message)
                else:
                    time.sleep(self._config.ws_reconnect_seconds)
                    self._ws = websocket.create_connection(self._config.ws_url)
            except Exception as e:
                self._on_ws_error(e)

    def __del__(self):
        if self._thread:
            self._thread.join()
        self._ws.close()

    def wait_for_one_message(self, timeout=None) -> None:
        """
        Call this method if you need to wait for an action before continuing
        """
        self._message_condition.acquire()
        self._message_condition.wait(timeout)
        self._message_condition.release()

    def add_on_action_executed(self, callback: Callable[[str], None]) -> None:
        if callback not in self._on_action_executed_callbacks:
            self._on_action_executed_callbacks.append(callback)

    def remove_on_action_executed(self, callback: Callable[[str], None]) -> None:
        if callback in self._on_action_executed_callbacks:
            self._on_action_executed_callbacks.remove(callback)

    def _call_action_executed_callbacks(self, action_name: str) -> None:
        for callback in self._on_action_executed_callbacks:
            callback(action_name)

    def _on_ws_message(self, message):
        msg = BaseIncoming.from_json(message)
        if msg.command == "action":
            msg = IncomingAction.from_json(message)
            for action in self._actions:
                if msg.data.name == action.get_name():
                    if action.validate_action(msg.data.data):
                        self._ws.send(
                            ResultAction(
                                game=self._config.game_name,
                                data=action.execute_action(
                                    msg.data.id, action.dict_to_data(msg.data.data)
                                ),
                            ).to_json()
                        )

                        self._call_action_executed_callbacks(action.get_name())
                        with self._message_condition:
                            self._message_condition.notify_all()
                    else:
                        self._ws.send(
                            ResultAction(
                                game=self._config.game_name,
                                data=ResultActionData(
                                    id=msg.data.id,
                                    success=False,
                                    message="Schema validation failed, try again",
                                ),
                            ).to_json()
                        )
                        break
        elif msg.command == "actions/reregister_all":
            self.resend_registered_actions()
        else:
            print("unsupported action", file=sys.stderr)

    def _on_ws_error(self, error):
        print(f"error: {error}", file=sys.stderr)

    def get_action(self, action_name: str) -> NeuroAction | None:
        result = list(
            filter(lambda action: action.get_name() == action_name, self._actions)
        )
        return result[0] if len(result) > 0 else None

    def register_actions(self, actions: list[NeuroAction]):
        self._actions.extend(actions)
        self._ws.send(
            RegisterAction(
                game=self._config.game_name,
                data={"actions": [action.to_json() for action in actions]},
            ).to_json()
        )

    def force_actions(
        self,
        actions: list[NeuroAction],
        query: str,
        state: str,
        ephemeral_context: bool,
    ):
        data = ForceActionData(
            state=state,
            query=query,
            ephemeral_context=ephemeral_context,
            action_names=list(map(lambda action: action.get_name(), actions)),
        )
        self._ws.send(
            ForceAction(
                game=self._config.game_name,
                data=data,
            ).to_json()
        )

    def unregister_actions(self, actions: list[NeuroAction]):
        self._actions = list(filter(lambda x: x not in actions, self._actions))

        self._ws.send(
            UnregisterAction(
                game=self._config.game_name,
                data={"action_names": [action.get_name() for action in actions]},
            ).to_json()
        )

    def resend_registered_actions(self):
        self._ws.send(
            RegisterAction(
                game=self._config.game_name,
                data={"actions": [action.to_json() for action in self._actions]},
            ).to_json()
        )

    def send_context(self, context_message: str, context_silent: bool):
        self._ws.send(
            Context(
                game=self._config.game_name,
                data=ContextData(context_message, context_silent),
            ).to_json()
        )
