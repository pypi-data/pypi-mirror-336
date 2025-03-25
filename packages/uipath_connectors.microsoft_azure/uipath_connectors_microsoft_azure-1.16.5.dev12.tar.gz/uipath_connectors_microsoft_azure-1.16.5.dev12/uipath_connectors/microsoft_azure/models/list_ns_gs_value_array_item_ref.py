from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_ns_gs_value_properties import ListNSGsValueProperties


class ListNSGsValueArrayItemRef(BaseModel):
    """
    Attributes:
        etag (Optional[str]): A unique string that identifies the current version of the resource. Example:
                W/"fde31089-5926-4b4c-adcc-6a4677e476b2".
        id (Optional[str]): Unique identifier for the resource. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/cis-
                dtl4187768393001/providers/Microsoft.Network/networkSecurityGroups/PaaSAutomationRobot2-nsg.
        location (Optional[str]): Specifies the geographical location of the resource. Example: westus.
        name (Optional[str]): The name assigned to the network security group. Example: PaaSAutomationRobot2-nsg.
        properties (Optional[ListNSGsValueProperties]):
        type_ (Optional[str]): Specifies the type of the Azure resource. Example:
                Microsoft.Network/networkSecurityGroups.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    etag: Optional[str] = Field(alias="etag", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    location: Optional[str] = Field(alias="location", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["ListNSGsValueProperties"] = Field(
        alias="properties", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListNSGsValueArrayItemRef"], src_dict: Dict[str, Any]):
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
