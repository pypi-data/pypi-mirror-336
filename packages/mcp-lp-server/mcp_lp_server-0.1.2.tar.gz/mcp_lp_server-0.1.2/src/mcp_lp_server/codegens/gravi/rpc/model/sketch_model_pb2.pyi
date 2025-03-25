from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.extra import sketch_extra_pb2 as _sketch_extra_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SplineAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Missing: _ClassVar[SplineAction]
    Finalise: _ClassVar[SplineAction]
    StartEdit: _ClassVar[SplineAction]
    UpdateEdit: _ClassVar[SplineAction]
    EndEdit: _ClassVar[SplineAction]
    Delete: _ClassVar[SplineAction]
    Destroy: _ClassVar[SplineAction]
    StartGrab: _ClassVar[SplineAction]
    GrabMove: _ClassVar[SplineAction]
    EndGrab: _ClassVar[SplineAction]
    StartCreation: _ClassVar[SplineAction]
    StartMatChange: _ClassVar[SplineAction]
    UpdateMat: _ClassVar[SplineAction]
    EndMatChange: _ClassVar[SplineAction]
    StartAtomicUpdateEdit: _ClassVar[SplineAction]
    EndAtomicUpdateEdit: _ClassVar[SplineAction]
    Reparent: _ClassVar[SplineAction]

class VRSDK(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VRSDKNone: _ClassVar[VRSDK]
    Oculus: _ClassVar[VRSDK]
    OpenVR: _ClassVar[VRSDK]
    UWP: _ClassVar[VRSDK]
    WaveVR: _ClassVar[VRSDK]
    Varjo: _ClassVar[VRSDK]
    PicoVR: _ClassVar[VRSDK]
    Simulator: _ClassVar[VRSDK]

class VRControllerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VRControllerTypeNone: _ClassVar[VRControllerType]
    Vive: _ClassVar[VRControllerType]
    Touch: _ClassVar[VRControllerType]
    WindowsMixed: _ClassVar[VRControllerType]
    deprecated_Infinity: _ClassVar[VRControllerType]
    Knuckles: _ClassVar[VRControllerType]
    Quest: _ClassVar[VRControllerType]
    LogitechStylusSteamVR: _ClassVar[VRControllerType]
    ViveCosmos: _ClassVar[VRControllerType]
    ReverbG2: _ClassVar[VRControllerType]
    Wave: _ClassVar[VRControllerType]
    Pico: _ClassVar[VRControllerType]
    TouchPro: _ClassVar[VRControllerType]
    Quest2: _ClassVar[VRControllerType]
    Pico4: _ClassVar[VRControllerType]
    UnusedReserved6: _ClassVar[VRControllerType]
    UnusedReserved7: _ClassVar[VRControllerType]
    UnusedReserved8: _ClassVar[VRControllerType]
    UnusedReserved9: _ClassVar[VRControllerType]
    LogitechStylusQuest: _ClassVar[VRControllerType]
    Quest3: _ClassVar[VRControllerType]
    deprecated_Tangi0: _ClassVar[VRControllerType]
    deprecated_Massless: _ClassVar[VRControllerType]

class CoSketchAvatarType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CoSketchAvatarVR: _ClassVar[CoSketchAvatarType]
    CoSketchAvatar2DScreen: _ClassVar[CoSketchAvatarType]

class CameraProjectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Perspective: _ClassVar[CameraProjectionMode]
    Orthographic: _ClassVar[CameraProjectionMode]
Missing: SplineAction
Finalise: SplineAction
StartEdit: SplineAction
UpdateEdit: SplineAction
EndEdit: SplineAction
Delete: SplineAction
Destroy: SplineAction
StartGrab: SplineAction
GrabMove: SplineAction
EndGrab: SplineAction
StartCreation: SplineAction
StartMatChange: SplineAction
UpdateMat: SplineAction
EndMatChange: SplineAction
StartAtomicUpdateEdit: SplineAction
EndAtomicUpdateEdit: SplineAction
Reparent: SplineAction
VRSDKNone: VRSDK
Oculus: VRSDK
OpenVR: VRSDK
UWP: VRSDK
WaveVR: VRSDK
Varjo: VRSDK
PicoVR: VRSDK
Simulator: VRSDK
VRControllerTypeNone: VRControllerType
Vive: VRControllerType
Touch: VRControllerType
WindowsMixed: VRControllerType
deprecated_Infinity: VRControllerType
Knuckles: VRControllerType
Quest: VRControllerType
LogitechStylusSteamVR: VRControllerType
ViveCosmos: VRControllerType
ReverbG2: VRControllerType
Wave: VRControllerType
Pico: VRControllerType
TouchPro: VRControllerType
Quest2: VRControllerType
Pico4: VRControllerType
UnusedReserved6: VRControllerType
UnusedReserved7: VRControllerType
UnusedReserved8: VRControllerType
UnusedReserved9: VRControllerType
LogitechStylusQuest: VRControllerType
Quest3: VRControllerType
deprecated_Tangi0: VRControllerType
deprecated_Massless: VRControllerType
CoSketchAvatarVR: CoSketchAvatarType
CoSketchAvatar2DScreen: CoSketchAvatarType
Perspective: CameraProjectionMode
Orthographic: CameraProjectionMode

class ColorHistoryTO(_message.Message):
    __slots__ = ("colors",)
    COLORS_FIELD_NUMBER: _ClassVar[int]
    colors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, colors: _Optional[_Iterable[str]] = ...) -> None: ...

class StrokeDataSnapshot(_message.Message):
    __slots__ = ("SplineType", "Space", "transformParentId", "strokeId", "strokeName", "groupGuid", "materialGuid", "layerId", "linkedObjectId", "importedMetaData", "mesh", "sketchTransform", "mirrorTransformState", "hidden", "isMarkUp")
    SPLINETYPE_FIELD_NUMBER: _ClassVar[int]
    SPACE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMPARENTID_FIELD_NUMBER: _ClassVar[int]
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    STROKENAME_FIELD_NUMBER: _ClassVar[int]
    GROUPGUID_FIELD_NUMBER: _ClassVar[int]
    MATERIALGUID_FIELD_NUMBER: _ClassVar[int]
    LAYERID_FIELD_NUMBER: _ClassVar[int]
    LINKEDOBJECTID_FIELD_NUMBER: _ClassVar[int]
    IMPORTEDMETADATA_FIELD_NUMBER: _ClassVar[int]
    MESH_FIELD_NUMBER: _ClassVar[int]
    SKETCHTRANSFORM_FIELD_NUMBER: _ClassVar[int]
    MIRRORTRANSFORMSTATE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    ISMARKUP_FIELD_NUMBER: _ClassVar[int]
    SplineType: _sketch_common_pb2.SplineType
    Space: _sketch_common_pb2.TransformSpace
    transformParentId: _sketch_common_pb2.GSDataID
    strokeId: _sketch_common_pb2.GSDataID
    strokeName: str
    groupGuid: str
    materialGuid: str
    layerId: str
    linkedObjectId: _sketch_common_pb2.GSDataID
    importedMetaData: _sketch_common_pb2.ImportedObjectMetaData
    mesh: SketchMeshSnapshot
    sketchTransform: _gravi_unity_pb2.TransformTO
    mirrorTransformState: _sketch_common_pb2.MirrorTransformState
    hidden: bool
    isMarkUp: bool
    def __init__(self, SplineType: _Optional[_Union[_sketch_common_pb2.SplineType, str]] = ..., Space: _Optional[_Union[_sketch_common_pb2.TransformSpace, str]] = ..., transformParentId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeName: _Optional[str] = ..., groupGuid: _Optional[str] = ..., materialGuid: _Optional[str] = ..., layerId: _Optional[str] = ..., linkedObjectId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., importedMetaData: _Optional[_Union[_sketch_common_pb2.ImportedObjectMetaData, _Mapping]] = ..., mesh: _Optional[_Union[SketchMeshSnapshot, _Mapping]] = ..., sketchTransform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., mirrorTransformState: _Optional[_Union[_sketch_common_pb2.MirrorTransformState, _Mapping]] = ..., hidden: bool = ..., isMarkUp: bool = ...) -> None: ...

class StrokeGroupRelationship(_message.Message):
    __slots__ = ("id", "strokeId", "groupId")
    ID_FIELD_NUMBER: _ClassVar[int]
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    GROUPID_FIELD_NUMBER: _ClassVar[int]
    id: _sketch_common_pb2.GSDataID
    strokeId: _sketch_common_pb2.GSDataID
    groupId: str
    def __init__(self, id: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., groupId: _Optional[str] = ...) -> None: ...

class StrokeLayerRelationship(_message.Message):
    __slots__ = ("id", "strokeId", "layerId")
    ID_FIELD_NUMBER: _ClassVar[int]
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    LAYERID_FIELD_NUMBER: _ClassVar[int]
    id: _sketch_common_pb2.GSDataID
    strokeId: _sketch_common_pb2.GSDataID
    layerId: str
    def __init__(self, id: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., layerId: _Optional[str] = ...) -> None: ...

class StrokeProperties(_message.Message):
    __slots__ = ("SplineType", "Space", "transformParentID", "linkedObjectId", "isMarkUp", "importedMetaData")
    SPLINETYPE_FIELD_NUMBER: _ClassVar[int]
    SPACE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMPARENTID_FIELD_NUMBER: _ClassVar[int]
    LINKEDOBJECTID_FIELD_NUMBER: _ClassVar[int]
    ISMARKUP_FIELD_NUMBER: _ClassVar[int]
    IMPORTEDMETADATA_FIELD_NUMBER: _ClassVar[int]
    SplineType: _sketch_common_pb2.SplineType
    Space: _sketch_common_pb2.TransformSpace
    transformParentID: _sketch_common_pb2.GSDataID
    linkedObjectId: _sketch_common_pb2.GSDataID
    isMarkUp: bool
    importedMetaData: _sketch_common_pb2.ImportedObjectMetaData
    def __init__(self, SplineType: _Optional[_Union[_sketch_common_pb2.SplineType, str]] = ..., Space: _Optional[_Union[_sketch_common_pb2.TransformSpace, str]] = ..., transformParentID: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., linkedObjectId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., isMarkUp: bool = ..., importedMetaData: _Optional[_Union[_sketch_common_pb2.ImportedObjectMetaData, _Mapping]] = ...) -> None: ...

class SketchMeshSnapshot(_message.Message):
    __slots__ = ("extraDataType", "VectorData", "revisionId", "revolveExtraData", "strokeExtraData", "splineCurvedSurfaceExtraData", "splineNURBSSurfaceExtraData", "riggedModelExtraData", "textSketchObjectExtraData", "primitiveShapeExtraData", "meshContentExtraData", "proceduralObjectExtraData", "subdivisionObjectExtraData", "genericNURBSCurveExtraData", "videoExtraData", "genericNURBSSurfaceExtraData", "trimmedNURBSSurfaceExtraData", "genericRiggedModelExtraData", "cameraSketchObjectExtraData", "dimensionObjectExtraDataSnapshot", "annotationSketchObjectExtraData", "Mirrored", "rotationalSymmetryData", "offsetData")
    EXTRADATATYPE_FIELD_NUMBER: _ClassVar[int]
    VECTORDATA_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    REVOLVEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    STROKEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SPLINECURVEDSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SPLINENURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    RIGGEDMODELEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    TEXTSKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVESHAPEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    MESHCONTENTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    PROCEDURALOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    SUBDIVISIONOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICNURBSCURVEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    VIDEOEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICNURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    TRIMMEDNURBSSURFACEEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    GENERICRIGGEDMODELEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    CAMERASKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONOBJECTEXTRADATASNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONSKETCHOBJECTEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    MIRRORED_FIELD_NUMBER: _ClassVar[int]
    ROTATIONALSYMMETRYDATA_FIELD_NUMBER: _ClassVar[int]
    OFFSETDATA_FIELD_NUMBER: _ClassVar[int]
    extraDataType: _sketch_common_pb2.ExtraDataType
    VectorData: _containers.RepeatedCompositeFieldContainer[VectorDataSnapshot]
    revisionId: int
    revolveExtraData: _sketch_extra_pb2.RevolveExtraDataSnapshot
    strokeExtraData: _sketch_extra_pb2.StrokeExtraDataSnapshot
    splineCurvedSurfaceExtraData: _sketch_extra_pb2.SplineCurvedSurfaceExtraDataSnapshot
    splineNURBSSurfaceExtraData: _sketch_extra_pb2.SplineNURBSSurfaceExtraDataSnapshot
    riggedModelExtraData: _sketch_extra_pb2.RiggedModelExtraDataSnapshot
    textSketchObjectExtraData: _sketch_extra_pb2.TextSketchObjectExtraDataSnapshot
    primitiveShapeExtraData: _sketch_extra_pb2.PrimitiveShapeExtraDataSnapshot
    meshContentExtraData: _sketch_extra_pb2.MeshContentExtraDataSnapshot
    proceduralObjectExtraData: _sketch_extra_pb2.ProceduralObjectExtraDataSnapshot
    subdivisionObjectExtraData: _sketch_extra_pb2.SubdivisionObjectExtraDataSnapshot
    genericNURBSCurveExtraData: _sketch_extra_pb2.GenericNURBSCurveExtraDataSnapshot
    videoExtraData: _sketch_extra_pb2.VideoExtraDataSnapshot
    genericNURBSSurfaceExtraData: _sketch_extra_pb2.GenericNURBSSurfaceExtraDataSnapshot
    trimmedNURBSSurfaceExtraData: _sketch_extra_pb2.TrimmedNURBSSurfaceExtraDataSnapshot
    genericRiggedModelExtraData: _sketch_extra_pb2.GenericRiggedModelExtraDataSnapshot
    cameraSketchObjectExtraData: _sketch_extra_pb2.CameraSketchObjectExtraDataSnapshot
    dimensionObjectExtraDataSnapshot: _sketch_extra_pb2.DimensionObjectExtraDataSnapshot
    annotationSketchObjectExtraData: _sketch_extra_pb2.AnnotationSketchObjectExtraDataSnapshot
    Mirrored: bool
    rotationalSymmetryData: _sketch_common_pb2.RotationalSymmetryData
    offsetData: _sketch_common_pb2.OffsetData
    def __init__(self, extraDataType: _Optional[_Union[_sketch_common_pb2.ExtraDataType, str]] = ..., VectorData: _Optional[_Iterable[_Union[VectorDataSnapshot, _Mapping]]] = ..., revisionId: _Optional[int] = ..., revolveExtraData: _Optional[_Union[_sketch_extra_pb2.RevolveExtraDataSnapshot, _Mapping]] = ..., strokeExtraData: _Optional[_Union[_sketch_extra_pb2.StrokeExtraDataSnapshot, _Mapping]] = ..., splineCurvedSurfaceExtraData: _Optional[_Union[_sketch_extra_pb2.SplineCurvedSurfaceExtraDataSnapshot, _Mapping]] = ..., splineNURBSSurfaceExtraData: _Optional[_Union[_sketch_extra_pb2.SplineNURBSSurfaceExtraDataSnapshot, _Mapping]] = ..., riggedModelExtraData: _Optional[_Union[_sketch_extra_pb2.RiggedModelExtraDataSnapshot, _Mapping]] = ..., textSketchObjectExtraData: _Optional[_Union[_sketch_extra_pb2.TextSketchObjectExtraDataSnapshot, _Mapping]] = ..., primitiveShapeExtraData: _Optional[_Union[_sketch_extra_pb2.PrimitiveShapeExtraDataSnapshot, _Mapping]] = ..., meshContentExtraData: _Optional[_Union[_sketch_extra_pb2.MeshContentExtraDataSnapshot, _Mapping]] = ..., proceduralObjectExtraData: _Optional[_Union[_sketch_extra_pb2.ProceduralObjectExtraDataSnapshot, _Mapping]] = ..., subdivisionObjectExtraData: _Optional[_Union[_sketch_extra_pb2.SubdivisionObjectExtraDataSnapshot, _Mapping]] = ..., genericNURBSCurveExtraData: _Optional[_Union[_sketch_extra_pb2.GenericNURBSCurveExtraDataSnapshot, _Mapping]] = ..., videoExtraData: _Optional[_Union[_sketch_extra_pb2.VideoExtraDataSnapshot, _Mapping]] = ..., genericNURBSSurfaceExtraData: _Optional[_Union[_sketch_extra_pb2.GenericNURBSSurfaceExtraDataSnapshot, _Mapping]] = ..., trimmedNURBSSurfaceExtraData: _Optional[_Union[_sketch_extra_pb2.TrimmedNURBSSurfaceExtraDataSnapshot, _Mapping]] = ..., genericRiggedModelExtraData: _Optional[_Union[_sketch_extra_pb2.GenericRiggedModelExtraDataSnapshot, _Mapping]] = ..., cameraSketchObjectExtraData: _Optional[_Union[_sketch_extra_pb2.CameraSketchObjectExtraDataSnapshot, _Mapping]] = ..., dimensionObjectExtraDataSnapshot: _Optional[_Union[_sketch_extra_pb2.DimensionObjectExtraDataSnapshot, _Mapping]] = ..., annotationSketchObjectExtraData: _Optional[_Union[_sketch_extra_pb2.AnnotationSketchObjectExtraDataSnapshot, _Mapping]] = ..., Mirrored: bool = ..., rotationalSymmetryData: _Optional[_Union[_sketch_common_pb2.RotationalSymmetryData, _Mapping]] = ..., offsetData: _Optional[_Union[_sketch_common_pb2.OffsetData, _Mapping]] = ...) -> None: ...

class VectorDataSnapshot(_message.Message):
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

class StrokeActionData(_message.Message):
    __slots__ = ("strokeId", "strokeData", "cachedMaterialHistory", "cachedLayerModel", "cachedNextExpectedConfirmIncrementalEditSeqID", "strokeName", "actionMetaData")
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    STROKEDATA_FIELD_NUMBER: _ClassVar[int]
    CACHEDMATERIALHISTORY_FIELD_NUMBER: _ClassVar[int]
    CACHEDLAYERMODEL_FIELD_NUMBER: _ClassVar[int]
    CACHEDNEXTEXPECTEDCONFIRMINCREMENTALEDITSEQID_FIELD_NUMBER: _ClassVar[int]
    STROKENAME_FIELD_NUMBER: _ClassVar[int]
    ACTIONMETADATA_FIELD_NUMBER: _ClassVar[int]
    strokeId: _sketch_common_pb2.GSDataID
    strokeData: StrokeDataSnapshot
    cachedMaterialHistory: _sketch_common_pb2.DrawMaterial
    cachedLayerModel: _sketch_common_pb2.LayerModelTO
    cachedNextExpectedConfirmIncrementalEditSeqID: int
    strokeName: str
    actionMetaData: StrokeActionMetaData
    def __init__(self, strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeData: _Optional[_Union[StrokeDataSnapshot, _Mapping]] = ..., cachedMaterialHistory: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ..., cachedLayerModel: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ..., cachedNextExpectedConfirmIncrementalEditSeqID: _Optional[int] = ..., strokeName: _Optional[str] = ..., actionMetaData: _Optional[_Union[StrokeActionMetaData, _Mapping]] = ...) -> None: ...

class StrokeActionMetaData(_message.Message):
    __slots__ = ("inUseByClientId", "seqId", "action", "RevisionId", "lastModifiedByClientId")
    INUSEBYCLIENTID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIEDBYCLIENTID_FIELD_NUMBER: _ClassVar[int]
    inUseByClientId: int
    seqId: int
    action: SplineAction
    RevisionId: int
    lastModifiedByClientId: int
    def __init__(self, inUseByClientId: _Optional[int] = ..., seqId: _Optional[int] = ..., action: _Optional[_Union[SplineAction, str]] = ..., RevisionId: _Optional[int] = ..., lastModifiedByClientId: _Optional[int] = ...) -> None: ...

class CoSketchUser(_message.Message):
    __slots__ = ("clientId", "isOnline", "username", "colourR", "colourG", "colourB", "colourA", "userSavedPreferences", "role", "userState", "avatarType", "isAndroid", "unityUserId", "userId")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    ISONLINE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    COLOURR_FIELD_NUMBER: _ClassVar[int]
    COLOURG_FIELD_NUMBER: _ClassVar[int]
    COLOURB_FIELD_NUMBER: _ClassVar[int]
    COLOURA_FIELD_NUMBER: _ClassVar[int]
    USERSAVEDPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USERSTATE_FIELD_NUMBER: _ClassVar[int]
    AVATARTYPE_FIELD_NUMBER: _ClassVar[int]
    ISANDROID_FIELD_NUMBER: _ClassVar[int]
    UNITYUSERID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    clientId: int
    isOnline: bool
    username: str
    colourR: int
    colourG: int
    colourB: int
    colourA: int
    userSavedPreferences: _preferences_pb2.UserSavedPreferencesTO
    role: _gravi_model_pb2.CollaborationRole
    userState: CoSketchUserState
    avatarType: CoSketchAvatarType
    isAndroid: bool
    unityUserId: str
    userId: str
    def __init__(self, clientId: _Optional[int] = ..., isOnline: bool = ..., username: _Optional[str] = ..., colourR: _Optional[int] = ..., colourG: _Optional[int] = ..., colourB: _Optional[int] = ..., colourA: _Optional[int] = ..., userSavedPreferences: _Optional[_Union[_preferences_pb2.UserSavedPreferencesTO, _Mapping]] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., userState: _Optional[_Union[CoSketchUserState, _Mapping]] = ..., avatarType: _Optional[_Union[CoSketchAvatarType, str]] = ..., isAndroid: bool = ..., unityUserId: _Optional[str] = ..., userId: _Optional[str] = ...) -> None: ...

class CoSketchUserState(_message.Message):
    __slots__ = ("isBroadcastingUI", "followingClientId", "isMuted", "supportsMetaAvatars", "isUsingPassthrough", "supportsColocation", "isUsingPOVLighting", "selectedViewpoint", "leftControllerType", "rightControllerType")
    ISBROADCASTINGUI_FIELD_NUMBER: _ClassVar[int]
    FOLLOWINGCLIENTID_FIELD_NUMBER: _ClassVar[int]
    ISMUTED_FIELD_NUMBER: _ClassVar[int]
    SUPPORTSMETAAVATARS_FIELD_NUMBER: _ClassVar[int]
    ISUSINGPASSTHROUGH_FIELD_NUMBER: _ClassVar[int]
    SUPPORTSCOLOCATION_FIELD_NUMBER: _ClassVar[int]
    ISUSINGPOVLIGHTING_FIELD_NUMBER: _ClassVar[int]
    SELECTEDVIEWPOINT_FIELD_NUMBER: _ClassVar[int]
    LEFTCONTROLLERTYPE_FIELD_NUMBER: _ClassVar[int]
    RIGHTCONTROLLERTYPE_FIELD_NUMBER: _ClassVar[int]
    isBroadcastingUI: bool
    followingClientId: int
    isMuted: bool
    supportsMetaAvatars: bool
    isUsingPassthrough: bool
    supportsColocation: bool
    isUsingPOVLighting: bool
    selectedViewpoint: _sketch_common_pb2.GSDataID
    leftControllerType: VRControllerType
    rightControllerType: VRControllerType
    def __init__(self, isBroadcastingUI: bool = ..., followingClientId: _Optional[int] = ..., isMuted: bool = ..., supportsMetaAvatars: bool = ..., isUsingPassthrough: bool = ..., supportsColocation: bool = ..., isUsingPOVLighting: bool = ..., selectedViewpoint: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., leftControllerType: _Optional[_Union[VRControllerType, str]] = ..., rightControllerType: _Optional[_Union[VRControllerType, str]] = ...) -> None: ...

class CameraState(_message.Message):
    __slots__ = ("focalLength", "projectionMode", "orthographicSizeSketchSpace")
    FOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    PROJECTIONMODE_FIELD_NUMBER: _ClassVar[int]
    ORTHOGRAPHICSIZESKETCHSPACE_FIELD_NUMBER: _ClassVar[int]
    focalLength: float
    projectionMode: CameraProjectionMode
    orthographicSizeSketchSpace: float
    def __init__(self, focalLength: _Optional[float] = ..., projectionMode: _Optional[_Union[CameraProjectionMode, str]] = ..., orthographicSizeSketchSpace: _Optional[float] = ...) -> None: ...

class CoSketchRoomExtraData(_message.Message):
    __slots__ = ("coordinatorId", "customSettings", "presetIndex", "sectionViewData", "userEntityIds", "roomFullyLoaded")
    class UserEntityIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    COORDINATORID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMSETTINGS_FIELD_NUMBER: _ClassVar[int]
    PRESETINDEX_FIELD_NUMBER: _ClassVar[int]
    SECTIONVIEWDATA_FIELD_NUMBER: _ClassVar[int]
    USERENTITYIDS_FIELD_NUMBER: _ClassVar[int]
    ROOMFULLYLOADED_FIELD_NUMBER: _ClassVar[int]
    coordinatorId: int
    customSettings: _gravi_model_pb2.EnvironmentSettingTO
    presetIndex: int
    sectionViewData: _sketch_common_pb2.SectionViewData
    userEntityIds: _containers.ScalarMap[int, int]
    roomFullyLoaded: bool
    def __init__(self, coordinatorId: _Optional[int] = ..., customSettings: _Optional[_Union[_gravi_model_pb2.EnvironmentSettingTO, _Mapping]] = ..., presetIndex: _Optional[int] = ..., sectionViewData: _Optional[_Union[_sketch_common_pb2.SectionViewData, _Mapping]] = ..., userEntityIds: _Optional[_Mapping[int, int]] = ..., roomFullyLoaded: bool = ...) -> None: ...

class EMeshMeta(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    def __init__(self, version: _Optional[int] = ...) -> None: ...

class StrokeGroupMetaData(_message.Message):
    __slots__ = ("seqId", "name")
    SEQID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    seqId: int
    name: str
    def __init__(self, seqId: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class StrokeGroupTO(_message.Message):
    __slots__ = ("groupId", "groupName", "parentGroupId", "seqId", "deleted")
    GROUPID_FIELD_NUMBER: _ClassVar[int]
    GROUPNAME_FIELD_NUMBER: _ClassVar[int]
    PARENTGROUPID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    groupId: str
    groupName: str
    parentGroupId: str
    seqId: int
    deleted: bool
    def __init__(self, groupId: _Optional[str] = ..., groupName: _Optional[str] = ..., parentGroupId: _Optional[str] = ..., seqId: _Optional[int] = ..., deleted: bool = ...) -> None: ...

class SplineAnimation(_message.Message):
    __slots__ = ("splinePoints",)
    SPLINEPOINTS_FIELD_NUMBER: _ClassVar[int]
    splinePoints: _containers.RepeatedCompositeFieldContainer[SplineAnimationPoint]
    def __init__(self, splinePoints: _Optional[_Iterable[_Union[SplineAnimationPoint, _Mapping]]] = ...) -> None: ...

class SplineAnimationPoint(_message.Message):
    __slots__ = ("posX", "posY", "posZ")
    POSX_FIELD_NUMBER: _ClassVar[int]
    POSY_FIELD_NUMBER: _ClassVar[int]
    POSZ_FIELD_NUMBER: _ClassVar[int]
    posX: float
    posY: float
    posZ: float
    def __init__(self, posX: _Optional[float] = ..., posY: _Optional[float] = ..., posZ: _Optional[float] = ...) -> None: ...
