from qa.config.enums import UserRole

get_all_users = [
    {"description": "Get all users as a normal user", "role": UserRole.USER},
    {"description": "Get all users as a super admin", "role": UserRole.SUPER_ADMIN},
]


get_all_users_exceptions = [
    {
        "description": "Missing Authorization token",
        "role": UserRole.USER,
        "headers": {},
    },
    {
        "description": "Invalid Authorization token",
        "role": UserRole.USER,
        "headers": {"Authorization": "123"},
    },
    {
        "description": "Incorrect request method",
        "role": UserRole.USER,
        "method": "POST",
    },
]
