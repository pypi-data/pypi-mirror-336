from abc import ABCMeta, abstractmethod
from typing import Annotated

OtpCode = Annotated[str, "A four number code"]


class ABCOtp(metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> OtpCode: ...
