import gs_options_pb2 as _gs_options_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rest.user import profile_pb2 as _profile_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrgTeamRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgTeamRoleNormal: _ClassVar[OrgTeamRole]
    OrgTeamRoleAdmin: _ClassVar[OrgTeamRole]

class CreateOrgTeamResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateOrgTeamResponseCodeSuccess: _ClassVar[CreateOrgTeamResponseCode]
    CreateOrgTeamResponseCodeSomeEmailsAreNotOrgMembers: _ClassVar[CreateOrgTeamResponseCode]
    CreateOrgTeamResponseCodeTeamNameAlreadyUsed: _ClassVar[CreateOrgTeamResponseCode]

class UpdateOrgTeamResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateOrgTeamResponseCodeSuccess: _ClassVar[UpdateOrgTeamResponseCode]
    UpdateOrgTeamResponseCodeTeamNotFoundOrDeleted: _ClassVar[UpdateOrgTeamResponseCode]
    UpdateOrgTeamResponseCodeSomeEmailsAreNotOrgMembers: _ClassVar[UpdateOrgTeamResponseCode]
    UpdateOrgTeamResponseCodeHasExternalMembers: _ClassVar[UpdateOrgTeamResponseCode]
    UpdateOrgTeamResponseCodeTeamNameAlreadyUsed: _ClassVar[UpdateOrgTeamResponseCode]

class MarkTeamAsFavoriteResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MarkTeamAsFavoriteResponseCodeUnknown: _ClassVar[MarkTeamAsFavoriteResponseCode]
    MarkTeamAsFavoriteResponseCodeSuccess: _ClassVar[MarkTeamAsFavoriteResponseCode]
    MarkTeamAsFavoriteResponseCodeNotAMember: _ClassVar[MarkTeamAsFavoriteResponseCode]

class RemoveExternalMembersFromTeamResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RemoveExternalMembersFromTeamResponseCodeUnkown: _ClassVar[RemoveExternalMembersFromTeamResponseCode]
    RemoveExternalMembersFromTeamResponseCodeSuccess: _ClassVar[RemoveExternalMembersFromTeamResponseCode]
    RemoveExternalMembersFromTeamResponseCodeTeamNotFound: _ClassVar[RemoveExternalMembersFromTeamResponseCode]

class DeleteOrgTeamResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeleteOrgTeamResponseCodeSuccess: _ClassVar[DeleteOrgTeamResponseCode]
    DeleteOrgTeamResponseCodeTeamHasUntrashedItems: _ClassVar[DeleteOrgTeamResponseCode]
    DeleteOrgTeamResponseCodeTeamHasTrashedItems: _ClassVar[DeleteOrgTeamResponseCode]
    DeleteOrgTeamResponseCodeTeamHasMembers: _ClassVar[DeleteOrgTeamResponseCode]

class ViewLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ViewLevel_Normal: _ClassVar[ViewLevel]
    ViewLevel_NoMembers: _ClassVar[ViewLevel]
    ViewLevel_MemberCount: _ClassVar[ViewLevel]

class GetOrgTeamResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetOrgTeamsResponseCodeSuccess: _ClassVar[GetOrgTeamResponseCode]
    GetOrgTeamsResponseCodeTeamNotFound: _ClassVar[GetOrgTeamResponseCode]

class InviteStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InviteStatus_InvitedNewUser: _ClassVar[InviteStatus]
    InviteStatus_AddedUserToOrg: _ClassVar[InviteStatus]
    InviteStatus_RejectedUserAlreadyInOrg: _ClassVar[InviteStatus]
    InviteStatus_RejectedInvalidEmail: _ClassVar[InviteStatus]
    InviteStatus_RejectedNoSeatsAvailable: _ClassVar[InviteStatus]
    InviteStatus_AddedInactiveUserToOrg: _ClassVar[InviteStatus]
    InviteStatus_RejectedOrgAccountDueToExists: _ClassVar[InviteStatus]
    InviteStatus_ResentInviteEmailToUser: _ClassVar[InviteStatus]
    InviteStatus_RejectedUserInAnotherOrg: _ClassVar[InviteStatus]

class RemoveUserFromOrgResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RemoveUserFromOrgResult_Unknown: _ClassVar[RemoveUserFromOrgResult]
    RemoveUserFromOrgResult_Success: _ClassVar[RemoveUserFromOrgResult]
    RemoveUserFromOrgResult_MoveDeletedFilesToUserIdNotExistInOrg: _ClassVar[RemoveUserFromOrgResult]
    RemoveUserFromOrgResult_UserIdNotFound: _ClassVar[RemoveUserFromOrgResult]

class SwitchResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SwitchResult_SwitchUnknown: _ClassVar[SwitchResult]
    SwitchResult_SwitchSuccess: _ClassVar[SwitchResult]
    SwitchResult_SwitchNoPermission: _ClassVar[SwitchResult]
    SwitchResult_SwitchNetError: _ClassVar[SwitchResult]

class EditMemberRoleResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EditMemberRoleResult_EditMemberRoleSuccess: _ClassVar[EditMemberRoleResult]
    EditMemberRoleResult_EditMemberRoleNoPermission: _ClassVar[EditMemberRoleResult]
    EditMemberRoleResult_EditMemberRoleNotMember: _ClassVar[EditMemberRoleResult]
    EditMemberRoleResult_EditMemberRoleChangedByOther: _ClassVar[EditMemberRoleResult]
    EditMemberRoleResult_EditMemberRoleInvalidRole: _ClassVar[EditMemberRoleResult]
    EditMemberRoleResult_EditMemberRoleNotEnoughSeats: _ClassVar[EditMemberRoleResult]

class RequestUserInviteStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RequestUserInviteStatus_Unknown: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_RequestSent: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_RejectedUserAlreadyInOrg: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_RejectedInvalidEmail: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_RejectedUnauthorized: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_AlreadyRequested: _ClassVar[RequestUserInviteStatus]
    RequestUserInviteStatus_RejectedUserInAnotherOrg: _ClassVar[RequestUserInviteStatus]
OrgTeamRoleNormal: OrgTeamRole
OrgTeamRoleAdmin: OrgTeamRole
CreateOrgTeamResponseCodeSuccess: CreateOrgTeamResponseCode
CreateOrgTeamResponseCodeSomeEmailsAreNotOrgMembers: CreateOrgTeamResponseCode
CreateOrgTeamResponseCodeTeamNameAlreadyUsed: CreateOrgTeamResponseCode
UpdateOrgTeamResponseCodeSuccess: UpdateOrgTeamResponseCode
UpdateOrgTeamResponseCodeTeamNotFoundOrDeleted: UpdateOrgTeamResponseCode
UpdateOrgTeamResponseCodeSomeEmailsAreNotOrgMembers: UpdateOrgTeamResponseCode
UpdateOrgTeamResponseCodeHasExternalMembers: UpdateOrgTeamResponseCode
UpdateOrgTeamResponseCodeTeamNameAlreadyUsed: UpdateOrgTeamResponseCode
MarkTeamAsFavoriteResponseCodeUnknown: MarkTeamAsFavoriteResponseCode
MarkTeamAsFavoriteResponseCodeSuccess: MarkTeamAsFavoriteResponseCode
MarkTeamAsFavoriteResponseCodeNotAMember: MarkTeamAsFavoriteResponseCode
RemoveExternalMembersFromTeamResponseCodeUnkown: RemoveExternalMembersFromTeamResponseCode
RemoveExternalMembersFromTeamResponseCodeSuccess: RemoveExternalMembersFromTeamResponseCode
RemoveExternalMembersFromTeamResponseCodeTeamNotFound: RemoveExternalMembersFromTeamResponseCode
DeleteOrgTeamResponseCodeSuccess: DeleteOrgTeamResponseCode
DeleteOrgTeamResponseCodeTeamHasUntrashedItems: DeleteOrgTeamResponseCode
DeleteOrgTeamResponseCodeTeamHasTrashedItems: DeleteOrgTeamResponseCode
DeleteOrgTeamResponseCodeTeamHasMembers: DeleteOrgTeamResponseCode
ViewLevel_Normal: ViewLevel
ViewLevel_NoMembers: ViewLevel
ViewLevel_MemberCount: ViewLevel
GetOrgTeamsResponseCodeSuccess: GetOrgTeamResponseCode
GetOrgTeamsResponseCodeTeamNotFound: GetOrgTeamResponseCode
InviteStatus_InvitedNewUser: InviteStatus
InviteStatus_AddedUserToOrg: InviteStatus
InviteStatus_RejectedUserAlreadyInOrg: InviteStatus
InviteStatus_RejectedInvalidEmail: InviteStatus
InviteStatus_RejectedNoSeatsAvailable: InviteStatus
InviteStatus_AddedInactiveUserToOrg: InviteStatus
InviteStatus_RejectedOrgAccountDueToExists: InviteStatus
InviteStatus_ResentInviteEmailToUser: InviteStatus
InviteStatus_RejectedUserInAnotherOrg: InviteStatus
RemoveUserFromOrgResult_Unknown: RemoveUserFromOrgResult
RemoveUserFromOrgResult_Success: RemoveUserFromOrgResult
RemoveUserFromOrgResult_MoveDeletedFilesToUserIdNotExistInOrg: RemoveUserFromOrgResult
RemoveUserFromOrgResult_UserIdNotFound: RemoveUserFromOrgResult
SwitchResult_SwitchUnknown: SwitchResult
SwitchResult_SwitchSuccess: SwitchResult
SwitchResult_SwitchNoPermission: SwitchResult
SwitchResult_SwitchNetError: SwitchResult
EditMemberRoleResult_EditMemberRoleSuccess: EditMemberRoleResult
EditMemberRoleResult_EditMemberRoleNoPermission: EditMemberRoleResult
EditMemberRoleResult_EditMemberRoleNotMember: EditMemberRoleResult
EditMemberRoleResult_EditMemberRoleChangedByOther: EditMemberRoleResult
EditMemberRoleResult_EditMemberRoleInvalidRole: EditMemberRoleResult
EditMemberRoleResult_EditMemberRoleNotEnoughSeats: EditMemberRoleResult
RequestUserInviteStatus_Unknown: RequestUserInviteStatus
RequestUserInviteStatus_RequestSent: RequestUserInviteStatus
RequestUserInviteStatus_RejectedUserAlreadyInOrg: RequestUserInviteStatus
RequestUserInviteStatus_RejectedInvalidEmail: RequestUserInviteStatus
RequestUserInviteStatus_RejectedUnauthorized: RequestUserInviteStatus
RequestUserInviteStatus_AlreadyRequested: RequestUserInviteStatus
RequestUserInviteStatus_RejectedUserInAnotherOrg: RequestUserInviteStatus

class OrgTeamMember(_message.Message):
    __slots__ = ("id", "role", "orgId", "orgName", "teamId", "teamName", "teamHexColour", "userId", "userEmail", "userName", "joinedOn", "isGuest", "guestOrgId")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ORGNAME_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    TEAMNAME_FIELD_NUMBER: _ClassVar[int]
    TEAMHEXCOLOUR_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    JOINEDON_FIELD_NUMBER: _ClassVar[int]
    ISGUEST_FIELD_NUMBER: _ClassVar[int]
    GUESTORGID_FIELD_NUMBER: _ClassVar[int]
    id: str
    role: OrgTeamRole
    orgId: str
    orgName: str
    teamId: str
    teamName: str
    teamHexColour: str
    userId: str
    userEmail: str
    userName: str
    joinedOn: int
    isGuest: bool
    guestOrgId: str
    def __init__(self, id: _Optional[str] = ..., role: _Optional[_Union[OrgTeamRole, str]] = ..., orgId: _Optional[str] = ..., orgName: _Optional[str] = ..., teamId: _Optional[str] = ..., teamName: _Optional[str] = ..., teamHexColour: _Optional[str] = ..., userId: _Optional[str] = ..., userEmail: _Optional[str] = ..., userName: _Optional[str] = ..., joinedOn: _Optional[int] = ..., isGuest: bool = ..., guestOrgId: _Optional[str] = ...) -> None: ...

class SharedOrgTeam(_message.Message):
    __slots__ = ("teamId", "name")
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    name: str
    def __init__(self, teamId: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ExternalOrgInfo(_message.Message):
    __slots__ = ("id", "name", "deleted")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    deleted: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., deleted: bool = ...) -> None: ...

class OrgTeam(_message.Message):
    __slots__ = ("id", "name", "hexColour", "orgId", "createdOn", "members", "guestAllowed", "guestOrgInfo", "hostOrgInfo", "memberCount", "guestsCount", "lastModified", "markedAsFavorite", "allowExternalUsers")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HEXCOLOUR_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    GUESTALLOWED_FIELD_NUMBER: _ClassVar[int]
    GUESTORGINFO_FIELD_NUMBER: _ClassVar[int]
    HOSTORGINFO_FIELD_NUMBER: _ClassVar[int]
    MEMBERCOUNT_FIELD_NUMBER: _ClassVar[int]
    GUESTSCOUNT_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIED_FIELD_NUMBER: _ClassVar[int]
    MARKEDASFAVORITE_FIELD_NUMBER: _ClassVar[int]
    ALLOWEXTERNALUSERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    hexColour: str
    orgId: str
    createdOn: int
    members: _containers.RepeatedCompositeFieldContainer[OrgTeamMember]
    guestAllowed: bool
    guestOrgInfo: ExternalOrgInfo
    hostOrgInfo: ExternalOrgInfo
    memberCount: int
    guestsCount: int
    lastModified: int
    markedAsFavorite: bool
    allowExternalUsers: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., hexColour: _Optional[str] = ..., orgId: _Optional[str] = ..., createdOn: _Optional[int] = ..., members: _Optional[_Iterable[_Union[OrgTeamMember, _Mapping]]] = ..., guestAllowed: bool = ..., guestOrgInfo: _Optional[_Union[ExternalOrgInfo, _Mapping]] = ..., hostOrgInfo: _Optional[_Union[ExternalOrgInfo, _Mapping]] = ..., memberCount: _Optional[int] = ..., guestsCount: _Optional[int] = ..., lastModified: _Optional[int] = ..., markedAsFavorite: bool = ..., allowExternalUsers: bool = ...) -> None: ...

class CreateOrgTeamRequest(_message.Message):
    __slots__ = ("orgId", "teamName")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMNAME_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamName: str
    def __init__(self, orgId: _Optional[str] = ..., teamName: _Optional[str] = ...) -> None: ...

class OrgTeamMemberRoleChange(_message.Message):
    __slots__ = ("email", "role")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    email: str
    role: OrgTeamRole
    def __init__(self, email: _Optional[str] = ..., role: _Optional[_Union[OrgTeamRole, str]] = ...) -> None: ...

class CreateOrgTeamResponse(_message.Message):
    __slots__ = ("code", "team")
    CODE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    code: CreateOrgTeamResponseCode
    team: OrgTeam
    def __init__(self, code: _Optional[_Union[CreateOrgTeamResponseCode, str]] = ..., team: _Optional[_Union[OrgTeam, _Mapping]] = ...) -> None: ...

class UpdateOrgTeamRequest(_message.Message):
    __slots__ = ("orgId", "teamId", "membersToAdd", "memberUserIdsToRemove", "newTeamName", "allowExternalUsers")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSTOADD_FIELD_NUMBER: _ClassVar[int]
    MEMBERUSERIDSTOREMOVE_FIELD_NUMBER: _ClassVar[int]
    NEWTEAMNAME_FIELD_NUMBER: _ClassVar[int]
    ALLOWEXTERNALUSERS_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    membersToAdd: _containers.RepeatedCompositeFieldContainer[OrgTeamMemberRoleChange]
    memberUserIdsToRemove: _containers.RepeatedScalarFieldContainer[str]
    newTeamName: _wrappers_pb2.OptionalString
    allowExternalUsers: _wrappers_pb2.OptionalBool
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ..., membersToAdd: _Optional[_Iterable[_Union[OrgTeamMemberRoleChange, _Mapping]]] = ..., memberUserIdsToRemove: _Optional[_Iterable[str]] = ..., newTeamName: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., allowExternalUsers: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ...) -> None: ...

class UpdateOrgTeamResponse(_message.Message):
    __slots__ = ("code", "team")
    CODE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    code: UpdateOrgTeamResponseCode
    team: OrgTeam
    def __init__(self, code: _Optional[_Union[UpdateOrgTeamResponseCode, str]] = ..., team: _Optional[_Union[OrgTeam, _Mapping]] = ...) -> None: ...

class RemoveExternalMembersFromTeamRequest(_message.Message):
    __slots__ = ("orgId", "teamId")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ...) -> None: ...

class MarkTeamAsFavoriteRequest(_message.Message):
    __slots__ = ("orgId", "teamId", "isFavorite")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    ISFAVORITE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    isFavorite: bool
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ..., isFavorite: bool = ...) -> None: ...

class MarkTeamAsFavoriteResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: MarkTeamAsFavoriteResponseCode
    def __init__(self, code: _Optional[_Union[MarkTeamAsFavoriteResponseCode, str]] = ...) -> None: ...

class RemoveExternalMembersFromTeamResponse(_message.Message):
    __slots__ = ("removeExternalMembersFromTeamResponseCode",)
    REMOVEEXTERNALMEMBERSFROMTEAMRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    removeExternalMembersFromTeamResponseCode: RemoveExternalMembersFromTeamResponseCode
    def __init__(self, removeExternalMembersFromTeamResponseCode: _Optional[_Union[RemoveExternalMembersFromTeamResponseCode, str]] = ...) -> None: ...

class DeleteOrgTeamRequest(_message.Message):
    __slots__ = ("orgId", "teamId")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ...) -> None: ...

class DeleteOrgTeamResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: DeleteOrgTeamResponseCode
    def __init__(self, code: _Optional[_Union[DeleteOrgTeamResponseCode, str]] = ...) -> None: ...

class ListAllTeamsForUserRequest(_message.Message):
    __slots__ = ("pageSize", "pageToken")
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    pageSize: int
    pageToken: str
    def __init__(self, pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ...) -> None: ...

class ListAllTeamsForUserResponse(_message.Message):
    __slots__ = ("teams", "nextPageToken")
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[OrgTeam]
    nextPageToken: str
    def __init__(self, teams: _Optional[_Iterable[_Union[OrgTeam, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class ListOrgTeamsRequest(_message.Message):
    __slots__ = ("orgId", "pageSize", "pageToken", "viewLevel")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    VIEWLEVEL_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    pageSize: int
    pageToken: str
    viewLevel: ViewLevel
    def __init__(self, orgId: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ..., viewLevel: _Optional[_Union[ViewLevel, str]] = ...) -> None: ...

class ListOrgTeamsResponse(_message.Message):
    __slots__ = ("teams", "nextPageToken")
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[OrgTeam]
    nextPageToken: str
    def __init__(self, teams: _Optional[_Iterable[_Union[OrgTeam, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class GetAllOrgTeamsRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class GetAllOrgTeamsResponse(_message.Message):
    __slots__ = ("teams",)
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[OrgTeam]
    def __init__(self, teams: _Optional[_Iterable[_Union[OrgTeam, _Mapping]]] = ...) -> None: ...

class ListUserOrgTeamMembershipsRequest(_message.Message):
    __slots__ = ("orgId", "pageSize", "pageToken")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    pageSize: int
    pageToken: str
    def __init__(self, orgId: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ...) -> None: ...

class ListUserOrgTeamMembershipsResponse(_message.Message):
    __slots__ = ("teamMemberships", "nextPageToken")
    TEAMMEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    teamMemberships: _containers.RepeatedCompositeFieldContainer[OrgTeamMember]
    nextPageToken: str
    def __init__(self, teamMemberships: _Optional[_Iterable[_Union[OrgTeamMember, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class GetOrgTeamRequest(_message.Message):
    __slots__ = ("orgId", "teamId", "viewLevel")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    VIEWLEVEL_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    viewLevel: ViewLevel
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ..., viewLevel: _Optional[_Union[ViewLevel, str]] = ...) -> None: ...

class GetOrgTeamResponse(_message.Message):
    __slots__ = ("team", "code")
    TEAM_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    team: OrgTeam
    code: GetOrgTeamResponseCode
    def __init__(self, team: _Optional[_Union[OrgTeam, _Mapping]] = ..., code: _Optional[_Union[GetOrgTeamResponseCode, str]] = ...) -> None: ...

class GetTeamRequest(_message.Message):
    __slots__ = ("teamId",)
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    def __init__(self, teamId: _Optional[str] = ...) -> None: ...

class GetTeamResponse(_message.Message):
    __slots__ = ("team",)
    TEAM_FIELD_NUMBER: _ClassVar[int]
    team: OrgTeam
    def __init__(self, team: _Optional[_Union[OrgTeam, _Mapping]] = ...) -> None: ...

class InviteMembersRequest(_message.Message):
    __slots__ = ("emails", "isOrgAccount", "orgId", "role")
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    ISORGACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    emails: _containers.RepeatedScalarFieldContainer[str]
    isOrgAccount: bool
    orgId: str
    role: _gravi_model_pb2.OrgMemberRole
    def __init__(self, emails: _Optional[_Iterable[str]] = ..., isOrgAccount: bool = ..., orgId: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ...) -> None: ...

class InviteMembersResponse(_message.Message):
    __slots__ = ("inviteResult",)
    INVITERESULT_FIELD_NUMBER: _ClassVar[int]
    inviteResult: _containers.RepeatedCompositeFieldContainer[InviteResult]
    def __init__(self, inviteResult: _Optional[_Iterable[_Union[InviteResult, _Mapping]]] = ...) -> None: ...

class InviteResult(_message.Message):
    __slots__ = ("email", "inviteStatus")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    INVITESTATUS_FIELD_NUMBER: _ClassVar[int]
    email: str
    inviteStatus: InviteStatus
    def __init__(self, email: _Optional[str] = ..., inviteStatus: _Optional[_Union[InviteStatus, str]] = ...) -> None: ...

class EditMemberActiveStatusRequest(_message.Message):
    __slots__ = ("userId", "toStatusId", "orgId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    TOSTATUSID_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    toStatusId: int
    orgId: str
    def __init__(self, userId: _Optional[str] = ..., toStatusId: _Optional[int] = ..., orgId: _Optional[str] = ...) -> None: ...

class EditMemberActiveStatusResponse(_message.Message):
    __slots__ = ("isSuccess",)
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    def __init__(self, isSuccess: bool = ...) -> None: ...

class RemoveMemberFromOrgRequest(_message.Message):
    __slots__ = ("userId", "orgId", "moveRemovedFilesToUserId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    MOVEREMOVEDFILESTOUSERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    orgId: str
    moveRemovedFilesToUserId: str
    def __init__(self, userId: _Optional[str] = ..., orgId: _Optional[str] = ..., moveRemovedFilesToUserId: _Optional[str] = ...) -> None: ...

class RemoveMemberFromOrgResponse(_message.Message):
    __slots__ = ("resultCode",)
    RESULTCODE_FIELD_NUMBER: _ClassVar[int]
    resultCode: RemoveUserFromOrgResult
    def __init__(self, resultCode: _Optional[_Union[RemoveUserFromOrgResult, str]] = ...) -> None: ...

class SwitchUserOrgRequest(_message.Message):
    __slots__ = ("switchToOrgId",)
    SWITCHTOORGID_FIELD_NUMBER: _ClassVar[int]
    switchToOrgId: str
    def __init__(self, switchToOrgId: _Optional[str] = ...) -> None: ...

class SwitchUserOrgResponse(_message.Message):
    __slots__ = ("priceTier", "switchResult")
    PRICETIER_FIELD_NUMBER: _ClassVar[int]
    SWITCHRESULT_FIELD_NUMBER: _ClassVar[int]
    priceTier: _gravi_model_pb2.PriceTier
    switchResult: SwitchResult
    def __init__(self, priceTier: _Optional[_Union[_gravi_model_pb2.PriceTier, str]] = ..., switchResult: _Optional[_Union[SwitchResult, str]] = ...) -> None: ...

class EditMemberRoleRequest(_message.Message):
    __slots__ = ("userId", "fromRole", "toRole", "orgId", "fromLicense", "fromPermissionRole", "toLicense", "toPermissionRole")
    USERID_FIELD_NUMBER: _ClassVar[int]
    FROMROLE_FIELD_NUMBER: _ClassVar[int]
    TOROLE_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    FROMLICENSE_FIELD_NUMBER: _ClassVar[int]
    FROMPERMISSIONROLE_FIELD_NUMBER: _ClassVar[int]
    TOLICENSE_FIELD_NUMBER: _ClassVar[int]
    TOPERMISSIONROLE_FIELD_NUMBER: _ClassVar[int]
    userId: str
    fromRole: _gravi_model_pb2.OrgMemberRole
    toRole: _gravi_model_pb2.OrgMemberRole
    orgId: str
    fromLicense: _gravi_model_pb2.OrgLicenseType
    fromPermissionRole: _gravi_model_pb2.OrgRoleType
    toLicense: _gravi_model_pb2.OrgLicenseType
    toPermissionRole: _gravi_model_pb2.OrgRoleType
    def __init__(self, userId: _Optional[str] = ..., fromRole: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., toRole: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., orgId: _Optional[str] = ..., fromLicense: _Optional[_Union[_gravi_model_pb2.OrgLicenseType, str]] = ..., fromPermissionRole: _Optional[_Union[_gravi_model_pb2.OrgRoleType, str]] = ..., toLicense: _Optional[_Union[_gravi_model_pb2.OrgLicenseType, str]] = ..., toPermissionRole: _Optional[_Union[_gravi_model_pb2.OrgRoleType, str]] = ...) -> None: ...

class EditMemberRoleResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EditMemberRoleResult
    def __init__(self, result: _Optional[_Union[EditMemberRoleResult, str]] = ...) -> None: ...

class GetUsersInOrgRequest(_message.Message):
    __slots__ = ("pageSize", "pageToken", "orgId")
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    pageSize: int
    pageToken: str
    orgId: str
    def __init__(self, pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ..., orgId: _Optional[str] = ...) -> None: ...

class GetUsersInOrgResponse(_message.Message):
    __slots__ = ("userInfo", "nextPageToken")
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    userInfo: _containers.RepeatedCompositeFieldContainer[_profile_pb2.UserInfo]
    nextPageToken: str
    def __init__(self, userInfo: _Optional[_Iterable[_Union[_profile_pb2.UserInfo, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class RequestUserInviteToOrgAdminRequest(_message.Message):
    __slots__ = ("orgId", "emails", "role", "orgAccountInvite")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ORGACCOUNTINVITE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    emails: _containers.RepeatedScalarFieldContainer[str]
    role: _gravi_model_pb2.OrgMemberRole
    orgAccountInvite: bool
    def __init__(self, orgId: _Optional[str] = ..., emails: _Optional[_Iterable[str]] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., orgAccountInvite: bool = ...) -> None: ...

class RequestUserInviteResult(_message.Message):
    __slots__ = ("email", "requestStatus", "userId")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    REQUESTSTATUS_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    email: str
    requestStatus: RequestUserInviteStatus
    userId: str
    def __init__(self, email: _Optional[str] = ..., requestStatus: _Optional[_Union[RequestUserInviteStatus, str]] = ..., userId: _Optional[str] = ...) -> None: ...

class RequestUserInviteToOrgAdminResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[RequestUserInviteResult]
    def __init__(self, results: _Optional[_Iterable[_Union[RequestUserInviteResult, _Mapping]]] = ...) -> None: ...

class UserInviteApprovalRequest(_message.Message):
    __slots__ = ("orgId", "email", "role", "orgAccountInvite", "approve")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ORGACCOUNTINVITE_FIELD_NUMBER: _ClassVar[int]
    APPROVE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    email: str
    role: _gravi_model_pb2.OrgMemberRole
    orgAccountInvite: bool
    approve: bool
    def __init__(self, orgId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., orgAccountInvite: bool = ..., approve: bool = ...) -> None: ...

class UserInviteApprovalResponse(_message.Message):
    __slots__ = ("inviteStatus",)
    INVITESTATUS_FIELD_NUMBER: _ClassVar[int]
    inviteStatus: InviteStatus
    def __init__(self, inviteStatus: _Optional[_Union[InviteStatus, str]] = ...) -> None: ...

class UserOrgJoinRequest(_message.Message):
    __slots__ = ("orgId", "email", "role", "orgAccountInvite", "requestedOn", "requestedBy", "forcePersonalAccount", "userId")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ORGACCOUNTINVITE_FIELD_NUMBER: _ClassVar[int]
    REQUESTEDON_FIELD_NUMBER: _ClassVar[int]
    REQUESTEDBY_FIELD_NUMBER: _ClassVar[int]
    FORCEPERSONALACCOUNT_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    email: str
    role: _gravi_model_pb2.OrgMemberRole
    orgAccountInvite: bool
    requestedOn: int
    requestedBy: str
    forcePersonalAccount: bool
    userId: str
    def __init__(self, orgId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., orgAccountInvite: bool = ..., requestedOn: _Optional[int] = ..., requestedBy: _Optional[str] = ..., forcePersonalAccount: bool = ..., userId: _Optional[str] = ...) -> None: ...

class ListOrgJoinRequestsRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class ListOrgJoinRequestsResponse(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[UserOrgJoinRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[UserOrgJoinRequest, _Mapping]]] = ...) -> None: ...
