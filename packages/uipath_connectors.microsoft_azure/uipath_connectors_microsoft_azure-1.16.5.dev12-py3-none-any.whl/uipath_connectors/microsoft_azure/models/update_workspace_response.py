from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class UpdateWorkspaceResponse(BaseModel):
    """
    Attributes:
        description (Optional[str]): A brief summary of the workspace's purpose or contents. Example: new description.
        friendly_name (Optional[str]): A name that is easy to read and remember, used to identify an item. Example:
                hello-dap.
        id (Optional[str]): The unique identifier for the workspace resource. Example:
                /subscriptions/b65b0225-ce9b-4a79-9dd9-c00071d40d64/resourcegroups/devtest-activities-azure-
                rg/providers/Microsoft.DesktopVirtualization/workspaces/dap-new-1.
        name (Optional[str]): The unique name identifying the workspace. Example: dap-new-1.
        region (Optional[str]): The geographic region where the workspace is deployed. Example: northeurope.
        resource_group_name (Optional[str]): The name of the Azure resource group containing the resources. Example:
                devtest-activities-azure-rg.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: Optional[str] = Field(alias="description", default=None)
    friendly_name: Optional[str] = Field(alias="friendlyName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    region: Optional[str] = Field(alias="region", default=None)
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["UpdateWorkspaceResponse"], src_dict: Dict[str, Any]):
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
