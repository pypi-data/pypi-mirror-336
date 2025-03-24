import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeUserCollaborationRoleResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ChangeUserCollaborationRoleResponseCode_Unknown: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_Success: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_NoPermission: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_RoomNotFound: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_UserNotFound: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_RoleMustNotBeHigherThanLicenseCap: _ClassVar[ChangeUserCollaborationRoleResponseCode]
    ChangeUserCollaborationRoleResponseCode_RoleMustNotBeHigherThanActorRole: _ClassVar[ChangeUserCollaborationRoleResponseCode]

class AbusiveBehaviourScale(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AbusiveBehaviourScaleUnset: _ClassVar[AbusiveBehaviourScale]
    AbusiveBehaviourScaleLow: _ClassVar[AbusiveBehaviourScale]
    AbusiveBehaviourScaleMedium: _ClassVar[AbusiveBehaviourScale]
    AbusiveBehaviourScaleHigh: _ClassVar[AbusiveBehaviourScale]
ChangeUserCollaborationRoleResponseCode_Unknown: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_Success: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_NoPermission: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_RoomNotFound: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_UserNotFound: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_RoleMustNotBeHigherThanLicenseCap: ChangeUserCollaborationRoleResponseCode
ChangeUserCollaborationRoleResponseCode_RoleMustNotBeHigherThanActorRole: ChangeUserCollaborationRoleResponseCode
AbusiveBehaviourScaleUnset: AbusiveBehaviourScale
AbusiveBehaviourScaleLow: AbusiveBehaviourScale
AbusiveBehaviourScaleMedium: AbusiveBehaviourScale
AbusiveBehaviourScaleHigh: AbusiveBehaviourScale

class ChangeUserCollaborationRoleRequest(_message.Message):
    __slots__ = ("roomId", "userId", "newRole")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    NEWROLE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    userId: str
    newRole: _gravi_model_pb2.CollaborationRole
    def __init__(self, roomId: _Optional[str] = ..., userId: _Optional[str] = ..., newRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class ChangeUserCollaborationRoleResponse(_message.Message):
    __slots__ = ("changeUserCollaborationRoleResponseCode",)
    CHANGEUSERCOLLABORATIONROLERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    changeUserCollaborationRoleResponseCode: ChangeUserCollaborationRoleResponseCode
    def __init__(self, changeUserCollaborationRoleResponseCode: _Optional[_Union[ChangeUserCollaborationRoleResponseCode, str]] = ...) -> None: ...

class ReportAbusiveBehaviourRequest(_message.Message):
    __slots__ = ("scale", "roomId", "roomSessionId", "abuserUserId", "description", "image")
    SCALE_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMSESSIONID_FIELD_NUMBER: _ClassVar[int]
    ABUSERUSERID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    scale: AbusiveBehaviourScale
    roomId: str
    roomSessionId: str
    abuserUserId: str
    description: str
    image: str
    def __init__(self, scale: _Optional[_Union[AbusiveBehaviourScale, str]] = ..., roomId: _Optional[str] = ..., roomSessionId: _Optional[str] = ..., abuserUserId: _Optional[str] = ..., description: _Optional[str] = ..., image: _Optional[str] = ...) -> None: ...

class ReportAbusiveBehaviourResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
