from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_network_interface_response_ip_configurations_array_item_ref import (
    GetNetworkInterfaceResponseIpConfigurationsArrayItemRef,
)
from ..models.get_network_interface_response_tags import GetNetworkInterfaceResponseTags


class GetNetworkInterfaceResponse(BaseModel):
    """
    Attributes:
        accelerated_networking_enabled (Optional[bool]): Indicates if accelerated networking is enabled.
        ip_configurations (Optional[list['GetNetworkInterfaceResponseIpConfigurationsArrayItemRef']]):
        ip_forwarding_enabled (Optional[bool]): Indicates if IP forwarding is enabled for the interface.
        location (Optional[str]): Specifies the geographic location of the network interface. Example: eastus.
        nsg_name (Optional[str]): The name of the associated network security group.
        name (Optional[str]): The unique name of the network interface. Example: test-proxy-vnet-nic.
        resource_group_name (Optional[str]): The name of the resource group containing the network interface. Example:
                anub-experiments.
        subnet_name (Optional[list[str]]):
        tags (Optional[GetNetworkInterfaceResponseTags]):
        virtual_network_names (Optional[list[str]]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    accelerated_networking_enabled: Optional[bool] = Field(
        alias="AcceleratedNetworkingEnabled", default=None
    )
    ip_configurations: Optional[
        list["GetNetworkInterfaceResponseIpConfigurationsArrayItemRef"]
    ] = Field(alias="IpConfigurations", default=None)
    ip_forwarding_enabled: Optional[bool] = Field(
        alias="IpForwardingEnabled", default=None
    )
    location: Optional[str] = Field(alias="Location", default=None)
    nsg_name: Optional[str] = Field(alias="NSGName", default=None)
    name: Optional[str] = Field(alias="Name", default=None)
    resource_group_name: Optional[str] = Field(alias="ResourceGroupName", default=None)
    subnet_name: Optional[list[str]] = Field(alias="SubnetName", default=None)
    tags: Optional["GetNetworkInterfaceResponseTags"] = Field(
        alias="Tags", default=None
    )
    virtual_network_names: Optional[list[str]] = Field(
        alias="VirtualNetworkNames", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetNetworkInterfaceResponse"], src_dict: Dict[str, Any]):
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
