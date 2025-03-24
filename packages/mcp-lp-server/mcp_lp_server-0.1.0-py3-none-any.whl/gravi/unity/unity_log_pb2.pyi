import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UnityLog(_message.Message):
    __slots__ = ("logLevel", "counter", "message", "sessionId", "timestamp", "versionMajor", "versionMinor", "versionHotfix", "versionLetter", "gsid", "unityUserId", "orgId", "roomId", "requestId", "roomClientId", "maxMemory", "maxTexture", "stackTrace", "className", "err", "level")
    LOGLEVEL_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONHOTFIX_FIELD_NUMBER: _ClassVar[int]
    VERSIONLETTER_FIELD_NUMBER: _ClassVar[int]
    GSID_FIELD_NUMBER: _ClassVar[int]
    UNITYUSERID_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    ROOMCLIENTID_FIELD_NUMBER: _ClassVar[int]
    MAXMEMORY_FIELD_NUMBER: _ClassVar[int]
    MAXTEXTURE_FIELD_NUMBER: _ClassVar[int]
    STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    ERR_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    logLevel: int
    counter: int
    message: str
    sessionId: str
    timestamp: int
    versionMajor: int
    versionMinor: int
    versionHotfix: int
    versionLetter: str
    gsid: str
    unityUserId: str
    orgId: str
    roomId: str
    requestId: str
    roomClientId: int
    maxMemory: float
    maxTexture: float
    stackTrace: str
    className: str
    err: str
    level: str
    def __init__(self, logLevel: _Optional[int] = ..., counter: _Optional[int] = ..., message: _Optional[str] = ..., sessionId: _Optional[str] = ..., timestamp: _Optional[int] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., versionHotfix: _Optional[int] = ..., versionLetter: _Optional[str] = ..., gsid: _Optional[str] = ..., unityUserId: _Optional[str] = ..., orgId: _Optional[str] = ..., roomId: _Optional[str] = ..., requestId: _Optional[str] = ..., roomClientId: _Optional[int] = ..., maxMemory: _Optional[float] = ..., maxTexture: _Optional[float] = ..., stackTrace: _Optional[str] = ..., className: _Optional[str] = ..., err: _Optional[str] = ..., level: _Optional[str] = ...) -> None: ...

class BatchedUnityLogs(_message.Message):
    __slots__ = ("logs", "pingTest")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    PINGTEST_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[UnityLog]
    pingTest: bool
    def __init__(self, logs: _Optional[_Iterable[_Union[UnityLog, _Mapping]]] = ..., pingTest: bool = ...) -> None: ...
