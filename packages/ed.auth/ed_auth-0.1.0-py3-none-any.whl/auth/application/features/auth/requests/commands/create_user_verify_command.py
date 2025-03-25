from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.auth.application.common.responses.base_response import BaseResponse
from src.auth.application.features.auth.dtos import CreateUserVerifyDto
from src.auth.application.features.auth.dtos.user_dto import UserDto


@request(BaseResponse[UserDto])
@dataclass
class CreateUserVerifyCommand(Request):
    dto: CreateUserVerifyDto
