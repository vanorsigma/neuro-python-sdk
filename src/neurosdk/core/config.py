"""
SDK config
"""

import os
from dataclasses import dataclass


@dataclass
class SDKConfig:
    """
    SDK config
    """

    game_name: str

    ws_url: str = os.getenv("NEURO_SDK_WS_URL")
    ws_reconnect_seconds: int = 5
