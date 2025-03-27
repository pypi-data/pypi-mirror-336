import uuid

from typing import List
from uplink import Header, get, returns, delete, Query
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from gateway.models.gateway_models import Cluster, Reply


class ClusterApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/clusters")
    def list_tenant_clusters(self, tenant: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Cluster]:
        """
        Retrieve a list of all clusters associated with a specific tenant.

        Parameters:
            tenant (str): The name of the tenant for which clusters are to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            List[Cluster]: A list of Cluster objects, each containing details about a specific cluster, including:
                - name (str): The unique name of the cluster.
                - tenant (str): The tenant associated with the cluster.
                - workspace (str, optional): The workspace in which the cluster resides, if applicable.
                - description (str, optional): A detailed description of the cluster.
                - proxyTo (str, optional): The proxy address for the cluster.
                - protocol (str, optional): The communication protocol used by the cluster (e.g., "trino").
                - dialect (str, optional): The query dialect used by the cluster (e.g., "trino_sql" or "spark_sql").
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters")
    def list_workspace_clusters(self, tenant: str, workspace: str, protocol: Query('protocol') = None,
                                dialect: Query('dialect') =  None,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Cluster]:
        """
        Retrieve a list of clusters associated with a specific tenant and workspace, with optional filtering
        by protocol and dialect.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace for which clusters are to be retrieved.
            protocol (str, optional): An optional query parameter to filter clusters by their communication protocol
                (e.g., "trino").
            dialect (str, optional): An optional query parameter to filter clusters by their query dialect
                (e.g., "trino_sql" or "spark_sql").
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            List[Cluster]: A list of Cluster objects, each containing details about a specific cluster, including:
                - name (str): The unique name of the cluster.
                - tenant (str): The tenant associated with the cluster.
                - workspace (str): The workspace in which the cluster resides.
                - description (str, optional): A detailed description of the cluster.
                - proxyTo (str, optional): The proxy address for the cluster.
                - protocol (str, optional): The communication protocol used by the cluster (e.g., "trino").
                - dialect (str, optional): The query dialect used by the cluster (e.g., "trino_sql" or "spark_sql").
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/active")
    def list_workspace_active_clusters(self, tenant: str, workspace: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Cluster]:
        """
        Retrieve a list of active clusters associated with a specific tenant and workspace.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace for which active clusters are to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            List[Cluster]: A list of Cluster objects representing active clusters, each containing details about the cluster, including:
                - name (str): The unique name of the cluster.
                - tenant (str): The tenant associated with the cluster.
                - workspace (str): The workspace in which the cluster resides.
                - description (str, optional): A detailed description of the cluster.
                - proxyTo (str, optional): The proxy address for the cluster.
                - protocol (str, optional): The communication protocol used by the cluster (e.g., "trino").
                - dialect (str, optional): The query dialect used by the cluster (e.g., "trino_sql" or "spark_sql").
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/{cluster}")
    def get_cluster(self, tenant: str, workspace: str, cluster: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Cluster:
        """
        This method retrieve details of a specific cluster in a given tenant and workspace.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace containing the cluster.
            cluster (str): The name of the cluster to retrieve.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            Cluster: A Cluster object containing details of the requested cluster, including:
                - name (str): The unique name of the cluster.
                - tenant (str): The tenant associated with the cluster.
                - workspace (str): The workspace in which the cluster resides.
                - description (str, optional): A detailed description of the cluster.
                - proxyTo (str, optional): The proxy address for the cluster.
                - protocol (str, optional): The communication protocol used by the cluster (e.g., "trino").
                - dialect (str, optional): The query dialect used by the cluster (e.g., "trino_sql" or "spark_sql").
        """
        pass

    # @raise_for_status_code
    # @delete("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/{cluster}")
    # def delete_cluster(self, tenant: str, workspace: str, cluster: str,
    #          correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
    #     """
    #     This method deletes a specific cluster within a given tenant and workspace.
    #
    #     Parameters:
    #         tenant (str): The name of the tenant to which the workspace belongs.
    #         workspace (str): The name of the workspace containing the cluster.
    #         cluster (str): The name of the cluster to be deleted.
    #         correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
    #             Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().
    #
    #     Returns:
    #         None
    #     """
    #     pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/{cluster}/catalogs")
    def fetch_cluster_catalogs(self, tenant: str, workspace: str, cluster: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Reply:
        """
        Retrieve a list of catalogs available in a specific cluster within a given tenant and workspace.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace containing the cluster.
            cluster (str): The name of the cluster for which catalogs are to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            Reply: A Reply object containing the catalog details, which includes:
                - columns (List[Column], optional): Metadata about the catalog's structure, including:
                    - name (str, optional): The name of the column.
                    - type (str, optional): The data type of the column.
                - rows (List[List[str]], optional): Data rows representing the catalogs in the cluster.
                - queryText (str, optional): The query executed to fetch the catalog information.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/{cluster}/catalogs/{catalog}/schemas")
    def fetch_catalog_schemas(self, tenant: str, workspace: str, cluster: str, catalog: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Reply:
        """
        Retrieve a list of schemas available within a specific catalog in a cluster, tenant, and workspace.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace containing the cluster.
            cluster (str): The name of the cluster where the catalog resides.
            catalog (str): The name of the catalog for which schemas are to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            Reply: A Reply object containing the schema details, which includes:
                - columns (List[Column], optional): Metadata about the schemas' structure, including:
                    - name (str, optional): The name of the column.
                    - type (str, optional): The data type of the column.
                - rows (List[List[str]], optional): Data rows representing the schemas in the catalog.
                - queryText (str, optional): The query executed to fetch the schema information.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/workspaces/{workspace}/clusters/{cluster}/catalogs/{catalog}/schemas/{schema}/tables")
    def fetch_schema_tables(self, tenant: str, workspace: str, cluster: str, catalog: str, schema: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Reply:
        """
        Retrieve a list of tables available within a specific schema in a catalog, cluster, tenant, and workspace.

        Parameters:
            tenant (str): The name of the tenant to which the workspace belongs.
            workspace (str): The name of the workspace containing the cluster.
            cluster (str): The name of the cluster where the catalog resides.
            catalog (str): The name of the catalog containing the schema.
            schema (str): The name of the schema for which tables are to be retrieved.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            Reply: A Reply object containing the table details, which includes:
                - columns (List[Column], optional): Metadata about the tables' structure, including:
                    - name (str, optional): The name of the column.
                    - type (str, optional): The data type of the column.
                - rows (List[List[str]], optional): Data rows representing the tables in the schema.
        """
        pass


    @raise_for_status_code
    @get("api/v2/tenants/{tenant}/wrapped-token")
    def get_wrapped_token(self, tenant: str, workspace: Query('workspace'), cluster: Query('cluster'),
                          apikey: Query('apikey'), correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Retrieve a wrapped token for a specified tenant, workspace, and cluster using an API key.

        Parameters:
            tenant (str): The name of the tenant for which the wrapped token is to be retrieved.
            workspace (Query): The name of the workspace associated with the cluster.
            cluster (Query): The name of the cluster for which the wrapped token is to be generated.
            apikey (Query): The API key used for authentication and authorization of the request.
            correlation_id (str, optional): A unique correlation ID used for request tracking and logging.
                Defaults to a newly generated UUID (Universally Unique Identifier) using uuid.uuid4().

        Returns:
            str: A wrapped token string that can be used for secure communication or further requests.
        """
        pass