"""Contains all the data models used in inputs/outputs"""

from .assign_user_to_application_group_response import (
    AssignUserToApplicationGroupResponse,
)
from .assign_user_to_application_group_response_properties import (
    AssignUserToApplicationGroupResponseProperties,
)
from .create_host_pool_response import CreateHostPoolResponse
from .create_host_pool_response_host_pool_type import CreateHostPoolResponseHostPoolType
from .create_host_pool_response_load_balancer_type import (
    CreateHostPoolResponseLoadBalancerType,
)
from .create_host_pool_response_personal_desktop_assignment_type import (
    CreateHostPoolResponsePersonalDesktopAssignmentType,
)
from .create_nsg_request import CreateNSGRequest
from .create_nsg_response import CreateNSGResponse
from .create_nsg_response_properties import CreateNSGResponseProperties
from .create_nsg_response_properties_default_security_rules_array_item_ref import (
    CreateNSGResponsePropertiesDefaultSecurityRulesArrayItemRef,
)
from .create_nsg_response_properties_default_security_rules_properties import (
    CreateNSGResponsePropertiesDefaultSecurityRulesProperties,
)
from .create_resource_group_request import CreateResourceGroupRequest
from .create_resource_group_response import CreateResourceGroupResponse
from .create_resource_group_response_properties import (
    CreateResourceGroupResponseProperties,
)
from .create_security_rule_request import CreateSecurityRuleRequest
from .create_security_rule_response import CreateSecurityRuleResponse
from .create_workspace_response import CreateWorkspaceResponse
from .default_error import DefaultError
from .get_assignment_id_response import GetAssignmentIDResponse
from .get_host_pool_response import GetHostPoolResponse
from .get_host_pool_response_host_pool_type import GetHostPoolResponseHostPoolType
from .get_host_pool_response_load_balancer_type import (
    GetHostPoolResponseLoadBalancerType,
)
from .get_host_pool_response_personal_desktop_assignment_type import (
    GetHostPoolResponsePersonalDesktopAssignmentType,
)
from .get_network_interface_response import GetNetworkInterfaceResponse
from .get_network_interface_response_ip_configurations_array_item_ref import (
    GetNetworkInterfaceResponseIpConfigurationsArrayItemRef,
)
from .get_network_interface_response_tags import GetNetworkInterfaceResponseTags
from .get_nsg_response import GetNSGResponse
from .get_nsg_response_properties import GetNSGResponseProperties
from .get_nsg_response_properties_default_security_rules_array_item_ref import (
    GetNSGResponsePropertiesDefaultSecurityRulesArrayItemRef,
)
from .get_nsg_response_properties_default_security_rules_properties import (
    GetNSGResponsePropertiesDefaultSecurityRulesProperties,
)
from .get_nsg_response_properties_flow_logs_array_item_ref import (
    GetNSGResponsePropertiesFlowLogsArrayItemRef,
)
from .get_nsg_response_properties_network_interfaces_array_item_ref import (
    GetNSGResponsePropertiesNetworkInterfacesArrayItemRef,
)
from .get_nsg_response_properties_security_rules_array_item_ref import (
    GetNSGResponsePropertiesSecurityRulesArrayItemRef,
)
from .get_nsg_response_properties_security_rules_properties import (
    GetNSGResponsePropertiesSecurityRulesProperties,
)
from .get_registration_token_for_hostpool_response import (
    GetRegistrationTokenForHostpoolResponse,
)
from .get_registration_token_for_hostpool_response_properties import (
    GetRegistrationTokenForHostpoolResponseProperties,
)
from .get_registration_token_for_hostpool_response_properties_registration_info import (
    GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo,
)
from .get_registration_token_for_hostpool_response_system_data import (
    GetRegistrationTokenForHostpoolResponseSystemData,
)
from .get_security_alert_response import GetSecurityAlertResponse
from .get_security_rule_list import GetSecurityRuleList
from .get_security_rule_response import GetSecurityRuleResponse
from .get_session_host_response import GetSessionHostResponse
from .get_virtual_machine_list import GetVirtualMachineList
from .get_workspace_response import GetWorkspaceResponse
from .list_host_pool import ListHostPool
from .list_host_pool_host_pool_type import ListHostPoolHostPoolType
from .list_host_pool_load_balancer_type import ListHostPoolLoadBalancerType
from .list_host_pool_personal_desktop_assignment_type import (
    ListHostPoolPersonalDesktopAssignmentType,
)
from .list_network_interface import ListNetworkInterface
from .list_network_interface_ip_configurations_array_item_ref import (
    ListNetworkInterfaceIpConfigurationsArrayItemRef,
)
from .list_network_interface_tags import ListNetworkInterfaceTags
from .list_ns_gs import ListNSGs
from .list_ns_gs_properties import ListNSGsProperties
from .list_ns_gs_properties_default_security_rules_array_item_ref import (
    ListNSGsPropertiesDefaultSecurityRulesArrayItemRef,
)
from .list_ns_gs_properties_default_security_rules_properties import (
    ListNSGsPropertiesDefaultSecurityRulesProperties,
)
from .list_ns_gs_properties_flow_logs_array_item_ref import (
    ListNSGsPropertiesFlowLogsArrayItemRef,
)
from .list_ns_gs_properties_network_interfaces_array_item_ref import (
    ListNSGsPropertiesNetworkInterfacesArrayItemRef,
)
from .list_ns_gs_properties_security_rules_array_item_ref import (
    ListNSGsPropertiesSecurityRulesArrayItemRef,
)
from .list_ns_gs_properties_security_rules_properties import (
    ListNSGsPropertiesSecurityRulesProperties,
)
from .list_ns_gs_value_array_item_ref import ListNSGsValueArrayItemRef
from .list_ns_gs_value_properties import ListNSGsValueProperties
from .list_ns_gs_value_properties_default_security_rules_array_item_ref import (
    ListNSGsValuePropertiesDefaultSecurityRulesArrayItemRef,
)
from .list_ns_gs_value_properties_default_security_rules_properties import (
    ListNSGsValuePropertiesDefaultSecurityRulesProperties,
)
from .list_ns_gs_value_properties_flow_logs_array_item_ref import (
    ListNSGsValuePropertiesFlowLogsArrayItemRef,
)
from .list_ns_gs_value_properties_network_interfaces_array_item_ref import (
    ListNSGsValuePropertiesNetworkInterfacesArrayItemRef,
)
from .list_ns_gs_value_properties_security_rules_array_item_ref import (
    ListNSGsValuePropertiesSecurityRulesArrayItemRef,
)
from .list_ns_gs_value_properties_security_rules_properties import (
    ListNSGsValuePropertiesSecurityRulesProperties,
)
from .list_security_alerts import ListSecurityAlerts
from .list_security_alerts_properties import ListSecurityAlertsProperties
from .list_security_alerts_properties_entities_array_item_ref import (
    ListSecurityAlertsPropertiesEntitiesArrayItemRef,
)
from .list_security_alerts_properties_entities_metadata import (
    ListSecurityAlertsPropertiesEntitiesMetadata,
)
from .list_security_alerts_properties_extended_links_array_item_ref import (
    ListSecurityAlertsPropertiesExtendedLinksArrayItemRef,
)
from .list_security_alerts_properties_extended_properties import (
    ListSecurityAlertsPropertiesExtendedProperties,
)
from .list_security_alerts_properties_resource_identifiers_array_item_ref import (
    ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef,
)
from .list_security_alerts_properties_supporting_evidence import (
    ListSecurityAlertsPropertiesSupportingEvidence,
)
from .list_security_alerts_properties_supporting_evidence_supporting_evidence_list_array_item_ref import (
    ListSecurityAlertsPropertiesSupportingEvidenceSupportingEvidenceListArrayItemRef,
)
from .list_session_host import ListSessionHost
from .list_workspaces import ListWorkspaces
from .update_host_pool_response import UpdateHostPoolResponse
from .update_host_pool_response_host_pool_type import UpdateHostPoolResponseHostPoolType
from .update_host_pool_response_load_balancer_type import (
    UpdateHostPoolResponseLoadBalancerType,
)
from .update_host_pool_response_personal_desktop_assignment_type import (
    UpdateHostPoolResponsePersonalDesktopAssignmentType,
)
from .update_session_host_response import UpdateSessionHostResponse
from .update_workspace_response import UpdateWorkspaceResponse

__all__ = (
    "AssignUserToApplicationGroupResponse",
    "AssignUserToApplicationGroupResponseProperties",
    "CreateHostPoolResponse",
    "CreateHostPoolResponseHostPoolType",
    "CreateHostPoolResponseLoadBalancerType",
    "CreateHostPoolResponsePersonalDesktopAssignmentType",
    "CreateNSGRequest",
    "CreateNSGResponse",
    "CreateNSGResponseProperties",
    "CreateNSGResponsePropertiesDefaultSecurityRulesArrayItemRef",
    "CreateNSGResponsePropertiesDefaultSecurityRulesProperties",
    "CreateResourceGroupRequest",
    "CreateResourceGroupResponse",
    "CreateResourceGroupResponseProperties",
    "CreateSecurityRuleRequest",
    "CreateSecurityRuleResponse",
    "CreateWorkspaceResponse",
    "DefaultError",
    "GetAssignmentIDResponse",
    "GetHostPoolResponse",
    "GetHostPoolResponseHostPoolType",
    "GetHostPoolResponseLoadBalancerType",
    "GetHostPoolResponsePersonalDesktopAssignmentType",
    "GetNetworkInterfaceResponse",
    "GetNetworkInterfaceResponseIpConfigurationsArrayItemRef",
    "GetNetworkInterfaceResponseTags",
    "GetNSGResponse",
    "GetNSGResponseProperties",
    "GetNSGResponsePropertiesDefaultSecurityRulesArrayItemRef",
    "GetNSGResponsePropertiesDefaultSecurityRulesProperties",
    "GetNSGResponsePropertiesFlowLogsArrayItemRef",
    "GetNSGResponsePropertiesNetworkInterfacesArrayItemRef",
    "GetNSGResponsePropertiesSecurityRulesArrayItemRef",
    "GetNSGResponsePropertiesSecurityRulesProperties",
    "GetRegistrationTokenForHostpoolResponse",
    "GetRegistrationTokenForHostpoolResponseProperties",
    "GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo",
    "GetRegistrationTokenForHostpoolResponseSystemData",
    "GetSecurityAlertResponse",
    "GetSecurityRuleList",
    "GetSecurityRuleResponse",
    "GetSessionHostResponse",
    "GetVirtualMachineList",
    "GetWorkspaceResponse",
    "ListHostPool",
    "ListHostPoolHostPoolType",
    "ListHostPoolLoadBalancerType",
    "ListHostPoolPersonalDesktopAssignmentType",
    "ListNetworkInterface",
    "ListNetworkInterfaceIpConfigurationsArrayItemRef",
    "ListNetworkInterfaceTags",
    "ListNSGs",
    "ListNSGsProperties",
    "ListNSGsPropertiesDefaultSecurityRulesArrayItemRef",
    "ListNSGsPropertiesDefaultSecurityRulesProperties",
    "ListNSGsPropertiesFlowLogsArrayItemRef",
    "ListNSGsPropertiesNetworkInterfacesArrayItemRef",
    "ListNSGsPropertiesSecurityRulesArrayItemRef",
    "ListNSGsPropertiesSecurityRulesProperties",
    "ListNSGsValueArrayItemRef",
    "ListNSGsValueProperties",
    "ListNSGsValuePropertiesDefaultSecurityRulesArrayItemRef",
    "ListNSGsValuePropertiesDefaultSecurityRulesProperties",
    "ListNSGsValuePropertiesFlowLogsArrayItemRef",
    "ListNSGsValuePropertiesNetworkInterfacesArrayItemRef",
    "ListNSGsValuePropertiesSecurityRulesArrayItemRef",
    "ListNSGsValuePropertiesSecurityRulesProperties",
    "ListSecurityAlerts",
    "ListSecurityAlertsProperties",
    "ListSecurityAlertsPropertiesEntitiesArrayItemRef",
    "ListSecurityAlertsPropertiesEntitiesMetadata",
    "ListSecurityAlertsPropertiesExtendedLinksArrayItemRef",
    "ListSecurityAlertsPropertiesExtendedProperties",
    "ListSecurityAlertsPropertiesResourceIdentifiersArrayItemRef",
    "ListSecurityAlertsPropertiesSupportingEvidence",
    "ListSecurityAlertsPropertiesSupportingEvidenceSupportingEvidenceListArrayItemRef",
    "ListSessionHost",
    "ListWorkspaces",
    "UpdateHostPoolResponse",
    "UpdateHostPoolResponseHostPoolType",
    "UpdateHostPoolResponseLoadBalancerType",
    "UpdateHostPoolResponsePersonalDesktopAssignmentType",
    "UpdateSessionHostResponse",
    "UpdateWorkspaceResponse",
)
