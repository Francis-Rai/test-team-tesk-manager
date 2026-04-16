import os

BASE_API_URL = "http://localhost:8080"
BASE_UI_URL = "http://localhost:5173"

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SUPER_USER_EMAIL = os.getenv("BOOTSTRAP_ADMIN_EMAIL")
SUPER_USER_PASSWORD = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")

ENDPOINTS = {
    "login": "/api/auth/login",
    "register": "/api/auth/register",
    "get_all_users": "/api/users",
    "change_user_role": "/api/admin/users/{user_id}/role"
}

# allure reporting
SUCCESS_TAG = "success_case"
ERROR_TAG = "error_case"