from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_ns_gs_value_properties_security_rules_properties import (
    ListNSGsValuePropertiesSecurityRulesProperties,
)


class ListNSGsValuePropertiesSecurityRulesArrayItemRef(BaseModel):
    """
    Attributes:
        etag (Optional[str]): Entity tag for the security rule, used for concurrency control. Example:
                W/"fde31089-5926-4b4c-adcc-6a4677e476b2".
        id (Optional[str]): Unique identifier for the security rule. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/cis-dtl4187768393001/providers/Microsoft.Netw
                ork/networkSecurityGroups/PaaSAutomationRobot2-nsg/securityRules/MicrosoftDefenderForCloud-
                JITRule_-2060018277_F71F4F64799F4B6DBBE1914AB79A527C.
        name (Optional[str]): The name of the security rule in the network security group. Example:
                MicrosoftDefenderForCloud-JITRule_-2060018277_F71F4F64799F4B6DBBE1914AB79A527C.
        properties (Optional[ListNSGsValuePropertiesSecurityRulesProperties]):
        type_ (Optional[str]): The type of security rule applied to the network security group. Example:
                Microsoft.Network/networkSecurityGroups/securityRules.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    etag: Optional[str] = Field(alias="etag", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["ListNSGsValuePropertiesSecurityRulesProperties"] = Field(
        alias="properties", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListNSGsValuePropertiesSecurityRulesArrayItemRef"],
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
