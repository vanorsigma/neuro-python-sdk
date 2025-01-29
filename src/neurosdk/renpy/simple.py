from neurosdk.core.action.neuro_handler import NeuroActionHandler
from neurosdk.renpy.simple_handler import SimpleHandler
from neurosdk.core.config import SDKConfig


def make_neuro_handler_for_config(config: SDKConfig) -> NeuroActionHandler:
    return NeuroActionHandler(config)


def simple_neuro_handler(game_name: str) -> SimpleHandler:
    """
    This all-encompassing handler makes it easy to talk to the Neuro SDK.
    I hope.
    """
    config = SDKConfig(game_name)
    return SimpleHandler(config)
