from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_security_alerts_properties_entities_metadata import (
    ListSecurityAlertsPropertiesEntitiesMetadata,
)


class ListSecurityAlertsPropertiesEntitiesArrayItemRef(BaseModel):
    """
    Attributes:
        id (Optional[str]): Unique identifier for the entity within the alert context. Example: westeurope_3.
        asset (Optional[bool]): Identifies the asset associated with the entity in the alert. Example: True.
        metadata (Optional[ListSecurityAlertsPropertiesEntitiesMetadata]):
        resource_id (Optional[str]): Unique identifier for the resource involved in the alert. Example:
                /subscriptions/d10f042e-70ac-4da0-a626-ed1937d5cf4b/resourceGroups/pmc-dev-infra-we-
                rg/providers/Microsoft.DBforPostgreSQL/flexibleServers/pmc-dev-dc-we-airflow-postgress-server.
        resource_name (Optional[str]): The name of the resource associated with the alert. Example: pmc-dev-dc-we-
                airflow-postgress-server.
        resource_type (Optional[str]): Specifies the type of resource associated with the entity. Example: Azure
                Database for PostgreSQL Server.
        type_ (Optional[str]): Specifies the type of entity involved in the alert. Example: azure-resource.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[str] = Field(alias="$id", default=None)
    asset: Optional[bool] = Field(alias="asset", default=None)
    metadata: Optional["ListSecurityAlertsPropertiesEntitiesMetadata"] = Field(
        alias="metadata", default=None
    )
    resource_id: Optional[str] = Field(alias="resourceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_type: Optional[str] = Field(alias="resourceType", default=None)
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListSecurityAlertsPropertiesEntitiesArrayItemRef"],
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
