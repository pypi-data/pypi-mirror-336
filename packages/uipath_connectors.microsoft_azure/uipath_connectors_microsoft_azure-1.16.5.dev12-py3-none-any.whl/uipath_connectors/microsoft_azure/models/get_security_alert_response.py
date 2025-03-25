from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetSecurityAlertResponse(BaseModel):
    r"""
    Attributes:
        actions_taken (Optional[list[str]]):
        associated_resource_type (Optional[str]): Type of resource linked to the security alert. Example: SQL Database.
        description (Optional[str]): Provides a detailed explanation of the security alert. Example: Login from an
                unusual location is an anomaly that occurs in the access pattern to your resource.
                Usually, data resources are accessed from similar locations.
                This can be from an application that is accessing the data to provide business logic, or from a user that is
                performing administrative tasks.
                For production workloads, access pattern stabilizes over time to a concrete list of locations. If a login to
                your resource occurs from an unusual location, this indicates an anomaly that should be investigated.
                At times, it can come from a familiar origin that moved to a different location due to IP change/lease, travel,
                or use of different cloud providers, VPNs, etc.
                Often, access from data center is used by IPs that belong to cloud providers, but are leased to customers, and
                therefore do not represent access from the cloud provider company.
                Please inspect the login event, identify the application/user (based on application name and IP/Location) and
                try to find out whether it is familiar to you, or suspicious.
                If it is unrecognized, use firewall rules to limit the access to your resource, and make sure you use strong
                passwords and not well known user names.
                Also, consider using only AAD authentication to further enhance your security posture.
                Finally, review the Audit logs (if turned on) to understand the activity that was made, and consider taking
                additional actions to protect the data.
                .
        detected_time_utc (Optional[datetime.datetime]): Specifies the time when the alert was detected in UTC. Example:
                2025-02-07T20:41:19Z.
        display_name (Optional[str]): User-friendly name for the security alert. Example: Login from an unusual
                location.
        full_json (Optional[str]): Complete JSON data related to the security alert. Example:
                {"id":"/subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/crpa-alpha-orch-fc-rg/providers/Micros
                oft.Security/locations/westeurope/alerts/b7df3375-ae56-8eeb-92b6-3f7428033f04","name":"b7df3375-ae56-8eeb-92b6-
                3f7428033f04","type":"Microsoft.Security/Locations/alerts","properties":{"status":"Resolved","timeGeneratedUtc":
                "2025-02-07T21:12:00.133Z","processingEndTimeUtc":"2025-02-07T21:11:59.9614932Z","version":"2022-01-
                01.1","vendorName":"Microsoft","productName":"Microsoft Defender for Cloud","productComponentName":"Databases","
                alertType":"SQL.DB_GeoAnomaly","startTimeUtc":"2025-02-07T20:41:19Z","endTimeUtc":"2025-02-
                07T20:41:19Z","severity":"Medium","isIncident":false,"systemAlertId":"b7df3375-ae56-8eeb-92b6-
                3f7428033f04","correlationKey":"Ezz7RP/4Gyqg8Mm2MiKpILOzm0ZRUmkrPyePfxjOG1Dw8BZyXnN8q1hZwh4KEnlJvpTD0Sy7++PL70G7
                t0CpSw==","intent":"InitialAccess","resourceIdentifiers":[{"$id":"westeurope_1","azureResourceId":"/subscription
                s/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/crpa-alpha-orch-fc-
                rg/providers/Microsoft.Sql/servers/crpa-alpha-orch0-fc-sql/databases/crpa-alpha-orch0-fc-db","type":"AzureResour
                ce","azureResourceTenantId":"d8353d2a-b153-4d17-8827-
                902c51f72357"},{"$id":"westeurope_2","aadTenantId":"d8353d2a-b153-4d17-8827-
                902c51f72357","type":"AAD"}],"compromisedEntity":"crpa-alpha-orch0-fc-db","alertDisplayName":"Login from an
                unusual location","description":"Login from an unusual location is an anomaly that occurs in the access pattern
                to your resource. \r\nUsually, data resources are accessed from similar locations. \r\nThis can be from an
                application that is accessing the data to provide business logic, or from a user that is performing
                administrative tasks. \r\nFor production workloads, access pattern stabilizes over time to a concrete list of
                locations. If a login to your resource occurs from an unusual location, this indicates an anomaly that should be
                investigated. \r\nAt times, it can come from a familiar origin that moved to a different location due to IP
                change/lease, travel, or use of different cloud providers, VPNs, etc. \r\nOften, access from data center is used
                by IPs that belong to cloud providers, but are leased to customers, and therefore do not represent access from
                the cloud provider company. \r\nPlease inspect the login event, identify the application/user (based on
                application name and IP/Location) and try to find out whether it is familiar to you, or suspicious. \r\nIf it is
                unrecognized, use firewall rules to limit the access to your resource, and make sure you use strong passwords
                and not well known user names.\r\nAlso, consider using only AAD authentication to further enhance your security
                posture. \r\nFinally, review the Audit logs (if turned on) to understand the activity that was made, and
                consider taking additional actions to protect the data.\r\n","remediationSteps":["Go to the firewall settings
                (in the Networking page of the resource) in order to lock down the firewall as tightly as
                possible."],"extendedProperties":{"alert Id":"f92309f7-e047-4f96-976d-14b2010f3435","compromised entity":"crpa-
                alpha-orch0-fc-db","client IP address":"73.230.141.252","client hostname":"LAPTOP-TMFNH8IN","client principal
                name":"insights","client application":"Microsoft SQL Server Management Studio - Transact-SQL
                IntelliSense","investigation steps":"{\"detailBlade\":\"EngineAuditRecordsBlade\",\"detailBladeInputs\":\"resour
                ceId=\\/subscriptions\\/d10f042e-70ac-4da0-a626-ed1937d5cf4b\\/resourceGroups\\/crpa-alpha-orch-fc-
                rg\\/providers\\/Microsoft.Sql\\/servers\\/crpa-alpha-orch0-fc-sql\\/databases\\/crpa-alpha-orch0-fc-db;fromDate
                Time=2025-02-07T20:41:19.5Z;eventId=cc93d9f4-a4b4-422c-b38c-
                ddfcc7afe73e;showSecurityAlertsRecords=false;showServerRecords=true\",\"displayValue\":\"View suspicious
                activity\",\"extension\":\"SqlAzureExtension\",\"kind\":\"openBlade\"}","potential causes":"Unauthorized access
                that exploits an opening in the firewall; legitimate access from a new location.","resourceType":"SQL
                Database","effectiveAzureResourceId":"/subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/crpa-
                alpha-orch-fc-rg/providers/Microsoft.Sql/servers/crpa-alpha-orch0-fc-sql/databases/crpa-alpha-orch0-fc-
                db","compromisedEntity":"crpa-alpha-orch0-fc-db","productComponentName":"Databases","effectiveSubscriptionId":"d
                10f042e-70ac-4da0-a626-ed1937d5cf4b"},"entities":[{"$id":"westeurope_3","resourceId":"/subscriptions/d10f042e-
                70ac-4da0-a626-ed1937d5cf4b/resourceGroups/crpa-alpha-orch-fc-rg/providers/Microsoft.Sql/servers/crpa-alpha-
                orch0-fc-sql/databases/crpa-alpha-orch0-fc-db","resourceType":"SQL Database","resourceName":"crpa-alpha-
                orch0-fc-db","metadata":{"isGraphCenter":true},"asset":true,"type":"azure-resource"},{"$id":"westeurope_4","sour
                ceAddress":{"$id":"westeurope_5","address":"73.230.141.252","location":{"countryCode":"us","countryName":"united
                states","state":"pennsylvania","city":"reading","longitude":-
                76,"latitude":40,"asn":7922,"carrier":"comcast","organization":"comcast","organizationType":"Internet Service Pr
                ovider","cloudProvider":"N/A"},"asset":false,"type":"ip"},"friendlyName":"73.230.141.252","asset":false,"type":"
                network-connection"},{"$ref":"westeurope_5"},{"$id":"westeurope_6","name":"insights","host":{"$id":"westeurope_7
                ","hostName":"LAPTOP-TMFNH8IN","asset":false,"type":"host"},"isDomainJoined":false,"asset":true,"type":"account"
                },{"$ref":"westeurope_7"}],"alertUri":"https://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderFor
                Data/AlertBlade/alertId/b7df3375-ae56-8eeb-92b6-3f7428033f04/subscriptionId/d10f042e-70ac-4da0-a626-
                ed1937d5cf4b/resourceGroup/crpa-alpha-orch-fc-rg/referencedFrom/alertDeepLink/location/westeurope"}}.
        id (Optional[str]): A unique identifier for the security alert or resource. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/at-alp-
                eus-01-rg/providers/Microsoft.Security/locations/westeurope/alerts/b845b92d-1228-8d9f-5567-b368386e7d7a.
        location (Optional[str]): Specifies the geographical region of the resource.
        reported_time_utc (Optional[datetime.datetime]): Indicates the time when the alert was reported in UTC. Example:
                2025-02-07T21:12:00.133Z.
        resource_group_name (Optional[str]): Name of the resource group containing the alert.
        resource_names (Optional[list[str]]):
        state (Optional[str]): Indicates the current status of the security alert. Example: Resolved.
        unique_name (Optional[str]): A distinct identifier for the security alert. Example:
                b7df3375-ae56-8eeb-92b6-3f7428033f04.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actions_taken: Optional[list[str]] = Field(alias="actionsTaken", default=None)
    associated_resource_type: Optional[str] = Field(
        alias="associatedResourceType", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    detected_time_utc: Optional[datetime.datetime] = Field(
        alias="detectedTimeUtc", default=None
    )
    display_name: Optional[str] = Field(alias="displayName", default=None)
    full_json: Optional[str] = Field(alias="fullJson", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    location: Optional[str] = Field(alias="location", default=None)
    reported_time_utc: Optional[datetime.datetime] = Field(
        alias="reportedTimeUtc", default=None
    )
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)
    resource_names: Optional[list[str]] = Field(alias="resourceNames", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    unique_name: Optional[str] = Field(alias="uniqueName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetSecurityAlertResponse"], src_dict: Dict[str, Any]):
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
