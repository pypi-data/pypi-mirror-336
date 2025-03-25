from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_security_alerts_properties import ListSecurityAlertsProperties
import datetime


class ListSecurityAlerts(BaseModel):
    """
    Attributes:
        actions_taken (Optional[list[str]]):
        associated_resource_type (Optional[str]): The type of resource linked to the security alert. Example: Virtual
                Machine Scale Set.
        description (Optional[str]): Provides a detailed description of the security alert. Example: Analysis of DNS
                transactions detected a possible DNS tunnel. Such activity, while possibly legitimate user behavior, is
                frequently performed by attackers to evade network monitoring and filtering. Typical related attacker activity
                is likely to include the download and execution of malicious software or remote administration tools..
        detected_time_utc (Optional[datetime.datetime]): The date and time when the security alert was detected, in UTC.
                Example: 2025-02-19T06:45:10.0652248Z.
        display_name (Optional[str]): The user-friendly name of the security alert. Example: Possible data download via
                DNS tunnel.
        full_json (Optional[str]): The complete JSON data of the security alert. Example:
                {"id":"/subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/mc_crpa-alpha-ekb-we-rg_crpa-alpha-
                ekb-we-aks_westeurope/providers/Microsoft.Security/locations/westeurope/alerts/abc0de5d-725d-da22-7a5e-
                1d5873b7f76e","name":"abc0de5d-725d-da22-7a5e-
                1d5873b7f76e","type":"Microsoft.Security/Locations/alerts","properties":{"status":"Active","timeGeneratedUtc":"2
                025-02-19T07:04:02.641Z","processingEndTimeUtc":"2025-02-19T07:04:01.9086034Z","version":"2022-01-
                01.0","vendorName":"Microsoft","productName":"Microsoft Defender for Cloud","productComponentName":"DNS","alertT
                ype":"AzureDNS_DataInfiltration","startTimeUtc":"2025-02-19T06:45:10.0652248Z","endTimeUtc":"2025-02-
                19T06:45:10.0652248Z","severity":"Low","isIncident":false,"systemAlertId":"abc0de5d-725d-da22-7a5e-
                1d5873b7f76e","correlationKey":"","intent":"Exfiltration","resourceIdentifiers":[{"$id":"westeurope_1","azureRes
                ourceId":"/subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourcegroups/mc_crpa-alpha-ekb-we-rg_crpa-alpha-
                ekb-we-aks_westeurope/providers/microsoft.compute/virtualmachinescalesets/aks-nodepool-21258703-
                vmss/virtualmachines/0","type":"AzureResource","azureResourceTenantId":"d8353d2a-b153-4d17-8827-
                902c51f72357"},{"$id":"westeurope_2","aadTenantId":"d8353d2a-b153-4d17-8827-
                902c51f72357","type":"AAD"}],"compromisedEntity":"0","alertDisplayName":"Possible data download via DNS
                tunnel","description":"Analysis of DNS transactions detected a possible DNS tunnel. Such activity, while
                possibly legitimate user behavior, is frequently performed by attackers to evade network monitoring and
                filtering. Typical related attacker activity is likely to include the download and execution of malicious
                software or remote administration tools.","remediationSteps":["Ask the machine owner if this is intended
                behavior.","If the activity is unexpected, treat the machine as potentially compromised and remediate as
                follows.","Isolate the machine from the network to prevent lateral movement.","Run a full antimalware scan on
                the machine, following any resulting remediation advice.","Review installed and running software on the machine,
                removing any unknown or unwanted packages.","Revert the machine to a known good state, reinstalling operating
                system if required and restoring software from a verified malware-free source.","Resolve Azure Security Center
                recommendations for the machine, remediating highlighted security issues to prevent future
                breaches."],"extendedProperties":{"resourceType":"Virtual Machine Scale
                Set","effectiveAzureResourceId":"/subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourcegroups/mc_crpa-
                alpha-ekb-we-rg_crpa-alpha-ekb-we-aks_westeurope/providers/microsoft.compute/virtualmachinescalesets/aks-nodepoo
                l-21258703-
                vmss/virtualmachines/0","compromisedEntity":"0","productComponentName":"DNS","effectiveSubscriptionId":"d10f042e
                -70ac-4da0-a626-
                ed1937d5cf4b","domainName":"tunnel.us3.app.wiz.io"},"entities":[{"$id":"westeurope_3","domainName":"tunnel.us3.a
                pp.wiz.io","asset":false,"type":"dns"},{"$id":"westeurope_4","hostName":"0","azureID":"/subscriptions/d10f042e-
                70ac-4da0-a626-ed1937d5cf4b/resourcegroups/mc_crpa-alpha-ekb-we-rg_crpa-alpha-ekb-we-
                aks_westeurope/providers/microsoft.compute/virtualmachinescalesets/aks-nodepool-21258703-
                vmss/virtualmachines/0","asset":true,"type":"host"},{"$id":"westeurope_5","resourceId":"/subscriptions/d10f042e-
                70ac-4da0-a626-ed1937d5cf4b/resourcegroups/mc_crpa-alpha-ekb-we-rg_crpa-alpha-ekb-we-
                aks_westeurope/providers/microsoft.compute/virtualmachinescalesets/aks-
                nodepool-21258703-vmss/virtualmachines/0","resourceType":"Virtual Machine Scale
                Set","resourceName":"0","metadata":{"isGraphCenter":true},"asset":true,"type":"azure-resource"}],"alertUri":"htt
                ps://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData/AlertBlade/alertId/abc0de5d-725d-
                da22-7a5e-1d5873b7f76e/subscriptionId/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroup/mc_crpa-alpha-ekb-we-
                rg_crpa-alpha-ekb-we-aks_westeurope/referencedFrom/alertDeepLink/location/westeurope"}}.
        id (Optional[str]): The unique identifier for the security alert. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/pmc-dev-infra-we-
                rg/providers/Microsoft.Security/locations/westeurope/alerts/dbea39d8-d158-139e-d206-de56c6042a74.
        location (Optional[str]): Geographical location of the resource. Example: westeurope.
        name (Optional[str]): The unique identifier for the security alert. Example:
                dbea39d8-d158-139e-d206-de56c6042a74.
        properties (Optional[ListSecurityAlertsProperties]):
        reported_time_utc (Optional[datetime.datetime]): Shows the time when the security alert was reported in UTC.
                Example: 2025-02-19T07:04:02.641Z.
        resource_group_name (Optional[str]): The name of the resource group where the alert is located. Example:
                mc_crpa-alpha-ekb-we-rg_crpa-alpha-ekb-we-aks_westeurope.
        resource_names (Optional[list[str]]):
        state (Optional[str]): Indicates the current state of the security alert. Example: Active.
        type_ (Optional[str]): Type of the security alert. Example: Microsoft.Security/Locations/alerts.
        unique_name (Optional[str]): A distinct identifier for the security alert. Example:
                abc0de5d-725d-da22-7a5e-1d5873b7f76e.
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
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["ListSecurityAlertsProperties"] = Field(
        alias="properties", default=None
    )
    reported_time_utc: Optional[datetime.datetime] = Field(
        alias="reportedTimeUtc", default=None
    )
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)
    resource_names: Optional[list[str]] = Field(alias="resourceNames", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    unique_name: Optional[str] = Field(alias="uniqueName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListSecurityAlerts"], src_dict: Dict[str, Any]):
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
