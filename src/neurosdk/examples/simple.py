from neurosdk.core.manager import Manager
from neurosdk.core.config import SDKConfig
from neurosdk.core.action.neuro_action import NeuroAction
from neurosdk.core.messages.action import Action, ResultActionData
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Any

@dataclass
class ExampleActionData(DataClassJsonMixin):
    example_schema_item: int

class ExampleAction(NeuroAction):
    dataType = ExampleActionData

    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return 'An example action for example things'

    def can_be_used(self) -> bool:
        return True

    def validate_action(self, data: str) -> bool:
        # NOTE: you can add your own validate action here
        return super().validate_action(data)

    def execute_action(self, id: str, _data) -> ResultActionData:
        print('in theory we would execute an action')
        return ResultActionData(id=id, success=True, message="executed!")

config = SDKConfig(game_name='game', ws_url='ws://127.0.0.1:8000')
manager = Manager(config)

# register actions that can be taken at any time
manager.neuro_action_handler.register_actions([ExampleAction("global action")])

# forced actions
action_group = manager.instantiate_action_window()
action_group.add_action(ExampleAction("example forced windowed action 1"))
action_group.add_action(ExampleAction("example forced windowed action 2"))
action_group.set_force('do something (poke)', None, True)

manager.register_active_action_window()
print('Waiting for message before continuing')
manager.neuro_action_handler.wait_for_one_message()

# normal actions
action_group = manager.instantiate_action_window()
action_group.add_action(ExampleAction("example windowed action 1"))
action_group.add_action(ExampleAction("example windowed action 2"))

manager.register_active_action_window()
print('Waiting for message before continuing')
manager.neuro_action_handler.wait_for_one_message()

print('theoretically we can quit now')
