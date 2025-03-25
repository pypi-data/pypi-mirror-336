from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListSecurityAlertsPropertiesExtendedProperties(BaseModel):
    r"""
    Attributes:
        agent_id (Optional[str]): Unique identifier for the security agent. Example:
                2a157bca-3203-4c42-beff-55fc9316625c.
        alert_id (Optional[str]): Unique identifier for the security alert. Example:
                acc47da5-df44-449a-aa0a-6f4311bdb372.
        client_ip_address (Optional[str]): Shows the IP address of the client involved in the alert. Example:
                212.146.94.118.
        client_application (Optional[str]): Name of the application interacting with the security alert.
        client_hostname (Optional[str]): Shows the hostname of the client related to the alert. Example: MN000003.
        client_principal_name (Optional[str]): Name of the client principal related to the security alert. Example:
                db_admin.
        compromised_entity (Optional[str]): The entity that may have been compromised in the alert. Example: airflow.
        compromised_entity (Optional[str]): Name of the entity that is suspected to be compromised. Example: airflow.
        domain_name (Optional[str]): The domain name related to the security alert. Example: uipath.com.
        domain_name (Optional[str]): The domain name associated with the security alert. Example: solutions-builder-eu-
                alp.uipath.com.
        effective_azure_resource_id (Optional[str]): Azure resource ID that is effectively impacted by the alert.
                Example: /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/pmc-dev-infra-we-
                rg/providers/Microsoft.DBforPostgreSQL/flexibleServers/pmc-dev-dc-we-airflow-postgress-server.
        effective_subscription_id (Optional[str]): Identifier for the subscription under which the alert is effective.
                Example: d10f042e-70ac-4da0-a626-ed1937d5cf4b.
        failed_logins (Optional[str]): The number of unsuccessful login attempts detected. Example: 50.
        investigation_steps (Optional[str]): The steps taken during the investigation of the security alert. Example: {"
                detailBlade":"EngineAuditRecordsBlade","detailBladeInputs":"resourceId=\/subscriptions\/d10f042e-70ac-4da0-a626-
                ed1937d5cf4b\/resourceGroups\/pmc-dev-infra-we-rg\/providers\/Microsoft.DBforPostgreSQL\/flexibleServers\/pmc-
                dev-dc-we-airflow-postgress-server;fromDateTime=2025-02-
                18T10:48:55.5Z;eventId=;showSecurityAlertsRecords=false;showServerRecords=true","displayValue":"View suspicious
                activity","extension":"SqlAzureExtension","kind":"openBlade"}.
        ip_address (Optional[str]): IP address from which the activity triggering the alert originated. Example:
                31.43.185.42.
        log_analytics_workspace_id (Optional[str]): Identifier for the Log Analytics workspace associated with the
                alert. Example: 6c5dc75a-0b7c-45a7-ae5e-ddd1512c4983.
        machine_name (Optional[str]): Specifies the name of the machine involved in the security alert. Example: tmmsi.
        machine_id (Optional[str]): Unique identifier for the machine related to the alert. Example:
                7472a2054ae5b4c9cb98f5871eaa771448531af8.
        microsoft_defender_for_endpoint_link (Optional[str]): Link to the Microsoft Defender for Endpoint details.
                Example: {"displayValue":"Investigate in M365 Defender portal","kind":"Link","value":"https://security.microsoft
                .com/alerts/daae5a082b-fad2-4751-83bf-8bd5af10ac6c_1","alertBladeVisible":true}.
        potential_causes (Optional[str]): Possible reasons why the security alert was triggered. Example: Unauthorized
                access that exploits an opening in the firewall; legitimate access from a new location..
        product_component_name (Optional[str]): Name of the product component related to the alert. Example: Databases.
        resource_type (Optional[str]): Type of resource associated with the security alert. Example: Azure Database for
                PostgreSQL Server.
        sql_instance_name (Optional[str]): Name of the SQL instance related to the security alert. Example: MSSQLSERVER.
        sql_server_name (Optional[str]): Name of the SQL server associated with the security alert. Example: tmmsi.
        successful_logins (Optional[str]): Lists the number of successful logins related to the alert. Example: 0.
        wdatp_tenant_id (Optional[str]): The unique identifier for the Windows Defender ATP tenant. Example:
                d8353d2a-b153-4d17-8827-902c51f72357.
        workspace_resource_group (Optional[str]): Resource group associated with the security workspace. Example: N/A.
        workspace_subscription_id (Optional[str]): The subscription ID of the workspace related to the alert. Example:
                d10f042e-70ac-4da0-a626-ed1937d5cf4b.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    agent_id: Optional[str] = Field(alias="agent ID", default=None)
    alert_id: Optional[str] = Field(alias="alert Id", default=None)
    client_ip_address: Optional[str] = Field(alias="client IP address", default=None)
    client_application: Optional[str] = Field(alias="client application", default=None)
    client_hostname: Optional[str] = Field(alias="client hostname", default=None)
    client_principal_name: Optional[str] = Field(
        alias="client principal name", default=None
    )
    compromised_entity: Optional[str] = Field(alias="compromised entity", default=None)
    compromised_entity: Optional[str] = Field(alias="compromisedEntity", default=None)
    domain_name: Optional[str] = Field(alias="domain name", default=None)
    domain_name: Optional[str] = Field(alias="domainName", default=None)
    effective_azure_resource_id: Optional[str] = Field(
        alias="effectiveAzureResourceId", default=None
    )
    effective_subscription_id: Optional[str] = Field(
        alias="effectiveSubscriptionId", default=None
    )
    failed_logins: Optional[str] = Field(alias="failed logins", default=None)
    investigation_steps: Optional[str] = Field(
        alias="investigation steps", default=None
    )
    ip_address: Optional[str] = Field(alias="ip Address", default=None)
    log_analytics_workspace_id: Optional[str] = Field(
        alias="log Analytics workspace ID", default=None
    )
    machine_name: Optional[str] = Field(alias="machine Name", default=None)
    machine_id: Optional[str] = Field(alias="machineId", default=None)
    microsoft_defender_for_endpoint_link: Optional[str] = Field(
        alias="microsoft Defender for Endpoint link", default=None
    )
    potential_causes: Optional[str] = Field(alias="potential causes", default=None)
    product_component_name: Optional[str] = Field(
        alias="productComponentName", default=None
    )
    resource_type: Optional[str] = Field(alias="resourceType", default=None)
    sql_instance_name: Optional[str] = Field(alias="sql instance name", default=None)
    sql_server_name: Optional[str] = Field(alias="sql server name", default=None)
    successful_logins: Optional[str] = Field(alias="successful logins", default=None)
    wdatp_tenant_id: Optional[str] = Field(alias="wdatpTenantId", default=None)
    workspace_resource_group: Optional[str] = Field(
        alias="workspaceResourceGroup", default=None
    )
    workspace_subscription_id: Optional[str] = Field(
        alias="workspaceSubscriptionId", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListSecurityAlertsPropertiesExtendedProperties"],
        src_dict: Dict[str, Any],
    ):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
