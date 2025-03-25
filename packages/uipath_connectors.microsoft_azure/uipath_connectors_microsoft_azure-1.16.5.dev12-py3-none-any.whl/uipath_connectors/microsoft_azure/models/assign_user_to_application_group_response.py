from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.assign_user_to_application_group_response_properties import (
    AssignUserToApplicationGroupResponseProperties,
)


class AssignUserToApplicationGroupResponse(BaseModel):
    """
    Attributes:
        id (Optional[str]): A unique identifier for the user or group assignment. Example: /subscriptions/c77d325f-9d98-
                4440-9cae-b6aa4465f44d/resourcegroups/test/providers/Microsoft.DesktopVirtualization/applicationgroups/test1-
                DAG/providers/Microsoft.Authorization/roleAssignments/caaf9de4-cb64-4a5e-bc11-84b88266e8a8.
        name (Optional[str]): The name of the user or group being assigned. Example:
                caaf9de4-cb64-4a5e-bc11-84b88266e8a8.
        properties (Optional[AssignUserToApplicationGroupResponseProperties]):
        type_ (Optional[str]): Specifies the type of assignment being made. Example:
                Microsoft.Authorization/roleAssignments.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[str] = Field(alias="id", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    properties: Optional["AssignUserToApplicationGroupResponseProperties"] = Field(
        alias="properties", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AssignUserToApplicationGroupResponse"], src_dict: Dict[str, Any]
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
