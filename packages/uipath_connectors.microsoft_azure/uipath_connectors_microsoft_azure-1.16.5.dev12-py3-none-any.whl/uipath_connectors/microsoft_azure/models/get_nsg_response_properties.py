from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_nsg_response_properties_default_security_rules_array_item_ref import (
    GetNSGResponsePropertiesDefaultSecurityRulesArrayItemRef,
)
from ..models.get_nsg_response_properties_flow_logs_array_item_ref import (
    GetNSGResponsePropertiesFlowLogsArrayItemRef,
)
from ..models.get_nsg_response_properties_network_interfaces_array_item_ref import (
    GetNSGResponsePropertiesNetworkInterfacesArrayItemRef,
)
from ..models.get_nsg_response_properties_security_rules_array_item_ref import (
    GetNSGResponsePropertiesSecurityRulesArrayItemRef,
)


class GetNSGResponseProperties(BaseModel):
    """
    Attributes:
        default_security_rules (Optional[list['GetNSGResponsePropertiesDefaultSecurityRulesArrayItemRef']]):
        flow_logs (Optional[list['GetNSGResponsePropertiesFlowLogsArrayItemRef']]):
        network_interfaces (Optional[list['GetNSGResponsePropertiesNetworkInterfacesArrayItemRef']]):
        provisioning_state (Optional[str]): The Properties provisioning state Example: Succeeded.
        resource_guid (Optional[str]): The Properties resource guid Example: b596efa3-a95d-4185-a3d6-b0fdc4bc9deb.
        security_rules (Optional[list['GetNSGResponsePropertiesSecurityRulesArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    default_security_rules: Optional[
        list["GetNSGResponsePropertiesDefaultSecurityRulesArrayItemRef"]
    ] = Field(alias="defaultSecurityRules", default=None)
    flow_logs: Optional[list["GetNSGResponsePropertiesFlowLogsArrayItemRef"]] = Field(
        alias="flowLogs", default=None
    )
    network_interfaces: Optional[
        list["GetNSGResponsePropertiesNetworkInterfacesArrayItemRef"]
    ] = Field(alias="networkInterfaces", default=None)
    provisioning_state: Optional[str] = Field(alias="provisioningState", default=None)
    resource_guid: Optional[str] = Field(alias="resourceGuid", default=None)
    security_rules: Optional[
        list["GetNSGResponsePropertiesSecurityRulesArrayItemRef"]
    ] = Field(alias="securityRules", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetNSGResponseProperties"], src_dict: Dict[str, Any]):
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
