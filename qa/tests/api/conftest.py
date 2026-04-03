import pytest
import psycopg2
import os
from qa.config.settings import BASE_API_URL
from qa.clients.api_client import APIClient
from qa.utils.common import generate_email, generate_password
from qa.config.enums import UserRole
from qa.config.environment import Environment


@pytest.fixture(scope="session")
def env():
    return Environment()


@pytest.fixture(scope="session")
def db_conn(env):
    conn = psycopg2.connect(
        dbname="taskmanager",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433",
    )

    # get id of original super admin
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM public.users WHERE role = 'SUPER_ADMIN' LIMIT 1;")
            result = cur.fetchone()
            if result:
                env.super_admin_id = result[0]
            else:
                pytest.exit("No SUPER_ADMIN user found")

    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def clean_db(db_conn, env):
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
            cur.execute(f"DELETE FROM users WHERE id != '{env.super_admin_id}';")


@pytest.fixture
def user_factory(env):
    api_client = APIClient(BASE_API_URL)

    def _register_user(role=UserRole.USER):
        test_user = {
            "firstName": "Test",
            "lastName": "User",
            "email": generate_email(),
            "password": generate_password(),
        }
        response = api_client.register(test_user, attach=False)

        assert response.status_code == 200, (
            f"Registration failed. "
            f"Status: {response.status_code}, "
            f"Body: {response.text}"
        )
        register_json = response.json()

        if role != UserRole.USER:
            # Login as super admin
            super_admin_creds = {
                "email": os.getenv("BOOTSTRAP_ADMIN_EMAIL"),
                "password": os.getenv("BOOTSTRAP_ADMIN_PASSWORD"),
            }
            response = api_client.login(super_admin_creds, attach=False)
            assert (
                response.status_code == 200
            ), f"Super admin login failed: {response.text}"
            headers = {"Authorization": f"Bearer {response.json()['token']}"}

            # Change registered user role
            response = api_client.change_user_role(
                env=env,
                headers=headers,
                user_id=register_json["user"]["userId"],
                request_body={"role": role.value},
                attach=False,
            )
            assert response.status_code == 204, f"Role change failed: {response.text}"

            # check role was updated with get api
            get_response = api_client.get_all_users(
                env=env,
                headers=headers,
                attach=False,
            )
            assert get_response.status_code == 200, "Unable to get users"
            user = next(
                u
                for u in get_response.json()
                if u["id"] == register_json["user"]["userId"]
            )
            # update id key id to userId
            user["userId"] = user.pop("id")
            register_json.update({"user": user})

        register_json["user"].update({"password": test_user["password"]})
        return register_json

    return _register_user


@pytest.fixture
def login_user(request, user_factory, env):
    role = request.param
    user = user_factory(role)
    env.token = f"Bearer {user["token"]}"
    return {"token": env.token, "userId": user["user"]["userId"]}
