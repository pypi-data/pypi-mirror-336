from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_nsg_response_properties import GetNSGResponseProperties


class GetNSGResponse(BaseModel):
    """
    Attributes:
        etag (Optional[str]): The Etag Example: W/"4bc43114-eefb-47e9-bbd0-50d7834ccb41".
        id (Optional[str]): The ID Example: /subscriptions/d10f042e-70ac-4da0-a626-
                ed1937d5cf4b/resourceGroups/kshitijRGDevTestEA/providers/Microsoft.Network/networkSecurityGroups/KshitijVM-nsg.
        location (Optional[str]): The Azure region for the network security group
        name (Optional[str]): The Name Example: KshitijVM-nsg.
        properties (Optional[GetNSGResponseProperties]):
        resource_group_name (Optional[str]): The name of the resource group.
        type_ (Optional[str]): The Type Example: Microsoft.Network/networkSecurityGroups.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    etag: Optional[str] = Field(alias="etag", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    location: Optional[str] = Field(alias="location", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["GetNSGResponseProperties"] = Field(
        alias="properties", default=None
    )
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetNSGResponse"], src_dict: Dict[str, Any]):
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
