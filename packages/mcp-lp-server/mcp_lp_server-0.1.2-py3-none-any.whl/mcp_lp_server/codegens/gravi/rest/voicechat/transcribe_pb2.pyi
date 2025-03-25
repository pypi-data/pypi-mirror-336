from gravi.rest.common import async_pb2 as _async_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TranscribeRequest(_message.Message):
    __slots__ = ("pendingAsyncJob", "voiceTranscribeRequest")
    PENDINGASYNCJOB_FIELD_NUMBER: _ClassVar[int]
    VOICETRANSCRIBEREQUEST_FIELD_NUMBER: _ClassVar[int]
    pendingAsyncJob: _async_pb2.AsyncJob
    voiceTranscribeRequest: TranscribeRequestPayload
    def __init__(self, pendingAsyncJob: _Optional[_Union[_async_pb2.AsyncJob, _Mapping]] = ..., voiceTranscribeRequest: _Optional[_Union[TranscribeRequestPayload, _Mapping]] = ...) -> None: ...

class TranscribeRequestPayload(_message.Message):
    __slots__ = ("audio",)
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    audio: bytes
    def __init__(self, audio: _Optional[bytes] = ...) -> None: ...

class TranscribeResponse(_message.Message):
    __slots__ = ("pendingAsyncJob", "transcribeResult")
    PENDINGASYNCJOB_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIBERESULT_FIELD_NUMBER: _ClassVar[int]
    pendingAsyncJob: _async_pb2.AsyncJob
    transcribeResult: TranscribeResponsePayload
    def __init__(self, pendingAsyncJob: _Optional[_Union[_async_pb2.AsyncJob, _Mapping]] = ..., transcribeResult: _Optional[_Union[TranscribeResponsePayload, _Mapping]] = ...) -> None: ...

class TranscribeResponsePayload(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
