"""
Find OneDrive folder paths.
Developer: Dominik I. Braun
Contact: dome.braun@fau.de
Last Update: 2025-03-13
"""

from aenum import Enum
import os


class Flag(Enum):
    """
    Enum class for possible OneDrive environment variables.
    """

    _init_ = "value __doc__"

    DEFAULT = "OneDrive", "Default OneDrive environment variable."
    COMMERCIAL = "OneDriveCommercial", "OneDrive Commercial environment variable."
    CONSUMER = "OneDriveConsumer", "OneDrive Consumer environment variable."


def find(env_vars: list[Flag] | Flag = None) -> list[str]:
    """
    Search for OneDrive folders across all drives (Windows only).

    Args:
        env_vars (list[Flag] or Flag, optional): Provided Parameters for OneDrive, e.g., ONEDRIVE.BASIC, "ONEDRIVE.COMMERCIAL", "ONEDRIVE.CONSUMER" Defaults to None.

    Returns:
        list[str]: List of OneDrive paths.
    """
    onedrive_paths = set()

    if isinstance(env_vars, Flag):
        env_vars = [env_vars]

    if env_vars is None:
        # 1. Check environment variables (OneDrive, OneDriveCommercial, OneDriveConsumer)
        env_vars = [
            Flag.DEFAULT,
            Flag.COMMERCIAL,
            Flag.CONSUMER,
        ]

    for var in env_vars:
        path = os.getenv(var.value)
        if path and os.path.isdir(path):
            onedrive_paths.add(path)

    return list(onedrive_paths)
