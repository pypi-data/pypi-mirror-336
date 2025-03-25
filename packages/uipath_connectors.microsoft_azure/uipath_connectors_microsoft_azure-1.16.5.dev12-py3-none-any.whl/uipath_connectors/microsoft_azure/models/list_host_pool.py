from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_host_pool_host_pool_type import ListHostPoolHostPoolType
from ..models.list_host_pool_load_balancer_type import ListHostPoolLoadBalancerType
from ..models.list_host_pool_personal_desktop_assignment_type import (
    ListHostPoolPersonalDesktopAssignmentType,
)


class ListHostPool(BaseModel):
    """
    Attributes:
        description (Optional[str]): A brief summary of the host pool's purpose and contents.
        host_pool_type (Optional[ListHostPoolHostPoolType]): Specifies whether the host pool is personal or shared.
                Default: ListHostPoolHostPoolType.PERSONAL.
        id (Optional[str]): The unique identifier for the host pool. Example:
                /subscriptions/b65b0225-ce9b-4a79-9dd9-c00071d40d64/resourcegroups/devtest-activities-azure-
                rg/providers/Microsoft.DesktopVirtualization/hostpools/DAP-HOST-POOL.
        is_validation_environment (Optional[bool]): Indicates if the host pool is for validation purposes.
        load_balancer_type (Optional[ListHostPoolLoadBalancerType]): Type of load balancing used for distributing user
                sessions. Default: ListHostPoolLoadBalancerType.DEPTH_FIRST.
        max_session_limit (Optional[int]): The maximum number of concurrent sessions allowed on each host in the pool.
                Example: 999999.0.
        name (Optional[str]): The unique name identifying the host pool. Example: DAP-HOST-POOL.
        personal_desktop_assignment_type (Optional[ListHostPoolPersonalDesktopAssignmentType]): The method used to
                assign personal desktops to users. Default: ListHostPoolPersonalDesktopAssignmentType.AUTOMATIC.
        preferred_app_group_type (Optional[str]): Specifies the default type of application group. Example: Desktop.
        region (Optional[str]): The geographic region where the host pool is located. Example: northeurope.
        resource_group_name (Optional[str]): Name of the Azure resource group containing resources. Example: devtest-
                activities-azure-rg.
        vm_template (Optional[str]): Identifier for the virtual machine template to use. Example: {"domain":"","galleryI
                mageOffer":"windows-10","galleryImagePublisher":"microsoftwindowsdesktop","galleryImageSKU":"win10-22h2-ent-
                g2","imageType":"Gallery","customImageId":null,"namePrefix":"dap","osDiskType":"Standard_LRS","vmSize":{"id":"St
                andard_D2as_v5","cores":2,"ram":8},"galleryItemId":"microsoftwindowsdesktop.windows-10win10-22h2-ent-
                g2","hibernate":false,"diskSizeGB":128,"securityType":"Standard","secureBoot":false,"vTPM":false,"vmInfrastructu
                reType":"Cloud","virtualProcessorCount":null,"memoryGB":null,"maximumMemoryGB":null,"minimumMemoryGB":null,"dyna
                micMemoryConfig":false}.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: Optional[str] = Field(alias="description", default=None)
    host_pool_type: Optional["ListHostPoolHostPoolType"] = Field(
        alias="hostPoolType", default=ListHostPoolHostPoolType.PERSONAL
    )
    id: Optional[str] = Field(alias="id", default=None)
    is_validation_environment: Optional[bool] = Field(
        alias="isValidationEnvironment", default=None
    )
    load_balancer_type: Optional["ListHostPoolLoadBalancerType"] = Field(
        alias="loadBalancerType", default=ListHostPoolLoadBalancerType.DEPTH_FIRST
    )
    max_session_limit: Optional[int] = Field(alias="maxSessionLimit", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    personal_desktop_assignment_type: Optional[
        "ListHostPoolPersonalDesktopAssignmentType"
    ] = Field(
        alias="personalDesktopAssignmentType",
        default=ListHostPoolPersonalDesktopAssignmentType.AUTOMATIC,
    )
    preferred_app_group_type: Optional[str] = Field(
        alias="preferredAppGroupType", default=None
    )
    region: Optional[str] = Field(alias="region", default=None)
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)
    vm_template: Optional[str] = Field(alias="vmTemplate", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListHostPool"], src_dict: Dict[str, Any]):
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
