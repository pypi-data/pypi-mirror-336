from abc import ABCMeta, abstractmethod

from src.auth.application.contracts.infrastructure.persistence.abc_otp_repository import \
    ABCOtpRepository
from src.auth.application.contracts.infrastructure.persistence.abc_user_repository import \
    ABCUserRepository


class ABCUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def user_repository(self) -> ABCUserRepository:
        pass

    @property
    @abstractmethod
    def otp_repository(self) -> ABCOtpRepository:
        pass
