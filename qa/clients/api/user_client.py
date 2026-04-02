from qa.clients.api.base_client import BaseClient
from qa.utils.test_helpers import attach_api_data, set_report_parameters
from qa.config.settings import ENDPOINTS


class UserClient(BaseClient):

    def get_all_users(self, env, method=None, headers=None, attach=True):
        endpoint = ENDPOINTS["get_all_users"]
        if not headers:
            headers = {"Authorization": env.token}

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=endpoint
            )
        else:
            response = self.get(endpoint, headers=headers)

        if attach:
            attach_api_data(request_payload=None, response=response)

        return response

    def change_user_role(
        self, env, user_id, request_body, method=None, headers=None, attach=True
    ):
        endpoint = ENDPOINTS["change_user_role"].format(user_id=user_id)
        if not headers:
            headers = {"Authorization": env.token}

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=endpoint, json=request_body
            )
        else:
            response = self.post(
                endpoint, headers=headers, json=request_body
            )

        if attach:
            attach_api_data(request_payload=None, response=response)

        return response
