from abc import ABCMeta

from ed.domain.entities import User

from src.auth.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCUserRepository(
    ABCGenericRepository[User],
    metaclass=ABCMeta,
): ...
