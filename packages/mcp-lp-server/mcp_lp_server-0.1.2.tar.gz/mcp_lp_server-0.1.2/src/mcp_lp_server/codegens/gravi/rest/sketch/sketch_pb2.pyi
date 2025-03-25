import gs_options_pb2 as _gs_options_pb2
from gravi.rest.model import online_sketch_pb2 as _online_sketch_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from gravi.rpc import cosketch_rpc_pb2 as _cosketch_rpc_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Int128Id(_message.Message):
    __slots__ = ("high", "low")
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    high: int
    low: int
    def __init__(self, high: _Optional[int] = ..., low: _Optional[int] = ...) -> None: ...

class ClientSentMessage(_message.Message):
    __slots__ = ("joinSketch", "heartbeat", "clientStateChange", "sketchStateChange")
    JOINSKETCH_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    CLIENTSTATECHANGE_FIELD_NUMBER: _ClassVar[int]
    SKETCHSTATECHANGE_FIELD_NUMBER: _ClassVar[int]
    joinSketch: JoinSketchPayload
    heartbeat: HeartbeatPayload
    clientStateChange: OneClientStateChangePayload
    sketchStateChange: SketchStateChangePayload
    def __init__(self, joinSketch: _Optional[_Union[JoinSketchPayload, _Mapping]] = ..., heartbeat: _Optional[_Union[HeartbeatPayload, _Mapping]] = ..., clientStateChange: _Optional[_Union[OneClientStateChangePayload, _Mapping]] = ..., sketchStateChange: _Optional[_Union[SketchStateChangePayload, _Mapping]] = ...) -> None: ...

class JoinSketchPayload(_message.Message):
    __slots__ = ("token", "docId", "clientId", "startingRevisionId", "sourceApp")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    STARTINGREVISIONID_FIELD_NUMBER: _ClassVar[int]
    SOURCEAPP_FIELD_NUMBER: _ClassVar[int]
    token: str
    docId: str
    clientId: int
    startingRevisionId: Int128Id
    sourceApp: _gravi_model_pb2.SourceApp
    def __init__(self, token: _Optional[str] = ..., docId: _Optional[str] = ..., clientId: _Optional[int] = ..., startingRevisionId: _Optional[_Union[Int128Id, _Mapping]] = ..., sourceApp: _Optional[_Union[_gravi_model_pb2.SourceApp, str]] = ...) -> None: ...

class HeartbeatPayload(_message.Message):
    __slots__ = ("isAck",)
    ISACK_FIELD_NUMBER: _ClassVar[int]
    isAck: bool
    def __init__(self, isAck: bool = ...) -> None: ...

class ManyClientStateChangesPayload(_message.Message):
    __slots__ = ("revisionId", "changes")
    class ChangesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: OneClientStateChangePayload
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[OneClientStateChangePayload, _Mapping]] = ...) -> None: ...
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    revisionId: Int128Id
    changes: _containers.MessageMap[int, OneClientStateChangePayload]
    def __init__(self, revisionId: _Optional[_Union[Int128Id, _Mapping]] = ..., changes: _Optional[_Mapping[int, OneClientStateChangePayload]] = ...) -> None: ...

class OneClientStateChangePayload(_message.Message):
    __slots__ = ("overwrites",)
    OVERWRITES_FIELD_NUMBER: _ClassVar[int]
    overwrites: ClientStateObjectOverwrites
    def __init__(self, overwrites: _Optional[_Union[ClientStateObjectOverwrites, _Mapping]] = ...) -> None: ...

class ClientStateObjectOverwrites(_message.Message):
    __slots__ = ("overwrites",)
    OVERWRITES_FIELD_NUMBER: _ClassVar[int]
    overwrites: _containers.RepeatedCompositeFieldContainer[ClientStateObjectOverwrite]
    def __init__(self, overwrites: _Optional[_Iterable[_Union[ClientStateObjectOverwrite, _Mapping]]] = ...) -> None: ...

class ClientStateObjectOverwrite(_message.Message):
    __slots__ = ("transform", "uiState", "userState", "preference")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    UISTATE_FIELD_NUMBER: _ClassVar[int]
    USERSTATE_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    transform: _cosketch_rpc_pb2.SyncTransformBroadcast
    uiState: _cosketch_rpc_pb2.SyncUIBroadcast
    userState: _cosketch_rpc_pb2.UserStateBroadcast
    preference: _cosketch_rpc_pb2.SyncUserPreferencesBroadcast
    def __init__(self, transform: _Optional[_Union[_cosketch_rpc_pb2.SyncTransformBroadcast, _Mapping]] = ..., uiState: _Optional[_Union[_cosketch_rpc_pb2.SyncUIBroadcast, _Mapping]] = ..., userState: _Optional[_Union[_cosketch_rpc_pb2.UserStateBroadcast, _Mapping]] = ..., preference: _Optional[_Union[_cosketch_rpc_pb2.SyncUserPreferencesBroadcast, _Mapping]] = ...) -> None: ...

class SketchStateChangePayload(_message.Message):
    __slots__ = ("revisionId", "changes")
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    revisionId: Int128Id
    changes: _containers.RepeatedCompositeFieldContainer[_online_sketch_pb2.SketchObjectUpdate]
    def __init__(self, revisionId: _Optional[_Union[Int128Id, _Mapping]] = ..., changes: _Optional[_Iterable[_Union[_online_sketch_pb2.SketchObjectUpdate, _Mapping]]] = ...) -> None: ...

class ServerSentMessage(_message.Message):
    __slots__ = ("ingestedAt", "ingestedFromBridge", "heartbeat", "clientStateChange", "sketchStateChange")
    INGESTEDAT_FIELD_NUMBER: _ClassVar[int]
    INGESTEDFROMBRIDGE_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    CLIENTSTATECHANGE_FIELD_NUMBER: _ClassVar[int]
    SKETCHSTATECHANGE_FIELD_NUMBER: _ClassVar[int]
    ingestedAt: int
    ingestedFromBridge: bool
    heartbeat: HeartbeatPayload
    clientStateChange: ManyClientStateChangesPayload
    sketchStateChange: SketchStateChangePayload
    def __init__(self, ingestedAt: _Optional[int] = ..., ingestedFromBridge: bool = ..., heartbeat: _Optional[_Union[HeartbeatPayload, _Mapping]] = ..., clientStateChange: _Optional[_Union[ManyClientStateChangesPayload, _Mapping]] = ..., sketchStateChange: _Optional[_Union[SketchStateChangePayload, _Mapping]] = ...) -> None: ...
