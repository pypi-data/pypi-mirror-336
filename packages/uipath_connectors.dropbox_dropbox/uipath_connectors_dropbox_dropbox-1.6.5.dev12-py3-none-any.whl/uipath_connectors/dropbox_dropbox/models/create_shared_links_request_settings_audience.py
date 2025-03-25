from enum import Enum


class CreateSharedLinksRequestSettingsAudience(str, Enum):
    MEMBERS = "members"
    NO_ONE = "no_one"
    PASSWORD = "password"
    PUBLIC = "public"
    TEAM = "team"

    def __str__(self) -> str:
        return str(self.value)
