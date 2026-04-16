from pydantic import BaseModel
from qa.models.api.common_models import ErrorResponse
from qa.config.settings import ENDPOINTS


class UserRoleRequest(BaseModel):
    pass
