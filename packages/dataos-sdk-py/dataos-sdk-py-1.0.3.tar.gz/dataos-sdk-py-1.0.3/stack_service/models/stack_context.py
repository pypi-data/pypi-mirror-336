from pydantic import BaseModel


class StackContext(BaseModel):
    tenantId: str
    contextId: str
    executionId: str
    properties: dict
    data: dict