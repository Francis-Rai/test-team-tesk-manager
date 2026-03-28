from qa.clients.auth_client import AuthClient


def before_all(context):
    context.base_url = "http://localhost:8080"
    context.auth_client = AuthClient(context.base_url)
