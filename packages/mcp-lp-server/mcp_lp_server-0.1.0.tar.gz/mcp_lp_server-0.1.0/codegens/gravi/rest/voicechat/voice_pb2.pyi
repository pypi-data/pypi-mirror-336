from gravi.models import gravi_model_pb2 as _gravi_model_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientSentMessage(_message.Message):
    __slots__ = ("joinChat", "voice", "heartbeat")
    JOINCHAT_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    joinChat: JoinChatPayload
    voice: VoicePayload
    heartbeat: HeartbeatPayload
    def __init__(self, joinChat: _Optional[_Union[JoinChatPayload, _Mapping]] = ..., voice: _Optional[_Union[VoicePayload, _Mapping]] = ..., heartbeat: _Optional[_Union[HeartbeatPayload, _Mapping]] = ...) -> None: ...

class ServerSentMessage(_message.Message):
    __slots__ = ("fromId", "ingestedAt", "ingestedFromBridge", "voice", "heartbeat", "allClientsInChat")
    FROMID_FIELD_NUMBER: _ClassVar[int]
    INGESTEDAT_FIELD_NUMBER: _ClassVar[int]
    INGESTEDFROMBRIDGE_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    ALLCLIENTSINCHAT_FIELD_NUMBER: _ClassVar[int]
    fromId: int
    ingestedAt: int
    ingestedFromBridge: bool
    voice: VoicePayload
    heartbeat: HeartbeatPayload
    allClientsInChat: AllClientsInChatPayload
    def __init__(self, fromId: _Optional[int] = ..., ingestedAt: _Optional[int] = ..., ingestedFromBridge: bool = ..., voice: _Optional[_Union[VoicePayload, _Mapping]] = ..., heartbeat: _Optional[_Union[HeartbeatPayload, _Mapping]] = ..., allClientsInChat: _Optional[_Union[AllClientsInChatPayload, _Mapping]] = ...) -> None: ...

class JoinChatPayload(_message.Message):
    __slots__ = ("clientId", "chatId", "sourceApp", "sToken")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    CHATID_FIELD_NUMBER: _ClassVar[int]
    SOURCEAPP_FIELD_NUMBER: _ClassVar[int]
    STOKEN_FIELD_NUMBER: _ClassVar[int]
    clientId: int
    chatId: ChatId
    sourceApp: _gravi_model_pb2.SourceApp
    sToken: str
    def __init__(self, clientId: _Optional[int] = ..., chatId: _Optional[_Union[ChatId, _Mapping]] = ..., sourceApp: _Optional[_Union[_gravi_model_pb2.SourceApp, str]] = ..., sToken: _Optional[str] = ...) -> None: ...

class ChatId(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class VoicePayload(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class HeartbeatPayload(_message.Message):
    __slots__ = ("isAck",)
    ISACK_FIELD_NUMBER: _ClassVar[int]
    isAck: bool
    def __init__(self, isAck: bool = ...) -> None: ...

class AllClientsInChatPayload(_message.Message):
    __slots__ = ("clientIds",)
    CLIENTIDS_FIELD_NUMBER: _ClassVar[int]
    clientIds: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, clientIds: _Optional[_Iterable[int]] = ...) -> None: ...

class ServerInitiatedDisconnectionInfo(_message.Message):
    __slots__ = ("isRetryable",)
    ISRETRYABLE_FIELD_NUMBER: _ClassVar[int]
    isRetryable: bool
    def __init__(self, isRetryable: bool = ...) -> None: ...
