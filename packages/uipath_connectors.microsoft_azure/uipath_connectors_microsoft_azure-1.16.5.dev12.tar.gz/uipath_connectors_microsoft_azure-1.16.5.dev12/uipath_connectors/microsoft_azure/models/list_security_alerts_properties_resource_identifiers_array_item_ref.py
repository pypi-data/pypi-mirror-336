from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef(BaseModel):
    """
    Attributes:
        id (Optional[str]): Unique identifier for the resource involved in the alert. Example: westeurope_1.
        azure_resource_id (Optional[str]): Unique identifier for the Azure resource. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/pmc-dev-infra-we-
                rg/providers/Microsoft.DBforPostgreSQL/flexibleServers/pmc-dev-dc-we-airflow-postgress-server.
        azure_resource_tenant_id (Optional[str]): The tenant ID of the Azure resource linked to the alert. Example:
                d8353d2a-b153-4d17-8827-902c51f72357.
        type_ (Optional[str]): Defines the type of resource identifier associated with the alert. Example:
                AzureResource.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[str] = Field(alias="$id", default=None)
    azure_resource_id: Optional[str] = Field(alias="azureResourceId", default=None)
    azure_resource_tenant_id: Optional[str] = Field(
        alias="azureResourceTenantId", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef"],
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
