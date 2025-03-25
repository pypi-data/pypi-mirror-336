import os
import requests
import floriday_supplier_client
from floriday_supplier_client.rest import ApiException


class ApiFactory:
    def __init__(self):
        self.client_id = os.getenv("FLORIDAY_CLIENT_ID")
        self.client_secret = os.getenv("FLORIDAY_CLIENT_SECRET")
        self.api_key = os.getenv("FLORIDAY_API_KEY")
        self.auth_url = os.getenv("FLORIDAY_AUTH_URL")
        self.base_url = os.getenv("FLORIDAY_BASE_URL")
        self.access_token = self._get_access_token()
        self.configuration = self._configure_client()

    def _get_access_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": (
                "role:app catalog:read sales-order:write organization:read supply:read "
                "supply:write sales-order:read delivery-conditions:read fulfillment:write "
                "fulfillment:read"
            ),
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request(
            "POST", self.auth_url, headers=headers, data=payload
        )
        response.raise_for_status()
        return response.json().get("access_token")

    def _configure_client(self):
        configuration = floriday_supplier_client.Configuration()
        configuration.api_key["Authorization"] = self.access_token
        configuration.api_key_prefix["Authorization"] = "Bearer"
        configuration.api_key["X-Api-Key"] = self.api_key
        # Set the host to the base URL from the environment variable
        configuration.host = self.base_url
        return configuration

    def get_api_instance(self, api_class):
        return api_class(self.get_api_client())

    def get_api_client(self):
        return floriday_supplier_client.ApiClient(self.configuration)
