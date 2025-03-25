from abc import ABCMeta, abstractmethod
from uuid import UUID

from ed_domain.services.common.api_response import ApiResponse

from ed_auth.application.features.auth.dtos import (CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    UnverifiedUserDto, UserDto,
                                                    VerifyTokenDto)


class ABCAuthApiClient(metaclass=ABCMeta):
    @abstractmethod
    def create_get_otp(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[UnverifiedUserDto]: ...

    @abstractmethod
    def create_verify_otp(
        self, create_user_verify_dto: CreateUserVerifyDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    def login_get_otp(
        self, login_user_dto: LoginUserDto
    ) -> ApiResponse[UnverifiedUserDto]: ...

    @abstractmethod
    def login_verify_otp(
        self, login_user_verify_dto: LoginUserVerifyDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    def verify_token(
        self, verify_token_dto: VerifyTokenDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    def delete_user(self, id: UUID) -> ApiResponse[None]: ...
