from enum import Enum


class CreateSharedLinksRequestSettingsAccess(str, Enum):
    DEFAULT = "default"
    EDITOR = "editor"
    MAX = "max"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
