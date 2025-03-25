from abc import ABCMeta, abstractmethod


class ABCPassword(metaclass=ABCMeta):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, hash: str) -> bool: ...
