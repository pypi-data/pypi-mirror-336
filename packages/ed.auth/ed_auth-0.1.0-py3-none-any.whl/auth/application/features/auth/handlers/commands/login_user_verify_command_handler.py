from ed.domain.entities.otp import OtpVerificationAction
from ed.domain.tokens.auth_payload import AuthPayload, UserType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.auth.application.common.responses.base_response import BaseResponse
from src.auth.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from src.auth.application.contracts.infrastructure.utils.abc_jwt import ABCJwt
from src.auth.application.features.auth.dtos import UserDto
from src.auth.application.features.auth.dtos.validators.verify_otp_dto_validator import \
    VerifyOtpDtoValidator
from src.auth.application.features.auth.requests.commands.login_user_verify_command import \
    LoginUserVerifyCommand
from src.auth.common.exception_helpers import ApplicationException, Exceptions
from src.auth.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginUserVerifyCommand, BaseResponse[UserDto])
class LoginUserVerifyCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, jwt: ABCJwt):
        self._uow = uow
        self._jwt = jwt

    async def handle(self, request: LoginUserVerifyCommand) -> BaseResponse[UserDto]:
        dto_validator = VerifyOtpDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Login failed.",
                dto_validator.errors,
            )

        dto = request.dto
        user = self._uow.user_repository.get(id=dto["user_id"])
        if not user:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Otp verification failed.",
                [f"User with that id = {dto['user_id']} does not exist."],
            )

        otp = self._uow.otp_repository.get(user_id=dto["user_id"])
        if not otp or otp["action"] != OtpVerificationAction.LOGIN:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Otp verification failed.",
                [
                    f"Otp has not been sent to the user with id = {dto['user_id']} recently."
                ],
            )

        if otp["value"] != dto["otp"]:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Otp verification failed.",
                ["Otp does not match with the one sent."],
            )

        payload: AuthPayload = {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user.get("email", ""),
            "phone_number": user.get("phone_number", ""),
            "user_type": UserType.DRIVER,
        }

        return BaseResponse[UserDto].success(
            "Login successful.",
            UserDto(
                **user,  # type: ignore
                token=self._jwt.encode(payload),
            ),
        )
