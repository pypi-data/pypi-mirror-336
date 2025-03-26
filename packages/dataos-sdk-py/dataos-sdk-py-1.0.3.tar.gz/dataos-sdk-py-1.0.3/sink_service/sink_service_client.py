from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from sink_service.api.sink_service_api import SinkServiceApi


class SinkServiceClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "SinkServiceClient"

    def build(self):
        """
        Build the SinkServiceClient instance.

        Returns:
            SinkServiceClient: An instance of SinkServiceClient with the configured settings.
        """
        return SinkServiceClient(self.base_url, self.apikey, self.get_http_client())


class SinkServiceClient:
    def __init__(self, base_url, apikey, client = None):
        """
        Initialize the SinkServiceClient.

        This class provides a client to interact with an API related to Sink services.

        Parameters:
            base_url (str): The base URL of the Sink Service API.
            apikey (str): The API key for authentication with the Sink Service API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        """
        self.client = client
        self.base_url = base_url
        self.apikey = apikey

        base_url = normalize_base_url(base_url)
        self.sink_service_api = SinkServiceApi(base_url, self.apikey, client=self.client)
