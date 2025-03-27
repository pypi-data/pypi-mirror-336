from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

# Column Schema
class Column(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

# Reply Schema
class Reply(BaseModel):
    columns: Optional[List[Column]] = None
    rows: Optional[List[List[str]]] = None
    queryText: Optional[str] = None

# Cluster Schema
class Cluster(BaseModel):
    name: str = Field(..., min_length=3, max_length=64, pattern="^[a-z]{1}[a-z0-9\\-]{0,63}$")
    tenant: str = Field(..., min_length=3, max_length=128, pattern="^[a-zA-Z0-9\\-]{1,128}$")
    workspace: str = Field(..., min_length=3, max_length=128, pattern="^[a-zA-Z0-9\\-]{1,128}$")
    description: Optional[str] = Field(None, min_length=0, max_length=2048)
    proxyTo: Optional[str] = None
    protocol: Optional[str] = Field(None, enum=["trino"])
    dialect: Optional[str] = Field(None, enum=["trino_sql", "spark_sql"])

# Query Schema
class Query(BaseModel):
    tenant: Optional[str] = None
    workspace: Optional[str] = None
    queryId: Optional[str] = None
    queryHash: Optional[str] = None
    queryText: Optional[str] = None
    originalQuery: Optional[str] = None
    proxyToCluster: Optional[str] = Field(..., min_length=3, max_length=64, pattern="^[a-z]{1}[a-z0-9\\-]{0,63}$")
    proxyToClusterDialect: Optional[str] = Field(None, enum=["trino_sql", "spark_sql"])
    proxyTo: Optional[str] = None
    userName: Optional[str] = None
    source: Optional[str] = None
    createdAt: Optional[int] = None
    correlationId: Optional[str] = None
    lenses: Optional[List[str]] = None

# QueryList Schema
class QueryList(BaseModel):
    queries: Optional[List[Query]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort: Optional[str] = None

# ErrorLocation Schema
class ErrorLocation(BaseModel):
    lineNumber: Optional[int] = None
    columnNumber: Optional[int] = None

# FailureInfo Schema
class FailureInfo(BaseModel):
    type: Optional[str] = None
    message: Optional[str] = None
    cause: Optional["FailureInfo"] = None
    suppressed: Optional[List["FailureInfo"]] = None
    stack: Optional[List[str]] = None
    errorLocation: Optional[ErrorLocation] = None

# QueryError Schema
class QueryError(BaseModel):
    message: Optional[str] = None
    sqlState: Optional[str] = None
    errorCode: Optional[int] = None
    errorName: Optional[str] = None
    errorType: Optional[str] = None
    errorLocation: Optional[ErrorLocation] = None
    failureInfo: Optional[FailureInfo] = None

# ParseQueryResult Schema
class ParseQueryResult(BaseModel):
    tables: Optional[List[str]] = None
    lenses: Optional[List[str]] = None
    columns: Optional[List[Column]] = None
    modifiedQuery: Optional[str] = None
    columnQueryError: Optional[QueryError] = None
    columnQuery: Optional[str] = None
