from qa.utils.common import generate_email, generate_password
from qa.config.settings import SUPER_USER_EMAIL, SUPER_USER_PASSWORD
from qa.models.api.auth_models import LoginRequest


success_cases = [
    {
        "description": "Login as a user",
        "request": {},
    },  # login data will be generated dynamically in the test
    {
        "description": "Login as a super user",
        "request": LoginRequest(email=SUPER_USER_EMAIL, password=SUPER_USER_PASSWORD),
    },
]

error_cases = [
    {
        "description": "Payload is null",
        "request": None,
        "response": {
            "status": 400,
            "error": "INVALID_REQUEST",
            "message": "Request body is missing or malformed",
        },
    },
    {
        "description": "Missing email",
        "request": {"password": generate_password()},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: required field",
        },
    },
    {
        "description": "Email is null",
        "request": {"email": None, "password": generate_password()},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must not be blank",
        },
    },
    {
        "description": "Email is not a string",
        "request": {"email": 1, "password": generate_password()},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must be a string",
        },
    },
    {
        "description": "Email is not a valid email",
        "request": LoginRequest(email="invalidemail", password=generate_password()),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must be a well-formed email address",
        },
    },
    {
        "description": "Missing password",
        "request": {"email": generate_email()},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: required field",
        },
    },
    {
        "description": "Password is null",
        "request": {"email": generate_email(), "password": None},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: must not be blank",
        },
    },
    {
        "description": "Password is not a string",
        "request": {"email": generate_email(), "password": 2},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: must be a string",
        },
    },
    {
        "description": "Password is less than minimum length",
        "request": LoginRequest(email=generate_email(), password="Short1!"),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: Password should be at least 8 characters",
        },
    },
    {
        "description": "Password is not a strong password",
        "request": LoginRequest(email=generate_email(), password="notastrongpassword"),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: Password must contain upper, lower, digit, and special character",
        },
    },
    {
        "description": "User does not exist",
        "request": LoginRequest(email=generate_email(), password=generate_password()),
        "response": {
            "status": 401,
            "error": "INVALID_CREDENTIALS",
            "message": "Invalid Credentials",
        },
    },
    {
        "description": "Incorrect request method",
        "method": "GET",
        "response": {
            "status": 405,
            "error": "METHOD_NOT_ALLOWED",
            "message": "Request method 'GET' not supported",
        },
    },
]
