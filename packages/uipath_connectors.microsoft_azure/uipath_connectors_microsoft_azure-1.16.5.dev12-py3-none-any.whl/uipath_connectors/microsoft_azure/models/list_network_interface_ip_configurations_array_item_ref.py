from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListNetworkInterfaceIpConfigurationsArrayItemRef(BaseModel):
    """
    Attributes:
        is_primary (Optional[bool]): Shows if the IP configuration is the primary one. Example: True.
        name (Optional[str]): The name of the IP configuration. Example:
                privateEndpointIpConfig.f7457d82-475f-4345-9252-d8b36491229c.
        private_ip_address (Optional[str]): The private IP address assigned to the network interface. Example:
                10.50.255.12.
        private_ip_address_version (Optional[str]): Indicates the version of the private IP address used. Example: IPv4.
        private_ip_allocation_method (Optional[str]): Specifies how the private IP address is allocated. Example:
                Dynamic.
        public_ip_address (Optional[str]): The public IP address associated with the IP configuration.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    is_primary: Optional[bool] = Field(alias="IsPrimary", default=None)
    name: Optional[str] = Field(alias="Name", default=None)
    private_ip_address: Optional[str] = Field(alias="PrivateIpAddress", default=None)
    private_ip_address_version: Optional[str] = Field(
        alias="PrivateIpAddressVersion", default=None
    )
    private_ip_allocation_method: Optional[str] = Field(
        alias="PrivateIpAllocationMethod", default=None
    )
    public_ip_address: Optional[str] = Field(alias="PublicIpAddress", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListNetworkInterfaceIpConfigurationsArrayItemRef"],
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
