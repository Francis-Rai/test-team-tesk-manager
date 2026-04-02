from qa.config.enums import UserRole

change_user_role = [
    {"description": "Get all users as a normal user", "role": UserRole.USER},
    {"description": "Get all users as a normal user", "role": UserRole.ADMIN},
    {"description": "Get all users as a super admin", "role": UserRole.SUPER_ADMIN},
]


change_user_role_exceptions = [
    {
        "description": "Missing Authorization token",
        "role": UserRole.USER,
        "headers": {},
        "response": {
            "status": 403
        }
    },
    {
        "description": "Invalid Authorization token",
        "role": UserRole.USER,
        "headers": {"Authorization": "123"},
        "response": {
            "status": 403
        }
    },
    {
        "description": "Incorrect request method",
        "role": UserRole.USER,
        "method": "POST",
        "response": {
            "status": 405
        }
    },
]
