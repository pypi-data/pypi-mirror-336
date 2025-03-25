from .group_operation_for_lifecycle_policy import (
    add_group_to_lifecycle_policy as _add_group_to_lifecycle_policy,
    add_group_to_lifecycle_policy_async as _add_group_to_lifecycle_policy_async,
)
from ..models.add_group_to_lifecycle_policy_request import (
    AddGroupToLifecyclePolicyRequest,
)
from ..models.default_error import DefaultError
from typing import cast
from .group_add_member_to_group import (
    add_member_to_group as _add_member_to_group,
    add_member_to_group_async as _add_member_to_group_async,
)
from ..models.add_member_to_group_request import AddMemberToGroupRequest
from .directory_roles_add_member_to_role import (
    add_member_to_role as _add_member_to_role,
    add_member_to_role_async as _add_member_to_role_async,
)
from ..models.add_member_to_role_request import AddMemberToRoleRequest
from .groups_add_owner import (
    add_owner_to_group as _add_owner_to_group,
    add_owner_to_group_async as _add_owner_to_group_async,
)
from ..models.add_owner_to_group_request import AddOwnerToGroupRequest
from .users_assign_license import (
    assign_license as _assign_license,
    assign_license_async as _assign_license_async,
)
from ..models.assign_license_request import AssignLicenseRequest
from ..models.assign_license_response import AssignLicenseResponse
from .groups import (
    create_assigned_group as _create_assigned_group,
    create_assigned_group_async as _create_assigned_group_async,
    delete_group as _delete_group,
    delete_group_async as _delete_group_async,
    get_group_by_id as _get_group_by_id,
    get_group_by_id_async as _get_group_by_id_async,
    list_groups as _list_groups,
    list_groups_async as _list_groups_async,
    update_group as _update_group,
    update_group_async as _update_group_async,
)
from ..models.create_assigned_group_request import CreateAssignedGroupRequest
from ..models.create_assigned_group_response import CreateAssignedGroupResponse
from ..models.get_group_by_id_response import GetGroupByIdResponse
from ..models.list_groups import ListGroups
from ..models.update_group_request import UpdateGroupRequest
from .group_lifecycle_policies import (
    create_lifecycle_policy as _create_lifecycle_policy,
    create_lifecycle_policy_async as _create_lifecycle_policy_async,
    delete_lifecycle_policy as _delete_lifecycle_policy,
    delete_lifecycle_policy_async as _delete_lifecycle_policy_async,
    lists_lifecycle_policy as _lists_lifecycle_policy,
    lists_lifecycle_policy_async as _lists_lifecycle_policy_async,
    update_lifecycle_policy as _update_lifecycle_policy,
    update_lifecycle_policy_async as _update_lifecycle_policy_async,
)
from ..models.create_lifecycle_policy_request import CreateLifecyclePolicyRequest
from ..models.lists_lifecycle_policy import ListsLifecyclePolicy
from ..models.update_lifecycle_policy_request import UpdateLifecyclePolicyRequest
from ..models.update_lifecycle_policy_response import UpdateLifecyclePolicyResponse
from .user import (
    create_user as _create_user,
    create_user_async as _create_user_async,
    delete_user as _delete_user,
    delete_user_async as _delete_user_async,
    get_user as _get_user,
    get_user_async as _get_user_async,
    list_users as _list_users,
    list_users_async as _list_users_async,
    update_user as _update_user,
    update_user_async as _update_user_async,
)
from ..models.create_user_request import CreateUserRequest
from ..models.create_user_response import CreateUserResponse
from ..models.get_user_response import GetUserResponse
from ..models.list_users import ListUsers
from ..models.update_user_request import UpdateUserRequest
from .groups_get_group_by_name import (
    get_group_by_name as _get_group_by_name,
    get_group_by_name_async as _get_group_by_name_async,
)
from ..models.get_group_by_name_response import GetGroupByNameResponse
from .group_members_delta import (
    get_group_members_delta as _get_group_members_delta,
    get_group_members_delta_async as _get_group_members_delta_async,
)
from ..models.get_group_members_delta import GetGroupMembersDelta
from .user_get_manager import (
    get_manager as _get_manager,
    get_manager_async as _get_manager_async,
)
from ..models.get_manager_response import GetManagerResponse
from .user_roles import (
    get_user_roles as _get_user_roles,
    get_user_roles_async as _get_user_roles_async,
)
from ..models.get_user_roles import GetUserRoles
from .groups_exists import (
    group_exists as _group_exists,
    group_exists_async as _group_exists_async,
)
from ..models.group_exists_response import GroupExistsResponse
from .is_group_in_lifecycle_policy import (
    is_group_in_lifecycle_policy as _is_group_in_lifecycle_policy,
    is_group_in_lifecycle_policy_async as _is_group_in_lifecycle_policy_async,
)
from ..models.is_group_in_lifecycle_policy import IsGroupInLifecyclePolicy
from .directory_roles_is_member_in_role import (
    is_member_in_role as _is_member_in_role,
    is_member_in_role_async as _is_member_in_role_async,
)
from ..models.is_member_in_role_response import IsMemberInRoleResponse
from .groups_is_member_of_group import (
    is_member_of_group as _is_member_of_group,
    is_member_of_group_async as _is_member_of_group_async,
)
from ..models.is_member_of_group_response import IsMemberOfGroupResponse
from .is_owner_of_groupid import (
    is_owner_of_group as _is_owner_of_group,
    is_owner_of_group_async as _is_owner_of_group_async,
)
from ..models.is_owner_of_group import IsOwnerOfGroup
from .groups_groups_in_group import (
    list_all_groups_in_group as _list_all_groups_in_group,
    list_all_groups_in_group_async as _list_all_groups_in_group_async,
)
from ..models.list_all_groups_in_group import ListAllGroupsInGroup
from .usermember_of import (
    list_all_groups_of_a_user as _list_all_groups_of_a_user,
    list_all_groups_of_a_user_async as _list_all_groups_of_a_user_async,
)
from ..models.list_all_groups_of_a_user import ListAllGroupsOfAUser
from .user_list_direct_reports import (
    list_direct_reports as _list_direct_reports,
    list_direct_reports_async as _list_direct_reports_async,
)
from ..models.list_direct_reports import ListDirectReports
from .directory_roles import (
    list_directory_roles as _list_directory_roles,
    list_directory_roles_async as _list_directory_roles_async,
)
from ..models.list_directory_roles import ListDirectoryRoles
from .groups_list_owners import (
    list_owners_of_a_group as _list_owners_of_a_group,
    list_owners_of_a_group_async as _list_owners_of_a_group_async,
)
from ..models.list_owners_of_a_group import ListOwnersOfAGroup
from .groups_users_in_group import (
    list_users_in_group as _list_users_in_group,
    list_users_in_group_async as _list_users_in_group_async,
)
from ..models.list_users_in_group import ListUsersInGroup
from .directory_roles_list_users import (
    list_users_in_role as _list_users_in_role,
    list_users_in_role_async as _list_users_in_role_async,
)
from ..models.list_users_in_role import ListUsersInRole
from .grouplifecycle_policyremove_group import (
    remove_group_from_lifecycle_policy as _remove_group_from_lifecycle_policy,
    remove_group_from_lifecycle_policy_async as _remove_group_from_lifecycle_policy_async,
)
from .users_remove_license import (
    remove_license as _remove_license,
    remove_license_async as _remove_license_async,
)
from ..models.remove_license_request import RemoveLicenseRequest
from ..models.remove_license_response import RemoveLicenseResponse
from .groups_members import (
    remove_member_from_group as _remove_member_from_group,
    remove_member_from_group_async as _remove_member_from_group_async,
)
from .directory_roles_remove_member_from_role import (
    remove_member_from_role as _remove_member_from_role,
    remove_member_from_role_async as _remove_member_from_role_async,
)
from .groups_remove_owner_from_group import (
    remove_owner_from_group as _remove_owner_from_group,
    remove_owner_from_group_async as _remove_owner_from_group_async,
)
from .users_reset_password import (
    reset_password as _reset_password,
    reset_password_async as _reset_password_async,
)
from ..models.reset_password_request import ResetPasswordRequest
from .user_set_manager import (
    set_manager as _set_manager,
    set_manager_async as _set_manager_async,
)
from ..models.set_manager_request import SetManagerRequest
from .user_exists import (
    user_exists as _user_exists,
    user_exists_async as _user_exists_async,
)
from ..models.user_exists_response import UserExistsResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class MicrosoftAzureactivedirectory:
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

    def add_group_to_lifecycle_policy(
        self,
        id: str,
        *,
        body: AddGroupToLifecyclePolicyRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _add_group_to_lifecycle_policy(
            client=self.client,
            id=id,
            body=body,
        )

    async def add_group_to_lifecycle_policy_async(
        self,
        id: str,
        *,
        body: AddGroupToLifecyclePolicyRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _add_group_to_lifecycle_policy_async(
            client=self.client,
            id=id,
            body=body,
        )

    def add_member_to_group(
        self,
        id: str,
        *,
        body: AddMemberToGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _add_member_to_group(
            client=self.client,
            id=id,
            body=body,
        )

    async def add_member_to_group_async(
        self,
        id: str,
        *,
        body: AddMemberToGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _add_member_to_group_async(
            client=self.client,
            id=id,
            body=body,
        )

    def add_member_to_role(
        self,
        id: str,
        *,
        body: AddMemberToRoleRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _add_member_to_role(
            client=self.client,
            id=id,
            body=body,
        )

    async def add_member_to_role_async(
        self,
        id: str,
        *,
        body: AddMemberToRoleRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _add_member_to_role_async(
            client=self.client,
            id=id,
            body=body,
        )

    def add_owner_to_group(
        self,
        id: str,
        *,
        body: AddOwnerToGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _add_owner_to_group(
            client=self.client,
            id=id,
            body=body,
        )

    async def add_owner_to_group_async(
        self,
        id: str,
        *,
        body: AddOwnerToGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _add_owner_to_group_async(
            client=self.client,
            id=id,
            body=body,
        )

    def assign_license(
        self,
        id: str,
        *,
        body: AssignLicenseRequest,
    ) -> Optional[Union[AssignLicenseResponse, DefaultError]]:
        return _assign_license(
            client=self.client,
            id=id,
            body=body,
        )

    async def assign_license_async(
        self,
        id: str,
        *,
        body: AssignLicenseRequest,
    ) -> Optional[Union[AssignLicenseResponse, DefaultError]]:
        return await _assign_license_async(
            client=self.client,
            id=id,
            body=body,
        )

    def create_assigned_group(
        self,
        *,
        body: CreateAssignedGroupRequest,
    ) -> Optional[Union[CreateAssignedGroupResponse, DefaultError]]:
        return _create_assigned_group(
            client=self.client,
            body=body,
        )

    async def create_assigned_group_async(
        self,
        *,
        body: CreateAssignedGroupRequest,
    ) -> Optional[Union[CreateAssignedGroupResponse, DefaultError]]:
        return await _create_assigned_group_async(
            client=self.client,
            body=body,
        )

    def delete_group(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_group(
            client=self.client,
            id=id,
        )

    async def delete_group_async(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_group_async(
            client=self.client,
            id=id,
        )

    def get_group_by_id(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetGroupByIdResponse]]:
        return _get_group_by_id(
            client=self.client,
            id=id,
        )

    async def get_group_by_id_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetGroupByIdResponse]]:
        return await _get_group_by_id_async(
            client=self.client,
            id=id,
        )

    def list_groups(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListGroups"]]]:
        return _list_groups(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            filter_=filter_,
        )

    async def list_groups_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListGroups"]]]:
        return await _list_groups_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            filter_=filter_,
        )

    def update_group(
        self,
        id: str,
        *,
        body: UpdateGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _update_group(
            client=self.client,
            id=id,
            body=body,
        )

    async def update_group_async(
        self,
        id: str,
        *,
        body: UpdateGroupRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _update_group_async(
            client=self.client,
            id=id,
            body=body,
        )

    def create_lifecycle_policy(
        self,
        *,
        body: CreateLifecyclePolicyRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _create_lifecycle_policy(
            client=self.client,
            body=body,
        )

    async def create_lifecycle_policy_async(
        self,
        *,
        body: CreateLifecyclePolicyRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _create_lifecycle_policy_async(
            client=self.client,
            body=body,
        )

    def delete_lifecycle_policy(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_lifecycle_policy(
            client=self.client,
            id=id,
        )

    async def delete_lifecycle_policy_async(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_lifecycle_policy_async(
            client=self.client,
            id=id,
        )

    def lists_lifecycle_policy(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListsLifecyclePolicy"]]]:
        return _lists_lifecycle_policy(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
        )

    async def lists_lifecycle_policy_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListsLifecyclePolicy"]]]:
        return await _lists_lifecycle_policy_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
        )

    def update_lifecycle_policy(
        self,
        id: str,
        *,
        body: UpdateLifecyclePolicyRequest,
    ) -> Optional[Union[DefaultError, UpdateLifecyclePolicyResponse]]:
        return _update_lifecycle_policy(
            client=self.client,
            id=id,
            body=body,
        )

    async def update_lifecycle_policy_async(
        self,
        id: str,
        *,
        body: UpdateLifecyclePolicyRequest,
    ) -> Optional[Union[DefaultError, UpdateLifecyclePolicyResponse]]:
        return await _update_lifecycle_policy_async(
            client=self.client,
            id=id,
            body=body,
        )

    def create_user(
        self,
        *,
        body: CreateUserRequest,
    ) -> Optional[Union[CreateUserResponse, DefaultError]]:
        return _create_user(
            client=self.client,
            body=body,
        )

    async def create_user_async(
        self,
        *,
        body: CreateUserRequest,
    ) -> Optional[Union[CreateUserResponse, DefaultError]]:
        return await _create_user_async(
            client=self.client,
            body=body,
        )

    def delete_user(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_user(
            client=self.client,
            id=id,
        )

    async def delete_user_async(
        self,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_user_async(
            client=self.client,
            id=id,
        )

    def get_user(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetUserResponse]]:
        return _get_user(
            client=self.client,
            id=id,
        )

    async def get_user_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetUserResponse]]:
        return await _get_user_async(
            client=self.client,
            id=id,
        )

    def list_users(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListUsers"]]]:
        return _list_users(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            filter_=filter_,
        )

    async def list_users_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListUsers"]]]:
        return await _list_users_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            filter_=filter_,
        )

    def update_user(
        self,
        id: str,
        *,
        body: UpdateUserRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _update_user(
            client=self.client,
            id=id,
            body=body,
        )

    async def update_user_async(
        self,
        id: str,
        *,
        body: UpdateUserRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _update_user_async(
            client=self.client,
            id=id,
            body=body,
        )

    def get_group_by_name(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetGroupByNameResponse]]:
        return _get_group_by_name(
            client=self.client,
            id=id,
        )

    async def get_group_by_name_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetGroupByNameResponse]]:
        return await _get_group_by_name_async(
            client=self.client,
            id=id,
        )

    def get_group_members_delta(
        self,
        *,
        group_id: str,
    ) -> Optional[Union[DefaultError, list["GetGroupMembersDelta"]]]:
        return _get_group_members_delta(
            client=self.client,
            group_id=group_id,
        )

    async def get_group_members_delta_async(
        self,
        *,
        group_id: str,
    ) -> Optional[Union[DefaultError, list["GetGroupMembersDelta"]]]:
        return await _get_group_members_delta_async(
            client=self.client,
            group_id=group_id,
        )

    def get_manager(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetManagerResponse]]:
        return _get_manager(
            client=self.client,
            id=id,
        )

    async def get_manager_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetManagerResponse]]:
        return await _get_manager_async(
            client=self.client,
            id=id,
        )

    def get_user_roles(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["GetUserRoles"]]]:
        return _get_user_roles(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    async def get_user_roles_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["GetUserRoles"]]]:
        return await _get_user_roles_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    def group_exists(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GroupExistsResponse]]:
        return _group_exists(
            client=self.client,
            id=id,
        )

    async def group_exists_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GroupExistsResponse]]:
        return await _group_exists_async(
            client=self.client,
            id=id,
        )

    def is_group_in_lifecycle_policy(
        self,
        group_id: str,
        *,
        id: str,
    ) -> Optional[Union[DefaultError, list["IsGroupInLifecyclePolicy"]]]:
        return _is_group_in_lifecycle_policy(
            client=self.client,
            group_id=group_id,
            id=id,
        )

    async def is_group_in_lifecycle_policy_async(
        self,
        group_id: str,
        *,
        id: str,
    ) -> Optional[Union[DefaultError, list["IsGroupInLifecyclePolicy"]]]:
        return await _is_group_in_lifecycle_policy_async(
            client=self.client,
            group_id=group_id,
            id=id,
        )

    def is_member_in_role(
        self,
        id: str,
        *,
        member_id: str,
    ) -> Optional[Union[DefaultError, IsMemberInRoleResponse]]:
        return _is_member_in_role(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    async def is_member_in_role_async(
        self,
        id: str,
        *,
        member_id: str,
    ) -> Optional[Union[DefaultError, IsMemberInRoleResponse]]:
        return await _is_member_in_role_async(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    def is_member_of_group(
        self,
        id: str,
        *,
        member_id: str,
    ) -> Optional[Union[DefaultError, IsMemberOfGroupResponse]]:
        return _is_member_of_group(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    async def is_member_of_group_async(
        self,
        id: str,
        *,
        member_id: str,
    ) -> Optional[Union[DefaultError, IsMemberOfGroupResponse]]:
        return await _is_member_of_group_async(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    def is_owner_of_group(
        self,
        id: str,
        *,
        owner_id: str,
    ) -> Optional[Union[DefaultError, list["IsOwnerOfGroup"]]]:
        return _is_owner_of_group(
            client=self.client,
            id=id,
            owner_id=owner_id,
        )

    async def is_owner_of_group_async(
        self,
        id: str,
        *,
        owner_id: str,
    ) -> Optional[Union[DefaultError, list["IsOwnerOfGroup"]]]:
        return await _is_owner_of_group_async(
            client=self.client,
            id=id,
            owner_id=owner_id,
        )

    def list_all_groups_in_group(
        self,
        id: str,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Optional[Union[DefaultError, list["ListAllGroupsInGroup"]]]:
        return _list_all_groups_in_group(
            client=self.client,
            id=id,
            next_page=next_page,
            page_size=page_size,
        )

    async def list_all_groups_in_group_async(
        self,
        id: str,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Optional[Union[DefaultError, list["ListAllGroupsInGroup"]]]:
        return await _list_all_groups_in_group_async(
            client=self.client,
            id=id,
            next_page=next_page,
            page_size=page_size,
        )

    def list_all_groups_of_a_user(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListAllGroupsOfAUser"]]]:
        return _list_all_groups_of_a_user(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            id=id,
        )

    async def list_all_groups_of_a_user_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListAllGroupsOfAUser"]]]:
        return await _list_all_groups_of_a_user_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            id=id,
        )

    def list_direct_reports(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListDirectReports"]]]:
        return _list_direct_reports(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    async def list_direct_reports_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListDirectReports"]]]:
        return await _list_direct_reports_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    def list_directory_roles(
        self,
    ) -> Optional[Union[DefaultError, list["ListDirectoryRoles"]]]:
        return _list_directory_roles(
            client=self.client,
        )

    async def list_directory_roles_async(
        self,
    ) -> Optional[Union[DefaultError, list["ListDirectoryRoles"]]]:
        return await _list_directory_roles_async(
            client=self.client,
        )

    def list_owners_of_a_group(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListOwnersOfAGroup"]]]:
        return _list_owners_of_a_group(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    async def list_owners_of_a_group_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListOwnersOfAGroup"]]]:
        return await _list_owners_of_a_group_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            id=id,
        )

    def list_users_in_group(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListUsersInGroup"]]]:
        return _list_users_in_group(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            id=id,
        )

    async def list_users_in_group_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListUsersInGroup"]]]:
        return await _list_users_in_group_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            id=id,
        )

    def list_users_in_role(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListUsersInRole"]]]:
        return _list_users_in_role(
            client=self.client,
            id=id,
        )

    async def list_users_in_role_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, list["ListUsersInRole"]]]:
        return await _list_users_in_role_async(
            client=self.client,
            id=id,
        )

    def remove_group_from_lifecycle_policy(
        self,
        id: str,
        *,
        group_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _remove_group_from_lifecycle_policy(
            client=self.client,
            id=id,
            group_id=group_id,
        )

    async def remove_group_from_lifecycle_policy_async(
        self,
        id: str,
        *,
        group_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _remove_group_from_lifecycle_policy_async(
            client=self.client,
            id=id,
            group_id=group_id,
        )

    def remove_license(
        self,
        id: str,
        *,
        body: RemoveLicenseRequest,
    ) -> Optional[Union[DefaultError, RemoveLicenseResponse]]:
        return _remove_license(
            client=self.client,
            id=id,
            body=body,
        )

    async def remove_license_async(
        self,
        id: str,
        *,
        body: RemoveLicenseRequest,
    ) -> Optional[Union[DefaultError, RemoveLicenseResponse]]:
        return await _remove_license_async(
            client=self.client,
            id=id,
            body=body,
        )

    def remove_member_from_group(
        self,
        id: str,
        member_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _remove_member_from_group(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    async def remove_member_from_group_async(
        self,
        id: str,
        member_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _remove_member_from_group_async(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    def remove_member_from_role(
        self,
        id: str,
        member_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _remove_member_from_role(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    async def remove_member_from_role_async(
        self,
        id: str,
        member_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _remove_member_from_role_async(
            client=self.client,
            id=id,
            member_id=member_id,
        )

    def remove_owner_from_group(
        self,
        id: str,
        owner_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _remove_owner_from_group(
            client=self.client,
            id=id,
            owner_id=owner_id,
        )

    async def remove_owner_from_group_async(
        self,
        id: str,
        owner_id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _remove_owner_from_group_async(
            client=self.client,
            id=id,
            owner_id=owner_id,
        )

    def reset_password(
        self,
        id: str,
        *,
        body: ResetPasswordRequest,
        select: Optional[str] = "id",
    ) -> Optional[Union[Any, DefaultError]]:
        return _reset_password(
            client=self.client,
            id=id,
            body=body,
            select=select,
        )

    async def reset_password_async(
        self,
        id: str,
        *,
        body: ResetPasswordRequest,
        select: Optional[str] = "id",
    ) -> Optional[Union[Any, DefaultError]]:
        return await _reset_password_async(
            client=self.client,
            id=id,
            body=body,
            select=select,
        )

    def set_manager(
        self,
        id: str,
        *,
        body: SetManagerRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _set_manager(
            client=self.client,
            id=id,
            body=body,
        )

    async def set_manager_async(
        self,
        id: str,
        *,
        body: SetManagerRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _set_manager_async(
            client=self.client,
            id=id,
            body=body,
        )

    def user_exists(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, UserExistsResponse]]:
        return _user_exists(
            client=self.client,
            id=id,
        )

    async def user_exists_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, UserExistsResponse]]:
        return await _user_exists_async(
            client=self.client,
            id=id,
        )
