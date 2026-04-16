from behave import fixture
from qa.utils.test_helpers import create_user_via_api
from qa.models.entity.user import User

@fixture
def user_factory(context, role):
    test_user = create_user_via_api(context.api_client, role)
    context.test_user = User(**test_user["user"])
    yield
    # user deleted in after_scenario fixture
