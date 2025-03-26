import uuid

from typing import Dict
from uplink import Header, get, returns
from uplink import Query as Query_param
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from gateway.models.gateway_models import QueryList, Query


class QueryApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/queries")
    def list_queries(self, tenant: str, limit: Query_param('limit') = 2000, offset: Query_param('offset') = 0,
                     sort: Query_param('sort') = "created_at desc",
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> QueryList:
        """
        Retrieve a list of queries associated with a specific tenant, with optional pagination and sorting.

        Parameters:
            tenant (str): The name of the tenant for which queries are to be retrieved.
            limit (Query): The maximum number of queries to retrieve in the response.
                Defaults to 2000.
            offset (Query): The number of queries to skip before starting to return results.
                Defaults to 0.
            sort (Query): The sort order of the queries, specified as a field name and direction
                Defaults to "created_at desc".
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            QueryList: A QueryList object containing the list of queries, including:
                - queries (List[Query], optional): A list of Query objects, each containing:
                    - tenant (str, optional): The name of the tenant associated with the query.
                    - workspace (str, optional): The name of the workspace where the query was executed.
                    - queryId (str, optional): The unique identifier of the query.
                    - queryHash (str, optional): A hash representation of the query.
                    - queryText (str, optional): The actual SQL or query text.
                    - originalQuery (str, optional): The original query text before any modifications or parsing.
                    - proxyToCluster (str, optional): The cluster to which the query is proxied.
                    - proxyToClusterDialect (str, optional): The dialect used in the cluster.
                    - proxyTo (str, optional): The proxy address for the cluster.
                    - userName (str, optional): The name of the user who executed the query.
                    - source (str, optional): The source from where the query originated.
                    - createdAt (int, optional): The timestamp of query creation (in epoch format).
                    - correlationId (str, optional): The unique correlation ID associated with the query.
                    - lenses (List[str], optional): A list of lenses associated with the query.
                - limit (int): The limit value used for pagination.
                - offset (int): The offset value used for pagination.
                - sort (str): The sort order applied to the query results.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/queries/{query_id}")
    def get_query(self, tenant:str, query_id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Query:
        """
        Retrieve the details of a specific query associated with a tenant.

        Parameters:
            tenant (str): The name of the tenant to which the query belongs.
            query_id (str): The unique identifier of the query to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            Query: A Query object containing details about the specified query, including:
                - tenant (str, optional): The name of the tenant associated with the query.
                - workspace (str, optional): The name of the workspace where the query was executed.
                - queryId (str, optional): The unique identifier of the query.
                - queryHash (str, optional): A hash representation of the query.
                - queryText (str, optional): The actual SQL or query text.
                - originalQuery (str, optional): The original query text before any modifications or parsing.
                - proxyToCluster (str, optional): The cluster to which the query is proxied.
                - proxyToClusterDialect (str, optional): The dialect used in the cluster.
                - proxyTo (str, optional): The proxy address for the cluster.
                - userName (str, optional): The name of the user who executed the query.
                - source (str, optional): The source from where the query originated.
                - createdAt (int, optional): The timestamp of query creation (in epoch format).
                - correlationId (str, optional): The unique correlation ID associated with the query.
                - lenses (List[str], optional): A list of lenses associated with the query.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/queries/distribution")
    def get_query_distribution(self, tenant: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Dict[str, int]:
        """
         Retrieve the distribution of queries for a specific tenant.

         Parameters:
             tenant (str): The name of the tenant for which the query distribution is to be retrieved.
             correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                 Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

         Returns:
             Dict[str, int]: A dictionary where the keys represent distribution categories
             and the values represent the count of queries in each category.
         """
        pass

