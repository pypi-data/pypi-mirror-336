from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_ns_gs_value_properties_default_security_rules_array_item_ref import (
    ListNSGsValuePropertiesDefaultSecurityRulesArrayItemRef,
)
from ..models.list_ns_gs_value_properties_flow_logs_array_item_ref import (
    ListNSGsValuePropertiesFlowLogsArrayItemRef,
)
from ..models.list_ns_gs_value_properties_network_interfaces_array_item_ref import (
    ListNSGsValuePropertiesNetworkInterfacesArrayItemRef,
)
from ..models.list_ns_gs_value_properties_security_rules_array_item_ref import (
    ListNSGsValuePropertiesSecurityRulesArrayItemRef,
)


class ListNSGsValueProperties(BaseModel):
    """
    Attributes:
        default_security_rules (Optional[list['ListNSGsValuePropertiesDefaultSecurityRulesArrayItemRef']]):
        flow_logs (Optional[list['ListNSGsValuePropertiesFlowLogsArrayItemRef']]):
        network_interfaces (Optional[list['ListNSGsValuePropertiesNetworkInterfacesArrayItemRef']]):
        provisioning_state (Optional[str]): Indicates the current state of the provisioning process. Example: Succeeded.
        resource_guid (Optional[str]): A unique identifier for the network security group resource. Example:
                cc564f1d-a648-4815-bed4-85b53eafda5a.
        security_rules (Optional[list['ListNSGsValuePropertiesSecurityRulesArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    default_security_rules: Optional[
        list["ListNSGsValuePropertiesDefaultSecurityRulesArrayItemRef"]
    ] = Field(alias="defaultSecurityRules", default=None)
    flow_logs: Optional[list["ListNSGsValuePropertiesFlowLogsArrayItemRef"]] = Field(
        alias="flowLogs", default=None
    )
    network_interfaces: Optional[
        list["ListNSGsValuePropertiesNetworkInterfacesArrayItemRef"]
    ] = Field(alias="networkInterfaces", default=None)
    provisioning_state: Optional[str] = Field(alias="provisioningState", default=None)
    resource_guid: Optional[str] = Field(alias="resourceGuid", default=None)
    security_rules: Optional[
        list["ListNSGsValuePropertiesSecurityRulesArrayItemRef"]
    ] = Field(alias="securityRules", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListNSGsValueProperties"], src_dict: Dict[str, Any]):
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
