from typing import Dict, Any
from pydantic import BaseModel

class SinkRequest(BaseModel):
    """
    Pydantic model for the SinkRequest.

    Attributes:
        tenant_id (str): The tenant ID of the context.
        context_id (str): The specific context that this data is in relation to.
        execution_id (str): The specific execution this data is in relation to.
        properties (Dict[str, str]): A dictionary of metadata associated with the message.
        data (Dict[str, Any]): The payload of information.
    """
    tenant_id: str
    context_id: str
    execution_id: str
    properties: Dict[str, str]
    data: Dict[str, Any]