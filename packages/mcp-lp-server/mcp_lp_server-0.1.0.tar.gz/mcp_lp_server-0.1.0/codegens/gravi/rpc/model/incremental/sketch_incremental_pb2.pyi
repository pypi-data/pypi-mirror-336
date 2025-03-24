from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.extra import sketch_extra_pb2 as _sketch_extra_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IncrementalAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Create: _ClassVar[IncrementalAction]
    Update: _ClassVar[IncrementalAction]
    Delete: _ClassVar[IncrementalAction]
    OverwritePrimitiveData: _ClassVar[IncrementalAction]
    SetMirrored: _ClassVar[IncrementalAction]
Create: IncrementalAction
Update: IncrementalAction
Delete: IncrementalAction
OverwritePrimitiveData: IncrementalAction
SetMirrored: IncrementalAction

class StrokeIncrementalMetaData(_message.Message):
    __slots__ = ("previewSeqID", "confirmSeqID")
    PREVIEWSEQID_FIELD_NUMBER: _ClassVar[int]
    CONFIRMSEQID_FIELD_NUMBER: _ClassVar[int]
    previewSeqID: int
    confirmSeqID: int
    def __init__(self, previewSeqID: _Optional[int] = ..., confirmSeqID: _Optional[int] = ...) -> None: ...

class StrokeIncrementalData(_message.Message):
    __slots__ = ("strokeId", "seqID", "vertexEdits", "incrementalEdits", "previewSeqID", "offsetData", "polarDuplicateCountPlusOne")
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    VERTEXEDITS_FIELD_NUMBER: _ClassVar[int]
    INCREMENTALEDITS_FIELD_NUMBER: _ClassVar[int]
    PREVIEWSEQID_FIELD_NUMBER: _ClassVar[int]
    OFFSETDATA_FIELD_NUMBER: _ClassVar[int]
    POLARDUPLICATECOUNTPLUSONE_FIELD_NUMBER: _ClassVar[int]
    strokeId: _sketch_common_pb2.GSDataID
    seqID: int
    vertexEdits: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.PolygonVertex]
    incrementalEdits: _containers.RepeatedCompositeFieldContainer[IncrementalEdit]
    previewSeqID: int
    offsetData: _sketch_common_pb2.OffsetData
    polarDuplicateCountPlusOne: int
    def __init__(self, strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., seqID: _Optional[int] = ..., vertexEdits: _Optional[_Iterable[_Union[_sketch_common_pb2.PolygonVertex, _Mapping]]] = ..., incrementalEdits: _Optional[_Iterable[_Union[IncrementalEdit, _Mapping]]] = ..., previewSeqID: _Optional[int] = ..., offsetData: _Optional[_Union[_sketch_common_pb2.OffsetData, _Mapping]] = ..., polarDuplicateCountPlusOne: _Optional[int] = ...) -> None: ...

class IncrementalEdit(_message.Message):
    __slots__ = ("action", "polygonVertexID", "polygonID", "polygonVertex", "polygon", "primitiveData", "mirrored", "creasedPolygonEdge")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    POLYGONVERTEXID_FIELD_NUMBER: _ClassVar[int]
    POLYGONID_FIELD_NUMBER: _ClassVar[int]
    POLYGONVERTEX_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVEDATA_FIELD_NUMBER: _ClassVar[int]
    MIRRORED_FIELD_NUMBER: _ClassVar[int]
    CREASEDPOLYGONEDGE_FIELD_NUMBER: _ClassVar[int]
    action: IncrementalAction
    polygonVertexID: _sketch_common_pb2.GSDataID
    polygonID: _sketch_common_pb2.GSDataID
    polygonVertex: _sketch_common_pb2.PolygonVertex
    polygon: _sketch_common_pb2.Polygon
    primitiveData: StrokePrimitiveData
    mirrored: bool
    creasedPolygonEdge: _sketch_common_pb2.CreasedPolygonEdge
    def __init__(self, action: _Optional[_Union[IncrementalAction, str]] = ..., polygonVertexID: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., polygonID: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., polygonVertex: _Optional[_Union[_sketch_common_pb2.PolygonVertex, _Mapping]] = ..., polygon: _Optional[_Union[_sketch_common_pb2.Polygon, _Mapping]] = ..., primitiveData: _Optional[_Union[StrokePrimitiveData, _Mapping]] = ..., mirrored: bool = ..., creasedPolygonEdge: _Optional[_Union[_sketch_common_pb2.CreasedPolygonEdge, _Mapping]] = ...) -> None: ...

class StrokePrimitiveData(_message.Message):
    __slots__ = ("subdivisionExtraData",)
    SUBDIVISIONEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    subdivisionExtraData: _sketch_extra_pb2.SubdivisionObjectExtraDataSnapshot
    def __init__(self, subdivisionExtraData: _Optional[_Union[_sketch_extra_pb2.SubdivisionObjectExtraDataSnapshot, _Mapping]] = ...) -> None: ...
