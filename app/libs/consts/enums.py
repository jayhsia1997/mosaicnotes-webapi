"""
Enums for the application
"""
from enum import IntEnum, StrEnum


class LoginMethod(StrEnum):
    """
    Login method
    """
    PASSWORD = "password"


class Gender(IntEnum):
    """
    Gender
    """
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2
    OTHER = 3
