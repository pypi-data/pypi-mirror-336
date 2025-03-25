from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Type



class CreateSecurityRuleRequest(BaseModel):
    """
    Attributes:
        access (str): Specifies whether the rule allows or denies traffic. Example: Deny.
        description (str): Provides a brief description of the network security rule. Example: MDC JIT Network Access
                rule for policy 'default' of VM 'KshitijVM'..
        destination_address_prefix (str): Specifies the destination address prefix for the rule. Example: 11.0.0.0/8.
        destination_port_range (str): Specifies the port range for the destination of the traffic. Example: 8080.
        direction (str): Indicates whether the rule applies to inbound or outbound traffic. Example: Outbound.
        priority (int): Defines the order in which rules are applied. Example: 100.0.
        protocol (str): Specifies the protocol used by the network security rule. Example: Any.
        source_address_prefix (str): Specifies the source address prefix for the rule. Example: 10.0.0.0/8.
        source_port_range (str): Indicates the range of source ports for the rule. Example: *.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: str = Field(alias="Access")
    description: str = Field(alias="Description")
    destination_address_prefix: str = Field(alias="DestinationAddressPrefix")
    destination_port_range: str = Field(alias="DestinationPortRange")
    direction: str = Field(alias="Direction")
    priority: int = Field(alias="Priority")
    protocol: str = Field(alias="Protocol")
    source_address_prefix: str = Field(alias="SourceAddressPrefix")
    source_port_range: str = Field(alias="SourcePortRange")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateSecurityRuleRequest"], src_dict: Dict[str, Any]):
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
