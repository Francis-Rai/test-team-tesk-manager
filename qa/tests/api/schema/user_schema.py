from qa.config.enums import UserRole

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "format": "uuid"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "role": {
            "type": "string",
            "enum": [role.value for role in UserRole]
        }
    },
    "required": ["id", "firstName", "lastName", "email", "role"],
    "additionalProperties": False
}

GET_ALL_USERS_SCHEMA = {
    "type": "array",
    "items": USER_SCHEMA
}
