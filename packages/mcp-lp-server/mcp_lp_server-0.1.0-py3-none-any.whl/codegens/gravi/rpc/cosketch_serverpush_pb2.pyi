from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerPushType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownPush: _ClassVar[ServerPushType]
    ReplaceStrokePush: _ClassVar[ServerPushType]
    RemoveStrokePush: _ClassVar[ServerPushType]
    UnlockLayerDeletion: _ClassVar[ServerPushType]
    JoinerRequestPermission: _ClassVar[ServerPushType]
    RoomShutdownInitiated: _ClassVar[ServerPushType]
    RoomShutdownCancelled: _ClassVar[ServerPushType]
UnknownPush: ServerPushType
ReplaceStrokePush: ServerPushType
RemoveStrokePush: ServerPushType
UnlockLayerDeletion: ServerPushType
JoinerRequestPermission: ServerPushType
RoomShutdownInitiated: ServerPushType
RoomShutdownCancelled: ServerPushType

class ServerPushBroadcast(_message.Message):
    __slots__ = ("pushType", "replaceStrokeBroadcast", "removeStrokeBroadcast", "unlockLayerDeletionBroadcast", "joinerRequestPermissionBroadcast")
    PUSHTYPE_FIELD_NUMBER: _ClassVar[int]
    REPLACESTROKEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    REMOVESTROKEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    UNLOCKLAYERDELETIONBROADCAST_FIELD_NUMBER: _ClassVar[int]
    JOINERREQUESTPERMISSIONBROADCAST_FIELD_NUMBER: _ClassVar[int]
    pushType: ServerPushType
    replaceStrokeBroadcast: ReplaceStrokeBroadcast
    removeStrokeBroadcast: RemoveStrokeBroadcast
    unlockLayerDeletionBroadcast: UnlockLayerDeletionBroadcast
    joinerRequestPermissionBroadcast: JoinerRequestPermissionBroadcast
    def __init__(self, pushType: _Optional[_Union[ServerPushType, str]] = ..., replaceStrokeBroadcast: _Optional[_Union[ReplaceStrokeBroadcast, _Mapping]] = ..., removeStrokeBroadcast: _Optional[_Union[RemoveStrokeBroadcast, _Mapping]] = ..., unlockLayerDeletionBroadcast: _Optional[_Union[UnlockLayerDeletionBroadcast, _Mapping]] = ..., joinerRequestPermissionBroadcast: _Optional[_Union[JoinerRequestPermissionBroadcast, _Mapping]] = ...) -> None: ...

class ReplaceStrokeBroadcast(_message.Message):
    __slots__ = ("actionData",)
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    actionData: _sketch_model_pb2.StrokeActionData
    def __init__(self, actionData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ...) -> None: ...

class RemoveStrokeBroadcast(_message.Message):
    __slots__ = ("strokeId",)
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    strokeId: _sketch_common_pb2.GSDataID
    def __init__(self, strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class UnlockLayerDeletionBroadcast(_message.Message):
    __slots__ = ("layerId",)
    LAYERID_FIELD_NUMBER: _ClassVar[int]
    layerId: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, layerId: _Optional[_Iterable[str]] = ...) -> None: ...

class JoinerRequestPermissionBroadcast(_message.Message):
    __slots__ = ("userName", "clientId")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    userName: str
    clientId: int
    def __init__(self, userName: _Optional[str] = ..., clientId: _Optional[int] = ...) -> None: ...
