from gravi.rest.auth import auth_pb2 as _auth_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListOrgUserActionAuditsRequest(_message.Message):
    __slots__ = ("orgId", "userId", "paginationToken", "resultCount")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    PAGINATIONTOKEN_FIELD_NUMBER: _ClassVar[int]
    RESULTCOUNT_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    userId: str
    paginationToken: str
    resultCount: int
    def __init__(self, orgId: _Optional[str] = ..., userId: _Optional[str] = ..., paginationToken: _Optional[str] = ..., resultCount: _Optional[int] = ...) -> None: ...

class ListOrgUserActionAuditsResponse(_message.Message):
    __slots__ = ("nextPaginationToken", "userSecurityAudits")
    NEXTPAGINATIONTOKEN_FIELD_NUMBER: _ClassVar[int]
    USERSECURITYAUDITS_FIELD_NUMBER: _ClassVar[int]
    nextPaginationToken: str
    userSecurityAudits: _containers.RepeatedCompositeFieldContainer[_auth_pb2.UserSecurityAudit]
    def __init__(self, nextPaginationToken: _Optional[str] = ..., userSecurityAudits: _Optional[_Iterable[_Union[_auth_pb2.UserSecurityAudit, _Mapping]]] = ...) -> None: ...
