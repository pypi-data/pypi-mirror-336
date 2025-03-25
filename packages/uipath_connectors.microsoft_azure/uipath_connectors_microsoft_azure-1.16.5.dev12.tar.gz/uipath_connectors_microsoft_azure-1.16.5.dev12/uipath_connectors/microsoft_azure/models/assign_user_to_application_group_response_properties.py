from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class AssignUserToApplicationGroupResponseProperties(BaseModel):
    """
    Attributes:
        created_on (Optional[datetime.datetime]): The date and time when the action was created. Example:
                2024-11-13T19:49:34.3653158Z.
        principal_id (Optional[str]): The unique identifier for the principal involved in the action. Example:
                bc9a52e1-7fe9-4e60-8c2d-59a935872467.
        principal_type (Optional[str]): The type of principal, such as user or group, involved in the action. Example:
                User.
        role_definition_id (Optional[str]): The unique identifier for the role definition associated with the action.
                Example: /subscriptions/c77d325f-9d98-4440-9cae-
                b6aa4465f44d/providers/Microsoft.Authorization/roleDefinitions/1d18fff3-a72a-46b5-b4a9-0b38a3cd7e63.
        scope (Optional[str]): Defines the scope of the application group assignment. Example: /subscriptions/c77d325f-
                9d98-4440-9cae-
                b6aa4465f44d/resourcegroups/test/providers/Microsoft.DesktopVirtualization/applicationgroups/test1-DAG.
        updated_by (Optional[str]): The user or system that last updated the action. Example:
                da72fc1e-bb75-4731-8cbf-69274f224a36.
        updated_on (Optional[datetime.datetime]): Indicates when the assignment was last updated. Example:
                2024-11-13T19:49:36.4033493Z.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_on: Optional[datetime.datetime] = Field(alias="createdOn", default=None)
    principal_id: Optional[str] = Field(alias="principalId", default=None)
    principal_type: Optional[str] = Field(alias="principalType", default=None)
    role_definition_id: Optional[str] = Field(alias="roleDefinitionId", default=None)
    scope: Optional[str] = Field(alias="scope", default=None)
    updated_by: Optional[str] = Field(alias="updatedBy", default=None)
    updated_on: Optional[datetime.datetime] = Field(alias="updatedOn", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AssignUserToApplicationGroupResponseProperties"],
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
