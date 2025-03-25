from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.auth.application.common.responses.base_response import BaseResponse
from src.auth.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.auth.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from src.auth.application.features.auth.dtos import UserDto
from src.auth.application.features.auth.requests.commands import VerifyTokenCommand
from src.auth.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(VerifyTokenCommand, BaseResponse[UserDto])
class VerifyTokenCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, jwt: ABCJwt):
        self._uow = uow
        self._jwt = jwt

    async def handle(self, request: VerifyTokenCommand) -> BaseResponse[UserDto]:
        payload = self._jwt.decode(request.dto["token"])
        user = self._uow.user_repository.get(email=payload["email"])

        return BaseResponse[UserDto].success(
            "Token validated.",
            UserDto(
                **user,  # type: ignore
                token=request.dto["token"],
            ),
        )
