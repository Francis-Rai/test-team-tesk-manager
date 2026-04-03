from pydantic import BaseModel
from qa.models.api.common_models import ErrorResponse
from qa.config.settings import ENDPOINTS


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
