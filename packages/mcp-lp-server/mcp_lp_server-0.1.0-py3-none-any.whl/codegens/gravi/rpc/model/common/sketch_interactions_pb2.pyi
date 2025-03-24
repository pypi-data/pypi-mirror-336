from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.rpc.model.common import sketch_configurable_ui_pb2 as _sketch_configurable_ui_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InteractionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidInteractionMode: _ClassVar[InteractionMode]
    Idle: _ClassVar[InteractionMode]
    Drawing: _ClassVar[InteractionMode]
    Grabbing: _ClassVar[InteractionMode]
    UIUsing: _ClassVar[InteractionMode]
    ToolSwitching: _ClassVar[InteractionMode]
    Typing: _ClassVar[InteractionMode]

class SketchEditorMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidSketchEditorMode: _ClassVar[SketchEditorMode]
    Creation: _ClassVar[SketchEditorMode]
    ControlPoint: _ClassVar[SketchEditorMode]
    SubDCustomisePrimitive: _ClassVar[SketchEditorMode]
    MiniMap: _ClassVar[SketchEditorMode]
    ViewPointEdit: _ClassVar[SketchEditorMode]
    Viewer: _ClassVar[SketchEditorMode]
    Import: _ClassVar[SketchEditorMode]
    InkShortageGame: _ClassVar[SketchEditorMode]

class ToggleHideObjectsSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Toggle: _ClassVar[ToggleHideObjectsSetting]
    SetHidden: _ClassVar[ToggleHideObjectsSetting]
    SetVisible: _ClassVar[ToggleHideObjectsSetting]

class OffHandQuickAccessMenuLockType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NotLocked: _ClassVar[OffHandQuickAccessMenuLockType]
    LockedExceptExit: _ClassVar[OffHandQuickAccessMenuLockType]
    LockedIncludingExit: _ClassVar[OffHandQuickAccessMenuLockType]

class PopupAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AddNewPopup: _ClassVar[PopupAction]
    AddAsOnlyPopup: _ClassVar[PopupAction]
    ClearAnyPopupsOnTarget: _ClassVar[PopupAction]
    ClearAllPopups: _ClassVar[PopupAction]

class LayerTransparencyThresholdListenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WhenTransitionAboveThreshold: _ClassVar[LayerTransparencyThresholdListenType]
    WhenTransitionBelowThreshold: _ClassVar[LayerTransparencyThresholdListenType]

class VRControllerButtonType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IndexTrigger: _ClassVar[VRControllerButtonType]
    GrabTrigger: _ClassVar[VRControllerButtonType]
    UpperFaceButton: _ClassVar[VRControllerButtonType]
    LowerFaceButton: _ClassVar[VRControllerButtonType]
    ThumbstickMoveAny: _ClassVar[VRControllerButtonType]

class VRControllerButtonListenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OnButtonDown: _ClassVar[VRControllerButtonListenType]
    OnButtonUp: _ClassVar[VRControllerButtonListenType]
    OnButtonLongPress: _ClassVar[VRControllerButtonListenType]

class CheckUserScaleSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoScaleCheck: _ClassVar[CheckUserScaleSetting]
    BelowUpperBound: _ClassVar[CheckUserScaleSetting]
    AboveLowerBound: _ClassVar[CheckUserScaleSetting]
    BetweenUpperAndLowerBounds: _ClassVar[CheckUserScaleSetting]

class VRMenuListenerMenuType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OffHandQuickAccessMenu: _ClassVar[VRMenuListenerMenuType]
    MainBlueMenu: _ClassVar[VRMenuListenerMenuType]
    BrushToolsMenu: _ClassVar[VRMenuListenerMenuType]
    ColourMenu: _ClassVar[VRMenuListenerMenuType]

class HighlightAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EnableHighlight: _ClassVar[HighlightAction]
    DisableHighlight: _ClassVar[HighlightAction]
    DisableAllHighlights: _ClassVar[HighlightAction]

class ParticleEffectAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AddEffect: _ClassVar[ParticleEffectAction]
    RemoveEffect: _ClassVar[ParticleEffectAction]
    RemoveAllEffects: _ClassVar[ParticleEffectAction]

class UserRestrictionLockType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DrawingLock: _ClassVar[UserRestrictionLockType]
    MainMenuLock: _ClassVar[UserRestrictionLockType]
    BrushMenuLock: _ClassVar[UserRestrictionLockType]
    EditModeLock: _ClassVar[UserRestrictionLockType]
    GrabObjectLock: _ClassVar[UserRestrictionLockType]
    GrabMoveLock: _ClassVar[UserRestrictionLockType]
    GrabScaleLock: _ClassVar[UserRestrictionLockType]
    ScaleGrabShapeLock: _ClassVar[UserRestrictionLockType]
    GrabDeleteLock: _ClassVar[UserRestrictionLockType]
    DuplicateLock: _ClassVar[UserRestrictionLockType]
    UndoButtonLock: _ClassVar[UserRestrictionLockType]
    UndoRedoClockLock: _ClassVar[UserRestrictionLockType]
    BrushScaleLock: _ClassVar[UserRestrictionLockType]
    SmartMoveLock: _ClassVar[UserRestrictionLockType]
    MinimapLock: _ClassVar[UserRestrictionLockType]
    QuickAccessMenuAllExceptExit: _ClassVar[UserRestrictionLockType]
    QuickAccessMenuAllIncludingExit: _ClassVar[UserRestrictionLockType]
    VerticalOrientationLock: _ClassVar[UserRestrictionLockType]
    NavigationLockLock: _ClassVar[UserRestrictionLockType]
    GrabShapeLock: _ClassVar[UserRestrictionLockType]
    PassthroughSwitchingLock: _ClassVar[UserRestrictionLockType]
    ClockSettingsLock: _ClassVar[UserRestrictionLockType]
    GrabScaleObjectLock: _ClassVar[UserRestrictionLockType]
    TurntableLock: _ClassVar[UserRestrictionLockType]
    PointerLock: _ClassVar[UserRestrictionLockType]
    AllMainHandGrabLock: _ClassVar[UserRestrictionLockType]
    SketchToolLock: _ClassVar[UserRestrictionLockType]
    OpenUIMenusLock: _ClassVar[UserRestrictionLockType]
    PencilModeLock: _ClassVar[UserRestrictionLockType]
    SwitchViewpointLock: _ClassVar[UserRestrictionLockType]
    MainThumbstickToggleLock: _ClassVar[UserRestrictionLockType]
    ToolSwitcherLock: _ClassVar[UserRestrictionLockType]
    AllMoveSketchLock: _ClassVar[UserRestrictionLockType]
    SelectionLock: _ClassVar[UserRestrictionLockType]
    GrabbedObjectsSnapLock: _ClassVar[UserRestrictionLockType]
    EditModeSlideConstraints: _ClassVar[UserRestrictionLockType]
    LayersMenuLock: _ClassVar[UserRestrictionLockType]
    GridLock: _ClassVar[UserRestrictionLockType]
    ExportMenuLock: _ClassVar[UserRestrictionLockType]
    MaterialsMenuLock: _ClassVar[UserRestrictionLockType]

class UserRestrictionSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidUserRestrictionSource: _ClassVar[UserRestrictionSourceType]
    InteractionSystem: _ClassVar[UserRestrictionSourceType]
    SpatialAnchors: _ClassVar[UserRestrictionSourceType]
    SketchExperience: _ClassVar[UserRestrictionSourceType]
    PencilMode: _ClassVar[UserRestrictionSourceType]
    ToolSwitcher: _ClassVar[UserRestrictionSourceType]
    ActiveTool: _ClassVar[UserRestrictionSourceType]
    MaterialChange: _ClassVar[UserRestrictionSourceType]
    UIInputRestriction: _ClassVar[UserRestrictionSourceType]
    UserFollowing: _ClassVar[UserRestrictionSourceType]
    InteractionModes: _ClassVar[UserRestrictionSourceType]
    SketchEditorModes: _ClassVar[UserRestrictionSourceType]
    ScreenshotPanel: _ClassVar[UserRestrictionSourceType]
    SubDFaceSelection: _ClassVar[UserRestrictionSourceType]
    UIInteraction: _ClassVar[UserRestrictionSourceType]
    WebBrowser: _ClassVar[UserRestrictionSourceType]
    TypingModeMonitor: _ClassVar[UserRestrictionSourceType]
    SmartMoveController: _ClassVar[UserRestrictionSourceType]
    GrabbedObjectsSnap: _ClassVar[UserRestrictionSourceType]
    ScreenAppModes: _ClassVar[UserRestrictionSourceType]
    SingleConnectionCollabRoom: _ClassVar[UserRestrictionSourceType]
InvalidInteractionMode: InteractionMode
Idle: InteractionMode
Drawing: InteractionMode
Grabbing: InteractionMode
UIUsing: InteractionMode
ToolSwitching: InteractionMode
Typing: InteractionMode
InvalidSketchEditorMode: SketchEditorMode
Creation: SketchEditorMode
ControlPoint: SketchEditorMode
SubDCustomisePrimitive: SketchEditorMode
MiniMap: SketchEditorMode
ViewPointEdit: SketchEditorMode
Viewer: SketchEditorMode
Import: SketchEditorMode
InkShortageGame: SketchEditorMode
Toggle: ToggleHideObjectsSetting
SetHidden: ToggleHideObjectsSetting
SetVisible: ToggleHideObjectsSetting
NotLocked: OffHandQuickAccessMenuLockType
LockedExceptExit: OffHandQuickAccessMenuLockType
LockedIncludingExit: OffHandQuickAccessMenuLockType
AddNewPopup: PopupAction
AddAsOnlyPopup: PopupAction
ClearAnyPopupsOnTarget: PopupAction
ClearAllPopups: PopupAction
WhenTransitionAboveThreshold: LayerTransparencyThresholdListenType
WhenTransitionBelowThreshold: LayerTransparencyThresholdListenType
IndexTrigger: VRControllerButtonType
GrabTrigger: VRControllerButtonType
UpperFaceButton: VRControllerButtonType
LowerFaceButton: VRControllerButtonType
ThumbstickMoveAny: VRControllerButtonType
OnButtonDown: VRControllerButtonListenType
OnButtonUp: VRControllerButtonListenType
OnButtonLongPress: VRControllerButtonListenType
NoScaleCheck: CheckUserScaleSetting
BelowUpperBound: CheckUserScaleSetting
AboveLowerBound: CheckUserScaleSetting
BetweenUpperAndLowerBounds: CheckUserScaleSetting
OffHandQuickAccessMenu: VRMenuListenerMenuType
MainBlueMenu: VRMenuListenerMenuType
BrushToolsMenu: VRMenuListenerMenuType
ColourMenu: VRMenuListenerMenuType
EnableHighlight: HighlightAction
DisableHighlight: HighlightAction
DisableAllHighlights: HighlightAction
AddEffect: ParticleEffectAction
RemoveEffect: ParticleEffectAction
RemoveAllEffects: ParticleEffectAction
DrawingLock: UserRestrictionLockType
MainMenuLock: UserRestrictionLockType
BrushMenuLock: UserRestrictionLockType
EditModeLock: UserRestrictionLockType
GrabObjectLock: UserRestrictionLockType
GrabMoveLock: UserRestrictionLockType
GrabScaleLock: UserRestrictionLockType
ScaleGrabShapeLock: UserRestrictionLockType
GrabDeleteLock: UserRestrictionLockType
DuplicateLock: UserRestrictionLockType
UndoButtonLock: UserRestrictionLockType
UndoRedoClockLock: UserRestrictionLockType
BrushScaleLock: UserRestrictionLockType
SmartMoveLock: UserRestrictionLockType
MinimapLock: UserRestrictionLockType
QuickAccessMenuAllExceptExit: UserRestrictionLockType
QuickAccessMenuAllIncludingExit: UserRestrictionLockType
VerticalOrientationLock: UserRestrictionLockType
NavigationLockLock: UserRestrictionLockType
GrabShapeLock: UserRestrictionLockType
PassthroughSwitchingLock: UserRestrictionLockType
ClockSettingsLock: UserRestrictionLockType
GrabScaleObjectLock: UserRestrictionLockType
TurntableLock: UserRestrictionLockType
PointerLock: UserRestrictionLockType
AllMainHandGrabLock: UserRestrictionLockType
SketchToolLock: UserRestrictionLockType
OpenUIMenusLock: UserRestrictionLockType
PencilModeLock: UserRestrictionLockType
SwitchViewpointLock: UserRestrictionLockType
MainThumbstickToggleLock: UserRestrictionLockType
ToolSwitcherLock: UserRestrictionLockType
AllMoveSketchLock: UserRestrictionLockType
SelectionLock: UserRestrictionLockType
GrabbedObjectsSnapLock: UserRestrictionLockType
EditModeSlideConstraints: UserRestrictionLockType
LayersMenuLock: UserRestrictionLockType
GridLock: UserRestrictionLockType
ExportMenuLock: UserRestrictionLockType
MaterialsMenuLock: UserRestrictionLockType
InvalidUserRestrictionSource: UserRestrictionSourceType
InteractionSystem: UserRestrictionSourceType
SpatialAnchors: UserRestrictionSourceType
SketchExperience: UserRestrictionSourceType
PencilMode: UserRestrictionSourceType
ToolSwitcher: UserRestrictionSourceType
ActiveTool: UserRestrictionSourceType
MaterialChange: UserRestrictionSourceType
UIInputRestriction: UserRestrictionSourceType
UserFollowing: UserRestrictionSourceType
InteractionModes: UserRestrictionSourceType
SketchEditorModes: UserRestrictionSourceType
ScreenshotPanel: UserRestrictionSourceType
SubDFaceSelection: UserRestrictionSourceType
UIInteraction: UserRestrictionSourceType
WebBrowser: UserRestrictionSourceType
TypingModeMonitor: UserRestrictionSourceType
SmartMoveController: UserRestrictionSourceType
GrabbedObjectsSnap: UserRestrictionSourceType
ScreenAppModes: UserRestrictionSourceType
SingleConnectionCollabRoom: UserRestrictionSourceType

class VRControllerButton(_message.Message):
    __slots__ = ("isMainHand", "buttonType")
    ISMAINHAND_FIELD_NUMBER: _ClassVar[int]
    BUTTONTYPE_FIELD_NUMBER: _ClassVar[int]
    isMainHand: bool
    buttonType: VRControllerButtonType
    def __init__(self, isMainHand: bool = ..., buttonType: _Optional[_Union[VRControllerButtonType, str]] = ...) -> None: ...

class UserInteractionModeState(_message.Message):
    __slots__ = ("interactionMode",)
    INTERACTIONMODE_FIELD_NUMBER: _ClassVar[int]
    interactionMode: InteractionMode
    def __init__(self, interactionMode: _Optional[_Union[InteractionMode, str]] = ...) -> None: ...

class UserSketchEditorModeState(_message.Message):
    __slots__ = ("sketchEditorMode",)
    SKETCHEDITORMODE_FIELD_NUMBER: _ClassVar[int]
    sketchEditorMode: SketchEditorMode
    def __init__(self, sketchEditorMode: _Optional[_Union[SketchEditorMode, str]] = ...) -> None: ...
