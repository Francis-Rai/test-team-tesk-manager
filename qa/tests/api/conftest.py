import pytest
import psycopg2
import os
from qa.config.settings import BASE_API_URL
from qa.clients.api.auth_client import AuthClient
from qa.clients.api.user_client import UserClient
from qa.utils.common import generate_email, generate_password
from qa.config.enums import UserRole
from qa.config.environment import Environment


@pytest.fixture(scope="session")
def env():
    return Environment()


@pytest.fixture(scope="session")
def db_conn():
    conn = psycopg2.connect(
        dbname="taskmanager",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433",
    )
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def clean_db(db_conn):
    yield
    with db_conn:
        with db_conn.cursor() as cur:
            # Truncate all tables except 'users'
            cur.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public' AND tablename != 'users';
            """
            )
            other_tables = [row[0] for row in cur.fetchall()]
            if other_tables:
                cur.execute(f"TRUNCATE TABLE {', '.join(other_tables)} CASCADE;")
                print(f"Truncated tables: {other_tables}")

            # Clean users table but preserve super admin
            cur.execute("DELETE FROM users WHERE role != 'SUPER_ADMIN';")


@pytest.fixture
def registered_user():
    test_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": generate_email(),
        "password": generate_password(),
    }
    response = AuthClient(BASE_API_URL).register(test_user, attach=False)

    assert response.status_code == 200, (
        f"Registration failed. "
        f"Status: {response.status_code}, "
        f"Body: {response.text}"
    )
    response_json = response.json()
    response_json["user"].update({"password": test_user["password"]})
    return response_json


@pytest.fixture
def login_user(request, registered_user, env):
    role = request.param
    token = registered_user["token"]

    if role != UserRole.USER:
        # Login as super admin
        super_admin_creds = {
            "email": os.getenv("BOOTSTRAP_ADMIN_EMAIL"),
            "password": os.getenv("BOOTSTRAP_ADMIN_PASSWORD"),
        }
        response = AuthClient(BASE_API_URL).login(super_admin_creds, attach=False)
        assert response.status_code == 200, f"Super admin login failed: {response.text}"
        super_token = f"Bearer {response.json()['token']}"
        env.token = super_token

        if role == UserRole.ADMIN:
            # Change registered user to admin and get new token
            response = UserClient(BASE_API_URL).change_user_role(
                env=env,
                user_id=registered_user["user"]["userId"],
                request_body={"role": UserRole.ADMIN.value},
                attach=False,
            )
            assert response.status_code == 204, f"Role change failed: {response.text}"
            token = f"Bearer {response.json()['token']}"
        else:
            # For SUPER_ADMIN, use super admin token
            token = super_token

    env.token = token
    return token
