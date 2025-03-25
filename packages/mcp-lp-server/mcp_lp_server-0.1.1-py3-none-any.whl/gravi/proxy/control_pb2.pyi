import gs_options_pb2 as _gs_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlFrame(_message.Message):
    __slots__ = ("establishTargetRequest", "connectionId", "pingTest")
    ESTABLISHTARGETREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONID_FIELD_NUMBER: _ClassVar[int]
    PINGTEST_FIELD_NUMBER: _ClassVar[int]
    establishTargetRequest: ControlFrameEstablishTargetRequest
    connectionId: str
    pingTest: bool
    def __init__(self, establishTargetRequest: _Optional[_Union[ControlFrameEstablishTargetRequest, _Mapping]] = ..., connectionId: _Optional[str] = ..., pingTest: bool = ...) -> None: ...

class ControlFrameEstablishTargetRequest(_message.Message):
    __slots__ = ("targetDNSAddress",)
    TARGETDNSADDRESS_FIELD_NUMBER: _ClassVar[int]
    targetDNSAddress: str
    def __init__(self, targetDNSAddress: _Optional[str] = ...) -> None: ...
