from abc import ABCMeta, abstractmethod

from ed.domain.tokens.auth_payload import AuthPayload


class ABCJwt(metaclass=ABCMeta):
    @abstractmethod
    def encode(self, payload: AuthPayload) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> AuthPayload: ...
