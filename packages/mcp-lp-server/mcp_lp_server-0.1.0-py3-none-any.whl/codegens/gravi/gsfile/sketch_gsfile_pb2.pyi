from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.gsfile.layergroup.persistence import layer_group_pb2 as _layer_group_pb2
from gravi.gsfile.metadata.persistence import metadata_pb2 as _metadata_pb2
from gravi.gsfile.asset.persistence import asset_pb2 as _asset_pb2
from gravi.gsfile.strokelayer.persistence import layer_pb2 as _layer_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Layer(_message.Message):
    __slots__ = ("LayerModel", "Strokes")
    LAYERMODEL_FIELD_NUMBER: _ClassVar[int]
    STROKES_FIELD_NUMBER: _ClassVar[int]
    LayerModel: _sketch_common_pb2.LayerModelTO
    Strokes: _containers.RepeatedCompositeFieldContainer[GSFileStrokeData]
    def __init__(self, LayerModel: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ..., Strokes: _Optional[_Iterable[_Union[GSFileStrokeData, _Mapping]]] = ...) -> None: ...

class PersistentGSFile(_message.Message):
    __slots__ = ("metadata", "nestedGroups", "materials", "layers", "strokes", "assets", "strokeLayers", "layerGroups", "strokeGroups")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NESTEDGROUPS_FIELD_NUMBER: _ClassVar[int]
    MATERIALS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    STROKES_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    STROKELAYERS_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPS_FIELD_NUMBER: _ClassVar[int]
    STROKEGROUPS_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.SketchMetadataModel
    nestedGroups: _containers.RepeatedCompositeFieldContainer[NestedGroupRelationship]
    materials: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    layers: _containers.RepeatedCompositeFieldContainer[_layer_pb2.LayerModel]
    strokes: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeDataSnapshot]
    assets: _containers.RepeatedCompositeFieldContainer[_asset_pb2.AssetModel]
    strokeLayers: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeLayerRelationship]
    layerGroups: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.NestedLayerRelationship]
    strokeGroups: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupRelationship]
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.SketchMetadataModel, _Mapping]] = ..., nestedGroups: _Optional[_Iterable[_Union[NestedGroupRelationship, _Mapping]]] = ..., materials: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., layers: _Optional[_Iterable[_Union[_layer_pb2.LayerModel, _Mapping]]] = ..., strokes: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeDataSnapshot, _Mapping]]] = ..., assets: _Optional[_Iterable[_Union[_asset_pb2.AssetModel, _Mapping]]] = ..., strokeLayers: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeLayerRelationship, _Mapping]]] = ..., layerGroups: _Optional[_Iterable[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]]] = ..., strokeGroups: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupRelationship, _Mapping]]] = ...) -> None: ...

class PersistentGSFileWithRevision(_message.Message):
    __slots__ = ("revisionId", "gsFile")
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    GSFILE_FIELD_NUMBER: _ClassVar[int]
    revisionId: str
    gsFile: PersistentGSFile
    def __init__(self, revisionId: _Optional[str] = ..., gsFile: _Optional[_Union[PersistentGSFile, _Mapping]] = ...) -> None: ...

class NestedGroupRelationship(_message.Message):
    __slots__ = ("id", "groupId", "parentGroupId")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUPID_FIELD_NUMBER: _ClassVar[int]
    PARENTGROUPID_FIELD_NUMBER: _ClassVar[int]
    id: str
    groupId: str
    parentGroupId: str
    def __init__(self, id: _Optional[str] = ..., groupId: _Optional[str] = ..., parentGroupId: _Optional[str] = ...) -> None: ...

class GSFileStrokeData(_message.Message):
    __slots__ = ("Name", "SplineType", "GSFileStrokeID", "Mirrored", "groupGuid", "materialGuid", "localPositionX", "localPositionY", "localPositionZ", "localRotationX", "localRotationY", "localRotationZ", "localRotationW", "localScaleX", "localScaleY", "localScaleZ", "mesh", "Space", "rotationalSymmetryData", "mirrorTransformState", "transformParentID", "linkedObjectId", "isMarkUp", "importedMetaData", "hidden")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SPLINETYPE_FIELD_NUMBER: _ClassVar[int]
    GSFILESTROKEID_FIELD_NUMBER: _ClassVar[int]
    MIRRORED_FIELD_NUMBER: _ClassVar[int]
    GROUPGUID_FIELD_NUMBER: _ClassVar[int]
    MATERIALGUID_FIELD_NUMBER: _ClassVar[int]
    LOCALPOSITIONX_FIELD_NUMBER: _ClassVar[int]
    LOCALPOSITIONY_FIELD_NUMBER: _ClassVar[int]
    LOCALPOSITIONZ_FIELD_NUMBER: _ClassVar[int]
    LOCALROTATIONX_FIELD_NUMBER: _ClassVar[int]
    LOCALROTATIONY_FIELD_NUMBER: _ClassVar[int]
    LOCALROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    LOCALROTATIONW_FIELD_NUMBER: _ClassVar[int]
    LOCALSCALEX_FIELD_NUMBER: _ClassVar[int]
    LOCALSCALEY_FIELD_NUMBER: _ClassVar[int]
    LOCALSCALEZ_FIELD_NUMBER: _ClassVar[int]
    MESH_FIELD_NUMBER: _ClassVar[int]
    SPACE_FIELD_NUMBER: _ClassVar[int]
    ROTATIONALSYMMETRYDATA_FIELD_NUMBER: _ClassVar[int]
    MIRRORTRANSFORMSTATE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMPARENTID_FIELD_NUMBER: _ClassVar[int]
    LINKEDOBJECTID_FIELD_NUMBER: _ClassVar[int]
    ISMARKUP_FIELD_NUMBER: _ClassVar[int]
    IMPORTEDMETADATA_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    Name: str
    SplineType: _sketch_common_pb2.SplineType
    GSFileStrokeID: _sketch_common_pb2.GSDataID
    Mirrored: bool
    groupGuid: str
    materialGuid: str
    localPositionX: float
    localPositionY: float
    localPositionZ: float
    localRotationX: float
    localRotationY: float
    localRotationZ: float
    localRotationW: float
    localScaleX: float
    localScaleY: float
    localScaleZ: float
    mesh: GSFileSketchMesh
    Space: _sketch_common_pb2.TransformSpace
    rotationalSymmetryData: _sketch_common_pb2.RotationalSymmetryData
    mirrorTransformState: _sketch_common_pb2.MirrorTransformState
    transformParentID: _sketch_common_pb2.GSDataID
    linkedObjectId: _sketch_common_pb2.GSDataID
    isMarkUp: bool
    importedMetaData: _sketch_common_pb2.ImportedObjectMetaData
    hidden: bool
    def __init__(self, Name: _Optional[str] = ..., SplineType: _Optional[_Union[_sketch_common_pb2.SplineType, str]] = ..., GSFileStrokeID: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., Mirrored: bool = ..., groupGuid: _Optional[str] = ..., materialGuid: _Optional[str] = ..., localPositionX: _Optional[float] = ..., localPositionY: _Optional[float] = ..., localPositionZ: _Optional[float] = ..., localRotationX: _Optional[float] = ..., localRotationY: _Optional[float] = ..., localRotationZ: _Optional[float] = ..., localRotationW: _Optional[float] = ..., localScaleX: _Optional[float] = ..., localScaleY: _Optional[float] = ..., localScaleZ: _Optional[float] = ..., mesh: _Optional[_Union[GSFileSketchMesh, _Mapping]] = ..., Space: _Optional[_Union[_sketch_common_pb2.TransformSpace, str]] = ..., rotationalSymmetryData: _Optional[_Union[_sketch_common_pb2.RotationalSymmetryData, _Mapping]] = ..., mirrorTransformState: _Optional[_Union[_sketch_common_pb2.MirrorTransformState, _Mapping]] = ..., transformParentID: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., linkedObjectId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., isMarkUp: bool = ..., importedMetaData: _Optional[_Union[_sketch_common_pb2.ImportedObjectMetaData, _Mapping]] = ..., hidden: bool = ...) -> None: ...

class GSFileSketchMesh(_message.Message):
    __slots__ = ("extraDataType", "VectorData", "deprecatedExtraData", "revolveExtraData", "strokeExtraData", "splineCurvedSurfaceExtraData", "splineNURBSSurfaceExtraData", "riggedModelExtraData", "textSketchObjectExtraData", "primitiveShapeExtraData", "deprecatedReferenceImageExtraData", "meshContentExtraData", "proceduralObjectExtraData", "subdivisionObjectExtraData", "genericNURBSCurveExtraData", "videoExtraData", "genericNURBSSurfaceExtraData", "trimmedNURBSSurfaceExtraData", "genericRiggedModelExtraData", "cameraSketchObjectExtraData", "dimensionObjectExtraData", "offsetData", "annotationSketchObjectExtraData")
    EXTRADATATYPE_FIELD_NUMBER: _ClassVar[int]
    VECTORDATA_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    REVOLVEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    STROKEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SPLINECURVEDSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SPLINENURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    RIGGEDMODELEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    TEXTSKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVESHAPEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDREFERENCEIMAGEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    MESHCONTENTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    PROCEDURALOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SUBDIVISIONOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICNURBSCURVEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    VIDEOEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICNURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMEDNURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICRIGGEDMODELEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    CAMERASKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    OFFSETDATA_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONSKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    extraDataType: _sketch_common_pb2.ExtraDataType
    VectorData: _containers.RepeatedCompositeFieldContainer[GSFileVectorData]
    deprecatedExtraData: bytes
    revolveExtraData: GSFileRevolveExtraData
    strokeExtraData: GSFileStrokeExtraData
    splineCurvedSurfaceExtraData: GSFileSplineCurvedSurfaceExtraData
    splineNURBSSurfaceExtraData: GSFileSplineNURBSSurfaceExtraData
    riggedModelExtraData: GSFileRiggedModelExtraData
    textSketchObjectExtraData: GSFileTextSketchObjectExtraData
    primitiveShapeExtraData: GSFilePrimitiveShapeExtraData
    deprecatedReferenceImageExtraData: GSFileReferenceImageExtraData
    meshContentExtraData: GSFileMeshContentExtraData
    proceduralObjectExtraData: GSFileProceduralObjectExtraData
    subdivisionObjectExtraData: GSFileSubdivisionObjectExtraData
    genericNURBSCurveExtraData: GSFileGenericNURBSCurveExtraData
    videoExtraData: GSFileVideoExtraData
    genericNURBSSurfaceExtraData: GSFileGenericNURBSSurfaceExtraData
    trimmedNURBSSurfaceExtraData: GSFileTrimmedNURBSSurfaceExtraData
    genericRiggedModelExtraData: GSFileGenericRiggedModelExtraData
    cameraSketchObjectExtraData: GSFileCameraSketchObjectExtraData
    dimensionObjectExtraData: GSFileDimensionObjectExtraData
    offsetData: _sketch_common_pb2.OffsetData
    annotationSketchObjectExtraData: GSFileAnnotationSketchObjectExtraData
    def __init__(self, extraDataType: _Optional[_Union[_sketch_common_pb2.ExtraDataType, str]] = ..., VectorData: _Optional[_Iterable[_Union[GSFileVectorData, _Mapping]]] = ..., deprecatedExtraData: _Optional[bytes] = ..., revolveExtraData: _Optional[_Union[GSFileRevolveExtraData, _Mapping]] = ..., strokeExtraData: _Optional[_Union[GSFileStrokeExtraData, _Mapping]] = ..., splineCurvedSurfaceExtraData: _Optional[_Union[GSFileSplineCurvedSurfaceExtraData, _Mapping]] = ..., splineNURBSSurfaceExtraData: _Optional[_Union[GSFileSplineNURBSSurfaceExtraData, _Mapping]] = ..., riggedModelExtraData: _Optional[_Union[GSFileRiggedModelExtraData, _Mapping]] = ..., textSketchObjectExtraData: _Optional[_Union[GSFileTextSketchObjectExtraData, _Mapping]] = ..., primitiveShapeExtraData: _Optional[_Union[GSFilePrimitiveShapeExtraData, _Mapping]] = ..., deprecatedReferenceImageExtraData: _Optional[_Union[GSFileReferenceImageExtraData, _Mapping]] = ..., meshContentExtraData: _Optional[_Union[GSFileMeshContentExtraData, _Mapping]] = ..., proceduralObjectExtraData: _Optional[_Union[GSFileProceduralObjectExtraData, _Mapping]] = ..., subdivisionObjectExtraData: _Optional[_Union[GSFileSubdivisionObjectExtraData, _Mapping]] = ..., genericNURBSCurveExtraData: _Optional[_Union[GSFileGenericNURBSCurveExtraData, _Mapping]] = ..., videoExtraData: _Optional[_Union[GSFileVideoExtraData, _Mapping]] = ..., genericNURBSSurfaceExtraData: _Optional[_Union[GSFileGenericNURBSSurfaceExtraData, _Mapping]] = ..., trimmedNURBSSurfaceExtraData: _Optional[_Union[GSFileTrimmedNURBSSurfaceExtraData, _Mapping]] = ..., genericRiggedModelExtraData: _Optional[_Union[GSFileGenericRiggedModelExtraData, _Mapping]] = ..., cameraSketchObjectExtraData: _Optional[_Union[GSFileCameraSketchObjectExtraData, _Mapping]] = ..., dimensionObjectExtraData: _Optional[_Union[GSFileDimensionObjectExtraData, _Mapping]] = ..., offsetData: _Optional[_Union[_sketch_common_pb2.OffsetData, _Mapping]] = ..., annotationSketchObjectExtraData: _Optional[_Union[GSFileAnnotationSketchObjectExtraData, _Mapping]] = ...) -> None: ...

class GSFileVectorData(_message.Message):
    __slots__ = ("VectorDataType", "PositionsX", "PositionsY", "PositionsZ", "NormalsX", "NormalsY", "NormalsZ", "RotationsX", "RotationsY", "RotationsZ", "RotationsW", "Sizes", "Weights", "IsOnMirror", "TriangleIndices", "QuadIndices", "NgonIndices", "NgonOffsets", "polygonVertices", "polygons", "creasedEdges")
    VECTORDATATYPE_FIELD_NUMBER: _ClassVar[int]
    POSITIONSX_FIELD_NUMBER: _ClassVar[int]
    POSITIONSY_FIELD_NUMBER: _ClassVar[int]
    POSITIONSZ_FIELD_NUMBER: _ClassVar[int]
    NORMALSX_FIELD_NUMBER: _ClassVar[int]
    NORMALSY_FIELD_NUMBER: _ClassVar[int]
    NORMALSZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONSX_FIELD_NUMBER: _ClassVar[int]
    ROTATIONSY_FIELD_NUMBER: _ClassVar[int]
    ROTATIONSZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONSW_FIELD_NUMBER: _ClassVar[int]
    SIZES_FIELD_NUMBER: _ClassVar[int]
    WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    ISONMIRROR_FIELD_NUMBER: _ClassVar[int]
    TRIANGLEINDICES_FIELD_NUMBER: _ClassVar[int]
    QUADINDICES_FIELD_NUMBER: _ClassVar[int]
    NGONINDICES_FIELD_NUMBER: _ClassVar[int]
    NGONOFFSETS_FIELD_NUMBER: _ClassVar[int]
    POLYGONVERTICES_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    CREASEDEDGES_FIELD_NUMBER: _ClassVar[int]
    VectorDataType: _sketch_common_pb2.VectorDataType
    PositionsX: _containers.RepeatedScalarFieldContainer[float]
    PositionsY: _containers.RepeatedScalarFieldContainer[float]
    PositionsZ: _containers.RepeatedScalarFieldContainer[float]
    NormalsX: _containers.RepeatedScalarFieldContainer[float]
    NormalsY: _containers.RepeatedScalarFieldContainer[float]
    NormalsZ: _containers.RepeatedScalarFieldContainer[float]
    RotationsX: _containers.RepeatedScalarFieldContainer[float]
    RotationsY: _containers.RepeatedScalarFieldContainer[float]
    RotationsZ: _containers.RepeatedScalarFieldContainer[float]
    RotationsW: _containers.RepeatedScalarFieldContainer[float]
    Sizes: _containers.RepeatedScalarFieldContainer[float]
    Weights: _containers.RepeatedScalarFieldContainer[float]
    IsOnMirror: _containers.RepeatedScalarFieldContainer[bool]
    TriangleIndices: _containers.RepeatedScalarFieldContainer[int]
    QuadIndices: _containers.RepeatedScalarFieldContainer[int]
    NgonIndices: _containers.RepeatedScalarFieldContainer[int]
    NgonOffsets: _containers.RepeatedScalarFieldContainer[int]
    polygonVertices: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.PolygonVertex]
    polygons: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.Polygon]
    creasedEdges: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID2]
    def __init__(self, VectorDataType: _Optional[_Union[_sketch_common_pb2.VectorDataType, str]] = ..., PositionsX: _Optional[_Iterable[float]] = ..., PositionsY: _Optional[_Iterable[float]] = ..., PositionsZ: _Optional[_Iterable[float]] = ..., NormalsX: _Optional[_Iterable[float]] = ..., NormalsY: _Optional[_Iterable[float]] = ..., NormalsZ: _Optional[_Iterable[float]] = ..., RotationsX: _Optional[_Iterable[float]] = ..., RotationsY: _Optional[_Iterable[float]] = ..., RotationsZ: _Optional[_Iterable[float]] = ..., RotationsW: _Optional[_Iterable[float]] = ..., Sizes: _Optional[_Iterable[float]] = ..., Weights: _Optional[_Iterable[float]] = ..., IsOnMirror: _Optional[_Iterable[bool]] = ..., TriangleIndices: _Optional[_Iterable[int]] = ..., QuadIndices: _Optional[_Iterable[int]] = ..., NgonIndices: _Optional[_Iterable[int]] = ..., NgonOffsets: _Optional[_Iterable[int]] = ..., polygonVertices: _Optional[_Iterable[_Union[_sketch_common_pb2.PolygonVertex, _Mapping]]] = ..., polygons: _Optional[_Iterable[_Union[_sketch_common_pb2.Polygon, _Mapping]]] = ..., creasedEdges: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID2, _Mapping]]] = ...) -> None: ...

class GSFileVideoExtraData(_message.Message):
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

class GSFileRevolveExtraData(_message.Message):
    __slots__ = ("StartSnap", "EndSnap", "Left", "Right", "Closed", "Loop", "deprecatedRotationAmount", "deprecatedSides", "Thickness", "deprecatedAxisX", "deprecatedAxisY", "deprecatedAxisZ", "rotationalSymmetryData", "LowPoly")
    STARTSNAP_FIELD_NUMBER: _ClassVar[int]
    ENDSNAP_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    LOOP_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDROTATIONAMOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDSIDES_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISX_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISY_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONALSYMMETRYDATA_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    StartSnap: bool
    EndSnap: bool
    Left: bool
    Right: bool
    Closed: bool
    Loop: bool
    deprecatedRotationAmount: int
    deprecatedSides: int
    Thickness: float
    deprecatedAxisX: float
    deprecatedAxisY: float
    deprecatedAxisZ: float
    rotationalSymmetryData: _sketch_common_pb2.RotationalSymmetryData
    LowPoly: bool
    def __init__(self, StartSnap: bool = ..., EndSnap: bool = ..., Left: bool = ..., Right: bool = ..., Closed: bool = ..., Loop: bool = ..., deprecatedRotationAmount: _Optional[int] = ..., deprecatedSides: _Optional[int] = ..., Thickness: _Optional[float] = ..., deprecatedAxisX: _Optional[float] = ..., deprecatedAxisY: _Optional[float] = ..., deprecatedAxisZ: _Optional[float] = ..., rotationalSymmetryData: _Optional[_Union[_sketch_common_pb2.RotationalSymmetryData, _Mapping]] = ..., LowPoly: bool = ...) -> None: ...

class GSFileStrokeExtraData(_message.Message):
    __slots__ = ("UsePressure", "BrushX", "BrushY", "Closed", "deprecatedRotationAmount", "deprecatedDup", "Shape", "CapType", "Planar", "DrawnPlanar", "Projected", "CustomNormals", "deprecatedDot", "deprecatedAxisX", "deprecatedAxisY", "deprecatedAxisZ", "LowPoly", "RepeatingUVs", "antiCoplanarityOffset")
    USEPRESSURE_FIELD_NUMBER: _ClassVar[int]
    BRUSHX_FIELD_NUMBER: _ClassVar[int]
    BRUSHY_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDROTATIONAMOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDDUP_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    CAPTYPE_FIELD_NUMBER: _ClassVar[int]
    PLANAR_FIELD_NUMBER: _ClassVar[int]
    DRAWNPLANAR_FIELD_NUMBER: _ClassVar[int]
    PROJECTED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMNORMALS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDDOT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISX_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISY_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDAXISZ_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    REPEATINGUVS_FIELD_NUMBER: _ClassVar[int]
    ANTICOPLANARITYOFFSET_FIELD_NUMBER: _ClassVar[int]
    UsePressure: bool
    BrushX: float
    BrushY: float
    Closed: bool
    deprecatedRotationAmount: int
    deprecatedDup: int
    Shape: _sketch_common_pb2.BrushShape
    CapType: _sketch_common_pb2.StrokeCapType
    Planar: bool
    DrawnPlanar: bool
    Projected: bool
    CustomNormals: bool
    deprecatedDot: bool
    deprecatedAxisX: float
    deprecatedAxisY: float
    deprecatedAxisZ: float
    LowPoly: bool
    RepeatingUVs: bool
    antiCoplanarityOffset: int
    def __init__(self, UsePressure: bool = ..., BrushX: _Optional[float] = ..., BrushY: _Optional[float] = ..., Closed: bool = ..., deprecatedRotationAmount: _Optional[int] = ..., deprecatedDup: _Optional[int] = ..., Shape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., CapType: _Optional[_Union[_sketch_common_pb2.StrokeCapType, str]] = ..., Planar: bool = ..., DrawnPlanar: bool = ..., Projected: bool = ..., CustomNormals: bool = ..., deprecatedDot: bool = ..., deprecatedAxisX: _Optional[float] = ..., deprecatedAxisY: _Optional[float] = ..., deprecatedAxisZ: _Optional[float] = ..., LowPoly: bool = ..., RepeatingUVs: bool = ..., antiCoplanarityOffset: _Optional[int] = ...) -> None: ...

class GSFileGenericNURBSCurveExtraData(_message.Message):
    __slots__ = ("KnotVector",)
    KNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    KnotVector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, KnotVector: _Optional[_Iterable[float]] = ...) -> None: ...

class GSFileSplineCurvedSurfaceExtraData(_message.Message):
    __slots__ = ("ClosedU", "ClosedV")
    CLOSEDU_FIELD_NUMBER: _ClassVar[int]
    CLOSEDV_FIELD_NUMBER: _ClassVar[int]
    ClosedU: bool
    ClosedV: bool
    def __init__(self, ClosedU: bool = ..., ClosedV: bool = ...) -> None: ...

class GSFileSplineNURBSSurfaceExtraData(_message.Message):
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

class GSFileGenericNURBSSurfaceExtraData(_message.Message):
    __slots__ = ("UKnotVector", "VKnotVector")
    UKNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    VKNOTVECTOR_FIELD_NUMBER: _ClassVar[int]
    UKnotVector: _containers.RepeatedScalarFieldContainer[float]
    VKnotVector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, UKnotVector: _Optional[_Iterable[float]] = ..., VKnotVector: _Optional[_Iterable[float]] = ...) -> None: ...

class GSFileTrimmedNURBSSurfaceExtraData(_message.Message):
    __slots__ = ("SurfaceData", "TrimmingCurvesData", "TrimmingCurvesLength")
    SURFACEDATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMINGCURVESDATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMINGCURVESLENGTH_FIELD_NUMBER: _ClassVar[int]
    SurfaceData: GSFileGenericNURBSSurfaceExtraData
    TrimmingCurvesData: _containers.RepeatedCompositeFieldContainer[GSFileGenericNURBSCurveExtraData]
    TrimmingCurvesLength: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, SurfaceData: _Optional[_Union[GSFileGenericNURBSSurfaceExtraData, _Mapping]] = ..., TrimmingCurvesData: _Optional[_Iterable[_Union[GSFileGenericNURBSCurveExtraData, _Mapping]]] = ..., TrimmingCurvesLength: _Optional[_Iterable[int]] = ...) -> None: ...

class GSFileRiggedModelExtraData(_message.Message):
    __slots__ = ("ModelID",)
    MODELID_FIELD_NUMBER: _ClassVar[int]
    ModelID: int
    def __init__(self, ModelID: _Optional[int] = ...) -> None: ...

class GSFileTextSketchObjectExtraData(_message.Message):
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

class GSFileAnnotationSketchObjectExtraData(_message.Message):
    __slots__ = ("text", "author", "commentParentId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    COMMENTPARENTID_FIELD_NUMBER: _ClassVar[int]
    text: str
    author: str
    commentParentId: str
    def __init__(self, text: _Optional[str] = ..., author: _Optional[str] = ..., commentParentId: _Optional[str] = ...) -> None: ...

class GSFilePrimitiveShapeExtraData(_message.Message):
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

class GSFileReferenceImageExtraData(_message.Message):
    __slots__ = ("deprecatedAnchor",)
    DEPRECATEDANCHOR_FIELD_NUMBER: _ClassVar[int]
    deprecatedAnchor: bool
    def __init__(self, deprecatedAnchor: bool = ...) -> None: ...

class GSFileMeshContentExtraData(_message.Message):
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

class GSFileProceduralObjectExtraData(_message.Message):
    __slots__ = ("ObjectAnchor", "Locked", "HideBlock")
    OBJECTANCHOR_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    HIDEBLOCK_FIELD_NUMBER: _ClassVar[int]
    ObjectAnchor: _sketch_common_pb2.AnchorPosition
    Locked: bool
    HideBlock: bool
    def __init__(self, ObjectAnchor: _Optional[_Union[_sketch_common_pb2.AnchorPosition, str]] = ..., Locked: bool = ..., HideBlock: bool = ...) -> None: ...

class GSFileSubdivisionObjectExtraData(_message.Message):
    __slots__ = ("SubdivisionIterations", "deprecatedPolygons", "deprecatedInternallyMirrored", "deprecatedExternalMirrorDisabled", "deprecatedLocalInternalMirrorTransform", "LowPoly", "IsInSubdivisionMode", "HardBoundaryCorners")
    SUBDIVISIONITERATIONS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDPOLYGONS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDINTERNALLYMIRRORED_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDEXTERNALMIRRORDISABLED_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDLOCALINTERNALMIRRORTRANSFORM_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    ISINSUBDIVISIONMODE_FIELD_NUMBER: _ClassVar[int]
    HARDBOUNDARYCORNERS_FIELD_NUMBER: _ClassVar[int]
    SubdivisionIterations: int
    deprecatedPolygons: _containers.RepeatedCompositeFieldContainer[DeprecatedIntPolygon]
    deprecatedInternallyMirrored: bool
    deprecatedExternalMirrorDisabled: bool
    deprecatedLocalInternalMirrorTransform: _gravi_unity_pb2.TransformTO
    LowPoly: bool
    IsInSubdivisionMode: bool
    HardBoundaryCorners: bool
    def __init__(self, SubdivisionIterations: _Optional[int] = ..., deprecatedPolygons: _Optional[_Iterable[_Union[DeprecatedIntPolygon, _Mapping]]] = ..., deprecatedInternallyMirrored: bool = ..., deprecatedExternalMirrorDisabled: bool = ..., deprecatedLocalInternalMirrorTransform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., LowPoly: bool = ..., IsInSubdivisionMode: bool = ..., HardBoundaryCorners: bool = ...) -> None: ...

class GSFileGenericRiggedModelExtraData(_message.Message):
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
    Nodes: _containers.RepeatedCompositeFieldContainer[GSFileGenericRiggedNodeData]
    deprecatedFileSize: int
    meshLodCollection: _sketch_common_pb2.MeshLODCollection
    BoundsCenterX: float
    BoundsCenterY: float
    BoundsCenterZ: float
    BoundsSizeX: float
    BoundsSizeY: float
    BoundsSizeZ: float
    def __init__(self, deprecatedMeshGuid: _Optional[str] = ..., deprecatedMeshName: _Optional[str] = ..., Nodes: _Optional[_Iterable[_Union[GSFileGenericRiggedNodeData, _Mapping]]] = ..., deprecatedFileSize: _Optional[int] = ..., meshLodCollection: _Optional[_Union[_sketch_common_pb2.MeshLODCollection, _Mapping]] = ..., BoundsCenterX: _Optional[float] = ..., BoundsCenterY: _Optional[float] = ..., BoundsCenterZ: _Optional[float] = ..., BoundsSizeX: _Optional[float] = ..., BoundsSizeY: _Optional[float] = ..., BoundsSizeZ: _Optional[float] = ...) -> None: ...

class GSFileGenericRiggedNodeData(_message.Message):
    __slots__ = ("Parent", "Children", "Name")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    Parent: int
    Children: _containers.RepeatedScalarFieldContainer[int]
    Name: str
    def __init__(self, Parent: _Optional[int] = ..., Children: _Optional[_Iterable[int]] = ..., Name: _Optional[str] = ...) -> None: ...

class GSFileCameraSketchObjectExtraData(_message.Message):
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

class GSFileDimensionObjectExtraData(_message.Message):
    __slots__ = ("ReadoutOffsetX", "ReadoutOffsetY", "ReadoutOffsetZ")
    READOUTOFFSETX_FIELD_NUMBER: _ClassVar[int]
    READOUTOFFSETY_FIELD_NUMBER: _ClassVar[int]
    READOUTOFFSETZ_FIELD_NUMBER: _ClassVar[int]
    ReadoutOffsetX: float
    ReadoutOffsetY: float
    ReadoutOffsetZ: float
    def __init__(self, ReadoutOffsetX: _Optional[float] = ..., ReadoutOffsetY: _Optional[float] = ..., ReadoutOffsetZ: _Optional[float] = ...) -> None: ...

class DeprecatedIntPolygon(_message.Message):
    __slots__ = ("Vertices",)
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    Vertices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, Vertices: _Optional[_Iterable[int]] = ...) -> None: ...
