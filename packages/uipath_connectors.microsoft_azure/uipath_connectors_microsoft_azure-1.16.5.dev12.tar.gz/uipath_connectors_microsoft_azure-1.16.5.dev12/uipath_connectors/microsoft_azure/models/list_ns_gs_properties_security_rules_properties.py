from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListNSGsPropertiesSecurityRulesProperties(BaseModel):
    """
    Attributes:
        access (Optional[str]): Indicates whether the security rule allows or denies traffic. Example: Deny.
        description (Optional[str]): Provides a description for the security rule. Example: MDC JIT Network Access rule
                for policy 'default' of VM 'KshitijVM'..
        destination_address_prefix (Optional[str]): Defines the destination address prefix for the security rule.
                Example: 192.168.0.4.
        destination_port_ranges (Optional[list[str]]):
        direction (Optional[str]): Specifies the direction of traffic the security rule applies to. Example: Inbound.
        priority (Optional[int]): Defines the priority of the security rule. Example: 4096.0.
        protocol (Optional[str]): Defines the network protocol the security rule applies to. Example: *.
        provisioning_state (Optional[str]): Indicates the current provisioning state of the security rule. Example:
                Succeeded.
        source_address_prefix (Optional[str]): Defines the source address prefix for the security rule. Example: *.
        source_port_range (Optional[str]): Specifies the range of source ports for the security rule. Example: *.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Optional[str] = Field(alias="access", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    destination_address_prefix: Optional[str] = Field(
        alias="destinationAddressPrefix", default=None
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
    source_port_range: Optional[str] = Field(alias="sourcePortRange", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListNSGsPropertiesSecurityRulesProperties"], src_dict: Dict[str, Any]
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
