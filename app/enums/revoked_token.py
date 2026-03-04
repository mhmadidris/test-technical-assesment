import enum

class RevokedType(enum.Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"