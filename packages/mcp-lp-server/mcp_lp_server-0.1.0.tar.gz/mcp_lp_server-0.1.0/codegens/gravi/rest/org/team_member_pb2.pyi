import gs_options_pb2 as _gs_options_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rest.user import profile_pb2 as _profile_pb2
from gravi.rest.org import team_pb2 as _team_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateOrgTeamMemberResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateOrgTeamMemberResponseCodeSuccess: _ClassVar[CreateOrgTeamMemberResponseCode]
    CreateOrgTeamMemberResponseCodeUserMustEitherBeInGuestOrgOrHostOrg: _ClassVar[CreateOrgTeamMemberResponseCode]
    CreateOrgTeamMemberResponseCodeUserAlreadyInTeam: _ClassVar[CreateOrgTeamMemberResponseCode]
    CreateOrgTeamMemberResponseCodeTeamNotFound: _ClassVar[CreateOrgTeamMemberResponseCode]
    CreateOrgTeamMemberResponseCodeUserNotFound: _ClassVar[CreateOrgTeamMemberResponseCode]

class UpdateOrgTeamMemberResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateOrgTeamMemberResponseCodeSuccess: _ClassVar[UpdateOrgTeamMemberResponseCode]
    UpdateOrgTeamMemberResponseCodeMemberNotFound: _ClassVar[UpdateOrgTeamMemberResponseCode]
CreateOrgTeamMemberResponseCodeSuccess: CreateOrgTeamMemberResponseCode
CreateOrgTeamMemberResponseCodeUserMustEitherBeInGuestOrgOrHostOrg: CreateOrgTeamMemberResponseCode
CreateOrgTeamMemberResponseCodeUserAlreadyInTeam: CreateOrgTeamMemberResponseCode
CreateOrgTeamMemberResponseCodeTeamNotFound: CreateOrgTeamMemberResponseCode
CreateOrgTeamMemberResponseCodeUserNotFound: CreateOrgTeamMemberResponseCode
UpdateOrgTeamMemberResponseCodeSuccess: UpdateOrgTeamMemberResponseCode
UpdateOrgTeamMemberResponseCodeMemberNotFound: UpdateOrgTeamMemberResponseCode

class CreateOrgTeamMemberRequest(_message.Message):
    __slots__ = ("orgId", "teamId", "email", "role")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    email: str
    role: _team_pb2.OrgTeamRole
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_team_pb2.OrgTeamRole, str]] = ...) -> None: ...

class CreateOrgTeamMemberResponse(_message.Message):
    __slots__ = ("code", "member")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    code: CreateOrgTeamMemberResponseCode
    member: _team_pb2.OrgTeamMember
    def __init__(self, code: _Optional[_Union[CreateOrgTeamMemberResponseCode, str]] = ..., member: _Optional[_Union[_team_pb2.OrgTeamMember, _Mapping]] = ...) -> None: ...

class UpdateOrgTeamMemberRequest(_message.Message):
    __slots__ = ("id", "newRole")
    ID_FIELD_NUMBER: _ClassVar[int]
    NEWROLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    newRole: _team_pb2.OrgTeamRole
    def __init__(self, id: _Optional[str] = ..., newRole: _Optional[_Union[_team_pb2.OrgTeamRole, str]] = ...) -> None: ...

class UpdateOrgTeamMemberResponse(_message.Message):
    __slots__ = ("code", "member")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    code: UpdateOrgTeamMemberResponseCode
    member: _team_pb2.OrgTeamMember
    def __init__(self, code: _Optional[_Union[UpdateOrgTeamMemberResponseCode, str]] = ..., member: _Optional[_Union[_team_pb2.OrgTeamMember, _Mapping]] = ...) -> None: ...

class DeleteOrgTeamMemberRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteOrgTeamMemberResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOrgTeamMembersRequest(_message.Message):
    __slots__ = ("orgId", "teamId", "pageSize", "pageToken")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    teamId: str
    pageSize: int
    pageToken: str
    def __init__(self, orgId: _Optional[str] = ..., teamId: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ...) -> None: ...

class ListOrgTeamMembersResponse(_message.Message):
    __slots__ = ("members", "nextPageToken")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[_team_pb2.OrgTeamMember]
    nextPageToken: str
    def __init__(self, members: _Optional[_Iterable[_Union[_team_pb2.OrgTeamMember, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...
