from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_security_alerts_properties_entities_array_item_ref import (
    ListSecurityAlertsPropertiesEntitiesArrayItemRef,
)
from ..models.list_security_alerts_properties_extended_links_array_item_ref import (
    ListSecurityAlertsPropertiesExtendedLinksArrayItemRef,
)
from ..models.list_security_alerts_properties_extended_properties import (
    ListSecurityAlertsPropertiesExtendedProperties,
)
from ..models.list_security_alerts_properties_resource_identifiers_array_item_ref import (
    ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef,
)
from ..models.list_security_alerts_properties_supporting_evidence import (
    ListSecurityAlertsPropertiesSupportingEvidence,
)
import datetime


class ListSecurityAlertsProperties(BaseModel):
    """
    Attributes:
        alert_display_name (Optional[str]): User-friendly name of the security alert. Example: Login from an unusual
                location.
        alert_type (Optional[str]): The category or type of the security alert. Example: SQL.PostgreSQL_GeoAnomaly.
        alert_uri (Optional[str]): The URI link to access detailed information about the alert. Example: https://portal.
                azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData/AlertBlade/alertId/dbea39d8-d158-139e-d206-
                de56c6042a74/subscriptionId/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroup/pmc-dev-infra-we-
                rg/referencedFrom/alertDeepLink/location/westeurope.
        compromised_entity (Optional[str]): The entity that has been compromised in the security alert. Example:
                airflow.
        correlation_key (Optional[str]): Key used to correlate related security alerts. Example:
                l5DZhUrGJdn42m9xmKrfVJm0z5iDMImsTKbgp/ZNrxggFeX/Fq2vIepKfp2ysJLH6e58ESqElz+H+KRaU1fL8A==.
        description (Optional[str]): Detailed description of the security alert. Example: Login from an unusual location
                is an anomaly that occurs in the access pattern to your resource.
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
        end_time_utc (Optional[datetime.datetime]): The time when the security alert ended, in UTC. Example:
                2025-02-18T10:48:55Z.
        entities (Optional[list['ListSecurityAlertsPropertiesEntitiesArrayItemRef']]):
        extended_links (Optional[list['ListSecurityAlertsPropertiesExtendedLinksArrayItemRef']]):
        extended_properties (Optional[ListSecurityAlertsPropertiesExtendedProperties]):
        intent (Optional[str]): The purpose or goal of the security alert. Example: InitialAccess.
        is_incident (Optional[bool]): Indicates if the alert is part of a security incident.
        processing_end_time_utc (Optional[datetime.datetime]): Indicates the time when alert processing was completed in
                UTC. Example: 2025-02-18T11:35:33.9556629Z.
        product_component_name (Optional[str]): Name of the product component associated with the alert. Example:
                Databases.
        product_name (Optional[str]): The name of the product associated with the alert. Example: Microsoft Defender for
                Cloud.
        resource_identifiers (Optional[list['ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef']]):
        severity (Optional[str]): The level of severity assigned to the security alert. Example: Medium.
        start_time_utc (Optional[datetime.datetime]): The date and time when the security alert started, in UTC.
                Example: 2025-02-18T10:48:55Z.
        status (Optional[str]): Indicates the current status of the security alert. Example: Resolved.
        supporting_evidence (Optional[ListSecurityAlertsPropertiesSupportingEvidence]):
        system_alert_id (Optional[str]): Unique identifier for the system-generated security alert. Example:
                dbea39d8-d158-139e-d206-de56c6042a74.
        time_generated_utc (Optional[datetime.datetime]): The time when the security alert was generated, in UTC.
                Example: 2025-02-18T11:35:33.998Z.
        vendor_name (Optional[str]): Name of the vendor providing the security alert. Example: Microsoft.
        version (Optional[str]): Specifies the version of the security alert. Example: 2022-01-01.1.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alert_display_name: Optional[str] = Field(alias="alertDisplayName", default=None)
    alert_type: Optional[str] = Field(alias="alertType", default=None)
    alert_uri: Optional[str] = Field(alias="alertUri", default=None)
    compromised_entity: Optional[str] = Field(alias="compromisedEntity", default=None)
    correlation_key: Optional[str] = Field(alias="correlationKey", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    end_time_utc: Optional[datetime.datetime] = Field(alias="endTimeUtc", default=None)
    entities: Optional[list["ListSecurityAlertsPropertiesEntitiesArrayItemRef"]] = (
        Field(alias="entities", default=None)
    )
    extended_links: Optional[
        list["ListSecurityAlertsPropertiesExtendedLinksArrayItemRef"]
    ] = Field(alias="extendedLinks", default=None)
    extended_properties: Optional["ListSecurityAlertsPropertiesExtendedProperties"] = (
        Field(alias="extendedProperties", default=None)
    )
    intent: Optional[str] = Field(alias="intent", default=None)
    is_incident: Optional[bool] = Field(alias="isIncident", default=None)
    processing_end_time_utc: Optional[datetime.datetime] = Field(
        alias="processingEndTimeUtc", default=None
    )
    product_component_name: Optional[str] = Field(
        alias="productComponentName", default=None
    )
    product_name: Optional[str] = Field(alias="productName", default=None)
    resource_identifiers: Optional[
        list["ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef"]
    ] = Field(alias="resourceIdentifiers", default=None)
    severity: Optional[str] = Field(alias="severity", default=None)
    start_time_utc: Optional[datetime.datetime] = Field(
        alias="startTimeUtc", default=None
    )
    status: Optional[str] = Field(alias="status", default=None)
    supporting_evidence: Optional["ListSecurityAlertsPropertiesSupportingEvidence"] = (
        Field(alias="supportingEvidence", default=None)
    )
    system_alert_id: Optional[str] = Field(alias="systemAlertId", default=None)
    time_generated_utc: Optional[datetime.datetime] = Field(
        alias="timeGeneratedUtc", default=None
    )
    vendor_name: Optional[str] = Field(alias="vendorName", default=None)
    version: Optional[str] = Field(alias="version", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListSecurityAlertsProperties"], src_dict: Dict[str, Any]):
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
