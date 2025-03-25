from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.rpc.model.inputs import sketch_inputs_pb2 as _sketch_inputs_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriBool(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TriBoolUndefined: _ClassVar[TriBool]
    TriBoolFalse: _ClassVar[TriBool]
    TriBoolTrue: _ClassVar[TriBool]

class ToolPanelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UndefinedToolPanelType: _ClassVar[ToolPanelType]
    Ink: _ClassVar[ToolPanelType]
    Stroke: _ClassVar[ToolPanelType]
    Revolve: _ClassVar[ToolPanelType]
    FilledSurface: _ClassVar[ToolPanelType]
    Primitive: _ClassVar[ToolPanelType]
    CurvedSurface: _ClassVar[ToolPanelType]
    Interactions: _ClassVar[ToolPanelType]
    EmptyToolPanelType: _ClassVar[ToolPanelType]

class MenuType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidMenuType: _ClassVar[MenuType]
    LobbyClipboard: _ClassVar[MenuType]
    AdvancedMenu: _ClassVar[MenuType]
    BrushMenu: _ClassVar[MenuType]
    MaterialPanel: _ClassVar[MenuType]
    ViewpointPanel: _ClassVar[MenuType]
    SelectionPanel: _ClassVar[MenuType]

class BrushMenuCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidCategory: _ClassVar[BrushMenuCategory]
    Draw: _ClassVar[BrushMenuCategory]
    Surface: _ClassVar[BrushMenuCategory]
    Shapes: _ClassVar[BrushMenuCategory]
    Text: _ClassVar[BrushMenuCategory]

class AdvancedMenuPanel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UndefinedAdvancedMenuPanel: _ClassVar[AdvancedMenuPanel]
    Save: _ClassVar[AdvancedMenuPanel]
    Settings: _ClassVar[AdvancedMenuPanel]
    Layers: _ClassVar[AdvancedMenuPanel]
    Users: _ClassVar[AdvancedMenuPanel]
    Orthographic: _ClassVar[AdvancedMenuPanel]
    Learn: _ClassVar[AdvancedMenuPanel]
    Debug: _ClassVar[AdvancedMenuPanel]
    RecordReplay: _ClassVar[AdvancedMenuPanel]
    Import: _ClassVar[AdvancedMenuPanel]
    Export: _ClassVar[AdvancedMenuPanel]

class AdvancedMenuSettingsTab(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UndefinedAdvancedMenuSettingsTab: _ClassVar[AdvancedMenuSettingsTab]
    SketchingAid: _ClassVar[AdvancedMenuSettingsTab]
    Preferences: _ClassVar[AdvancedMenuSettingsTab]
    Environment: _ClassVar[AdvancedMenuSettingsTab]
    Beta: _ClassVar[AdvancedMenuSettingsTab]

class AdvancedMenuPrefabTab(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UndefinedAdvancedMenuPrefabTab: _ClassVar[AdvancedMenuPrefabTab]
    BuiltIn: _ClassVar[AdvancedMenuPrefabTab]
    OBJImport: _ClassVar[AdvancedMenuPrefabTab]

class SmartMoveAxisColor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SmartMoveAxisColorNoAxis: _ClassVar[SmartMoveAxisColor]
    SmartMoveAxisColorNonMirror: _ClassVar[SmartMoveAxisColor]
    SmartMoveAxisColorMirror: _ClassVar[SmartMoveAxisColor]
    SmartMoveAxisColorUp: _ClassVar[SmartMoveAxisColor]

class SnapColor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SnapColorDefault: _ClassVar[SnapColor]
    SnapColorRed: _ClassVar[SnapColor]
    SnapColorGreen: _ClassVar[SnapColor]
    SnapColorBlue: _ClassVar[SnapColor]

class SubDToolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SubDToolNone: _ClassVar[SubDToolType]
    SubDToolLoopCut: _ClassVar[SubDToolType]
    SubDToolMerge: _ClassVar[SubDToolType]
    SubDToolEdgeCut: _ClassVar[SubDToolType]
    SubDToolSmooth: _ClassVar[SubDToolType]
    SubDToolCrease: _ClassVar[SubDToolType]
    SubDToolSplit: _ClassVar[SubDToolType]

class SavePanelTabs(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NewSketch: _ClassVar[SavePanelTabs]
    None: _ClassVar[SavePanelTabs]

class SavePanelSaveLocations(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Local: _ClassVar[SavePanelSaveLocations]
    Cloud: _ClassVar[SavePanelSaveLocations]

class SavePanelActionText(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SavePanelNoAction: _ClassVar[SavePanelActionText]
    ForceExit: _ClassVar[SavePanelActionText]
    ForceExport: _ClassVar[SavePanelActionText]
    ForceSave: _ClassVar[SavePanelActionText]

class SavePanelTopText(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoTopText: _ClassVar[SavePanelTopText]
    UploadsTopText: _ClassVar[SavePanelTopText]
    DownloadsTopText: _ClassVar[SavePanelTopText]

class SavePanelBottomText(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoBottomText: _ClassVar[SavePanelBottomText]
    UploadsBottomText: _ClassVar[SavePanelBottomText]

class ImportPanelTab(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidTab: _ClassVar[ImportPanelTab]
    FileTab: _ClassVar[ImportPanelTab]
    BuiltInModelTab: _ClassVar[ImportPanelTab]

class TabButtonType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidTabButton: _ClassVar[TabButtonType]
    HelpCentreLandingPage: _ClassVar[TabButtonType]
    HelpCentreFAQ: _ClassVar[TabButtonType]
    HelpCentreOrgSpecificContent: _ClassVar[TabButtonType]

class GumballDirectionalRestriction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoRestriction: _ClassVar[GumballDirectionalRestriction]
    RestrictToMirror: _ClassVar[GumballDirectionalRestriction]

class TimerPlayState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ReadyToStart: _ClassVar[TimerPlayState]
    Counting: _ClassVar[TimerPlayState]
    Paused: _ClassVar[TimerPlayState]
    Completed: _ClassVar[TimerPlayState]

class TimerCountDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CountingUp: _ClassVar[TimerCountDirection]
    CountingDown: _ClassVar[TimerCountDirection]

class CursorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidCursor: _ClassVar[CursorType]
    NoCursor: _ClassVar[CursorType]
    UIPointer: _ClassVar[CursorType]
    StrokeCursor: _ClassVar[CursorType]
    SurfaceCursor: _ClassVar[CursorType]
    DimensionCursor: _ClassVar[CursorType]
    PipetteCursor: _ClassVar[CursorType]
    PaintbrushCursor: _ClassVar[CursorType]
    SelectionCursor: _ClassVar[CursorType]
    TeleportCursor: _ClassVar[CursorType]
    RevolveCursor: _ClassVar[CursorType]
    NormalFlipCursor: _ClassVar[CursorType]
    LaserCursor: _ClassVar[CursorType]
    ControlPointCursor: _ClassVar[CursorType]
    UIPipette: _ClassVar[CursorType]
    ViewpointCursor: _ClassVar[CursorType]
    CrossSectionCursor: _ClassVar[CursorType]

class CursorTransformFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidFamily: _ClassVar[CursorTransformFamily]
    NoFamily: _ClassVar[CursorTransformFamily]
    Standard: _ClassVar[CursorTransformFamily]
    SplineOrigin: _ClassVar[CursorTransformFamily]
    Fixed: _ClassVar[CursorTransformFamily]
    Pointer: _ClassVar[CursorTransformFamily]
TriBoolUndefined: TriBool
TriBoolFalse: TriBool
TriBoolTrue: TriBool
UndefinedToolPanelType: ToolPanelType
Ink: ToolPanelType
Stroke: ToolPanelType
Revolve: ToolPanelType
FilledSurface: ToolPanelType
Primitive: ToolPanelType
CurvedSurface: ToolPanelType
Interactions: ToolPanelType
EmptyToolPanelType: ToolPanelType
InvalidMenuType: MenuType
LobbyClipboard: MenuType
AdvancedMenu: MenuType
BrushMenu: MenuType
MaterialPanel: MenuType
ViewpointPanel: MenuType
SelectionPanel: MenuType
InvalidCategory: BrushMenuCategory
Draw: BrushMenuCategory
Surface: BrushMenuCategory
Shapes: BrushMenuCategory
Text: BrushMenuCategory
UndefinedAdvancedMenuPanel: AdvancedMenuPanel
Save: AdvancedMenuPanel
Settings: AdvancedMenuPanel
Layers: AdvancedMenuPanel
Users: AdvancedMenuPanel
Orthographic: AdvancedMenuPanel
Learn: AdvancedMenuPanel
Debug: AdvancedMenuPanel
RecordReplay: AdvancedMenuPanel
Import: AdvancedMenuPanel
Export: AdvancedMenuPanel
UndefinedAdvancedMenuSettingsTab: AdvancedMenuSettingsTab
SketchingAid: AdvancedMenuSettingsTab
Preferences: AdvancedMenuSettingsTab
Environment: AdvancedMenuSettingsTab
Beta: AdvancedMenuSettingsTab
UndefinedAdvancedMenuPrefabTab: AdvancedMenuPrefabTab
BuiltIn: AdvancedMenuPrefabTab
OBJImport: AdvancedMenuPrefabTab
SmartMoveAxisColorNoAxis: SmartMoveAxisColor
SmartMoveAxisColorNonMirror: SmartMoveAxisColor
SmartMoveAxisColorMirror: SmartMoveAxisColor
SmartMoveAxisColorUp: SmartMoveAxisColor
SnapColorDefault: SnapColor
SnapColorRed: SnapColor
SnapColorGreen: SnapColor
SnapColorBlue: SnapColor
SubDToolNone: SubDToolType
SubDToolLoopCut: SubDToolType
SubDToolMerge: SubDToolType
SubDToolEdgeCut: SubDToolType
SubDToolSmooth: SubDToolType
SubDToolCrease: SubDToolType
SubDToolSplit: SubDToolType
NewSketch: SavePanelTabs
None: SavePanelTabs
Local: SavePanelSaveLocations
Cloud: SavePanelSaveLocations
SavePanelNoAction: SavePanelActionText
ForceExit: SavePanelActionText
ForceExport: SavePanelActionText
ForceSave: SavePanelActionText
NoTopText: SavePanelTopText
UploadsTopText: SavePanelTopText
DownloadsTopText: SavePanelTopText
NoBottomText: SavePanelBottomText
UploadsBottomText: SavePanelBottomText
InvalidTab: ImportPanelTab
FileTab: ImportPanelTab
BuiltInModelTab: ImportPanelTab
InvalidTabButton: TabButtonType
HelpCentreLandingPage: TabButtonType
HelpCentreFAQ: TabButtonType
HelpCentreOrgSpecificContent: TabButtonType
NoRestriction: GumballDirectionalRestriction
RestrictToMirror: GumballDirectionalRestriction
ReadyToStart: TimerPlayState
Counting: TimerPlayState
Paused: TimerPlayState
Completed: TimerPlayState
CountingUp: TimerCountDirection
CountingDown: TimerCountDirection
InvalidCursor: CursorType
NoCursor: CursorType
UIPointer: CursorType
StrokeCursor: CursorType
SurfaceCursor: CursorType
DimensionCursor: CursorType
PipetteCursor: CursorType
PaintbrushCursor: CursorType
SelectionCursor: CursorType
TeleportCursor: CursorType
RevolveCursor: CursorType
NormalFlipCursor: CursorType
LaserCursor: CursorType
ControlPointCursor: CursorType
UIPipette: CursorType
ViewpointCursor: CursorType
CrossSectionCursor: CursorType
InvalidFamily: CursorTransformFamily
NoFamily: CursorTransformFamily
Standard: CursorTransformFamily
SplineOrigin: CursorTransformFamily
Fixed: CursorTransformFamily
Pointer: CursorTransformFamily

class DetachableTransformStates(_message.Message):
    __slots__ = ("detached", "transform", "isActive")
    DETACHED_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    detached: bool
    transform: _gravi_unity_pb2.TransformTO
    isActive: bool
    def __init__(self, detached: bool = ..., transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., isActive: bool = ...) -> None: ...

class BrushMenuCategoryState(_message.Message):
    __slots__ = ("brushMenuCategory", "validBrushProfileIds", "selectedBrushProfileId")
    BRUSHMENUCATEGORY_FIELD_NUMBER: _ClassVar[int]
    VALIDBRUSHPROFILEIDS_FIELD_NUMBER: _ClassVar[int]
    SELECTEDBRUSHPROFILEID_FIELD_NUMBER: _ClassVar[int]
    brushMenuCategory: BrushMenuCategory
    validBrushProfileIds: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    selectedBrushProfileId: _sketch_common_pb2.GSDataID
    def __init__(self, brushMenuCategory: _Optional[_Union[BrushMenuCategory, str]] = ..., validBrushProfileIds: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., selectedBrushProfileId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class BrushMenuStates(_message.Message):
    __slots__ = ("menuOpen", "editPanelOpen", "selectedBrushMenuCategory", "brushMenuCategoryStates")
    MENUOPEN_FIELD_NUMBER: _ClassVar[int]
    EDITPANELOPEN_FIELD_NUMBER: _ClassVar[int]
    SELECTEDBRUSHMENUCATEGORY_FIELD_NUMBER: _ClassVar[int]
    BRUSHMENUCATEGORYSTATES_FIELD_NUMBER: _ClassVar[int]
    menuOpen: bool
    editPanelOpen: bool
    selectedBrushMenuCategory: BrushMenuCategory
    brushMenuCategoryStates: _containers.RepeatedCompositeFieldContainer[BrushMenuCategoryState]
    def __init__(self, menuOpen: bool = ..., editPanelOpen: bool = ..., selectedBrushMenuCategory: _Optional[_Union[BrushMenuCategory, str]] = ..., brushMenuCategoryStates: _Optional[_Iterable[_Union[BrushMenuCategoryState, _Mapping]]] = ...) -> None: ...

class AdvancedMenuSettingsPanelStates(_message.Message):
    __slots__ = ("tab", "supportsMultipleDisplayFrequencies", "supportsWebView")
    TAB_FIELD_NUMBER: _ClassVar[int]
    SUPPORTSMULTIPLEDISPLAYFREQUENCIES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTSWEBVIEW_FIELD_NUMBER: _ClassVar[int]
    tab: AdvancedMenuSettingsTab
    supportsMultipleDisplayFrequencies: bool
    supportsWebView: bool
    def __init__(self, tab: _Optional[_Union[AdvancedMenuSettingsTab, str]] = ..., supportsMultipleDisplayFrequencies: bool = ..., supportsWebView: bool = ...) -> None: ...

class AdvancedMenuStates(_message.Message):
    __slots__ = ("open", "panel")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PANEL_FIELD_NUMBER: _ClassVar[int]
    open: bool
    panel: AdvancedMenuPanel
    def __init__(self, open: bool = ..., panel: _Optional[_Union[AdvancedMenuPanel, str]] = ...) -> None: ...

class AdvancedMenuPrefabPanelStates(_message.Message):
    __slots__ = ("tab",)
    TAB_FIELD_NUMBER: _ClassVar[int]
    tab: AdvancedMenuPrefabTab
    def __init__(self, tab: _Optional[_Union[AdvancedMenuPrefabTab, str]] = ...) -> None: ...

class AdvancedMenuLayerPanelStates(_message.Message):
    __slots__ = ("activeLayer", "layerDeletePopupOn", "layerDeletionGuids", "layerButtonDisabled", "layerScroll", "anySolo", "cosketchShowAllLayers")
    ACTIVELAYER_FIELD_NUMBER: _ClassVar[int]
    LAYERDELETEPOPUPON_FIELD_NUMBER: _ClassVar[int]
    LAYERDELETIONGUIDS_FIELD_NUMBER: _ClassVar[int]
    LAYERBUTTONDISABLED_FIELD_NUMBER: _ClassVar[int]
    LAYERSCROLL_FIELD_NUMBER: _ClassVar[int]
    ANYSOLO_FIELD_NUMBER: _ClassVar[int]
    COSKETCHSHOWALLLAYERS_FIELD_NUMBER: _ClassVar[int]
    activeLayer: str
    layerDeletePopupOn: bool
    layerDeletionGuids: _containers.RepeatedScalarFieldContainer[str]
    layerButtonDisabled: bool
    layerScroll: float
    anySolo: bool
    cosketchShowAllLayers: bool
    def __init__(self, activeLayer: _Optional[str] = ..., layerDeletePopupOn: bool = ..., layerDeletionGuids: _Optional[_Iterable[str]] = ..., layerButtonDisabled: bool = ..., layerScroll: _Optional[float] = ..., anySolo: bool = ..., cosketchShowAllLayers: bool = ...) -> None: ...

class DeprecatedAdvancedMenuLayerStates(_message.Message):
    __slots__ = ("solo", "active", "local", "grabbed", "grabZ", "offsetZ", "visible")
    SOLO_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_FIELD_NUMBER: _ClassVar[int]
    GRABBED_FIELD_NUMBER: _ClassVar[int]
    GRABZ_FIELD_NUMBER: _ClassVar[int]
    OFFSETZ_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    solo: bool
    active: TriBool
    local: TriBool
    grabbed: bool
    grabZ: float
    offsetZ: float
    visible: bool
    def __init__(self, solo: bool = ..., active: _Optional[_Union[TriBool, str]] = ..., local: _Optional[_Union[TriBool, str]] = ..., grabbed: bool = ..., grabZ: _Optional[float] = ..., offsetZ: _Optional[float] = ..., visible: bool = ...) -> None: ...

class LayerStates(_message.Message):
    __slots__ = ("expanded",)
    EXPANDED_FIELD_NUMBER: _ClassVar[int]
    expanded: bool
    def __init__(self, expanded: bool = ...) -> None: ...

class SmartMoveStates(_message.Message):
    __slots__ = ("transform", "snapPreviewEnabled", "worldAxisEnabled", "axisIsInfinite", "axisColor")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    SNAPPREVIEWENABLED_FIELD_NUMBER: _ClassVar[int]
    WORLDAXISENABLED_FIELD_NUMBER: _ClassVar[int]
    AXISISINFINITE_FIELD_NUMBER: _ClassVar[int]
    AXISCOLOR_FIELD_NUMBER: _ClassVar[int]
    transform: _gravi_unity_pb2.TransformTO
    snapPreviewEnabled: bool
    worldAxisEnabled: bool
    axisIsInfinite: bool
    axisColor: SmartMoveAxisColor
    def __init__(self, transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., snapPreviewEnabled: bool = ..., worldAxisEnabled: bool = ..., axisIsInfinite: bool = ..., axisColor: _Optional[_Union[SmartMoveAxisColor, str]] = ...) -> None: ...

class GrabSphereStates(_message.Message):
    __slots__ = ("mainGrabVisible", "mainHandScale", "softSelectRatio", "anythingHighlighted", "sketchHighlighted", "shrinkCollider", "positionOffset", "grabShapeType")
    MAINGRABVISIBLE_FIELD_NUMBER: _ClassVar[int]
    MAINHANDSCALE_FIELD_NUMBER: _ClassVar[int]
    SOFTSELECTRATIO_FIELD_NUMBER: _ClassVar[int]
    ANYTHINGHIGHLIGHTED_FIELD_NUMBER: _ClassVar[int]
    SKETCHHIGHLIGHTED_FIELD_NUMBER: _ClassVar[int]
    SHRINKCOLLIDER_FIELD_NUMBER: _ClassVar[int]
    POSITIONOFFSET_FIELD_NUMBER: _ClassVar[int]
    GRABSHAPETYPE_FIELD_NUMBER: _ClassVar[int]
    mainGrabVisible: bool
    mainHandScale: float
    softSelectRatio: float
    anythingHighlighted: bool
    sketchHighlighted: bool
    shrinkCollider: bool
    positionOffset: float
    grabShapeType: _preferences_pb2.GrabShapeType
    def __init__(self, mainGrabVisible: bool = ..., mainHandScale: _Optional[float] = ..., softSelectRatio: _Optional[float] = ..., anythingHighlighted: bool = ..., sketchHighlighted: bool = ..., shrinkCollider: bool = ..., positionOffset: _Optional[float] = ..., grabShapeType: _Optional[_Union[_preferences_pb2.GrabShapeType, str]] = ...) -> None: ...

class ControlPointMenuStates(_message.Message):
    __slots__ = ("open", "lastGrabbedSketchObject", "editingSketchObjects", "editSnapType")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    LASTGRABBEDSKETCHOBJECT_FIELD_NUMBER: _ClassVar[int]
    EDITINGSKETCHOBJECTS_FIELD_NUMBER: _ClassVar[int]
    EDITSNAPTYPE_FIELD_NUMBER: _ClassVar[int]
    open: bool
    lastGrabbedSketchObject: _sketch_common_pb2.GSDataID
    editingSketchObjects: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    editSnapType: _preferences_pb2.EditSnapType
    def __init__(self, open: bool = ..., lastGrabbedSketchObject: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., editingSketchObjects: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., editSnapType: _Optional[_Union[_preferences_pb2.EditSnapType, str]] = ...) -> None: ...

class PointerStates(_message.Message):
    __slots__ = ("enabled", "pointerHighlighted")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    POINTERHIGHLIGHTED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    pointerHighlighted: bool
    def __init__(self, enabled: bool = ..., pointerHighlighted: bool = ...) -> None: ...

class ControllerStates(_message.Message):
    __slots__ = ("menuButton", "secondButton", "touchPadTouch", "touchPadButton", "gripButton", "gripAxis", "triggerFull", "triggerAxis", "triggerLight", "stylusLight", "stylusFull", "stylusAxis")
    MENUBUTTON_FIELD_NUMBER: _ClassVar[int]
    SECONDBUTTON_FIELD_NUMBER: _ClassVar[int]
    TOUCHPADTOUCH_FIELD_NUMBER: _ClassVar[int]
    TOUCHPADBUTTON_FIELD_NUMBER: _ClassVar[int]
    GRIPBUTTON_FIELD_NUMBER: _ClassVar[int]
    GRIPAXIS_FIELD_NUMBER: _ClassVar[int]
    TRIGGERFULL_FIELD_NUMBER: _ClassVar[int]
    TRIGGERAXIS_FIELD_NUMBER: _ClassVar[int]
    TRIGGERLIGHT_FIELD_NUMBER: _ClassVar[int]
    STYLUSLIGHT_FIELD_NUMBER: _ClassVar[int]
    STYLUSFULL_FIELD_NUMBER: _ClassVar[int]
    STYLUSAXIS_FIELD_NUMBER: _ClassVar[int]
    menuButton: bool
    secondButton: bool
    touchPadTouch: bool
    touchPadButton: bool
    gripButton: bool
    gripAxis: float
    triggerFull: bool
    triggerAxis: float
    triggerLight: bool
    stylusLight: bool
    stylusFull: bool
    stylusAxis: float
    def __init__(self, menuButton: bool = ..., secondButton: bool = ..., touchPadTouch: bool = ..., touchPadButton: bool = ..., gripButton: bool = ..., gripAxis: _Optional[float] = ..., triggerFull: bool = ..., triggerAxis: _Optional[float] = ..., triggerLight: bool = ..., stylusLight: bool = ..., stylusFull: bool = ..., stylusAxis: _Optional[float] = ...) -> None: ...

class DrawPlaneStates(_message.Message):
    __slots__ = ("transform", "enabled", "planeEnabled", "snapColor", "axisThickness")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PLANEENABLED_FIELD_NUMBER: _ClassVar[int]
    SNAPCOLOR_FIELD_NUMBER: _ClassVar[int]
    AXISTHICKNESS_FIELD_NUMBER: _ClassVar[int]
    transform: _gravi_unity_pb2.TransformTO
    enabled: bool
    planeEnabled: TriBool
    snapColor: SnapColor
    axisThickness: float
    def __init__(self, transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., enabled: bool = ..., planeEnabled: _Optional[_Union[TriBool, str]] = ..., snapColor: _Optional[_Union[SnapColor, str]] = ..., axisThickness: _Optional[float] = ...) -> None: ...

class SubDToolMenuStates(_message.Message):
    __slots__ = ("transform", "enabled", "toolEnabled", "toolType")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TOOLENABLED_FIELD_NUMBER: _ClassVar[int]
    TOOLTYPE_FIELD_NUMBER: _ClassVar[int]
    transform: _gravi_unity_pb2.TransformTO
    enabled: bool
    toolEnabled: bool
    toolType: SubDToolType
    def __init__(self, transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., enabled: bool = ..., toolEnabled: bool = ..., toolType: _Optional[_Union[SubDToolType, str]] = ...) -> None: ...

class SavePanelStates(_message.Message):
    __slots__ = ("CoSketchProgressTopText", "CoSketchProgressBottomText", "CoSketchActionText", "CoSketchProgressParentActive", "CoSketchActionParentActive", "PrefabRootActive", "ExportButtonActive", "ScreenshotButtonActive", "ReportIssueButtonActive", "SaveButtonActive", "SaveAsButtonActive", "SaveLocation", "ReconnectNetworkButtonActive", "ToggleGroupUIParentsSelection", "FileExplorerOpen", "LPLoginOpen")
    COSKETCHPROGRESSTOPTEXT_FIELD_NUMBER: _ClassVar[int]
    COSKETCHPROGRESSBOTTOMTEXT_FIELD_NUMBER: _ClassVar[int]
    COSKETCHACTIONTEXT_FIELD_NUMBER: _ClassVar[int]
    COSKETCHPROGRESSPARENTACTIVE_FIELD_NUMBER: _ClassVar[int]
    COSKETCHACTIONPARENTACTIVE_FIELD_NUMBER: _ClassVar[int]
    PREFABROOTACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXPORTBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    SCREENSHOTBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    REPORTISSUEBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    SAVEBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    SAVEASBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    SAVELOCATION_FIELD_NUMBER: _ClassVar[int]
    RECONNECTNETWORKBUTTONACTIVE_FIELD_NUMBER: _ClassVar[int]
    TOGGLEGROUPUIPARENTSSELECTION_FIELD_NUMBER: _ClassVar[int]
    FILEEXPLOREROPEN_FIELD_NUMBER: _ClassVar[int]
    LPLOGINOPEN_FIELD_NUMBER: _ClassVar[int]
    CoSketchProgressTopText: SavePanelTopText
    CoSketchProgressBottomText: SavePanelBottomText
    CoSketchActionText: SavePanelActionText
    CoSketchProgressParentActive: bool
    CoSketchActionParentActive: bool
    PrefabRootActive: bool
    ExportButtonActive: bool
    ScreenshotButtonActive: bool
    ReportIssueButtonActive: bool
    SaveButtonActive: bool
    SaveAsButtonActive: bool
    SaveLocation: SavePanelSaveLocations
    ReconnectNetworkButtonActive: bool
    ToggleGroupUIParentsSelection: SavePanelTabs
    FileExplorerOpen: bool
    LPLoginOpen: bool
    def __init__(self, CoSketchProgressTopText: _Optional[_Union[SavePanelTopText, str]] = ..., CoSketchProgressBottomText: _Optional[_Union[SavePanelBottomText, str]] = ..., CoSketchActionText: _Optional[_Union[SavePanelActionText, str]] = ..., CoSketchProgressParentActive: bool = ..., CoSketchActionParentActive: bool = ..., PrefabRootActive: bool = ..., ExportButtonActive: bool = ..., ScreenshotButtonActive: bool = ..., ReportIssueButtonActive: bool = ..., SaveButtonActive: bool = ..., SaveAsButtonActive: bool = ..., SaveLocation: _Optional[_Union[SavePanelSaveLocations, str]] = ..., ReconnectNetworkButtonActive: bool = ..., ToggleGroupUIParentsSelection: _Optional[_Union[SavePanelTabs, str]] = ..., FileExplorerOpen: bool = ..., LPLoginOpen: bool = ...) -> None: ...

class ExportConfigurationSettingsStates(_message.Message):
    __slots__ = ("AdvancedSettingsOn", "FileTypeToggleSelection", "UnitsToggleSelection", "SingleSidedToggleSelection", "SubDControlMeshToggleSelection", "MeshNurbsHybridToggleSelection", "CollectGroupsToggleSelection")
    ADVANCEDSETTINGSON_FIELD_NUMBER: _ClassVar[int]
    FILETYPETOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    UNITSTOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    SINGLESIDEDTOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    SUBDCONTROLMESHTOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    MESHNURBSHYBRIDTOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    COLLECTGROUPSTOGGLESELECTION_FIELD_NUMBER: _ClassVar[int]
    AdvancedSettingsOn: bool
    FileTypeToggleSelection: int
    UnitsToggleSelection: int
    SingleSidedToggleSelection: int
    SubDControlMeshToggleSelection: int
    MeshNurbsHybridToggleSelection: int
    CollectGroupsToggleSelection: int
    def __init__(self, AdvancedSettingsOn: bool = ..., FileTypeToggleSelection: _Optional[int] = ..., UnitsToggleSelection: _Optional[int] = ..., SingleSidedToggleSelection: _Optional[int] = ..., SubDControlMeshToggleSelection: _Optional[int] = ..., MeshNurbsHybridToggleSelection: _Optional[int] = ..., CollectGroupsToggleSelection: _Optional[int] = ...) -> None: ...

class ScreenshotPanelStates(_message.Message):
    __slots__ = ("transform", "isActive", "isSquare", "showSettings", "focalLength", "showDofModule", "transparentToggleOn", "renderToggleOn", "addToSketchToggleOn", "verticalLockToggleOn", "dofPreviewToggleOn")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    ISSQUARE_FIELD_NUMBER: _ClassVar[int]
    SHOWSETTINGS_FIELD_NUMBER: _ClassVar[int]
    FOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    SHOWDOFMODULE_FIELD_NUMBER: _ClassVar[int]
    TRANSPARENTTOGGLEON_FIELD_NUMBER: _ClassVar[int]
    RENDERTOGGLEON_FIELD_NUMBER: _ClassVar[int]
    ADDTOSKETCHTOGGLEON_FIELD_NUMBER: _ClassVar[int]
    VERTICALLOCKTOGGLEON_FIELD_NUMBER: _ClassVar[int]
    DOFPREVIEWTOGGLEON_FIELD_NUMBER: _ClassVar[int]
    transform: _gravi_unity_pb2.TransformTO
    isActive: bool
    isSquare: bool
    showSettings: bool
    focalLength: float
    showDofModule: bool
    transparentToggleOn: bool
    renderToggleOn: bool
    addToSketchToggleOn: bool
    verticalLockToggleOn: bool
    dofPreviewToggleOn: bool
    def __init__(self, transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., isActive: bool = ..., isSquare: bool = ..., showSettings: bool = ..., focalLength: _Optional[float] = ..., showDofModule: bool = ..., transparentToggleOn: bool = ..., renderToggleOn: bool = ..., addToSketchToggleOn: bool = ..., verticalLockToggleOn: bool = ..., dofPreviewToggleOn: bool = ...) -> None: ...

class ColorSelectorStates(_message.Message):
    __slots__ = ("discHeight", "discActivity", "isSwatches", "isActive", "selectedColor")
    DISCHEIGHT_FIELD_NUMBER: _ClassVar[int]
    DISCACTIVITY_FIELD_NUMBER: _ClassVar[int]
    ISSWATCHES_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    SELECTEDCOLOR_FIELD_NUMBER: _ClassVar[int]
    discHeight: float
    discActivity: float
    isSwatches: bool
    isActive: bool
    selectedColor: int
    def __init__(self, discHeight: _Optional[float] = ..., discActivity: _Optional[float] = ..., isSwatches: bool = ..., isActive: bool = ..., selectedColor: _Optional[int] = ...) -> None: ...

class ImportPanelStates(_message.Message):
    __slots__ = ("importPanelTab",)
    IMPORTPANELTAB_FIELD_NUMBER: _ClassVar[int]
    importPanelTab: ImportPanelTab
    def __init__(self, importPanelTab: _Optional[_Union[ImportPanelTab, str]] = ...) -> None: ...

class ImportMenuStates(_message.Message):
    __slots__ = ("enabled", "unitsSelection", "extraInfoEnabled", "fileType", "fileSize", "fileParts", "fileVertices", "fileTriangles")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    UNITSSELECTION_FIELD_NUMBER: _ClassVar[int]
    EXTRAINFOENABLED_FIELD_NUMBER: _ClassVar[int]
    FILETYPE_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    FILEPARTS_FIELD_NUMBER: _ClassVar[int]
    FILEVERTICES_FIELD_NUMBER: _ClassVar[int]
    FILETRIANGLES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    unitsSelection: int
    extraInfoEnabled: bool
    fileType: str
    fileSize: str
    fileParts: int
    fileVertices: int
    fileTriangles: int
    def __init__(self, enabled: bool = ..., unitsSelection: _Optional[int] = ..., extraInfoEnabled: bool = ..., fileType: _Optional[str] = ..., fileSize: _Optional[str] = ..., fileParts: _Optional[int] = ..., fileVertices: _Optional[int] = ..., fileTriangles: _Optional[int] = ...) -> None: ...

class ExportMenuStates(_message.Message):
    __slots__ = ("menuEnabled", "fileExplorerEnabled", "unitsSelection", "mirrorPlaneSelection", "upAxisSelection")
    MENUENABLED_FIELD_NUMBER: _ClassVar[int]
    FILEEXPLORERENABLED_FIELD_NUMBER: _ClassVar[int]
    UNITSSELECTION_FIELD_NUMBER: _ClassVar[int]
    MIRRORPLANESELECTION_FIELD_NUMBER: _ClassVar[int]
    UPAXISSELECTION_FIELD_NUMBER: _ClassVar[int]
    menuEnabled: bool
    fileExplorerEnabled: bool
    unitsSelection: int
    mirrorPlaneSelection: int
    upAxisSelection: int
    def __init__(self, menuEnabled: bool = ..., fileExplorerEnabled: bool = ..., unitsSelection: _Optional[int] = ..., mirrorPlaneSelection: _Optional[int] = ..., upAxisSelection: _Optional[int] = ...) -> None: ...

class ExportSettingsMenuStates(_message.Message):
    __slots__ = ("enabled", "showAdvancedSettings", "fileNameForExport", "resetButtonInteractable", "filePathReadout", "filePathButtonInteractable", "fileExplorerEnabled", "presetInfoEnabled", "exportSettings", "exportInfo")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SHOWADVANCEDSETTINGS_FIELD_NUMBER: _ClassVar[int]
    FILENAMEFOREXPORT_FIELD_NUMBER: _ClassVar[int]
    RESETBUTTONINTERACTABLE_FIELD_NUMBER: _ClassVar[int]
    FILEPATHREADOUT_FIELD_NUMBER: _ClassVar[int]
    FILEPATHBUTTONINTERACTABLE_FIELD_NUMBER: _ClassVar[int]
    FILEEXPLORERENABLED_FIELD_NUMBER: _ClassVar[int]
    PRESETINFOENABLED_FIELD_NUMBER: _ClassVar[int]
    EXPORTSETTINGS_FIELD_NUMBER: _ClassVar[int]
    EXPORTINFO_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    showAdvancedSettings: bool
    fileNameForExport: str
    resetButtonInteractable: bool
    filePathReadout: str
    filePathButtonInteractable: bool
    fileExplorerEnabled: bool
    presetInfoEnabled: bool
    exportSettings: _preferences_pb2.ExportPreferencesTO
    exportInfo: _preferences_pb2.ExportPreferenceHint
    def __init__(self, enabled: bool = ..., showAdvancedSettings: bool = ..., fileNameForExport: _Optional[str] = ..., resetButtonInteractable: bool = ..., filePathReadout: _Optional[str] = ..., filePathButtonInteractable: bool = ..., fileExplorerEnabled: bool = ..., presetInfoEnabled: bool = ..., exportSettings: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ..., exportInfo: _Optional[_Union[_preferences_pb2.ExportPreferenceHint, _Mapping]] = ...) -> None: ...

class EnableObjectStates(_message.Message):
    __slots__ = ("isActive",)
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    def __init__(self, isActive: bool = ...) -> None: ...

class BasicUIComponentStates(_message.Message):
    __slots__ = ("isActive",)
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    def __init__(self, isActive: bool = ...) -> None: ...

class ButtonStates(_message.Message):
    __slots__ = ("isActive", "isInteractable", "isOn")
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    ISINTERACTABLE_FIELD_NUMBER: _ClassVar[int]
    ISON_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    isInteractable: bool
    isOn: bool
    def __init__(self, isActive: bool = ..., isInteractable: bool = ..., isOn: bool = ...) -> None: ...

class SliderStates(_message.Message):
    __slots__ = ("isActive", "isInteractable", "value")
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    ISINTERACTABLE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    isInteractable: bool
    value: float
    def __init__(self, isActive: bool = ..., isInteractable: bool = ..., value: _Optional[float] = ...) -> None: ...

class MaterialButtonStates(_message.Message):
    __slots__ = ("buttonStates", "material")
    BUTTONSTATES_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    buttonStates: ButtonStates
    material: _sketch_common_pb2.DrawMaterial
    def __init__(self, buttonStates: _Optional[_Union[ButtonStates, _Mapping]] = ..., material: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...

class TabMenuStates(_message.Message):
    __slots__ = ("tabButtons", "selectedIndex")
    TABBUTTONS_FIELD_NUMBER: _ClassVar[int]
    SELECTEDINDEX_FIELD_NUMBER: _ClassVar[int]
    tabButtons: _containers.RepeatedScalarFieldContainer[TabButtonType]
    selectedIndex: int
    def __init__(self, tabButtons: _Optional[_Iterable[_Union[TabButtonType, str]]] = ..., selectedIndex: _Optional[int] = ...) -> None: ...

class ExpandableItemStates(_message.Message):
    __slots__ = ("isExpanded",)
    ISEXPANDED_FIELD_NUMBER: _ClassVar[int]
    isExpanded: bool
    def __init__(self, isExpanded: bool = ...) -> None: ...

class ToggleGroupStates(_message.Message):
    __slots__ = ("selectedIndex", "isActive")
    SELECTEDINDEX_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    selectedIndex: int
    isActive: bool
    def __init__(self, selectedIndex: _Optional[int] = ..., isActive: bool = ...) -> None: ...

class ProfileListStates(_message.Message):
    __slots__ = ("toggleGroupStates", "extendSelectedItem")
    TOGGLEGROUPSTATES_FIELD_NUMBER: _ClassVar[int]
    EXTENDSELECTEDITEM_FIELD_NUMBER: _ClassVar[int]
    toggleGroupStates: ToggleGroupStates
    extendSelectedItem: bool
    def __init__(self, toggleGroupStates: _Optional[_Union[ToggleGroupStates, _Mapping]] = ..., extendSelectedItem: bool = ...) -> None: ...

class ToggleSelectorStates(_message.Message):
    __slots__ = ("selectedIndex", "isActive")
    SELECTEDINDEX_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    selectedIndex: int
    isActive: bool
    def __init__(self, selectedIndex: _Optional[int] = ..., isActive: bool = ...) -> None: ...

class ShaderSelectorStates(_message.Message):
    __slots__ = ("selectedShaderIndex", "selectedColorR", "selectedColorG", "selectedColorB")
    SELECTEDSHADERINDEX_FIELD_NUMBER: _ClassVar[int]
    SELECTEDCOLORR_FIELD_NUMBER: _ClassVar[int]
    SELECTEDCOLORG_FIELD_NUMBER: _ClassVar[int]
    SELECTEDCOLORB_FIELD_NUMBER: _ClassVar[int]
    selectedShaderIndex: int
    selectedColorR: float
    selectedColorG: float
    selectedColorB: float
    def __init__(self, selectedShaderIndex: _Optional[int] = ..., selectedColorR: _Optional[float] = ..., selectedColorG: _Optional[float] = ..., selectedColorB: _Optional[float] = ...) -> None: ...

class MaterialDisplayStates(_message.Message):
    __slots__ = ("drawMaterial", "isActive")
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    drawMaterial: _sketch_common_pb2.DrawMaterial
    isActive: bool
    def __init__(self, drawMaterial: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ..., isActive: bool = ...) -> None: ...

class PaginationLayoutStates(_message.Message):
    __slots__ = ("currentPageIndex", "lastPageIndex")
    CURRENTPAGEINDEX_FIELD_NUMBER: _ClassVar[int]
    LASTPAGEINDEX_FIELD_NUMBER: _ClassVar[int]
    currentPageIndex: int
    lastPageIndex: int
    def __init__(self, currentPageIndex: _Optional[int] = ..., lastPageIndex: _Optional[int] = ...) -> None: ...

class DropdownListStates(_message.Message):
    __slots__ = ("selectedItemText", "isDropdownOpen")
    SELECTEDITEMTEXT_FIELD_NUMBER: _ClassVar[int]
    ISDROPDOWNOPEN_FIELD_NUMBER: _ClassVar[int]
    selectedItemText: str
    isDropdownOpen: bool
    def __init__(self, selectedItemText: _Optional[str] = ..., isDropdownOpen: bool = ...) -> None: ...

class TextureTransformChangePanelStates(_message.Message):
    __slots__ = ("isActive", "textureTransform")
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    TEXTURETRANSFORM_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    textureTransform: _sketch_common_pb2.MainTextureTransform
    def __init__(self, isActive: bool = ..., textureTransform: _Optional[_Union[_sketch_common_pb2.MainTextureTransform, _Mapping]] = ...) -> None: ...

class UserReportPanelStates(_message.Message):
    __slots__ = ("isActive", "userEmailText", "issueDescriptionText")
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEREMAILTEXT_FIELD_NUMBER: _ClassVar[int]
    ISSUEDESCRIPTIONTEXT_FIELD_NUMBER: _ClassVar[int]
    isActive: bool
    userEmailText: str
    issueDescriptionText: str
    def __init__(self, isActive: bool = ..., userEmailText: _Optional[str] = ..., issueDescriptionText: _Optional[str] = ...) -> None: ...

class ViewpointListStates(_message.Message):
    __slots__ = ("viewpointCount", "scrollPosition")
    VIEWPOINTCOUNT_FIELD_NUMBER: _ClassVar[int]
    SCROLLPOSITION_FIELD_NUMBER: _ClassVar[int]
    viewpointCount: int
    scrollPosition: float
    def __init__(self, viewpointCount: _Optional[int] = ..., scrollPosition: _Optional[float] = ...) -> None: ...

class CameraItemStates(_message.Message):
    __slots__ = ("cameraName", "isSpawnPoint")
    CAMERANAME_FIELD_NUMBER: _ClassVar[int]
    ISSPAWNPOINT_FIELD_NUMBER: _ClassVar[int]
    cameraName: str
    isSpawnPoint: bool
    def __init__(self, cameraName: _Optional[str] = ..., isSpawnPoint: bool = ...) -> None: ...

class TextplateStates(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class ScrollStates(_message.Message):
    __slots__ = ("scrollAmount",)
    SCROLLAMOUNT_FIELD_NUMBER: _ClassVar[int]
    scrollAmount: float
    def __init__(self, scrollAmount: _Optional[float] = ...) -> None: ...

class BoundingBoxStates(_message.Message):
    __slots__ = ("boundingBoxEnabled", "transform", "readoutsEnabled", "boxColorR", "boxColorG", "boxColorB", "boxColorA")
    BOUNDINGBOXENABLED_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    READOUTSENABLED_FIELD_NUMBER: _ClassVar[int]
    BOXCOLORR_FIELD_NUMBER: _ClassVar[int]
    BOXCOLORG_FIELD_NUMBER: _ClassVar[int]
    BOXCOLORB_FIELD_NUMBER: _ClassVar[int]
    BOXCOLORA_FIELD_NUMBER: _ClassVar[int]
    boundingBoxEnabled: bool
    transform: _gravi_unity_pb2.TransformTO
    readoutsEnabled: bool
    boxColorR: float
    boxColorG: float
    boxColorB: float
    boxColorA: float
    def __init__(self, boundingBoxEnabled: bool = ..., transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., readoutsEnabled: bool = ..., boxColorR: _Optional[float] = ..., boxColorG: _Optional[float] = ..., boxColorB: _Optional[float] = ..., boxColorA: _Optional[float] = ...) -> None: ...

class GumballStates(_message.Message):
    __slots__ = ("directionalRestriction", "showRecenterMirror", "transform", "axisConfiguration", "scaleGizmoLocalPositionX", "scaleGizmoLocalPositionY", "scaleGizmoLocalPositionZ", "highlightMoveHandle", "enabled")
    DIRECTIONALRESTRICTION_FIELD_NUMBER: _ClassVar[int]
    SHOWRECENTERMIRROR_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    AXISCONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCALEGIZMOLOCALPOSITIONX_FIELD_NUMBER: _ClassVar[int]
    SCALEGIZMOLOCALPOSITIONY_FIELD_NUMBER: _ClassVar[int]
    SCALEGIZMOLOCALPOSITIONZ_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTMOVEHANDLE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    directionalRestriction: GumballDirectionalRestriction
    showRecenterMirror: bool
    transform: _gravi_unity_pb2.TransformTO
    axisConfiguration: _preferences_pb2.BaseAxisConfiguration
    scaleGizmoLocalPositionX: float
    scaleGizmoLocalPositionY: float
    scaleGizmoLocalPositionZ: float
    highlightMoveHandle: bool
    enabled: bool
    def __init__(self, directionalRestriction: _Optional[_Union[GumballDirectionalRestriction, str]] = ..., showRecenterMirror: bool = ..., transform: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., axisConfiguration: _Optional[_Union[_preferences_pb2.BaseAxisConfiguration, str]] = ..., scaleGizmoLocalPositionX: _Optional[float] = ..., scaleGizmoLocalPositionY: _Optional[float] = ..., scaleGizmoLocalPositionZ: _Optional[float] = ..., highlightMoveHandle: bool = ..., enabled: bool = ...) -> None: ...

class TimerStates(_message.Message):
    __slots__ = ("playState", "countDirection", "baseTimerLengthSeconds", "timeStampAtLastPlay", "timerValueAtLastPlay", "timerValueAtLastPause")
    PLAYSTATE_FIELD_NUMBER: _ClassVar[int]
    COUNTDIRECTION_FIELD_NUMBER: _ClassVar[int]
    BASETIMERLENGTHSECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPATLASTPLAY_FIELD_NUMBER: _ClassVar[int]
    TIMERVALUEATLASTPLAY_FIELD_NUMBER: _ClassVar[int]
    TIMERVALUEATLASTPAUSE_FIELD_NUMBER: _ClassVar[int]
    playState: TimerPlayState
    countDirection: TimerCountDirection
    baseTimerLengthSeconds: int
    timeStampAtLastPlay: int
    timerValueAtLastPlay: float
    timerValueAtLastPause: float
    def __init__(self, playState: _Optional[_Union[TimerPlayState, str]] = ..., countDirection: _Optional[_Union[TimerCountDirection, str]] = ..., baseTimerLengthSeconds: _Optional[int] = ..., timeStampAtLastPlay: _Optional[int] = ..., timerValueAtLastPlay: _Optional[float] = ..., timerValueAtLastPause: _Optional[float] = ...) -> None: ...

class SharedCursorStates(_message.Message):
    __slots__ = ("activeCursorIds", "cursorMaterial")
    ACTIVECURSORIDS_FIELD_NUMBER: _ClassVar[int]
    CURSORMATERIAL_FIELD_NUMBER: _ClassVar[int]
    activeCursorIds: _containers.RepeatedCompositeFieldContainer[CursorID]
    cursorMaterial: _sketch_common_pb2.DrawMaterial
    def __init__(self, activeCursorIds: _Optional[_Iterable[_Union[CursorID, _Mapping]]] = ..., cursorMaterial: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...

class CursorID(_message.Message):
    __slots__ = ("cursorType", "cursorInstanceId")
    CURSORTYPE_FIELD_NUMBER: _ClassVar[int]
    CURSORINSTANCEID_FIELD_NUMBER: _ClassVar[int]
    cursorType: CursorType
    cursorInstanceId: str
    def __init__(self, cursorType: _Optional[_Union[CursorType, str]] = ..., cursorInstanceId: _Optional[str] = ...) -> None: ...

class CursorTransformID(_message.Message):
    __slots__ = ("transformFamily", "cursorInstanceId")
    TRANSFORMFAMILY_FIELD_NUMBER: _ClassVar[int]
    CURSORINSTANCEID_FIELD_NUMBER: _ClassVar[int]
    transformFamily: CursorTransformFamily
    cursorInstanceId: str
    def __init__(self, transformFamily: _Optional[_Union[CursorTransformFamily, str]] = ..., cursorInstanceId: _Optional[str] = ...) -> None: ...
