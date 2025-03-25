from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_ns_gs_properties_default_security_rules_array_item_ref import (
    ListNSGsPropertiesDefaultSecurityRulesArrayItemRef,
)
from ..models.list_ns_gs_properties_flow_logs_array_item_ref import (
    ListNSGsPropertiesFlowLogsArrayItemRef,
)
from ..models.list_ns_gs_properties_network_interfaces_array_item_ref import (
    ListNSGsPropertiesNetworkInterfacesArrayItemRef,
)
from ..models.list_ns_gs_properties_security_rules_array_item_ref import (
    ListNSGsPropertiesSecurityRulesArrayItemRef,
)


class ListNSGsProperties(BaseModel):
    """
    Attributes:
        default_security_rules (Optional[list['ListNSGsPropertiesDefaultSecurityRulesArrayItemRef']]):
        flow_logs (Optional[list['ListNSGsPropertiesFlowLogsArrayItemRef']]):
        network_interfaces (Optional[list['ListNSGsPropertiesNetworkInterfacesArrayItemRef']]):
        provisioning_state (Optional[str]): Indicates the current provisioning state of the resource. Example:
                Succeeded.
        resource_guid (Optional[str]): A unique identifier for the network security group resource. Example:
                b596efa3-a95d-4185-a3d6-b0fdc4bc9deb.
        security_rules (Optional[list['ListNSGsPropertiesSecurityRulesArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    default_security_rules: Optional[
        list["ListNSGsPropertiesDefaultSecurityRulesArrayItemRef"]
    ] = Field(alias="defaultSecurityRules", default=None)
    flow_logs: Optional[list["ListNSGsPropertiesFlowLogsArrayItemRef"]] = Field(
        alias="flowLogs", default=None
    )
    network_interfaces: Optional[
        list["ListNSGsPropertiesNetworkInterfacesArrayItemRef"]
    ] = Field(alias="networkInterfaces", default=None)
    provisioning_state: Optional[str] = Field(alias="provisioningState", default=None)
    resource_guid: Optional[str] = Field(alias="resourceGuid", default=None)
    security_rules: Optional[list["ListNSGsPropertiesSecurityRulesArrayItemRef"]] = (
        Field(alias="securityRules", default=None)
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListNSGsProperties"], src_dict: Dict[str, Any]):
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
