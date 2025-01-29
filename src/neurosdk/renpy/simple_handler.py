from neurosdk.core.action.neuro_handler import NeuroActionHandler
from neurosdk.core.action.pick_option_action import PickOptionAction
from neurosdk.core.config import SDKConfig


class SimpleHandler:
    def __init__(self, config: SDKConfig):
        self._handler = NeuroActionHandler(config)

    def send_options(self, options: list[Option]):
        option_action = PickOptionAction()
        self._handler.register_action(option_action)

    def send_context(self):
        pass
