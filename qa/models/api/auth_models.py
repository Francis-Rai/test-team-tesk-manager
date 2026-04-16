from pydantic import BaseModel, SecretStr, field_serializer
from qa.utils.common import generate_email, generate_password


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: SecretStr

    @classmethod
    def create_new_user(cls):
        return RegisterRequest(
            firstName="Test",
            lastName="User",
            email=generate_email(),
            password=generate_password(),
        )

    @field_serializer("password")
    def dump_password(self, v: SecretStr):
        return v.get_secret_value()
