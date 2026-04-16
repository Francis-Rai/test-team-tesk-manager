import pytest
import psycopg2
from functools import partial
from qa.config.settings import BASE_API_URL
from qa.clients.api_client import APIClient
from qa.config.settings import DB_USERNAME, DB_PASSWORD
from qa.config.environment import Environment
from qa.utils.test_helpers import create_user_via_api


@pytest.fixture(scope="session")
def env():
    return Environment()


@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_API_URL)


@pytest.fixture(scope="session")
def db_conn(env):
    conn = psycopg2.connect(
        dbname="taskmanager",
        user=DB_USERNAME,
        password=DB_PASSWORD,
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
def user_factory(api_client):
    return partial(create_user_via_api, api_client=api_client)


@pytest.fixture
def login_user(request, env, api_client):
    role = request.param
    user = create_user_via_api(api_client, role)
    env.token = f"Bearer {user["token"]}"
    return {"token": env.token, "userId": user["user"]["userId"]}
