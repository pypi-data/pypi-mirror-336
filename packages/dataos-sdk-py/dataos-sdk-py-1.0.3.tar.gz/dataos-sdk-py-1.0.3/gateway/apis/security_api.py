import uuid

from uplink import Header, returns, get, Query

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code

WRAPPED_TOKEN_PATH = "api/v2/tenants/{tenant}/wrapped-token"


class SecurityApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get(WRAPPED_TOKEN_PATH)
    def get_token(self,
                  tenant: str,
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4()),
                  apikey: Query('apikey') = None,
                  cluster: Query('cluster') = None,
                  workspace: Query('workspace') = None) -> str:
        """Return a wrapped token to be used for querying cluster correctly"""
        pass
