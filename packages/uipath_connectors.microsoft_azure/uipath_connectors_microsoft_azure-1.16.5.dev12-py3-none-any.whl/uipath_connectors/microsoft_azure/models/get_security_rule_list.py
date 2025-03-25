from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetSecurityRuleList(BaseModel):
    """
    Attributes:
        action (Optional[str]): Defines the action to be taken, such as allow or deny. Example: Deny.
        description (Optional[str]): Provides a brief description of the network security rule. Example: MDC JIT Network
                Access rule for policy 'default' of VM 'KshitijVM'..
        destination_address_prefixes (Optional[str]): Specifies the destination address prefixes for the rule. Example:
                11.0.0.0/8.
        destination_port_ranges (Optional[str]): Specifies the range of destination ports for the rule. Example: 8080.
        direction (Optional[str]): Indicates whether the rule applies to inbound or outbound traffic. Example: Outbound.
        id (Optional[str]): A unique identifier for the network security rule. Example: /subscriptions/d10f042e-70ac-
                4da0-a626-
                ed1937d5cf4b/resourceGroups/kshitijRGDevTestEA/providers/Microsoft.Network/networkSecurityGroups/KshitijVM-
                nsg/securityRules/divijRule.
        nsg_name (Optional[str]): The name of the network security group associated with the rule. Example: KshitijVM-
                nsg.
        name (Optional[str]): The unique identifier for the network security rule. Example: divijRule.
        priority (Optional[int]): Defines the order in which rules are applied. Example: 100.0.
        protocol (Optional[str]): Specifies the protocol used by the network security rule. Example: Any.
        resource_group_name (Optional[str]): The name of the resource group containing the network security rule.
                Example: kshitijRGDevTestEA.
        source_address_prefixes (Optional[str]): Lists the source address prefixes applicable to the rule. Example:
                10.0.0.0/8.
        source_port_ranges (Optional[str]): Specifies the range of source ports for the rule. Example: *.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    action: Optional[str] = Field(alias="Action", default=None)
    description: Optional[str] = Field(alias="Description", default=None)
    destination_address_prefixes: Optional[str] = Field(
        alias="DestinationAddressPrefixes", default=None
    )
    destination_port_ranges: Optional[str] = Field(
        alias="DestinationPortRanges", default=None
    )
    direction: Optional[str] = Field(alias="Direction", default=None)
    id: Optional[str] = Field(alias="Id", default=None)
    nsg_name: Optional[str] = Field(alias="NSGName", default=None)
    name: Optional[str] = Field(alias="Name", default=None)
    priority: Optional[int] = Field(alias="Priority", default=None)
    protocol: Optional[str] = Field(alias="Protocol", default=None)
    resource_group_name: Optional[str] = Field(alias="ResourceGroupName", default=None)
    source_address_prefixes: Optional[str] = Field(
        alias="SourceAddressPrefixes", default=None
    )
    source_port_ranges: Optional[str] = Field(alias="SourcePortRanges", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetSecurityRuleList"], src_dict: Dict[str, Any]):
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
