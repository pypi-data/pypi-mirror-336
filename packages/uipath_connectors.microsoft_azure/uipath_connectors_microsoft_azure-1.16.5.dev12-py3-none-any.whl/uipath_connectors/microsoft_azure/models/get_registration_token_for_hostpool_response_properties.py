from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_registration_token_for_hostpool_response_properties_registration_info import (
    GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo,
)


class GetRegistrationTokenForHostpoolResponseProperties(BaseModel):
    """
    Attributes:
        application_group_references (Optional[list[str]]):
        cloud_pc_resource (Optional[bool]): Specifies the cloud PC resource associated with the hostpool.
        custom_rdp_property (Optional[str]): Settings for Remote Desktop Protocol specific to this hostpool. Example: dr
                ivestoredirect:s:*;audiomode:i:0;videoplaybackmode:i:1;redirectclipboard:i:1;redirectprinters:i:1;devicestoredir
                ect:s:*;redirectcomports:i:1;redirectsmartcards:i:1;usbdevicestoredirect:s:*;enablecredsspsupport:i:1;redirectwe
                bauthn:i:1;use multimon:i:1;.
        host_pool_type (Optional[str]): Indicates the type of host pool being used. Example: Personal.
        load_balancer_type (Optional[str]): Defines the type of load balancing used for distributing sessions. Example:
                Persistent.
        max_session_limit (Optional[int]): Maximum number of sessions allowed per virtual machine. Example: 999999.0.
        object_id (Optional[str]): The unique identifier for the object in the directory. Example:
                730ae1b3-331c-4ae9-a883-9e9a037e0929.
        personal_desktop_assignment_type (Optional[str]): Specifies how personal desktops are assigned to users.
                Example: Automatic.
        preferred_app_group_type (Optional[str]): The type of application group preferred for this hostpool. Example:
                Desktop.
        registration_info (Optional[GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo]):
        ring (Optional[int]): Defines the deployment ring for the hostpool. Example: 1.0.
        start_vm_on_connect (Optional[bool]): Indicates if the virtual machine should start when a user connects.
        validation_environment (Optional[bool]): Specifies the environment used for validating the token.
        vm_template (Optional[str]): Template used for creating virtual machines in the hostpool. Example: {"domain":"",
                "galleryImageOffer":"windows-10","galleryImagePublisher":"microsoftwindowsdesktop","galleryImageSKU":"win10-
                22h2-ent-
                g2","imageType":"Gallery","customImageId":null,"namePrefix":"test2","osDiskType":"StandardSSD_LRS","vmSize":{"id
                ":"Standard_D2as_v5","cores":2,"ram":8},"galleryItemId":"microsoftwindowsdesktop.windows-10win10-22h2-ent-
                g2","hibernate":false,"diskSizeGB":128,"securityType":"TrustedLaunch","secureBoot":true,"vTPM":true,"vmInfrastru
                ctureType":"Cloud","virtualProcessorCount":null,"memoryGB":null,"maximumMemoryGB":null,"minimumMemoryGB":null,"d
                ynamicMemoryConfig":false}.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    application_group_references: Optional[list[str]] = Field(
        alias="applicationGroupReferences", default=None
    )
    cloud_pc_resource: Optional[bool] = Field(alias="cloudPcResource", default=None)
    custom_rdp_property: Optional[str] = Field(alias="customRdpProperty", default=None)
    host_pool_type: Optional[str] = Field(alias="hostPoolType", default=None)
    load_balancer_type: Optional[str] = Field(alias="loadBalancerType", default=None)
    max_session_limit: Optional[int] = Field(alias="maxSessionLimit", default=None)
    object_id: Optional[str] = Field(alias="objectId", default=None)
    personal_desktop_assignment_type: Optional[str] = Field(
        alias="personalDesktopAssignmentType", default=None
    )
    preferred_app_group_type: Optional[str] = Field(
        alias="preferredAppGroupType", default=None
    )
    registration_info: Optional[
        "GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo"
    ] = Field(alias="registrationInfo", default=None)
    ring: Optional[int] = Field(alias="ring", default=None)
    start_vm_on_connect: Optional[bool] = Field(alias="startVMOnConnect", default=None)
    validation_environment: Optional[bool] = Field(
        alias="validationEnvironment", default=None
    )
    vm_template: Optional[str] = Field(alias="vmTemplate", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetRegistrationTokenForHostpoolResponseProperties"],
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
