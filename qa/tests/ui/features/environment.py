from playwright.sync_api import sync_playwright
from qa.config.settings import BASE_UI_URL
from qa.pages.base_page import BasePage
from qa.utils.test_helpers import add_attachment
import psycopg2
import os

def before_all(context):
    """Run once before all scenarios."""
    context.base_url = BASE_UI_URL
   # Database connection
    context.db_conn = psycopg2.connect(
        dbname="taskmanager",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433"
    )

def before_scenario(context, scenario):
    """Run before each scenario."""
    # Launch browser for each scenario
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.context = context.browser.new_context()
    context.page = context.context.new_page()
    context.base_page = BasePage(context.page)

    context.context.tracing.start(screenshots=True, snapshots=True)

def before_step(context, step):
    """Log before each step."""
    print(f"\n{'→'*60}")
    print(f"STEP: {step.keyword} {step.name}")
    print(f"Scenario: {context.scenario.name}")
    print(f"{'→'*60}")

def after_step(context, step):
    """Log after each step."""
    if step.status == 'failed':
        print(f"\n❌ FAILED at step: {step.name}")
        # Screenshot
        screenshot = context.page.screenshot()
        add_attachment(screenshot, name=f"FAILED_{context.scenario.name}_screenshot")

def after_scenario(context, scenario):
    """Run after each scenario."""
    if scenario.status == "failed":
        # Trace
        context.context.tracing.stop(path="trace.zip")

        with open("logs/trace.zip", "rb") as f:
            import allure
            add_attachment(
                f.read(),
                name=f"FAILED_{context.scenario.name}_trace.zip",
                attachment_type=allure.attachment_type.ZIP,
            )
    else:
        # Stop tracing without saving (or skip entirely)
        context.context.tracing.stop()

    # Close browser
    if hasattr(context, 'page') and context.page:
        context.page.close()
    if hasattr(context, 'browser'):
        context.browser.close()
    if hasattr(context, 'playwright'):
        context.playwright.stop()

    # Clean database
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


def after_all(context):
    """Run once after all scenarios."""
    context.db_conn.close()
