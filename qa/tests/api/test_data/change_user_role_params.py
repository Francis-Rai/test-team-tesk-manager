from qa.config.enums import UserRole

success_cases = [
    {
        "description": "Change user role to user",
        "role": UserRole.SUPER_ADMIN,
        "setup": {"create_user": UserRole.ADMIN},
        "request": {"role": UserRole.USER.value},
    },
    {
        "description": "Change user role to admin",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": UserRole.ADMIN.value},
    },
    {
        "description": "Change user role to super admin",
        "setup": {"create_user": UserRole.ADMIN},
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": UserRole.SUPER_ADMIN.value},
    },
]


error_cases = [
    {
        "description": "Missing Authorization token",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "headers": {},
        "request": {"role": "user"},
        "response": {
            "status": 403
        }
    },
    {
        "description": "Invalid Authorization token",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "headers": {"Authorization": "123"},
        "request": {"role": "user"},
        "response": {
            "status": 403
        }
    },
    {
        "description": "Nonexistent User ID",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": None,
        "response": {
            "status": 404,
            "error": "NOT_FOUND",
            "message": "",  # TODO to add message
        },
    },
    {
        "description": "Payload is null",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": None,
        "response": {
            "status": 400,
            "error": "INVALID_REQUEST",
            "message": "Request body is missing or malformed",
        },
    },
    {
        "description": "Missing role",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": {},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "role: required field",
        },
    },
    {
        "description": "role is not a string",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": 1},
        "response": {
            "status": 400,
            "error": "INVALID_REQUEST",
            "message": "role: must be a string",
        },
    },
    {
        "description": "Nonexistent role",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": "unknown_role"},
        "response": {
            "status": 400,
            "error": "INVALID_REQUEST",
            "message": "role: not a valid value",
        },
    },
    {
        "description": "Changing own SUPER_ADMIN role to ADMIN",
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": UserRole.ADMIN.value},
        "response": {
            "status": 403,
            "error": "FORBIDDEN",
            "message": "SUPER ADMIN cannot demote themselves.",
        },
    },
    {
        "description": "Changing own SUPER_ADMIN role to USER",
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": UserRole.USER.value},
        "response": {
            "status": 403,
            "error": "FORBIDDEN",
            "message": "SUPER ADMIN cannot demote themselves.",
        },
    },
    {
        "description": "Incorrect request method",
        "setup": {"create_user": UserRole.USER},
        "role": UserRole.SUPER_ADMIN,
        "request": {"role": UserRole.USER.value},
        "method": "POST",
        "response": {
            "status": 405
        }
    },
]
