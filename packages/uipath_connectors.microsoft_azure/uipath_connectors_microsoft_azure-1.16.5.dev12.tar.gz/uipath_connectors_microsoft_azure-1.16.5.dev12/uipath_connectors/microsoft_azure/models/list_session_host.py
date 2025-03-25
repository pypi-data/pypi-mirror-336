from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class ListSessionHost(BaseModel):
    """
    Attributes:
        agent_version (Optional[str]): The version number of the agent software installed on the session host. Example:
                1.0.0.1391.
        allow_new_session (Optional[bool]): Indicates whether the session host can accept new user sessions. Example:
                True.
        assigned_user (Optional[str]): The username of the individual assigned to the session host. Example:
                user1@microsoft.com.
        host_pool_id (Optional[str]): A unique identifier for the host pool to which the session host belongs. Example:
                /subscriptions/daefabc0-95b4-48b3-b645-
                8a753a63c4fa/resourceGroups/resourceGroup1/providers/Microsoft.DesktopVirtualization/hostPools/hostPool1.
        host_pool_name (Optional[str]): Name of the host pool to which the session host belongs.
        id (Optional[str]): A unique identifier for the session host within the system. Example: /subscriptions/daefabc0
                -95b4-48b3-b645-
                8a753a63c4fa/resourceGroups/resourceGroup1/providers/Microsoft.DesktopVirtualization/hostPools/hostPool1/session
                Hosts/sessionHost1.microsoft.com.
        last_heart_beat (Optional[datetime.datetime]): The timestamp of the last heartbeat signal received from the
                session host. Example: 2008-09-22T14:01:54.9571247Z.
        last_update_time (Optional[datetime.datetime]): The date and time when the session host was last updated.
                Example: 2008-09-22T14:01:54.9571247Z.
        name (Optional[str]): The name displayed for the session host in the user interface. Example:
                sessionHost1.microsoft.com.
        number_of_sessions (Optional[int]): The total number of active sessions on the session host. Example: 1.0.
        os_version (Optional[str]): The version of the operating system running on the session host. Example:
                10.0.17763.
        resource_group_name (Optional[str]): Name of the Azure resource group containing the resources.
        status (Optional[str]): The current operational status of the session host. Example: Available.
        status_timestamp (Optional[datetime.datetime]): The timestamp indicating the last time the session host's status
                was updated. Example: 2008-09-22T14:01:54.9571247Z.
        sx_s_stack_version (Optional[str]): The version number of the side-by-side stack on the session host. Example:
                rdp-sxs190816002.
        update_error_message (Optional[str]): Error message detailing any issues encountered during the update.
        update_state (Optional[str]): Current state of the update process for the session host. Example: Succeeded.
        virtual_machine_id (Optional[str]): Unique ID for the virtual machine within Azure. Example:
                29491b54-c033-4dec-b09a-18bf0ebafaef.
        virtual_machine_resource_id (Optional[str]): A unique ID for the virtual machine within Azure resources.
                Example: /subscriptions/daefabc0-95b4-48b3-b645-
                8a753a63c4fa/resourceGroups/resourceGroup1/providers/Microsoft.Compute/virtualMachines/sessionHost1.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    agent_version: Optional[str] = Field(alias="agentVersion", default=None)
    allow_new_session: Optional[bool] = Field(alias="allowNewSession", default=None)
    assigned_user: Optional[str] = Field(alias="assignedUser", default=None)
    host_pool_id: Optional[str] = Field(alias="hostPoolId", default=None)
    host_pool_name: Optional[str] = Field(alias="hostPoolName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    last_heart_beat: Optional[datetime.datetime] = Field(
        alias="lastHeartBeat", default=None
    )
    last_update_time: Optional[datetime.datetime] = Field(
        alias="lastUpdateTime", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    number_of_sessions: Optional[int] = Field(alias="numberOfSessions", default=None)
    os_version: Optional[str] = Field(alias="osVersion", default=None)
    resource_group_name: Optional[str] = Field(alias="resourceGroupName", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_timestamp: Optional[datetime.datetime] = Field(
        alias="statusTimestamp", default=None
    )
    sx_s_stack_version: Optional[str] = Field(alias="sxSStackVersion", default=None)
    update_error_message: Optional[str] = Field(
        alias="updateErrorMessage", default=None
    )
    update_state: Optional[str] = Field(alias="updateState", default=None)
    virtual_machine_id: Optional[str] = Field(alias="virtualMachineID", default=None)
    virtual_machine_resource_id: Optional[str] = Field(
        alias="virtualMachineResourceID", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListSessionHost"], src_dict: Dict[str, Any]):
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
