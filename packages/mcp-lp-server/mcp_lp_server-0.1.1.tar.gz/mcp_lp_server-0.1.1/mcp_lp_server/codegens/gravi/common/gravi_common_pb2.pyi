import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Os(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OS_UNKNOWN: _ClassVar[Os]
    IOS: _ClassVar[Os]
    ANDROID: _ClassVar[Os]
    WINDOWS: _ClassVar[Os]
    MAC: _ClassVar[Os]
    LINUX: _ClassVar[Os]
    QUEST: _ClassVar[Os]
    PICO: _ClassVar[Os]
    WAVE: _ClassVar[Os]

class Arch(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARCH_UNKNOWN: _ClassVar[Arch]
    X86: _ClassVar[Arch]
    X64: _ClassVar[Arch]
    ARM: _ClassVar[Arch]
    ARM64: _ClassVar[Arch]
    MAC_UNIVERSAL: _ClassVar[Arch]
OS_UNKNOWN: Os
IOS: Os
ANDROID: Os
WINDOWS: Os
MAC: Os
LINUX: Os
QUEST: Os
PICO: Os
WAVE: Os
ARCH_UNKNOWN: Arch
X86: Arch
X64: Arch
ARM: Arch
ARM64: Arch
MAC_UNIVERSAL: Arch

class HostTO(_message.Message):
    __slots__ = ("host", "port")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
