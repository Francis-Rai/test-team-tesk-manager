from qa.utils.common import generate_email, generate_password
from qa.models.api.auth_models import RegisterRequest

setup = {
    "register_user": RegisterRequest(
        firstName="Test",
        lastName="User",
        email=generate_email(),
        password=generate_password(),
    )
}

success_cases = [
    {
        "description": "Register with unique email",
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email=generate_email(),
            password=generate_password(),
        )
    },
    {
        "description": "Register with whitespaces",
        "request": RegisterRequest(
            firstName=" Test ",
            lastName=" User ",
            email=generate_email(),
            password=f"{ generate_password() }",
        )
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
        "description": "Missing firstName",
        "request": {
            "lastName": "User",
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "firstName: required field",
        },
    },
    {
        "description": "firstName is null",
        "request": {
            "firstName": None,
            "lastName": "User",
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "firstName: must not be blank",
        },
    },
    {
        "description": "firstName is not a string",
        "request": {
            "firstName": 1,
            "lastName": "User",
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "firstName: must be a string",
        },
    },
    {
        "description": "Missing lastName",
        "request": {
            "firstName": "Test",
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "lastName: required field",
        },
    },
    {
        "description": "lastName is null",
        "request": {
            "firstName": "Test",
            "lastName": None,
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "lastName: must not be blank",
        },
    },
    {
        "description": "lastName is not a string",
        "request": {
            "firstName": "Test",
            "lastName": 1,
            "email": generate_email(),
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "lastName: must be a string",
        },
    },
    {
        "description": "Missing email",
        "request": {
            "firstName": "Test",
            "lastName": "User",
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: required field",
        },
    },
    {
        "description": "Email is null",
        "request": {
            "firstName": "Test",
            "lastName": "User",
            "email": None,
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must not be blank",
        },
    },
    {
        "description": "Email is not a string",
        "request": {
            "firstName": "Test",
            "lastName": "User",
            "email": 2,
            "password": generate_password(),
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must be a string",
        },
    },
    {
        "description": "Email is not a valid email",
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email="invalidemail",
            password=generate_password(),
        ),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "email: must be a well-formed email address",
        },
    },
    {
        "description": "Missing password",
        "request": {"firstName": "Test", "lastName": "User", "email": generate_email()},
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: required field",
        },
    },
    {
        "description": "Password is null",
        "request": {
            "firstName": "Test",
            "lastName": "User",
            "email": generate_email(),
            "password": None,
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: must not be blank",
        },
    },
    {
        "description": "Password is not a string",
        "request": {
            "firstName": "Test",
            "lastName": "User",
            "email": generate_email(),
            "password": 3,
        },
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: must be a string",
        },
    },
    {
        "description": "Password is less than minimum length",
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email=generate_email(),
            password="Short1@",
        ),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: Password should be at least 8 characters",
        },
    },
    {
        "description": "Password is not a strong password",
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email=generate_email(),
            password="notastrongpassword",
        ),
        "response": {
            "status": 400,
            "error": "VALIDATION_ERROR",
            "message": "password: Password must contain upper, lower, digit, and special character",
        },
    },
    {
        "description": "Register with an email already registered",
        "setup": setup,
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email=setup["register_user"].email,
            password=generate_password(),
        ),
        "response": {
            "status": 409,
            "error": "EMAIL_ALREADY_EXISTS",
            "message": "Email is already in use",
        },
    },
    {
        "description": "Incorrect request method",
        "method": "GET",
        "request": RegisterRequest(
            firstName="Test",
            lastName="User",
            email=generate_email(),
            password=generate_password(),
        ),
        "response": {
            "status": 405,
            "error": "METHOD_NOT_ALLOWED",
            "message": "Request method 'GET' not supported",
        },
    },
]
