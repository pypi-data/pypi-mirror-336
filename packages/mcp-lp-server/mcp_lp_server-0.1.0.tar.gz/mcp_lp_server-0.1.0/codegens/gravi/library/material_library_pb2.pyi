from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaterialLibraryEntry(_message.Message):
    __slots__ = ("materials", "name")
    MATERIALS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    materials: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    name: str
    def __init__(self, materials: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., name: _Optional[str] = ...) -> None: ...
