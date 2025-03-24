import gs_options_pb2 as _gs_options_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LayerModel(_message.Message):
    __slots__ = ("guid", "layerName", "baseVisibility", "locked", "ownerClientId", "localOrder", "layerHidden")
    GUID_FIELD_NUMBER: _ClassVar[int]
    LAYERNAME_FIELD_NUMBER: _ClassVar[int]
    BASEVISIBILITY_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    OWNERCLIENTID_FIELD_NUMBER: _ClassVar[int]
    LOCALORDER_FIELD_NUMBER: _ClassVar[int]
    LAYERHIDDEN_FIELD_NUMBER: _ClassVar[int]
    guid: str
    layerName: str
    baseVisibility: float
    locked: bool
    ownerClientId: int
    localOrder: float
    layerHidden: bool
    def __init__(self, guid: _Optional[str] = ..., layerName: _Optional[str] = ..., baseVisibility: _Optional[float] = ..., locked: bool = ..., ownerClientId: _Optional[int] = ..., localOrder: _Optional[float] = ..., layerHidden: bool = ...) -> None: ...
