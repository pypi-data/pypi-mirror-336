from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.gsfile import sketch_gsfile_pb2 as _sketch_gsfile_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeprecatedStrokeActionData(_message.Message):
    __slots__ = ("inUseByClientId", "seqId", "eventID", "action", "strokeData", "LayerGuid", "RevisionId", "fullData", "lastModifiedByClientId", "cachedMaterialHistory")
    INUSEBYCLIENTID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    STROKEDATA_FIELD_NUMBER: _ClassVar[int]
    LAYERGUID_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    FULLDATA_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIEDBYCLIENTID_FIELD_NUMBER: _ClassVar[int]
    CACHEDMATERIALHISTORY_FIELD_NUMBER: _ClassVar[int]
    inUseByClientId: int
    seqId: int
    eventID: str
    action: _sketch_model_pb2.SplineAction
    strokeData: _sketch_gsfile_pb2.GSFileStrokeData
    LayerGuid: str
    RevisionId: int
    fullData: bool
    lastModifiedByClientId: int
    cachedMaterialHistory: _sketch_common_pb2.DrawMaterial
    def __init__(self, inUseByClientId: _Optional[int] = ..., seqId: _Optional[int] = ..., eventID: _Optional[str] = ..., action: _Optional[_Union[_sketch_model_pb2.SplineAction, str]] = ..., strokeData: _Optional[_Union[_sketch_gsfile_pb2.GSFileStrokeData, _Mapping]] = ..., LayerGuid: _Optional[str] = ..., RevisionId: _Optional[int] = ..., fullData: bool = ..., lastModifiedByClientId: _Optional[int] = ..., cachedMaterialHistory: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...
