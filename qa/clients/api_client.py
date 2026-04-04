from qa.clients.base_api_client import BaseAPIClient
from qa.models.api.auth_models import LoginRequest
from qa.utils.test_helpers import attach_api_data, set_report_parameters
from qa.config.settings import ENDPOINTS


class APIClient(BaseAPIClient):

    def register(self, request: dict, method=None, attach=True):
        endpoint = ENDPOINTS["register"]
        if hasattr(request, "model_dump"):
            request = request.model_dump()

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=endpoint, json=request
            )
        else:
            response = self.post(endpoint, json=request)

        if attach:
            attach_api_data(request, response)

        return response

    def login(self, request: LoginRequest | dict, method=None, attach=True):
        endpoint = ENDPOINTS["login"]
        if hasattr(request, "model_dump"):
            request = request.model_dump()

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=endpoint, json=request
            )
        else:
            response = self.post(endpoint, json=request)

        if attach:
            attach_api_data(request, response)
        return response

    def get_all_users(self, env, method=None, headers=None, attach=True):
        endpoint = ENDPOINTS["get_all_users"]
        if headers is None:
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
        if headers is None:
            headers = {"Authorization": env.token}

        if method:
            set_report_parameters({"method": method})
            response = self.send_request(
                method=method, endpoint=endpoint, json=request_body
            )
        else:
            response = self.patch(
                endpoint, headers=headers, json=request_body
            )

        if attach:
            attach_api_data(request_payload=None, response=response)

        return response