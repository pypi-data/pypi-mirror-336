from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaterialVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LegacyPresets: _ClassVar[MaterialVersion]
    V1ConfigurableProperties: _ClassVar[MaterialVersion]

class BaseMaterialType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Standard: _ClassVar[BaseMaterialType]
    Flat: _ClassVar[BaseMaterialType]
    Reflective: _ClassVar[BaseMaterialType]
    Cartoon: _ClassVar[BaseMaterialType]
    XRay: _ClassVar[BaseMaterialType]
    Mobile: _ClassVar[BaseMaterialType]
    LowPoly: _ClassVar[BaseMaterialType]
    Stipped: _ClassVar[BaseMaterialType]
    Phong: _ClassVar[BaseMaterialType]
    Glossy: _ClassVar[BaseMaterialType]
    UI: _ClassVar[BaseMaterialType]
    Preview: _ClassVar[BaseMaterialType]
    Inktober: _ClassVar[BaseMaterialType]

class SplineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Revolution: _ClassVar[SplineType]
    Magic: _ClassVar[SplineType]
    Lines: _ClassVar[SplineType]
    Solid: _ClassVar[SplineType]
    CurvedSurface: _ClassVar[SplineType]
    Primitive: _ClassVar[SplineType]
    NURBSSurface: _ClassVar[SplineType]
    SketchText: _ClassVar[SplineType]
    ConvexHull: _ClassVar[SplineType]
    UIHandle: _ClassVar[SplineType]
    ControlGizmo: _ClassVar[SplineType]
    ReferenceImage: _ClassVar[SplineType]
    MenuItem: _ClassVar[SplineType]
    Light: _ClassVar[SplineType]
    ProceduralObject: _ClassVar[SplineType]
    RiggedObject: _ClassVar[SplineType]
    OBJModel: _ClassVar[SplineType]
    ScaleNode: _ClassVar[SplineType]
    SubdivisionObject: _ClassVar[SplineType]
    GenericNURBSCurve: _ClassVar[SplineType]
    Video: _ClassVar[SplineType]
    GenericNURBSSurface: _ClassVar[SplineType]
    TrimmedNURBSSurface: _ClassVar[SplineType]
    Gumball: _ClassVar[SplineType]
    GenericRiggedObject: _ClassVar[SplineType]
    Camera: _ClassVar[SplineType]
    DimensionObject: _ClassVar[SplineType]
    Avatar: _ClassVar[SplineType]
    Annotation: _ClassVar[SplineType]

class ExtraDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NA: _ClassVar[ExtraDataType]
    RevolveExtra: _ClassVar[ExtraDataType]
    StrokeExtra: _ClassVar[ExtraDataType]
    SplineCurvedSurfaceExtra: _ClassVar[ExtraDataType]
    SplineNURBSSurfaceExtra: _ClassVar[ExtraDataType]
    RiggedModelExtra: _ClassVar[ExtraDataType]
    TextSketchObjectExtra: _ClassVar[ExtraDataType]
    PrimitiveShapeExtra: _ClassVar[ExtraDataType]
    ReferenceImageExtra: _ClassVar[ExtraDataType]
    MeshContentExtra: _ClassVar[ExtraDataType]
    ProceduralObjectExtra: _ClassVar[ExtraDataType]
    SubdivisionObjectExtra: _ClassVar[ExtraDataType]
    GenericNURBSCurveExtra: _ClassVar[ExtraDataType]
    VideoExtra: _ClassVar[ExtraDataType]
    GenericNURBSSurfaceExtra: _ClassVar[ExtraDataType]
    TrimmedNURBSSurfaceExtra: _ClassVar[ExtraDataType]
    GenericRiggedObjectExtra: _ClassVar[ExtraDataType]
    CameraSketchObjectExtra: _ClassVar[ExtraDataType]
    DimensionObjectExtra: _ClassVar[ExtraDataType]
    AnnotationSketchObjectExtra: _ClassVar[ExtraDataType]
    InteractionTriggerExtra: _ClassVar[ExtraDataType]
    InteractionActionExtra: _ClassVar[ExtraDataType]

class TransformSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Sketch: _ClassVar[TransformSpace]
    World: _ClassVar[TransformSpace]
    Local: _ClassVar[TransformSpace]

class MirrorTransformType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Invalid: _ClassVar[MirrorTransformType]
    WorldMirror: _ClassVar[MirrorTransformType]
    LocalMirror: _ClassVar[MirrorTransformType]

class VectorDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ClampedBSpline: _ClassVar[VectorDataType]
    Bezier: _ClassVar[VectorDataType]
    Orientations: _ClassVar[VectorDataType]
    Positions: _ClassVar[VectorDataType]
    IDPolygons: _ClassVar[VectorDataType]
    RawPolygons: _ClassVar[VectorDataType]

class BrushShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Circle: _ClassVar[BrushShape]
    Square: _ClassVar[BrushShape]
    Triangle: _ClassVar[BrushShape]
    Diamond: _ClassVar[BrushShape]
    Capsule: _ClassVar[BrushShape]
    Cylinder: _ClassVar[BrushShape]
    Cone: _ClassVar[BrushShape]
    RoundedCube: _ClassVar[BrushShape]
    SuperEllipsoid: _ClassVar[BrushShape]
    Tape: _ClassVar[BrushShape]
    Torus: _ClassVar[BrushShape]
    Plane: _ClassVar[BrushShape]
    Circle2D: _ClassVar[BrushShape]
    Revolve: _ClassVar[BrushShape]
    DeprecatedSubDCube: _ClassVar[BrushShape]
    FakeNewRoundedCube: _ClassVar[BrushShape]
    ThinLine: _ClassVar[BrushShape]
    Pill: _ClassVar[BrushShape]

class StrokeCapType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FlatCap: _ClassVar[StrokeCapType]
    Round: _ClassVar[StrokeCapType]
    NonPoly: _ClassVar[StrokeCapType]

class AnchorPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Center: _ClassVar[AnchorPosition]
    Front: _ClassVar[AnchorPosition]

class ReadoutUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Metric: _ClassVar[ReadoutUnit]
    Imperial: _ClassVar[ReadoutUnit]

class OverrideUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AutoUnit: _ClassVar[OverrideUnit]
    Metres: _ClassVar[OverrideUnit]
    Centimetres: _ClassVar[OverrideUnit]
    Millimetres: _ClassVar[OverrideUnit]
    Inches: _ClassVar[OverrideUnit]
    Feet: _ClassVar[OverrideUnit]

class OffsetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidOffset: _ClassVar[OffsetType]
    None: _ClassVar[OffsetType]
    Thicken: _ClassVar[OffsetType]
    Offset: _ClassVar[OffsetType]

class TextAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TextAlignmentUndefined: _ClassVar[TextAlignment]
    TextAlignmentBase: _ClassVar[TextAlignment]
    TextAlignmentStart: _ClassVar[TextAlignment]
    TextAlignmentCenter: _ClassVar[TextAlignment]
    TextAlignmentEnd: _ClassVar[TextAlignment]
    TextAlignmentJustified: _ClassVar[TextAlignment]

class VideoLoopState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LoopStateTrue: _ClassVar[VideoLoopState]
    LoopStateFalse: _ClassVar[VideoLoopState]

class VideoAutoPlayState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AutoPlayStateTrue: _ClassVar[VideoAutoPlayState]
    AutoPlayStateFalse: _ClassVar[VideoAutoPlayState]

class VideoSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VideoAssetInFile: _ClassVar[VideoSource]
    PublicContentVideoAsset: _ClassVar[VideoSource]

class UsageHint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ExitPencilMode: _ClassVar[UsageHint]
    ToggleEditPanelBasic: _ClassVar[UsageHint]
    ToggleEditPanelAdvanced: _ClassVar[UsageHint]
    V6IntroTutorial: _ClassVar[UsageHint]
    SelectionGumball: _ClassVar[UsageHint]
    SelectionGumballGrabHandle: _ClassVar[UsageHint]
    SelectionGumballShiftHandle: _ClassVar[UsageHint]
    SwitchPipetteAndPaint: _ClassVar[UsageHint]
    Pipette: _ClassVar[UsageHint]
    TextureManipulation: _ClassVar[UsageHint]
    BrushMenu: _ClassVar[UsageHint]
    BrushEditMenu: _ClassVar[UsageHint]
    RibbonAxisMenu: _ClassVar[UsageHint]
    ImageSnapping: _ClassVar[UsageHint]
    EditModeTools: _ClassVar[UsageHint]

class LevelOfDetail(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Original: _ClassVar[LevelOfDetail]
    High: _ClassVar[LevelOfDetail]
    Mid: _ClassVar[LevelOfDetail]
    Low: _ClassVar[LevelOfDetail]
    VeryLow: _ClassVar[LevelOfDetail]
    Lowest: _ClassVar[LevelOfDetail]
    Box: _ClassVar[LevelOfDetail]
LegacyPresets: MaterialVersion
V1ConfigurableProperties: MaterialVersion
Standard: BaseMaterialType
Flat: BaseMaterialType
Reflective: BaseMaterialType
Cartoon: BaseMaterialType
XRay: BaseMaterialType
Mobile: BaseMaterialType
LowPoly: BaseMaterialType
Stipped: BaseMaterialType
Phong: BaseMaterialType
Glossy: BaseMaterialType
UI: BaseMaterialType
Preview: BaseMaterialType
Inktober: BaseMaterialType
Revolution: SplineType
Magic: SplineType
Lines: SplineType
Solid: SplineType
CurvedSurface: SplineType
Primitive: SplineType
NURBSSurface: SplineType
SketchText: SplineType
ConvexHull: SplineType
UIHandle: SplineType
ControlGizmo: SplineType
ReferenceImage: SplineType
MenuItem: SplineType
Light: SplineType
ProceduralObject: SplineType
RiggedObject: SplineType
OBJModel: SplineType
ScaleNode: SplineType
SubdivisionObject: SplineType
GenericNURBSCurve: SplineType
Video: SplineType
GenericNURBSSurface: SplineType
TrimmedNURBSSurface: SplineType
Gumball: SplineType
GenericRiggedObject: SplineType
Camera: SplineType
DimensionObject: SplineType
Avatar: SplineType
Annotation: SplineType
NA: ExtraDataType
RevolveExtra: ExtraDataType
StrokeExtra: ExtraDataType
SplineCurvedSurfaceExtra: ExtraDataType
SplineNURBSSurfaceExtra: ExtraDataType
RiggedModelExtra: ExtraDataType
TextSketchObjectExtra: ExtraDataType
PrimitiveShapeExtra: ExtraDataType
ReferenceImageExtra: ExtraDataType
MeshContentExtra: ExtraDataType
ProceduralObjectExtra: ExtraDataType
SubdivisionObjectExtra: ExtraDataType
GenericNURBSCurveExtra: ExtraDataType
VideoExtra: ExtraDataType
GenericNURBSSurfaceExtra: ExtraDataType
TrimmedNURBSSurfaceExtra: ExtraDataType
GenericRiggedObjectExtra: ExtraDataType
CameraSketchObjectExtra: ExtraDataType
DimensionObjectExtra: ExtraDataType
AnnotationSketchObjectExtra: ExtraDataType
InteractionTriggerExtra: ExtraDataType
InteractionActionExtra: ExtraDataType
Sketch: TransformSpace
World: TransformSpace
Local: TransformSpace
Invalid: MirrorTransformType
WorldMirror: MirrorTransformType
LocalMirror: MirrorTransformType
ClampedBSpline: VectorDataType
Bezier: VectorDataType
Orientations: VectorDataType
Positions: VectorDataType
IDPolygons: VectorDataType
RawPolygons: VectorDataType
Circle: BrushShape
Square: BrushShape
Triangle: BrushShape
Diamond: BrushShape
Capsule: BrushShape
Cylinder: BrushShape
Cone: BrushShape
RoundedCube: BrushShape
SuperEllipsoid: BrushShape
Tape: BrushShape
Torus: BrushShape
Plane: BrushShape
Circle2D: BrushShape
Revolve: BrushShape
DeprecatedSubDCube: BrushShape
FakeNewRoundedCube: BrushShape
ThinLine: BrushShape
Pill: BrushShape
FlatCap: StrokeCapType
Round: StrokeCapType
NonPoly: StrokeCapType
Center: AnchorPosition
Front: AnchorPosition
Metric: ReadoutUnit
Imperial: ReadoutUnit
AutoUnit: OverrideUnit
Metres: OverrideUnit
Centimetres: OverrideUnit
Millimetres: OverrideUnit
Inches: OverrideUnit
Feet: OverrideUnit
InvalidOffset: OffsetType
None: OffsetType
Thicken: OffsetType
Offset: OffsetType
TextAlignmentUndefined: TextAlignment
TextAlignmentBase: TextAlignment
TextAlignmentStart: TextAlignment
TextAlignmentCenter: TextAlignment
TextAlignmentEnd: TextAlignment
TextAlignmentJustified: TextAlignment
LoopStateTrue: VideoLoopState
LoopStateFalse: VideoLoopState
AutoPlayStateTrue: VideoAutoPlayState
AutoPlayStateFalse: VideoAutoPlayState
VideoAssetInFile: VideoSource
PublicContentVideoAsset: VideoSource
ExitPencilMode: UsageHint
ToggleEditPanelBasic: UsageHint
ToggleEditPanelAdvanced: UsageHint
V6IntroTutorial: UsageHint
SelectionGumball: UsageHint
SelectionGumballGrabHandle: UsageHint
SelectionGumballShiftHandle: UsageHint
SwitchPipetteAndPaint: UsageHint
Pipette: UsageHint
TextureManipulation: UsageHint
BrushMenu: UsageHint
BrushEditMenu: UsageHint
RibbonAxisMenu: UsageHint
ImageSnapping: UsageHint
EditModeTools: UsageHint
Original: LevelOfDetail
High: LevelOfDetail
Mid: LevelOfDetail
Low: LevelOfDetail
VeryLow: LevelOfDetail
Lowest: LevelOfDetail
Box: LevelOfDetail

class GSDataID(_message.Message):
    __slots__ = ("msb", "lsb")
    MSB_FIELD_NUMBER: _ClassVar[int]
    LSB_FIELD_NUMBER: _ClassVar[int]
    msb: int
    lsb: int
    def __init__(self, msb: _Optional[int] = ..., lsb: _Optional[int] = ...) -> None: ...

class GSDataID2(_message.Message):
    __slots__ = ("id1", "id2")
    ID1_FIELD_NUMBER: _ClassVar[int]
    ID2_FIELD_NUMBER: _ClassVar[int]
    id1: GSDataID
    id2: GSDataID
    def __init__(self, id1: _Optional[_Union[GSDataID, _Mapping]] = ..., id2: _Optional[_Union[GSDataID, _Mapping]] = ...) -> None: ...

class DrawMaterial(_message.Message):
    __slots__ = ("Guid", "materialType", "mainColorR", "mainColorG", "mainColorB", "mainColorA", "name", "isImported", "mainTexture", "ignoreTextureTransparency", "mainTextureTransform", "roughness", "metallic", "clearCoat", "specularHueShift", "receiveShadows", "shadowSoftness", "outlined", "outlineWidth", "outlineColorR", "outlineColorG", "outlineColorB")
    GUID_FIELD_NUMBER: _ClassVar[int]
    MATERIALTYPE_FIELD_NUMBER: _ClassVar[int]
    MAINCOLORR_FIELD_NUMBER: _ClassVar[int]
    MAINCOLORG_FIELD_NUMBER: _ClassVar[int]
    MAINCOLORB_FIELD_NUMBER: _ClassVar[int]
    MAINCOLORA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ISIMPORTED_FIELD_NUMBER: _ClassVar[int]
    MAINTEXTURE_FIELD_NUMBER: _ClassVar[int]
    IGNORETEXTURETRANSPARENCY_FIELD_NUMBER: _ClassVar[int]
    MAINTEXTURETRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ROUGHNESS_FIELD_NUMBER: _ClassVar[int]
    METALLIC_FIELD_NUMBER: _ClassVar[int]
    CLEARCOAT_FIELD_NUMBER: _ClassVar[int]
    SPECULARHUESHIFT_FIELD_NUMBER: _ClassVar[int]
    RECEIVESHADOWS_FIELD_NUMBER: _ClassVar[int]
    SHADOWSOFTNESS_FIELD_NUMBER: _ClassVar[int]
    OUTLINED_FIELD_NUMBER: _ClassVar[int]
    OUTLINEWIDTH_FIELD_NUMBER: _ClassVar[int]
    OUTLINECOLORR_FIELD_NUMBER: _ClassVar[int]
    OUTLINECOLORG_FIELD_NUMBER: _ClassVar[int]
    OUTLINECOLORB_FIELD_NUMBER: _ClassVar[int]
    Guid: str
    materialType: BaseMaterialType
    mainColorR: int
    mainColorG: int
    mainColorB: int
    mainColorA: int
    name: str
    isImported: bool
    mainTexture: _gravi_unity_pb2.Texture2DTO
    ignoreTextureTransparency: bool
    mainTextureTransform: MainTextureTransform
    roughness: float
    metallic: float
    clearCoat: bool
    specularHueShift: float
    receiveShadows: bool
    shadowSoftness: float
    outlined: bool
    outlineWidth: float
    outlineColorR: int
    outlineColorG: int
    outlineColorB: int
    def __init__(self, Guid: _Optional[str] = ..., materialType: _Optional[_Union[BaseMaterialType, str]] = ..., mainColorR: _Optional[int] = ..., mainColorG: _Optional[int] = ..., mainColorB: _Optional[int] = ..., mainColorA: _Optional[int] = ..., name: _Optional[str] = ..., isImported: bool = ..., mainTexture: _Optional[_Union[_gravi_unity_pb2.Texture2DTO, _Mapping]] = ..., ignoreTextureTransparency: bool = ..., mainTextureTransform: _Optional[_Union[MainTextureTransform, _Mapping]] = ..., roughness: _Optional[float] = ..., metallic: _Optional[float] = ..., clearCoat: bool = ..., specularHueShift: _Optional[float] = ..., receiveShadows: bool = ..., shadowSoftness: _Optional[float] = ..., outlined: bool = ..., outlineWidth: _Optional[float] = ..., outlineColorR: _Optional[int] = ..., outlineColorG: _Optional[int] = ..., outlineColorB: _Optional[int] = ...) -> None: ...

class MainTextureTransform(_message.Message):
    __slots__ = ("inUse", "offsetX", "offsetY", "scaleX", "scaleY", "rotation")
    INUSE_FIELD_NUMBER: _ClassVar[int]
    OFFSETX_FIELD_NUMBER: _ClassVar[int]
    OFFSETY_FIELD_NUMBER: _ClassVar[int]
    SCALEX_FIELD_NUMBER: _ClassVar[int]
    SCALEY_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    inUse: bool
    offsetX: float
    offsetY: float
    scaleX: float
    scaleY: float
    rotation: float
    def __init__(self, inUse: bool = ..., offsetX: _Optional[float] = ..., offsetY: _Optional[float] = ..., scaleX: _Optional[float] = ..., scaleY: _Optional[float] = ..., rotation: _Optional[float] = ...) -> None: ...

class LayerModelTO(_message.Message):
    __slots__ = ("guid", "layerName", "baseVisibility", "locked", "ownerClientId", "revisionId", "localOrder", "layerHidden", "group", "lastKnownUserColourR", "lastKnownUserColourG", "lastKnownUserColourB", "lastKnownUserColourA")
    GUID_FIELD_NUMBER: _ClassVar[int]
    LAYERNAME_FIELD_NUMBER: _ClassVar[int]
    BASEVISIBILITY_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    OWNERCLIENTID_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    LOCALORDER_FIELD_NUMBER: _ClassVar[int]
    LAYERHIDDEN_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    LASTKNOWNUSERCOLOURR_FIELD_NUMBER: _ClassVar[int]
    LASTKNOWNUSERCOLOURG_FIELD_NUMBER: _ClassVar[int]
    LASTKNOWNUSERCOLOURB_FIELD_NUMBER: _ClassVar[int]
    LASTKNOWNUSERCOLOURA_FIELD_NUMBER: _ClassVar[int]
    guid: str
    layerName: str
    baseVisibility: float
    locked: bool
    ownerClientId: int
    revisionId: int
    localOrder: float
    layerHidden: bool
    group: bool
    lastKnownUserColourR: int
    lastKnownUserColourG: int
    lastKnownUserColourB: int
    lastKnownUserColourA: int
    def __init__(self, guid: _Optional[str] = ..., layerName: _Optional[str] = ..., baseVisibility: _Optional[float] = ..., locked: bool = ..., ownerClientId: _Optional[int] = ..., revisionId: _Optional[int] = ..., localOrder: _Optional[float] = ..., layerHidden: bool = ..., group: bool = ..., lastKnownUserColourR: _Optional[int] = ..., lastKnownUserColourG: _Optional[int] = ..., lastKnownUserColourB: _Optional[int] = ..., lastKnownUserColourA: _Optional[int] = ...) -> None: ...

class NestedLayerRelationship(_message.Message):
    __slots__ = ("id", "layerId", "parentLayerId")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYERID_FIELD_NUMBER: _ClassVar[int]
    PARENTLAYERID_FIELD_NUMBER: _ClassVar[int]
    id: str
    layerId: str
    parentLayerId: str
    def __init__(self, id: _Optional[str] = ..., layerId: _Optional[str] = ..., parentLayerId: _Optional[str] = ...) -> None: ...

class MirrorTransformState(_message.Message):
    __slots__ = ("mirrorTransformType", "mirrorTransform")
    MIRRORTRANSFORMTYPE_FIELD_NUMBER: _ClassVar[int]
    MIRRORTRANSFORM_FIELD_NUMBER: _ClassVar[int]
    mirrorTransformType: MirrorTransformType
    mirrorTransform: _gravi_unity_pb2.TransformTO
    def __init__(self, mirrorTransformType: _Optional[_Union[MirrorTransformType, str]] = ..., mirrorTransform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ...) -> None: ...

class RotationalSymmetryData(_message.Message):
    __slots__ = ("DuplicateCount", "RotationAmount")
    DUPLICATECOUNT_FIELD_NUMBER: _ClassVar[int]
    ROTATIONAMOUNT_FIELD_NUMBER: _ClassVar[int]
    DuplicateCount: int
    RotationAmount: int
    def __init__(self, DuplicateCount: _Optional[int] = ..., RotationAmount: _Optional[int] = ...) -> None: ...

class PolygonVertex(_message.Message):
    __slots__ = ("ID", "positionX", "positionY", "positionZ", "isOnMirror")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITIONX_FIELD_NUMBER: _ClassVar[int]
    POSITIONY_FIELD_NUMBER: _ClassVar[int]
    POSITIONZ_FIELD_NUMBER: _ClassVar[int]
    ISONMIRROR_FIELD_NUMBER: _ClassVar[int]
    ID: GSDataID
    positionX: float
    positionY: float
    positionZ: float
    isOnMirror: bool
    def __init__(self, ID: _Optional[_Union[GSDataID, _Mapping]] = ..., positionX: _Optional[float] = ..., positionY: _Optional[float] = ..., positionZ: _Optional[float] = ..., isOnMirror: bool = ...) -> None: ...

class Polygon(_message.Message):
    __slots__ = ("ID", "vertices")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    ID: GSDataID
    vertices: _containers.RepeatedCompositeFieldContainer[GSDataID]
    def __init__(self, ID: _Optional[_Union[GSDataID, _Mapping]] = ..., vertices: _Optional[_Iterable[_Union[GSDataID, _Mapping]]] = ...) -> None: ...

class CreasedPolygonEdge(_message.Message):
    __slots__ = ("ID",)
    ID_FIELD_NUMBER: _ClassVar[int]
    ID: GSDataID2
    def __init__(self, ID: _Optional[_Union[GSDataID2, _Mapping]] = ...) -> None: ...

class DeprecatedViewPointModelTO(_message.Message):
    __slots__ = ("guid", "name", "cameraPositionX", "cameraPositionY", "cameraPositionZ", "cameraRotationX", "cameraRotationY", "cameraRotationZ", "cameraRotationW", "cameraSettings", "headPositionX", "headPositionY", "headPositionZ", "headRotationX", "headRotationY", "headRotationZ", "headRotationW", "sketchScale")
    GUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAMERAPOSITIONX_FIELD_NUMBER: _ClassVar[int]
    CAMERAPOSITIONY_FIELD_NUMBER: _ClassVar[int]
    CAMERAPOSITIONZ_FIELD_NUMBER: _ClassVar[int]
    CAMERAROTATIONX_FIELD_NUMBER: _ClassVar[int]
    CAMERAROTATIONY_FIELD_NUMBER: _ClassVar[int]
    CAMERAROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    CAMERAROTATIONW_FIELD_NUMBER: _ClassVar[int]
    CAMERASETTINGS_FIELD_NUMBER: _ClassVar[int]
    HEADPOSITIONX_FIELD_NUMBER: _ClassVar[int]
    HEADPOSITIONY_FIELD_NUMBER: _ClassVar[int]
    HEADPOSITIONZ_FIELD_NUMBER: _ClassVar[int]
    HEADROTATIONX_FIELD_NUMBER: _ClassVar[int]
    HEADROTATIONY_FIELD_NUMBER: _ClassVar[int]
    HEADROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    HEADROTATIONW_FIELD_NUMBER: _ClassVar[int]
    SKETCHSCALE_FIELD_NUMBER: _ClassVar[int]
    guid: str
    name: str
    cameraPositionX: float
    cameraPositionY: float
    cameraPositionZ: float
    cameraRotationX: float
    cameraRotationY: float
    cameraRotationZ: float
    cameraRotationW: float
    cameraSettings: CameraSettings
    headPositionX: float
    headPositionY: float
    headPositionZ: float
    headRotationX: float
    headRotationY: float
    headRotationZ: float
    headRotationW: float
    sketchScale: float
    def __init__(self, guid: _Optional[str] = ..., name: _Optional[str] = ..., cameraPositionX: _Optional[float] = ..., cameraPositionY: _Optional[float] = ..., cameraPositionZ: _Optional[float] = ..., cameraRotationX: _Optional[float] = ..., cameraRotationY: _Optional[float] = ..., cameraRotationZ: _Optional[float] = ..., cameraRotationW: _Optional[float] = ..., cameraSettings: _Optional[_Union[CameraSettings, _Mapping]] = ..., headPositionX: _Optional[float] = ..., headPositionY: _Optional[float] = ..., headPositionZ: _Optional[float] = ..., headRotationX: _Optional[float] = ..., headRotationY: _Optional[float] = ..., headRotationZ: _Optional[float] = ..., headRotationW: _Optional[float] = ..., sketchScale: _Optional[float] = ...) -> None: ...

class CameraSettings(_message.Message):
    __slots__ = ("focalLength", "orthographic", "orthographicSize")
    FOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    ORTHOGRAPHIC_FIELD_NUMBER: _ClassVar[int]
    ORTHOGRAPHICSIZE_FIELD_NUMBER: _ClassVar[int]
    focalLength: float
    orthographic: bool
    orthographicSize: float
    def __init__(self, focalLength: _Optional[float] = ..., orthographic: bool = ..., orthographicSize: _Optional[float] = ...) -> None: ...

class OffsetData(_message.Message):
    __slots__ = ("type", "value", "offsetGizmoIDs")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    OFFSETGIZMOIDS_FIELD_NUMBER: _ClassVar[int]
    type: OffsetType
    value: float
    offsetGizmoIDs: _containers.RepeatedCompositeFieldContainer[GSDataID]
    def __init__(self, type: _Optional[_Union[OffsetType, str]] = ..., value: _Optional[float] = ..., offsetGizmoIDs: _Optional[_Iterable[_Union[GSDataID, _Mapping]]] = ...) -> None: ...

class PersistentSpatialAnchorInformation(_message.Message):
    __slots__ = ("anchorPersistentID", "transformOfSketchOriginRelativeToAnchor")
    ANCHORPERSISTENTID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMOFSKETCHORIGINRELATIVETOANCHOR_FIELD_NUMBER: _ClassVar[int]
    anchorPersistentID: _containers.RepeatedScalarFieldContainer[str]
    transformOfSketchOriginRelativeToAnchor: _containers.RepeatedCompositeFieldContainer[_gravi_unity_pb2.TransformTO]
    def __init__(self, anchorPersistentID: _Optional[_Iterable[str]] = ..., transformOfSketchOriginRelativeToAnchor: _Optional[_Iterable[_Union[_gravi_unity_pb2.TransformTO, _Mapping]]] = ...) -> None: ...

class ImportedObjectMetaData(_message.Message):
    __slots__ = ("objectName", "nodePath", "hasMaterial")
    OBJECTNAME_FIELD_NUMBER: _ClassVar[int]
    NODEPATH_FIELD_NUMBER: _ClassVar[int]
    HASMATERIAL_FIELD_NUMBER: _ClassVar[int]
    objectName: str
    nodePath: str
    hasMaterial: bool
    def __init__(self, objectName: _Optional[str] = ..., nodePath: _Optional[str] = ..., hasMaterial: bool = ...) -> None: ...

class SectionViewData(_message.Message):
    __slots__ = ("sectionBoxTransform", "active")
    SECTIONBOXTRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    sectionBoxTransform: _gravi_unity_pb2.TransformTO
    active: bool
    def __init__(self, sectionBoxTransform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., active: bool = ...) -> None: ...

class MeshLODCollection(_message.Message):
    __slots__ = ("id", "meshes", "meshName")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESHES_FIELD_NUMBER: _ClassVar[int]
    MESHNAME_FIELD_NUMBER: _ClassVar[int]
    id: GSDataID
    meshes: _containers.RepeatedCompositeFieldContainer[MeshMetadata]
    meshName: str
    def __init__(self, id: _Optional[_Union[GSDataID, _Mapping]] = ..., meshes: _Optional[_Iterable[_Union[MeshMetadata, _Mapping]]] = ..., meshName: _Optional[str] = ...) -> None: ...

class MeshMetadata(_message.Message):
    __slots__ = ("meshGuid", "levelOfDetail", "filesize")
    MESHGUID_FIELD_NUMBER: _ClassVar[int]
    LEVELOFDETAIL_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    meshGuid: str
    levelOfDetail: LevelOfDetail
    filesize: int
    def __init__(self, meshGuid: _Optional[str] = ..., levelOfDetail: _Optional[_Union[LevelOfDetail, str]] = ..., filesize: _Optional[int] = ...) -> None: ...

class SelfOnboardingRoomProgressCollection(_message.Message):
    __slots__ = ("progresses",)
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[SelfOnboardingRoomProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[SelfOnboardingRoomProgress, _Mapping]]] = ...) -> None: ...

class SelfOnboardingRoomProgress(_message.Message):
    __slots__ = ("roomId", "videoCount", "completedVideoPublicContentPaths")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    VIDEOCOUNT_FIELD_NUMBER: _ClassVar[int]
    COMPLETEDVIDEOPUBLICCONTENTPATHS_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    videoCount: int
    completedVideoPublicContentPaths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, roomId: _Optional[str] = ..., videoCount: _Optional[int] = ..., completedVideoPublicContentPaths: _Optional[_Iterable[str]] = ...) -> None: ...
