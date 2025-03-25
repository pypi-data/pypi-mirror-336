from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListNSGsValuePropertiesDefaultSecurityRulesProperties(BaseModel):
    """
    Attributes:
        access (Optional[str]): Indicates the access level of the default security rule. Example: Allow.
        description (Optional[str]): Provides a description of the default security rule. Example: Allow inbound traffic
                from all VMs in VNET.
        destination_address_prefix (Optional[str]): Defines the destination address range for the security rule.
                Example: VirtualNetwork.
        destination_address_prefixes (Optional[list[Any]]): Lists the destination address prefixes for default security
                rules.
        destination_port_range (Optional[str]): Specifies the destination port range for the default security rule.
                Example: *.
        destination_port_ranges (Optional[list[Any]]): Lists the destination port ranges for the security rule.
        direction (Optional[str]): Indicates the direction of the default security rule. Example: Inbound.
        priority (Optional[int]): The priority of the default security rule in the list. Example: 65000.0.
        protocol (Optional[str]): Specifies the protocol used in default security rules. Example: *.
        provisioning_state (Optional[str]): Indicates the provisioning state of the default security rule. Example:
                Succeeded.
        source_address_prefix (Optional[str]): Specifies the source address range for the security rule. Example:
                VirtualNetwork.
        source_address_prefixes (Optional[list[Any]]): Lists the source address prefixes for default security rules.
        source_port_range (Optional[str]): The range of source ports for the default security rule. Example: *.
        source_port_ranges (Optional[list[Any]]): Lists the source port ranges for each default security rule.
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
    destination_port_range: Optional[str] = Field(
        alias="destinationPortRange", default=None
    )
    destination_port_ranges: Optional[list[Any]] = Field(
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
        cls: Type["ListNSGsValuePropertiesDefaultSecurityRulesProperties"],
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
