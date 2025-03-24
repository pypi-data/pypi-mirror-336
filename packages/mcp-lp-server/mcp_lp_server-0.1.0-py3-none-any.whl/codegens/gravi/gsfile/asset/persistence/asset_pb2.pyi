import gs_options_pb2 as _gs_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AssetModel(_message.Message):
    __slots__ = ("id", "size", "checksum")
    ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    id: str
    size: int
    checksum: str
    def __init__(self, id: _Optional[str] = ..., size: _Optional[int] = ..., checksum: _Optional[str] = ...) -> None: ...
