from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VideoExtraDataSnapshot(_message.Message):
    __slots__ = ("VideoGuid", "Loop", "audioEnabled", "originalName", "fileSize", "playbackEnabled", "autoplayEnabled", "showUI", "utcTimeAtLastSeek", "lastRecordedSeekTime", "volumePercentage", "playbackSpeed", "enableAudioOnAutoPlay", "videoSource", "publicContentVideoSourceFilePath")
    VIDEOGUID_FIELD_NUMBER: _ClassVar[int]
    LOOP_FIELD_NUMBER: _ClassVar[int]
    AUDIOENABLED_FIELD_NUMBER: _ClassVar[int]
    ORIGINALNAME_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    PLAYBACKENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTOPLAYENABLED_FIELD_NUMBER: _ClassVar[int]
    SHOWUI_FIELD_NUMBER: _ClassVar[int]
    UTCTIMEATLASTSEEK_FIELD_NUMBER: _ClassVar[int]
    LASTRECORDEDSEEKTIME_FIELD_NUMBER: _ClassVar[int]
    VOLUMEPERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    PLAYBACKSPEED_FIELD_NUMBER: _ClassVar[int]
    ENABLEAUDIOONAUTOPLAY_FIELD_NUMBER: _ClassVar[int]
    VIDEOSOURCE_FIELD_NUMBER: _ClassVar[int]
    PUBLICCONTENTVIDEOSOURCEFILEPATH_FIELD_NUMBER: _ClassVar[int]
    VideoGuid: str
    Loop: _sketch_common_pb2.VideoLoopState
    audioEnabled: bool
    originalName: str
    fileSize: int
    playbackEnabled: bool
    autoplayEnabled: _sketch_common_pb2.VideoAutoPlayState
    showUI: bool
    utcTimeAtLastSeek: int
    lastRecordedSeekTime: float
    volumePercentage: float
    playbackSpeed: float
    enableAudioOnAutoPlay: bool
    videoSource: _sketch_common_pb2.VideoSource
    publicContentVideoSourceFilePath: str
    def __init__(self, VideoGuid: _Optional[str] = ..., Loop: _Optional[_Union[_sketch_common_pb2.VideoLoopState, str]] = ..., audioEnabled: bool = ..., originalName: _Optional[str] = ..., fileSize: _Optional[int] = ..., playbackEnabled: bool = ..., autoplayEnabled: _Optional[_Union[_sketch_common_pb2.VideoAutoPlayState, str]] = ..., showUI: bool = ..., utcTimeAtLastSeek: _Optional[int] = ..., lastRecordedSeekTime: _Optional[float] = ..., volumePercentage: _Optional[float] = ..., playbackSpeed: _Optional[float] = ..., enableAudioOnAutoPlay: bool = ..., videoSource: _Optional[_Union[_sketch_common_pb2.VideoSource, str]] = ..., publicContentVideoSourceFilePath: _Optional[str] = ...) -> None: ...

class RevolveExtraDataSnapshot(_message.Message):
    __slots__ = ("StartSnap", "EndSnap", "Left", "Right", "Closed", "Loop", "Thickness", "rotationalSymmetryData", "LowPoly")
    STARTSNAP_FIELD_NUMBER: _ClassVar[int]
    ENDSNAP_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    LOOP_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ROTATIONALSYMMETRYDATA_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    StartSnap: bool
    EndSnap: bool
    Left: bool
    Right: bool
    Closed: bool
    Loop: bool
    Thickness: float
    rotationalSymmetryData: _sketch_common_pb2.RotationalSymmetryData
    LowPoly: bool
    def __init__(self, StartSnap: bool = ..., EndSnap: bool = ..., Left: bool = ..., Right: bool = ..., Closed: bool = ..., Loop: bool = ..., Thickness: _Optional[float] = ..., rotationalSymmetryData: _Optional[_Union[_sketch_common_pb2.RotationalSymmetryData, _Mapping]] = ..., LowPoly: bool = ...) -> None: ...

class StrokeExtraDataSnapshot(_message.Message):
    __slots__ = ("UsePressure", "BrushX", "BrushY", "Closed", "Shape", "capType", "Planar", "DrawnPlanar", "Projected", "CustomNormals", "LowPoly", "RepeatingUVs", "antiCoplanarityOffset")
    USEPRESSURE_FIELD_NUMBER: _ClassVar[int]
    BRUSHX_FIELD_NUMBER: _ClassVar[int]
    BRUSHY_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    CAPTYPE_FIELD_NUMBER: _ClassVar[int]
    PLANAR_FIELD_NUMBER: _ClassVar[int]
    DRAWNPLANAR_FIELD_NUMBER: _ClassVar[int]
    PROJECTED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMNORMALS_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    REPEATINGUVS_FIELD_NUMBER: _ClassVar[int]
    ANTICOPLANARITYOFFSET_FIELD_NUMBER: _ClassVar[int]
    UsePressure: bool
    BrushX: float
    BrushY: float
    Closed: bool
    Shape: _sketch_common_pb2.BrushShape
    capType: _sketch_common_pb2.StrokeCapType
    Planar: bool
    DrawnPlanar: bool
    Projected: bool
    CustomNormals: bool
    LowPoly: bool
    RepeatingUVs: bool
    antiCoplanarityOffset: int
    def __init__(self, UsePressure: bool = ..., BrushX: _Optional[float] = ..., BrushY: _Optional[float] = ..., Closed: bool = ..., Shape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., capType: _Optional[_Union[_sketch_common_pb2.StrokeCapType, str]] = ..., Planar: bool = ..., DrawnPlanar: bool = ..., Projected: bool = ..., CustomNormals: bool = ..., LowPoly: bool = ..., RepeatingUVs: bool = ..., antiCoplanarityOffset: _Optional[int] = ...) -> None: ...

class GenericNURBSCurveExtraDataSnapshot(_message.Message):
    __slots__ = ("KnotVector",)
    KNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    KnotVector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, KnotVector: _Optional[_Iterable[float]] = ...) -> None: ...

class SplineCurvedSurfaceExtraDataSnapshot(_message.Message):
    __slots__ = ("ClosedU", "ClosedV")
    CLOSEDU_FIELD_NUMBER: _ClassVar[int]
    CLOSEDV_FIELD_NUMBER: _ClassVar[int]
    ClosedU: bool
    ClosedV: bool
    def __init__(self, ClosedU: bool = ..., ClosedV: bool = ...) -> None: ...

class SplineNURBSSurfaceExtraDataSnapshot(_message.Message):
    __slots__ = ("ClosedU", "ClosedV", "LowPoly", "SecondKnotVector", "SecondDegree", "IsImportedIGESPatch")
    CLOSEDU_FIELD_NUMBER: _ClassVar[int]
    CLOSEDV_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    SECONDKNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    SECONDDEGREE_FIELD_NUMBER: _ClassVar[int]
    ISIMPORTEDIGESPATCH_FIELD_NUMBER: _ClassVar[int]
    ClosedU: bool
    ClosedV: bool
    LowPoly: bool
    SecondKnotVector: _containers.RepeatedScalarFieldContainer[float]
    SecondDegree: int
    IsImportedIGESPatch: bool
    def __init__(self, ClosedU: bool = ..., ClosedV: bool = ..., LowPoly: bool = ..., SecondKnotVector: _Optional[_Iterable[float]] = ..., SecondDegree: _Optional[int] = ..., IsImportedIGESPatch: bool = ...) -> None: ...

class GenericNURBSSurfaceExtraDataSnapshot(_message.Message):
    __slots__ = ("UKnotVector", "VKnotVector")
    UKNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    VKNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    UKnotVector: _containers.RepeatedScalarFieldContainer[float]
    VKnotVector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, UKnotVector: _Optional[_Iterable[float]] = ..., VKnotVector: _Optional[_Iterable[float]] = ...) -> None: ...

class TrimmedNURBSSurfaceExtraDataSnapshot(_message.Message):
    __slots__ = ("SurfaceData", "TrimmingCurvesData", "TrimmingCurvesLength")
    SURFACEDATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMINGCURVESDATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMINGCURVESLENGTH_FIELD_NUMBER: _ClassVar[int]
    SurfaceData: GenericNURBSSurfaceExtraDataSnapshot
    TrimmingCurvesData: _containers.RepeatedCompositeFieldContainer[GenericNURBSCurveExtraDataSnapshot]
    TrimmingCurvesLength: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, SurfaceData: _Optional[_Union[GenericNURBSSurfaceExtraDataSnapshot, _Mapping]] = ..., TrimmingCurvesData: _Optional[_Iterable[_Union[GenericNURBSCurveExtraDataSnapshot, _Mapping]]] = ..., TrimmingCurvesLength: _Optional[_Iterable[int]] = ...) -> None: ...

class RiggedModelExtraDataSnapshot(_message.Message):
    __slots__ = ("ModelID",)
    MODELID_FIELD_NUMBER: _ClassVar[int]
    ModelID: int
    def __init__(self, ModelID: _Optional[int] = ...) -> None: ...

class TextSketchObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("Text", "fontName", "isVertical", "majorAlignment", "minorAlignment")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FONTNAME_FIELD_NUMBER: _ClassVar[int]
    ISVERTICAL_FIELD_NUMBER: _ClassVar[int]
    MAJORALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    MINORALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    Text: str
    fontName: str
    isVertical: bool
    majorAlignment: _sketch_common_pb2.TextAlignment
    minorAlignment: _sketch_common_pb2.TextAlignment
    def __init__(self, Text: _Optional[str] = ..., fontName: _Optional[str] = ..., isVertical: bool = ..., majorAlignment: _Optional[_Union[_sketch_common_pb2.TextAlignment, str]] = ..., minorAlignment: _Optional[_Union[_sketch_common_pb2.TextAlignment, str]] = ...) -> None: ...

class AnnotationSketchObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("text", "author", "commentParentId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    COMMENTPARENTID_FIELD_NUMBER: _ClassVar[int]
    text: str
    author: str
    commentParentId: str
    def __init__(self, text: _Optional[str] = ..., author: _Optional[str] = ..., commentParentId: _Optional[str] = ...) -> None: ...

class PrimitiveShapeExtraDataSnapshot(_message.Message):
    __slots__ = ("shape", "depthSegmentTessellationParameter", "heightSegmentTessellationParameter", "widthSegmentTessellationParameter", "roundnessTessellationParameter", "filletTessellationParameter")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DEPTHSEGMENTTESSELLATIONPARAMETER_FIELD_NUMBER: _ClassVar[int]
    HEIGHTSEGMENTTESSELLATIONPARAMETER_FIELD_NUMBER: _ClassVar[int]
    WIDTHSEGMENTTESSELLATIONPARAMETER_FIELD_NUMBER: _ClassVar[int]
    ROUNDNESSTESSELLATIONPARAMETER_FIELD_NUMBER: _ClassVar[int]
    FILLETTESSELLATIONPARAMETER_FIELD_NUMBER: _ClassVar[int]
    shape: _sketch_common_pb2.BrushShape
    depthSegmentTessellationParameter: int
    heightSegmentTessellationParameter: int
    widthSegmentTessellationParameter: int
    roundnessTessellationParameter: float
    filletTessellationParameter: float
    def __init__(self, shape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., depthSegmentTessellationParameter: _Optional[int] = ..., heightSegmentTessellationParameter: _Optional[int] = ..., widthSegmentTessellationParameter: _Optional[int] = ..., roundnessTessellationParameter: _Optional[float] = ..., filletTessellationParameter: _Optional[float] = ...) -> None: ...

class ReferenceImageExtraDataSnapshot(_message.Message):
    __slots__ = ("deprecatedAnchor",)
    DEPRECATEDANCHOR_FIELD_NUMBER: _ClassVar[int]
    deprecatedAnchor: bool
    def __init__(self, deprecatedAnchor: bool = ...) -> None: ...

class MeshContentExtraDataSnapshot(_message.Message):
    __slots__ = ("deprecatedMeshGuid", "meshLodCollection", "deprecatedObjMeshName", "deprecatedFileSize", "BoundsCenterX", "BoundsCenterY", "BoundsCenterZ", "BoundsSizeX", "BoundsSizeY", "BoundsSizeZ", "levelOfDetail")
    DEPRECATEDMESHGUID_FIELD_NUMBER: _ClassVar[int]
    MESHLODCOLLECTION_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDOBJMESHNAME_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDFILESIZE_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERX_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERY_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERZ_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEX_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEY_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEZ_FIELD_NUMBER: _ClassVar[int]
    LEVELOFDETAIL_FIELD_NUMBER: _ClassVar[int]
    deprecatedMeshGuid: str
    meshLodCollection: _sketch_common_pb2.MeshLODCollection
    deprecatedObjMeshName: str
    deprecatedFileSize: int
    BoundsCenterX: float
    BoundsCenterY: float
    BoundsCenterZ: float
    BoundsSizeX: float
    BoundsSizeY: float
    BoundsSizeZ: float
    levelOfDetail: _sketch_common_pb2.LevelOfDetail
    def __init__(self, deprecatedMeshGuid: _Optional[str] = ..., meshLodCollection: _Optional[_Union[_sketch_common_pb2.MeshLODCollection, _Mapping]] = ..., deprecatedObjMeshName: _Optional[str] = ..., deprecatedFileSize: _Optional[int] = ..., BoundsCenterX: _Optional[float] = ..., BoundsCenterY: _Optional[float] = ..., BoundsCenterZ: _Optional[float] = ..., BoundsSizeX: _Optional[float] = ..., BoundsSizeY: _Optional[float] = ..., BoundsSizeZ: _Optional[float] = ..., levelOfDetail: _Optional[_Union[_sketch_common_pb2.LevelOfDetail, str]] = ...) -> None: ...

class ProceduralObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("ObjectAnchor", "Locked", "HideBlock")
    OBJECTANCHOR_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    HIDEBLOCK_FIELD_NUMBER: _ClassVar[int]
    ObjectAnchor: _sketch_common_pb2.AnchorPosition
    Locked: bool
    HideBlock: bool
    def __init__(self, ObjectAnchor: _Optional[_Union[_sketch_common_pb2.AnchorPosition, str]] = ..., Locked: bool = ..., HideBlock: bool = ...) -> None: ...

class SubdivisionObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("SubdivisionIterations", "LowPoly", "IsInSubdivisionMode", "HardBoundaryCorners")
    SUBDIVISIONITERATIONS_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    ISINSUBDIVISIONMODE_FIELD_NUMBER: _ClassVar[int]
    HARDBOUNDARYCORNERS_FIELD_NUMBER: _ClassVar[int]
    SubdivisionIterations: int
    LowPoly: bool
    IsInSubdivisionMode: bool
    HardBoundaryCorners: bool
    def __init__(self, SubdivisionIterations: _Optional[int] = ..., LowPoly: bool = ..., IsInSubdivisionMode: bool = ..., HardBoundaryCorners: bool = ...) -> None: ...

class GenericRiggedModelExtraDataSnapshot(_message.Message):
    __slots__ = ("deprecatedMeshGuid", "deprecatedMeshName", "Nodes", "deprecatedFileSize", "meshLodCollection", "BoundsCenterX", "BoundsCenterY", "BoundsCenterZ", "BoundsSizeX", "BoundsSizeY", "BoundsSizeZ")
    DEPRECATEDMESHGUID_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDMESHNAME_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDFILESIZE_FIELD_NUMBER: _ClassVar[int]
    MESHLODCOLLECTION_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERX_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERY_FIELD_NUMBER: _ClassVar[int]
    BOUNDSCENTERZ_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEX_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEY_FIELD_NUMBER: _ClassVar[int]
    BOUNDSSIZEZ_FIELD_NUMBER: _ClassVar[int]
    deprecatedMeshGuid: str
    deprecatedMeshName: str
    Nodes: _containers.RepeatedCompositeFieldContainer[GenericRiggedNodeSnapshotData]
    deprecatedFileSize: int
    meshLodCollection: _sketch_common_pb2.MeshLODCollection
    BoundsCenterX: float
    BoundsCenterY: float
    BoundsCenterZ: float
    BoundsSizeX: float
    BoundsSizeY: float
    BoundsSizeZ: float
    def __init__(self, deprecatedMeshGuid: _Optional[str] = ..., deprecatedMeshName: _Optional[str] = ..., Nodes: _Optional[_Iterable[_Union[GenericRiggedNodeSnapshotData, _Mapping]]] = ..., deprecatedFileSize: _Optional[int] = ..., meshLodCollection: _Optional[_Union[_sketch_common_pb2.MeshLODCollection, _Mapping]] = ..., BoundsCenterX: _Optional[float] = ..., BoundsCenterY: _Optional[float] = ..., BoundsCenterZ: _Optional[float] = ..., BoundsSizeX: _Optional[float] = ..., BoundsSizeY: _Optional[float] = ..., BoundsSizeZ: _Optional[float] = ...) -> None: ...

class GenericRiggedNodeSnapshotData(_message.Message):
    __slots__ = ("Parent", "Children", "Name")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    Parent: int
    Children: _containers.RepeatedScalarFieldContainer[int]
    Name: str
    def __init__(self, Parent: _Optional[int] = ..., Children: _Optional[_Iterable[int]] = ..., Name: _Optional[str] = ...) -> None: ...

class CameraSketchObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("Name", "isSpawnPoint", "isHidden", "cameraSettings", "order")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ISSPAWNPOINT_FIELD_NUMBER: _ClassVar[int]
    ISHIDDEN_FIELD_NUMBER: _ClassVar[int]
    CAMERASETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    Name: str
    isSpawnPoint: bool
    isHidden: bool
    cameraSettings: _sketch_common_pb2.CameraSettings
    order: int
    def __init__(self, Name: _Optional[str] = ..., isSpawnPoint: bool = ..., isHidden: bool = ..., cameraSettings: _Optional[_Union[_sketch_common_pb2.CameraSettings, _Mapping]] = ..., order: _Optional[int] = ...) -> None: ...

class DimensionObjectExtraDataSnapshot(_message.Message):
    __slots__ = ("ReadoutOffsetX", "ReadoutOffsetY", "ReadoutOffsetZ")
    READOUTOFFSETX_FIELD_NUMBER: _ClassVar[int]
    READOUTOFFSETY_FIELD_NUMBER: _ClassVar[int]
    READOUTOFFSETZ_FIELD_NUMBER: _ClassVar[int]
    ReadoutOffsetX: float
    ReadoutOffsetY: float
    ReadoutOffsetZ: float
    def __init__(self, ReadoutOffsetX: _Optional[float] = ..., ReadoutOffsetY: _Optional[float] = ..., ReadoutOffsetZ: _Optional[float] = ...) -> None: ...

class ColourMenuExtraData(_message.Message):
    __slots__ = ("ColourR", "ColourG", "ColourB")
    COLOURR_FIELD_NUMBER: _ClassVar[int]
    COLOURG_FIELD_NUMBER: _ClassVar[int]
    COLOURB_FIELD_NUMBER: _ClassVar[int]
    ColourR: float
    ColourG: float
    ColourB: float
    def __init__(self, ColourR: _Optional[float] = ..., ColourG: _Optional[float] = ..., ColourB: _Optional[float] = ...) -> None: ...
