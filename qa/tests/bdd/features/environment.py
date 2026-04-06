import psycopg2
import os
from qa.clients.api_client import APIClient
from behave import use_fixture
from qa.tests.bdd.fixtures import user_factory
from qa.config.settings import BASE_API_URL, SUPER_USER_EMAIL, SUPER_USER_PASSWORD
from qa.config.enums import UserRole
from qa.models.api.auth_models import LoginRequest
from hamcrest import assert_that, equal_to

super_user_login = LoginRequest(email=SUPER_USER_EMAIL, password=SUPER_USER_PASSWORD)


def before_all(context):
    context.api_client = APIClient(BASE_API_URL)

    # add conn to db
    context.db_conn = psycopg2.connect(
        dbname="taskmanager",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433"
    )

    # get token as a super user
    response = context.api_client.login(super_user_login, attach=False)
    assert_that(
        response.status_code,
        equal_to(200),
        f"Failed to login as super user: {response.content}",
    )
    context.super_user_token = f"Bearer {response.json()["token"]}"

def before_tag(context, tag):
    fixtures = {
        "fixture.create_user": (user_factory, {"role": UserRole.USER}),
    }

    if tag in fixtures:
        func, kwargs = fixtures[tag]
        use_fixture(func, context, **kwargs)

def after_all(context):
    """Run once after all features/scenarios."""
    context.db_conn.close()

def after_scenario(context, scenario):
    # clean db
    with context.db_conn:
        with context.db_conn.cursor() as cur:
            # Truncate all tables except 'users'
            cur.execute("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public' AND tablename != 'users';
            """)
            other_tables = [row[0] for row in cur.fetchall()]
            if other_tables:
                cur.execute(f"TRUNCATE TABLE {', '.join(other_tables)} CASCADE;")
                print(f"Truncated tables: {other_tables}")

            # Clean users table but preserve super admin
            cur.execute("DELETE FROM users WHERE role != 'SUPER_ADMIN';")
