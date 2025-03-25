from random import randint

from ed_auth.application.contracts.infrastructure.utils.abc_otp import (ABCOtp,
                                                                    OtpCode)


class Otp(ABCOtp):
    def generate(self) -> OtpCode:
        return "0000"  # TODO: As soon as SMS works, replace this
        return f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"
