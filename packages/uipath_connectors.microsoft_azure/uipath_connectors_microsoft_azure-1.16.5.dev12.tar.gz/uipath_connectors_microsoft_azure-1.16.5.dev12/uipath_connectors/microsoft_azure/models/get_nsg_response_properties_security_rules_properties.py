from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetNSGResponsePropertiesSecurityRulesProperties(BaseModel):
    """
    Attributes:
        access (Optional[str]): The Properties security rules properties access Example: Deny.
        description (Optional[str]): The Properties security rules properties description Example: MDC JIT Network
                Access rule for policy 'default' of VM 'KshitijVM'..
        destination_address_prefix (Optional[str]): The Properties security rules properties destination address prefix
                Example: 192.168.0.4.
        destination_address_prefixes (Optional[list[Any]]): The Properties security rules properties destination address
                prefixes
        destination_port_ranges (Optional[list[str]]):
        direction (Optional[str]): The Properties security rules properties direction Example: Inbound.
        priority (Optional[int]): The Properties security rules properties priority Example: 4096.0.
        protocol (Optional[str]): The Properties security rules properties protocol Example: *.
        provisioning_state (Optional[str]): The Properties security rules properties provisioning state Example:
                Succeeded.
        source_address_prefix (Optional[str]): The Properties security rules properties source address prefix Example:
                *.
        source_address_prefixes (Optional[list[Any]]): The Properties security rules properties source address prefixes
        source_port_range (Optional[str]): The Properties security rules properties source port range Example: *.
        source_port_ranges (Optional[list[Any]]): The Properties security rules properties source port ranges
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Optional[str] = Field(alias="access", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    destination_address_prefix: Optional[str] = Field(
        alias="destinationAddressPrefix", default=None
    )
    destination_address_prefixes: Optional[list[Any]] = Field(
        alias="destinationAddressPrefixes", default=None
    )
    destination_port_ranges: Optional[list[str]] = Field(
        alias="destinationPortRanges", default=None
    )
    direction: Optional[str] = Field(alias="direction", default=None)
    priority: Optional[int] = Field(alias="priority", default=None)
    protocol: Optional[str] = Field(alias="protocol", default=None)
    provisioning_state: Optional[str] = Field(alias="provisioningState", default=None)
    source_address_prefix: Optional[str] = Field(
        alias="sourceAddressPrefix", default=None
    )
    source_address_prefixes: Optional[list[Any]] = Field(
        alias="sourceAddressPrefixes", default=None
    )
    source_port_range: Optional[str] = Field(alias="sourcePortRange", default=None)
    source_port_ranges: Optional[list[Any]] = Field(
        alias="sourcePortRanges", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetNSGResponsePropertiesSecurityRulesProperties"],
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
