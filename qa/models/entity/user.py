from pydantic import BaseModel
from qa.config.enums import UserRole


class User(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: str
    role: UserRole
