import unittest

from requests import Response

from commons.utils.env_helper import get_env_or_throw
from depot_service.depot_service_client import DepotServiceClientBuilder
from depot_service.models.models import ResolverAddress
from gateway.gateway_client import GatewayClientBuilder

class TestResolveApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        base_url = f"https://{get_env_or_throw('DATAOS_FQDN')}/gateway"
        api_key = get_env_or_throw("DATAOS_RUN_AS_APIKEY")
        self.gateway_client = (GatewayClientBuilder().
                          set_base_url(base_url).
                          set_apikey(api_key).build())
        self.tenant = get_env_or_throw("DATAOS_TENANT_ID")

    def test_get_token(self):
        # Mock the response data from the DepotServiceClient
        wrap_token: Response = self.gateway_client.security_api.get_token(
            tenant=self.tenant, cluster="minervacluster", workspace="w01", apikey=get_env_or_throw("DATAOS_RUN_AS_APIKEY"))
        self.assertIsInstance(wrap_token.text, str)


if __name__ == "__main__":
    unittest.main()
