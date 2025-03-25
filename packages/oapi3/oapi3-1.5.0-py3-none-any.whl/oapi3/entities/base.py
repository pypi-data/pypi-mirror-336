"""Module contains base Entity class."""
from typing import Generic
from typing import TypeVar
import abc


T = TypeVar("T")


class Entity(Generic[T], abc.ABC):
    """Base entity class."""

    __slots__ = ["obj"]

    obj: T

    def __init__(self, obj: T):
        self.obj = obj
