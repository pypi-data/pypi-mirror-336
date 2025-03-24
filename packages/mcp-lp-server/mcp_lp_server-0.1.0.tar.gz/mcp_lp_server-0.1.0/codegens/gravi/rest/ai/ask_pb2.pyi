import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AskShrekRequest(_message.Message):
    __slots__ = ("text", "voice")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    text: str
    voice: VoiceQuestion
    def __init__(self, text: _Optional[str] = ..., voice: _Optional[_Union[VoiceQuestion, _Mapping]] = ...) -> None: ...

class VoiceQuestion(_message.Message):
    __slots__ = ("voice",)
    VOICE_FIELD_NUMBER: _ClassVar[int]
    voice: bytes
    def __init__(self, voice: _Optional[bytes] = ...) -> None: ...

class AskShrekResponse(_message.Message):
    __slots__ = ("quotes", "question")
    QUOTES_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    quotes: _containers.RepeatedCompositeFieldContainer[ShrekQuote]
    question: str
    def __init__(self, quotes: _Optional[_Iterable[_Union[ShrekQuote, _Mapping]]] = ..., question: _Optional[str] = ...) -> None: ...

class ShrekQuote(_message.Message):
    __slots__ = ("video", "summary")
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    video: ShrekQuoteVideo
    summary: ShrekQuoteGeneratedSummary
    def __init__(self, video: _Optional[_Union[ShrekQuoteVideo, _Mapping]] = ..., summary: _Optional[_Union[ShrekQuoteGeneratedSummary, _Mapping]] = ...) -> None: ...

class ShrekQuoteVideo(_message.Message):
    __slots__ = ("signedUrl", "startingPosition", "chunkHint")
    SIGNEDURL_FIELD_NUMBER: _ClassVar[int]
    STARTINGPOSITION_FIELD_NUMBER: _ClassVar[int]
    CHUNKHINT_FIELD_NUMBER: _ClassVar[int]
    signedUrl: str
    startingPosition: float
    chunkHint: str
    def __init__(self, signedUrl: _Optional[str] = ..., startingPosition: _Optional[float] = ..., chunkHint: _Optional[str] = ...) -> None: ...

class ShrekQuoteGeneratedSummary(_message.Message):
    __slots__ = ("summary",)
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    summary: str
    def __init__(self, summary: _Optional[str] = ...) -> None: ...
