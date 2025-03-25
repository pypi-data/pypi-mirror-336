from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetNetworkInterfaceResponseIpConfigurationsArrayItemRef(BaseModel):
    """
    Attributes:
        is_primary (Optional[bool]): Specifies if this is the primary IP configuration for the interface. Example: True.
        name (Optional[str]): The name of the IP configuration within the network interface. Example:
                privateEndpointIpConfig.0575f725-d7ed-4957-9d91-92998e381768.
        private_ip_address (Optional[str]): The private IP address assigned to the network interface. Example:
                10.50.128.26.
        private_ip_address_version (Optional[str]): Indicates the version of the private IP address. Example: IPv4.
        private_ip_allocation_method (Optional[str]): The method used for allocating the private IP address. Example:
                Dynamic.
        public_ip_address (Optional[str]): The public IP address associated with the network interface.
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
        cls: Type["GetNetworkInterfaceResponseIpConfigurationsArrayItemRef"],
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
