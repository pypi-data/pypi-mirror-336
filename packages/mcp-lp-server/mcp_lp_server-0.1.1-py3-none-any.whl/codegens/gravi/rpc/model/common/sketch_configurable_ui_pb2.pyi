from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PopupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Text: _ClassVar[PopupType]
    SmallText: _ClassVar[PopupType]
    PrefabContainer: _ClassVar[PopupType]
    TextAlert: _ClassVar[PopupType]

class PopupTailType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Tether: _ClassVar[PopupTailType]
    NoTail: _ClassVar[PopupTailType]
    Callout: _ClassVar[PopupTailType]

class TargetObject(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidTarget: _ClassVar[TargetObject]
    MainHandController: _ClassVar[TargetObject]
    OffHandController: _ClassVar[TargetObject]
    MainHandGripButton: _ClassVar[TargetObject]
    OffHandGripButton: _ClassVar[TargetObject]
    MainHandTrigger: _ClassVar[TargetObject]
    OffHandTrigger: _ClassVar[TargetObject]
    MainHandMenuButton: _ClassVar[TargetObject]
    OffHandMenuButton: _ClassVar[TargetObject]
    MainHandSecondButton: _ClassVar[TargetObject]
    OffHandSecondButton: _ClassVar[TargetObject]
    MainHandThumbstick: _ClassVar[TargetObject]
    OffHandThumbstick: _ClassVar[TargetObject]
    MainHandStylus: _ClassVar[TargetObject]
    OffHandStylus: _ClassVar[TargetObject]
    Cursor: _ClassVar[TargetObject]
    GrabSphere: _ClassVar[TargetObject]
    DualControllerCentre: _ClassVar[TargetObject]
    ScalePercentage: _ClassVar[TargetObject]
    StylusCursor: _ClassVar[TargetObject]
    UIQuickBugReportButton: _ClassVar[TargetObject]
    UIQuickExitSketchButton: _ClassVar[TargetObject]
    UIQuickScreenshotButton: _ClassVar[TargetObject]
    UIQuickSaveButton: _ClassVar[TargetObject]
    UIMaterialPuck: _ClassVar[TargetObject]
    UIInkTool: _ClassVar[TargetObject]
    UIStrokeTool: _ClassVar[TargetObject]
    UIRevolveTool: _ClassVar[TargetObject]
    UISurfaceTool: _ClassVar[TargetObject]
    UIVolumeTool: _ClassVar[TargetObject]
    UIPrimitivesTool: _ClassVar[TargetObject]
    UIViewpointsTool: _ClassVar[TargetObject]
    UIInteractionsTool: _ClassVar[TargetObject]
    UISaveMenu: _ClassVar[TargetObject]
    UISettingsMenu: _ClassVar[TargetObject]
    UIReferenceImagesMenu: _ClassVar[TargetObject]
    UIPrefabsMenu: _ClassVar[TargetObject]
    UILayersMenu: _ClassVar[TargetObject]
    UIOrthographicViewportMenu: _ClassVar[TargetObject]
    UILearnMenu: _ClassVar[TargetObject]
    UIDebugMenu: _ClassVar[TargetObject]
    UICollabUsersMenu: _ClassVar[TargetObject]
    UILobbyNewSketch: _ClassVar[TargetObject]
    UILobbyFileManager: _ClassVar[TargetObject]
    UILobbyCollab: _ClassVar[TargetObject]
    UILobbyBonusContent: _ClassVar[TargetObject]
    UILobbyOrgSwitcher: _ClassVar[TargetObject]
    UILobbyGallery: _ClassVar[TargetObject]
    UILobbyLearn: _ClassVar[TargetObject]
    UIGumballCentre: _ClassVar[TargetObject]
    UIGumballXArrow: _ClassVar[TargetObject]
    UIBrushMenuRibbonAxisX: _ClassVar[TargetObject]
    UISelectedBrushProfile: _ClassVar[TargetObject]
    UIQuickColorSelector: _ClassVar[TargetObject]
    UISketchToolSwitcher: _ClassVar[TargetObject]
    UIExitSketchButton: _ClassVar[TargetObject]
    UIImportPanelBuiltInModelsTab: _ClassVar[TargetObject]
    SpecifiedControlGizmo: _ClassVar[TargetObject]
    SpecifiedSketchObject: _ClassVar[TargetObject]
    MostRecentlyDrawnSketchObject: _ClassVar[TargetObject]
    SketchSpacePosition: _ClassVar[TargetObject]
    WorldSpacePosition: _ClassVar[TargetObject]
    InFrontOfUser: _ClassVar[TargetObject]
    BasicSkillsContinueButton: _ClassVar[TargetObject]
    MaterialPanelTextureManipulationButton: _ClassVar[TargetObject]

class PrefabFlipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoFlip: _ClassVar[PrefabFlipType]
    Flip: _ClassVar[PrefabFlipType]
    FlipInLeftHanded: _ClassVar[PrefabFlipType]
    FlipInRightHanded: _ClassVar[PrefabFlipType]

class PopupDisplacementSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Default: _ClassVar[PopupDisplacementSpace]
    LocalSpace: _ClassVar[PopupDisplacementSpace]
    WorldSpace: _ClassVar[PopupDisplacementSpace]
    ViewSpace: _ClassVar[PopupDisplacementSpace]

class ParticleEffectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Confetti: _ClassVar[ParticleEffectType]
    ConfettiBurst: _ClassVar[ParticleEffectType]
    Attention: _ClassVar[ParticleEffectType]
    SuccessAttention: _ClassVar[ParticleEffectType]
Text: PopupType
SmallText: PopupType
PrefabContainer: PopupType
TextAlert: PopupType
Tether: PopupTailType
NoTail: PopupTailType
Callout: PopupTailType
InvalidTarget: TargetObject
MainHandController: TargetObject
OffHandController: TargetObject
MainHandGripButton: TargetObject
OffHandGripButton: TargetObject
MainHandTrigger: TargetObject
OffHandTrigger: TargetObject
MainHandMenuButton: TargetObject
OffHandMenuButton: TargetObject
MainHandSecondButton: TargetObject
OffHandSecondButton: TargetObject
MainHandThumbstick: TargetObject
OffHandThumbstick: TargetObject
MainHandStylus: TargetObject
OffHandStylus: TargetObject
Cursor: TargetObject
GrabSphere: TargetObject
DualControllerCentre: TargetObject
ScalePercentage: TargetObject
StylusCursor: TargetObject
UIQuickBugReportButton: TargetObject
UIQuickExitSketchButton: TargetObject
UIQuickScreenshotButton: TargetObject
UIQuickSaveButton: TargetObject
UIMaterialPuck: TargetObject
UIInkTool: TargetObject
UIStrokeTool: TargetObject
UIRevolveTool: TargetObject
UISurfaceTool: TargetObject
UIVolumeTool: TargetObject
UIPrimitivesTool: TargetObject
UIViewpointsTool: TargetObject
UIInteractionsTool: TargetObject
UISaveMenu: TargetObject
UISettingsMenu: TargetObject
UIReferenceImagesMenu: TargetObject
UIPrefabsMenu: TargetObject
UILayersMenu: TargetObject
UIOrthographicViewportMenu: TargetObject
UILearnMenu: TargetObject
UIDebugMenu: TargetObject
UICollabUsersMenu: TargetObject
UILobbyNewSketch: TargetObject
UILobbyFileManager: TargetObject
UILobbyCollab: TargetObject
UILobbyBonusContent: TargetObject
UILobbyOrgSwitcher: TargetObject
UILobbyGallery: TargetObject
UILobbyLearn: TargetObject
UIGumballCentre: TargetObject
UIGumballXArrow: TargetObject
UIBrushMenuRibbonAxisX: TargetObject
UISelectedBrushProfile: TargetObject
UIQuickColorSelector: TargetObject
UISketchToolSwitcher: TargetObject
UIExitSketchButton: TargetObject
UIImportPanelBuiltInModelsTab: TargetObject
SpecifiedControlGizmo: TargetObject
SpecifiedSketchObject: TargetObject
MostRecentlyDrawnSketchObject: TargetObject
SketchSpacePosition: TargetObject
WorldSpacePosition: TargetObject
InFrontOfUser: TargetObject
BasicSkillsContinueButton: TargetObject
MaterialPanelTextureManipulationButton: TargetObject
NoFlip: PrefabFlipType
Flip: PrefabFlipType
FlipInLeftHanded: PrefabFlipType
FlipInRightHanded: PrefabFlipType
Default: PopupDisplacementSpace
LocalSpace: PopupDisplacementSpace
WorldSpace: PopupDisplacementSpace
ViewSpace: PopupDisplacementSpace
Confetti: ParticleEffectType
ConfettiBurst: ParticleEffectType
Attention: ParticleEffectType
SuccessAttention: ParticleEffectType

class PopupSettings(_message.Message):
    __slots__ = ("textReadout", "translateText", "popupType", "tailType", "popupTarget", "useCustomSize", "customSize", "sketchObjectTargetId", "prefabPath", "showContainerBackdrop", "containedPrefabFlipType", "lockToTargetOrientation", "useCustomFollowLag", "customFollowLag", "customDisplacementX", "customDisplacementY", "customDisplacementZ", "forceZeroDisplacement", "customRotationX", "customRotationY", "customRotationZ", "customRotationW")
    TEXTREADOUT_FIELD_NUMBER: _ClassVar[int]
    TRANSLATETEXT_FIELD_NUMBER: _ClassVar[int]
    POPUPTYPE_FIELD_NUMBER: _ClassVar[int]
    TAILTYPE_FIELD_NUMBER: _ClassVar[int]
    POPUPTARGET_FIELD_NUMBER: _ClassVar[int]
    USECUSTOMSIZE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMSIZE_FIELD_NUMBER: _ClassVar[int]
    SKETCHOBJECTTARGETID_FIELD_NUMBER: _ClassVar[int]
    PREFABPATH_FIELD_NUMBER: _ClassVar[int]
    SHOWCONTAINERBACKDROP_FIELD_NUMBER: _ClassVar[int]
    CONTAINEDPREFABFLIPTYPE_FIELD_NUMBER: _ClassVar[int]
    LOCKTOTARGETORIENTATION_FIELD_NUMBER: _ClassVar[int]
    USECUSTOMFOLLOWLAG_FIELD_NUMBER: _ClassVar[int]
    CUSTOMFOLLOWLAG_FIELD_NUMBER: _ClassVar[int]
    CUSTOMDISPLACEMENTX_FIELD_NUMBER: _ClassVar[int]
    CUSTOMDISPLACEMENTY_FIELD_NUMBER: _ClassVar[int]
    CUSTOMDISPLACEMENTZ_FIELD_NUMBER: _ClassVar[int]
    FORCEZERODISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOMROTATIONX_FIELD_NUMBER: _ClassVar[int]
    CUSTOMROTATIONY_FIELD_NUMBER: _ClassVar[int]
    CUSTOMROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    CUSTOMROTATIONW_FIELD_NUMBER: _ClassVar[int]
    textReadout: str
    translateText: bool
    popupType: PopupType
    tailType: PopupTailType
    popupTarget: TargetObject
    useCustomSize: bool
    customSize: float
    sketchObjectTargetId: _sketch_common_pb2.GSDataID
    prefabPath: str
    showContainerBackdrop: bool
    containedPrefabFlipType: PrefabFlipType
    lockToTargetOrientation: bool
    useCustomFollowLag: bool
    customFollowLag: float
    customDisplacementX: float
    customDisplacementY: float
    customDisplacementZ: float
    forceZeroDisplacement: bool
    customRotationX: float
    customRotationY: float
    customRotationZ: float
    customRotationW: float
    def __init__(self, textReadout: _Optional[str] = ..., translateText: bool = ..., popupType: _Optional[_Union[PopupType, str]] = ..., tailType: _Optional[_Union[PopupTailType, str]] = ..., popupTarget: _Optional[_Union[TargetObject, str]] = ..., useCustomSize: bool = ..., customSize: _Optional[float] = ..., sketchObjectTargetId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., prefabPath: _Optional[str] = ..., showContainerBackdrop: bool = ..., containedPrefabFlipType: _Optional[_Union[PrefabFlipType, str]] = ..., lockToTargetOrientation: bool = ..., useCustomFollowLag: bool = ..., customFollowLag: _Optional[float] = ..., customDisplacementX: _Optional[float] = ..., customDisplacementY: _Optional[float] = ..., customDisplacementZ: _Optional[float] = ..., forceZeroDisplacement: bool = ..., customRotationX: _Optional[float] = ..., customRotationY: _Optional[float] = ..., customRotationZ: _Optional[float] = ..., customRotationW: _Optional[float] = ...) -> None: ...
