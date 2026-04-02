from qa.clients.api.base_client import BaseClient
from qa.utils.test_helpers import attach_api_data, set_report_parameters
from qa.config.settings import ENDPOINTS


class UserClient(BaseClient):

    def get_all_users(self, env, method=None, headers=None, attach=True):
        if not headers:
            headers = {"Authorization": env.token}

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=ENDPOINTS["get_all_users"]
            )
        else:
            response = self.get(ENDPOINTS["get_all_users"], headers=headers)

        if attach:
            attach_api_data(request_payload=None, response=response)

        return response
