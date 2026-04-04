BASE_API_URL = "http://localhost:8080"
BASE_UI_URL = "http://localhost:5173"

SUPER_USER_EMAIL = "superuser@example.com"
SUPER_USER_PASSWORD = "Superuserpassword2!"

ENDPOINTS = {
    "login": "/api/auth/login",
    "register": "/api/auth/register",
    "get_all_users": "/api/users",
    "change_user_role": "/api/admin/users/{user_id}/role"
}

# allure reporting
SUCCESS_TAG = "success_case"
ERROR_TAG = "error_case"