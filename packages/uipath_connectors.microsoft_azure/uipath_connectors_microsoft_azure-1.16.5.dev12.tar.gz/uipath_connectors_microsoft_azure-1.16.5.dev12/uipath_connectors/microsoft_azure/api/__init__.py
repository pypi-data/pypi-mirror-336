from .application_groupresourcegroups import (
    assign_user_to_application_group as _assign_user_to_application_group,
    assign_user_to_application_group_async as _assign_user_to_application_group_async,
)
from ..models.assign_user_to_application_group_response import (
    AssignUserToApplicationGroupResponse,
)
from ..models.default_error import DefaultError
from typing import cast
from .hostpoolresource_groups import (
    create_host_pool as _create_host_pool,
    create_host_pool_async as _create_host_pool_async,
    delete_host_pool as _delete_host_pool,
    delete_host_pool_async as _delete_host_pool_async,
    get_host_pool as _get_host_pool,
    get_host_pool_async as _get_host_pool_async,
    list_host_pool as _list_host_pool,
    list_host_pool_async as _list_host_pool_async,
    update_host_pool as _update_host_pool,
    update_host_pool_async as _update_host_pool_async,
)
from ..models.create_host_pool_response import CreateHostPoolResponse
from ..models.get_host_pool_response import GetHostPoolResponse
from ..models.list_host_pool import ListHostPool
from ..models.update_host_pool_response import UpdateHostPoolResponse
from .network_security_groupresource_group import (
    create_nsg as _create_nsg,
    create_nsg_async as _create_nsg_async,
    get_nsg as _get_nsg,
    get_nsg_async as _get_nsg_async,
)
from ..models.create_nsg_request import CreateNSGRequest
from ..models.create_nsg_response import CreateNSGResponse
from ..models.get_nsg_response import GetNSGResponse
from .resource_groupresource import (
    create_resource_group as _create_resource_group,
    create_resource_group_async as _create_resource_group_async,
    delete_resource_group as _delete_resource_group,
    delete_resource_group_async as _delete_resource_group_async,
)
from ..models.create_resource_group_request import CreateResourceGroupRequest
from ..models.create_resource_group_response import CreateResourceGroupResponse
from .network_security_groupsresource_groupssecurity_rules import (
    create_security_rule as _create_security_rule,
    create_security_rule_async as _create_security_rule_async,
    delete_security_rule as _delete_security_rule,
    delete_security_rule_async as _delete_security_rule_async,
    get_security_rule as _get_security_rule,
    get_security_rule_async as _get_security_rule_async,
    get_security_rule_list as _get_security_rule_list,
    get_security_rule_list_async as _get_security_rule_list_async,
)
from ..models.create_security_rule_request import CreateSecurityRuleRequest
from ..models.create_security_rule_response import CreateSecurityRuleResponse
from ..models.get_security_rule_response import GetSecurityRuleResponse
from ..models.get_security_rule_list import GetSecurityRuleList
from .workspaceresource_group import (
    create_workspace as _create_workspace,
    create_workspace_async as _create_workspace_async,
    delete_workspace as _delete_workspace,
    delete_workspace_async as _delete_workspace_async,
    get_workspace as _get_workspace,
    get_workspace_async as _get_workspace_async,
    list_workspaces as _list_workspaces,
    list_workspaces_async as _list_workspaces_async,
    update_workspace as _update_workspace,
    update_workspace_async as _update_workspace_async,
)
from ..models.create_workspace_response import CreateWorkspaceResponse
from ..models.get_workspace_response import GetWorkspaceResponse
from ..models.list_workspaces import ListWorkspaces
from ..models.update_workspace_response import UpdateWorkspaceResponse
from .assignment_idresource_groupsapplication_groups import (
    delete_assignment_id as _delete_assignment_id,
    delete_assignment_id_async as _delete_assignment_id_async,
    get_assignment_id as _get_assignment_id,
    get_assignment_id_async as _get_assignment_id_async,
)
from ..models.get_assignment_id_response import GetAssignmentIDResponse
from .network_security_group import (
    delete_nsg as _delete_nsg,
    delete_nsg_async as _delete_nsg_async,
    list_ns_gs as _list_ns_gs,
    list_ns_gs_async as _list_ns_gs_async,
)
from ..models.list_ns_gs import ListNSGs
from .resource_groupsnetwork_interfaces import (
    delete_network_interface as _delete_network_interface,
    delete_network_interface_async as _delete_network_interface_async,
    get_network_interface as _get_network_interface,
    get_network_interface_async as _get_network_interface_async,
)
from ..models.get_network_interface_response import GetNetworkInterfaceResponse
from .session_hostresource_grouphost_pool import (
    delete_session_host as _delete_session_host,
    delete_session_host_async as _delete_session_host_async,
    get_session_host as _get_session_host,
    get_session_host_async as _get_session_host_async,
    list_session_host as _list_session_host,
    list_session_host_async as _list_session_host_async,
    update_session_host as _update_session_host,
    update_session_host_async as _update_session_host_async,
)
from ..models.get_session_host_response import GetSessionHostResponse
from ..models.list_session_host import ListSessionHost
from ..models.update_session_host_response import UpdateSessionHostResponse
from .host_poolsresource_groups import (
    get_registration_token_for_hostpool as _get_registration_token_for_hostpool,
    get_registration_token_for_hostpool_async as _get_registration_token_for_hostpool_async,
)
from ..models.get_registration_token_for_hostpool_response import (
    GetRegistrationTokenForHostpoolResponse,
)
from .locationsalerts import (
    get_security_alert as _get_security_alert,
    get_security_alert_async as _get_security_alert_async,
)
from ..models.get_security_alert_response import GetSecurityAlertResponse
from .virtual_machineresource_groups import (
    get_virtual_machine as _get_virtual_machine,
    get_virtual_machine_async as _get_virtual_machine_async,
)
from .virtual_machinesresource_groups import (
    get_virtual_machine_list as _get_virtual_machine_list,
    get_virtual_machine_list_async as _get_virtual_machine_list_async,
)
from ..models.get_virtual_machine_list import GetVirtualMachineList
from .network_interfaces import (
    list_network_interface as _list_network_interface,
    list_network_interface_async as _list_network_interface_async,
)
from ..models.list_network_interface import ListNetworkInterface
from .alerts import (
    list_security_alerts as _list_security_alerts,
    list_security_alerts_async as _list_security_alerts_async,
)
from ..models.list_security_alerts import ListSecurityAlerts
from .locationsalertsnew_state import (
    set_security_alert_state as _set_security_alert_state,
    set_security_alert_state_async as _set_security_alert_state_async,
)

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class MicrosoftAzure:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def assign_user_to_application_group(
        self,
        application_group_name: str,
        resource_group_name: str,
        *,
        object_id: str,
    ) -> Optional[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
        return _assign_user_to_application_group(
            client=self.client,
            application_group_name=application_group_name,
            resource_group_name=resource_group_name,
            object_id=object_id,
        )

    async def assign_user_to_application_group_async(
        self,
        application_group_name: str,
        resource_group_name: str,
        *,
        object_id: str,
    ) -> Optional[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
        return await _assign_user_to_application_group_async(
            client=self.client,
            application_group_name=application_group_name,
            resource_group_name=resource_group_name,
            object_id=object_id,
        )

    def create_host_pool(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[CreateHostPoolResponse, DefaultError]]:
        return _create_host_pool(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    async def create_host_pool_async(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[CreateHostPoolResponse, DefaultError]]:
        return await _create_host_pool_async(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    def delete_host_pool(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_host_pool(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    async def delete_host_pool_async(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_host_pool_async(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    def get_host_pool(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetHostPoolResponse]]:
        return _get_host_pool(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    async def get_host_pool_async(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetHostPoolResponse]]:
        return await _get_host_pool_async(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    def list_host_pool(
        self,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, list["ListHostPool"]]]:
        return _list_host_pool(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    async def list_host_pool_async(
        self,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, list["ListHostPool"]]]:
        return await _list_host_pool_async(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    def update_host_pool(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, UpdateHostPoolResponse]]:
        return _update_host_pool(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    async def update_host_pool_async(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, UpdateHostPoolResponse]]:
        return await _update_host_pool_async(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    def create_nsg(
        self,
        id: str,
        resource_group_name: str,
        *,
        body: CreateNSGRequest,
    ) -> Optional[Union[CreateNSGResponse, DefaultError]]:
        return _create_nsg(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
            body=body,
        )

    async def create_nsg_async(
        self,
        id: str,
        resource_group_name: str,
        *,
        body: CreateNSGRequest,
    ) -> Optional[Union[CreateNSGResponse, DefaultError]]:
        return await _create_nsg_async(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
            body=body,
        )

    def get_nsg(
        self,
        id: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetNSGResponse]]:
        return _get_nsg(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
        )

    async def get_nsg_async(
        self,
        id: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetNSGResponse]]:
        return await _get_nsg_async(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
        )

    def create_resource_group(
        self,
        resource_group_name: str,
        *,
        body: CreateResourceGroupRequest,
    ) -> Optional[Union[CreateResourceGroupResponse, DefaultError]]:
        return _create_resource_group(
            client=self.client,
            resource_group_name=resource_group_name,
            body=body,
        )

    async def create_resource_group_async(
        self,
        resource_group_name: str,
        *,
        body: CreateResourceGroupRequest,
    ) -> Optional[Union[CreateResourceGroupResponse, DefaultError]]:
        return await _create_resource_group_async(
            client=self.client,
            resource_group_name=resource_group_name,
            body=body,
        )

    def delete_resource_group(
        self,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_resource_group(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    async def delete_resource_group_async(
        self,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_resource_group_async(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    def create_security_rule(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
        *,
        body: CreateSecurityRuleRequest,
    ) -> Optional[Union[CreateSecurityRuleResponse, DefaultError]]:
        return _create_security_rule(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
            body=body,
        )

    async def create_security_rule_async(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
        *,
        body: CreateSecurityRuleRequest,
    ) -> Optional[Union[CreateSecurityRuleResponse, DefaultError]]:
        return await _create_security_rule_async(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
            body=body,
        )

    def delete_security_rule(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_security_rule(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
        )

    async def delete_security_rule_async(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_security_rule_async(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
        )

    def get_security_rule(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
    ) -> Optional[Union[DefaultError, GetSecurityRuleResponse]]:
        return _get_security_rule(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
        )

    async def get_security_rule_async(
        self,
        network_security_group: str,
        resource_group_name: str,
        network_security_rule: str,
    ) -> Optional[Union[DefaultError, GetSecurityRuleResponse]]:
        return await _get_security_rule_async(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
        )

    def get_security_rule_list(
        self,
        network_security_group: str,
        resource_group_name: str,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetSecurityRuleList"]]]:
        return _get_security_rule_list(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            page_size=page_size,
            next_page=next_page,
        )

    async def get_security_rule_list_async(
        self,
        network_security_group: str,
        resource_group_name: str,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetSecurityRuleList"]]]:
        return await _get_security_rule_list_async(
            client=self.client,
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            page_size=page_size,
            next_page=next_page,
        )

    def create_workspace(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[CreateWorkspaceResponse, DefaultError]]:
        return _create_workspace(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    async def create_workspace_async(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[CreateWorkspaceResponse, DefaultError]]:
        return await _create_workspace_async(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    def delete_workspace(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_workspace(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    async def delete_workspace_async(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_workspace_async(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    def get_workspace(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetWorkspaceResponse]]:
        return _get_workspace(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    async def get_workspace_async(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetWorkspaceResponse]]:
        return await _get_workspace_async(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    def list_workspaces(
        self,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, list["ListWorkspaces"]]]:
        return _list_workspaces(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    async def list_workspaces_async(
        self,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, list["ListWorkspaces"]]]:
        return await _list_workspaces_async(
            client=self.client,
            resource_group_name=resource_group_name,
        )

    def update_workspace(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, UpdateWorkspaceResponse]]:
        return _update_workspace(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    async def update_workspace_async(
        self,
        workspace_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, UpdateWorkspaceResponse]]:
        return await _update_workspace_async(
            client=self.client,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name,
        )

    def delete_assignment_id(
        self,
        resource_group_name: str,
        application_group_name: str,
        assignment_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_assignment_id(
            client=self.client,
            resource_group_name=resource_group_name,
            application_group_name=application_group_name,
            assignment_id=assignment_id,
        )

    async def delete_assignment_id_async(
        self,
        resource_group_name: str,
        application_group_name: str,
        assignment_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_assignment_id_async(
            client=self.client,
            resource_group_name=resource_group_name,
            application_group_name=application_group_name,
            assignment_id=assignment_id,
        )

    def get_assignment_id(
        self,
        resource_group_name: str,
        application_group_name: str,
        principal_id: str,
    ) -> Optional[Union[DefaultError, GetAssignmentIDResponse]]:
        return _get_assignment_id(
            client=self.client,
            resource_group_name=resource_group_name,
            application_group_name=application_group_name,
            principal_id=principal_id,
        )

    async def get_assignment_id_async(
        self,
        resource_group_name: str,
        application_group_name: str,
        principal_id: str,
    ) -> Optional[Union[DefaultError, GetAssignmentIDResponse]]:
        return await _get_assignment_id_async(
            client=self.client,
            resource_group_name=resource_group_name,
            application_group_name=application_group_name,
            principal_id=principal_id,
        )

    def delete_nsg(
        self,
        *,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_nsg(
            client=self.client,
            id=id,
        )

    async def delete_nsg_async(
        self,
        *,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_nsg_async(
            client=self.client,
            id=id,
        )

    def list_ns_gs(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListNSGs"]]]:
        return _list_ns_gs(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            resource_group_name=resource_group_name,
        )

    async def list_ns_gs_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListNSGs"]]]:
        return await _list_ns_gs_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            resource_group_name=resource_group_name,
        )

    def delete_network_interface(
        self,
        resource_group_name: str,
        network_interface_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_network_interface(
            client=self.client,
            resource_group_name=resource_group_name,
            network_interface_name=network_interface_name,
        )

    async def delete_network_interface_async(
        self,
        resource_group_name: str,
        network_interface_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_network_interface_async(
            client=self.client,
            resource_group_name=resource_group_name,
            network_interface_name=network_interface_name,
        )

    def get_network_interface(
        self,
        resource_group_name: str,
        network_interface_name: str,
    ) -> Optional[Union[DefaultError, GetNetworkInterfaceResponse]]:
        return _get_network_interface(
            client=self.client,
            resource_group_name=resource_group_name,
            network_interface_name=network_interface_name,
        )

    async def get_network_interface_async(
        self,
        resource_group_name: str,
        network_interface_name: str,
    ) -> Optional[Union[DefaultError, GetNetworkInterfaceResponse]]:
        return await _get_network_interface_async(
            client=self.client,
            resource_group_name=resource_group_name,
            network_interface_name=network_interface_name,
        )

    def delete_session_host(
        self,
        session_host_name: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_session_host(
            client=self.client,
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    async def delete_session_host_async(
        self,
        session_host_name: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_session_host_async(
            client=self.client,
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    def get_session_host(
        self,
        id: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, GetSessionHostResponse]]:
        return _get_session_host(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    async def get_session_host_async(
        self,
        id: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, GetSessionHostResponse]]:
        return await _get_session_host_async(
            client=self.client,
            id=id,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    def list_session_host(
        self,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, list["ListSessionHost"]]]:
        return _list_session_host(
            client=self.client,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    async def list_session_host_async(
        self,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, list["ListSessionHost"]]]:
        return await _list_session_host_async(
            client=self.client,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    def update_session_host(
        self,
        session_host_name: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, UpdateSessionHostResponse]]:
        return _update_session_host(
            client=self.client,
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    async def update_session_host_async(
        self,
        session_host_name: str,
        resource_group_name: str,
        host_pool_name: str,
    ) -> Optional[Union[DefaultError, UpdateSessionHostResponse]]:
        return await _update_session_host_async(
            client=self.client,
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        )

    def get_registration_token_for_hostpool(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetRegistrationTokenForHostpoolResponse]]:
        return _get_registration_token_for_hostpool(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    async def get_registration_token_for_hostpool_async(
        self,
        host_pool_name: str,
        resource_group_name: str,
    ) -> Optional[Union[DefaultError, GetRegistrationTokenForHostpoolResponse]]:
        return await _get_registration_token_for_hostpool_async(
            client=self.client,
            host_pool_name=host_pool_name,
            resource_group_name=resource_group_name,
        )

    def get_security_alert(
        self,
        asc_location: str,
        alert_name: str,
        *,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetSecurityAlertResponse]]:
        return _get_security_alert(
            client=self.client,
            asc_location=asc_location,
            alert_name=alert_name,
            resource_group_name=resource_group_name,
        )

    async def get_security_alert_async(
        self,
        asc_location: str,
        alert_name: str,
        *,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetSecurityAlertResponse]]:
        return await _get_security_alert_async(
            client=self.client,
            asc_location=asc_location,
            alert_name=alert_name,
            resource_group_name=resource_group_name,
        )

    def get_virtual_machine(
        self,
        vm_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _get_virtual_machine(
            client=self.client,
            vm_name=vm_name,
            resource_group_name=resource_group_name,
        )

    async def get_virtual_machine_async(
        self,
        vm_name: str,
        resource_group_name: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _get_virtual_machine_async(
            client=self.client,
            vm_name=vm_name,
            resource_group_name=resource_group_name,
        )

    def get_virtual_machine_list(
        self,
        resource_group_name: str,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetVirtualMachineList"]]]:
        return _get_virtual_machine_list(
            client=self.client,
            resource_group_name=resource_group_name,
            page_size=page_size,
            next_page=next_page,
        )

    async def get_virtual_machine_list_async(
        self,
        resource_group_name: str,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetVirtualMachineList"]]]:
        return await _get_virtual_machine_list_async(
            client=self.client,
            resource_group_name=resource_group_name,
            page_size=page_size,
            next_page=next_page,
        )

    def list_network_interface(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        resource_group_name: Optional[str] = None,
        asc_location: Optional[str] = None,
        name_starts_with: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListNetworkInterface"]]]:
        return _list_network_interface(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            name_starts_with=name_starts_with,
        )

    async def list_network_interface_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        resource_group_name: Optional[str] = None,
        asc_location: Optional[str] = None,
        name_starts_with: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListNetworkInterface"]]]:
        return await _list_network_interface_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            name_starts_with=name_starts_with,
        )

    def list_security_alerts(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        asc_location: Optional[str] = None,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListSecurityAlerts"]]]:
        return _list_security_alerts(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            asc_location=asc_location,
            resource_group_name=resource_group_name,
        )

    async def list_security_alerts_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        asc_location: Optional[str] = None,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListSecurityAlerts"]]]:
        return await _list_security_alerts_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            asc_location=asc_location,
            resource_group_name=resource_group_name,
        )

    def set_security_alert_state(
        self,
        asc_location: str,
        alert_name: str,
        new_state: str,
        *,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return _set_security_alert_state(
            client=self.client,
            asc_location=asc_location,
            alert_name=alert_name,
            new_state=new_state,
            resource_group_name=resource_group_name,
        )

    async def set_security_alert_state_async(
        self,
        asc_location: str,
        alert_name: str,
        new_state: str,
        *,
        resource_group_name: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _set_security_alert_state_async(
            client=self.client,
            asc_location=asc_location,
            alert_name=alert_name,
            new_state=new_state,
            resource_group_name=resource_group_name,
        )
