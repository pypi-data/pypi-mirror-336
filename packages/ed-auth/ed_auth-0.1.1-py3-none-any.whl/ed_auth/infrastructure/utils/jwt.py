import jwt
from ed_domain.tokens.auth_payload import AuthPayload

from ed_auth.application.contracts.infrastructure.utils.abc_jwt import ABCJwt


class Jwt(ABCJwt):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, payload: AuthPayload) -> str:
        return jwt.encode(
            dict(payload),
            self._secret,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> AuthPayload:
        return jwt.decode(
            token,
            self._secret,
            algorithms=[self._algorithm],
        )
