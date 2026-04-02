import psycopg2
import os
from qa.clients.api.auth_client import AuthClient

def before_all(context):
    context.base_url = "http://localhost:8080"
    context.auth_client = AuthClient(context.base_url)

    # add conn to db
    context.db_conn = psycopg2.connect(
        dbname="taskmanager",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433"
    )

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
