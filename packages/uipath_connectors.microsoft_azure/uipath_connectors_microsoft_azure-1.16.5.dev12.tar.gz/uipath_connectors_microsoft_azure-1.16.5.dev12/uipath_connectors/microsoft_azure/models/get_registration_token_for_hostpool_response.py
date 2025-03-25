from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_registration_token_for_hostpool_response_properties import (
    GetRegistrationTokenForHostpoolResponseProperties,
)
from ..models.get_registration_token_for_hostpool_response_system_data import (
    GetRegistrationTokenForHostpoolResponseSystemData,
)


class GetRegistrationTokenForHostpoolResponse(BaseModel):
    """
    Attributes:
        id (Optional[str]): A unique identifier for the resource. Example: /subscriptions/c77d325f-9d98-4440-9cae-
                b6aa4465f44d/resourcegroups/test/providers/Microsoft.DesktopVirtualization/hostpools/test2.
        location (Optional[str]): Specifies the geographical location of the resource. Example: northeurope.
        name (Optional[str]): The unique name assigned to the hostpool. Example: test2.
        properties (Optional[GetRegistrationTokenForHostpoolResponseProperties]):
        system_data (Optional[GetRegistrationTokenForHostpoolResponseSystemData]):
        type_ (Optional[str]): Indicates the type of resource being referenced. Example:
                Microsoft.DesktopVirtualization/hostpools.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[str] = Field(alias="id", default=None)
    location: Optional[str] = Field(alias="location", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["GetRegistrationTokenForHostpoolResponseProperties"] = Field(
        alias="properties", default=None
    )
    system_data: Optional["GetRegistrationTokenForHostpoolResponseSystemData"] = Field(
        alias="systemData", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetRegistrationTokenForHostpoolResponse"], src_dict: Dict[str, Any]
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
