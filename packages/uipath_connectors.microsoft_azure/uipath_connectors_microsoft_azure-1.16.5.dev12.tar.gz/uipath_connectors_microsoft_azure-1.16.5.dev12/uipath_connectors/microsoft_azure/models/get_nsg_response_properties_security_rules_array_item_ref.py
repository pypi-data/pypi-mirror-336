from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_nsg_response_properties_security_rules_properties import (
    GetNSGResponsePropertiesSecurityRulesProperties,
)


class GetNSGResponsePropertiesSecurityRulesArrayItemRef(BaseModel):
    """
    Attributes:
        etag (Optional[str]): The Properties security rules etag Example: W/"4bc43114-eefb-47e9-bbd0-50d7834ccb41".
        id (Optional[str]): The Properties security rules ID Example: /subscriptions/d10f042e-70ac-4da0-a626-
                ed1937d5cf4b/resourceGroups/kshitijRGDevTestEA/providers/Microsoft.Network/networkSecurityGroups/KshitijVM-
                nsg/securityRules/MicrosoftDefenderForCloud-JITRule_2114225062_213199037216425D9204C19E2158183D.
        name (Optional[str]): The Properties security rules name Example: MicrosoftDefenderForCloud-
                JITRule_2114225062_213199037216425D9204C19E2158183D.
        properties (Optional[GetNSGResponsePropertiesSecurityRulesProperties]):
        type_ (Optional[str]): The Properties security rules type Example:
                Microsoft.Network/networkSecurityGroups/securityRules.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    etag: Optional[str] = Field(alias="etag", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["GetNSGResponsePropertiesSecurityRulesProperties"] = Field(
        alias="properties", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetNSGResponsePropertiesSecurityRulesArrayItemRef"],
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
