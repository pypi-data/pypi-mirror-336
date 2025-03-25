from gravi.rpc.model.inputs import sketch_inputs_pb2 as _sketch_inputs_pb2
from gravi.localization import localization_pb2 as _localization_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
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

class BaseAxisConfiguration(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    YUpZMirror: _ClassVar[BaseAxisConfiguration]
    ZUpYMirror: _ClassVar[BaseAxisConfiguration]
    ZUpXMirror: _ClassVar[BaseAxisConfiguration]
    YUpXMirror: _ClassVar[BaseAxisConfiguration]

class ScaleSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ScaleMM: _ClassVar[ScaleSetting]
    ScaleCM: _ClassVar[ScaleSetting]
    ScaleM: _ClassVar[ScaleSetting]
    ScaleInch: _ClassVar[ScaleSetting]

class SmartMoveSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SmartMoveDisabled: _ClassVar[SmartMoveSetting]
    SmartMoveAxisOnly: _ClassVar[SmartMoveSetting]
    SmartMoveAnyDirection: _ClassVar[SmartMoveSetting]

class SurfaceContourSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SurfaceContoursAlwaysOff: _ClassVar[SurfaceContourSetting]
    SurfaceContoursOnInEditMode: _ClassVar[SurfaceContourSetting]
    SurfaceContoursAlwaysOn: _ClassVar[SurfaceContourSetting]

class ControllerLook(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ControllerLookSimple: _ClassVar[ControllerLook]
    ControllerLookSeeThrough: _ClassVar[ControllerLook]
    ControllerLookWireframe: _ClassVar[ControllerLook]
    ControllerLookNone: _ClassVar[ControllerLook]

class MirrorVisualisationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MirrorInvisible: _ClassVar[MirrorVisualisationType]
    MirrorStatic: _ClassVar[MirrorVisualisationType]
    MirrorAutoScale: _ClassVar[MirrorVisualisationType]

class WorldAxisType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WorldAxisInvisible: _ClassVar[WorldAxisType]
    WorldAxisVisible: _ClassVar[WorldAxisType]
    WorldAxisDeprecated: _ClassVar[WorldAxisType]

class StageFloorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    StageFloorInvisible: _ClassVar[StageFloorType]
    StageFloorRoundStage: _ClassVar[StageFloorType]
    StageFloorRectangleStage: _ClassVar[StageFloorType]
    StageFloorGrid: _ClassVar[StageFloorType]

class ScaleSnapType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ScaleSnapNone: _ClassVar[ScaleSnapType]
    ScaleSnapConstantRatio: _ClassVar[ScaleSnapType]
    ScaleSnapFreeScale: _ClassVar[ScaleSnapType]
    ScaleSnapNoneScaling: _ClassVar[ScaleSnapType]

class GrabShapeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GrabSphere: _ClassVar[GrabShapeType]
    GrabCube: _ClassVar[GrabShapeType]

class EditSnapType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EditSnapNone: _ClassVar[EditSnapType]
    EditSnapObjects: _ClassVar[EditSnapType]
    EditSnapNodes: _ClassVar[EditSnapType]

class MicrophonePreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MicrophoneOff: _ClassVar[MicrophonePreference]
    MicrophoneHoldUp: _ClassVar[MicrophonePreference]
    MicrophoneAlwaysOn: _ClassVar[MicrophonePreference]

class PrimitiveDrawingPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TwoHandsFreeMove: _ClassVar[PrimitiveDrawingPreference]
    CentralLine: _ClassVar[PrimitiveDrawingPreference]
    OneHandScale: _ClassVar[PrimitiveDrawingPreference]

class ComfortLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ComfortLevelUndefined: _ClassVar[ComfortLevel]
    ComfortLevelBlink: _ClassVar[ComfortLevel]
    ComfortLevelSmooth: _ClassVar[ComfortLevel]

class ExportFileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OBJ: _ClassVar[ExportFileType]
    FBX: _ClassVar[ExportFileType]
    IGES: _ClassVar[ExportFileType]
    USDZ: _ClassVar[ExportFileType]
    GLB: _ClassVar[ExportFileType]
    TurntableMP4: _ClassVar[ExportFileType]
    Thumbnail: _ClassVar[ExportFileType]
    GRS: _ClassVar[ExportFileType]
    Thumbnail360: _ClassVar[ExportFileType]
    PreProcessedGrsImport: _ClassVar[ExportFileType]
    TurntableGif: _ClassVar[ExportFileType]
    Blend: _ClassVar[ExportFileType]

class LocalStorageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownStorageType: _ClassVar[LocalStorageType]
    InternalStorage: _ClassVar[LocalStorageType]
    USBAccessibleStorage: _ClassVar[LocalStorageType]

class FbxExportNurbsPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FbxMesh: _ClassVar[FbxExportNurbsPreference]
    FbxNURBS: _ClassVar[FbxExportNurbsPreference]
    FbxFullData: _ClassVar[FbxExportNurbsPreference]

class ClockDisplayPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TwelveHour: _ClassVar[ClockDisplayPreference]
    TwentyFourHour: _ClassVar[ClockDisplayPreference]

class TimeReminderFrequency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Off: _ClassVar[TimeReminderFrequency]
    Hourly: _ClassVar[TimeReminderFrequency]
    EveryThirtyMinutes: _ClassVar[TimeReminderFrequency]
    EveryFifteenMinutes: _ClassVar[TimeReminderFrequency]

class UIVisibilityPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ObservationModeOnly: _ClassVar[UIVisibilityPolicy]
    AlwaysHide: _ClassVar[UIVisibilityPolicy]
    AlwaysShow: _ClassVar[UIVisibilityPolicy]

class WindowMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Maximised: _ClassVar[WindowMode]
    NotMaximised: _ClassVar[WindowMode]
    FullScreen: _ClassVar[WindowMode]

class AspectRatioType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ratio16To9: _ClassVar[AspectRatioType]
    ratio1To1: _ClassVar[AspectRatioType]

class SelectionToolMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidSelectionMode: _ClassVar[SelectionToolMode]
    CursorPaintSelect: _ClassVar[SelectionToolMode]
    BoxSelect: _ClassVar[SelectionToolMode]

class PadCameraType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DrawPlaneCamera: _ClassVar[PadCameraType]
    FreeCamera: _ClassVar[PadCameraType]

class PerspectiveMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Orthographic: _ClassVar[PerspectiveMode]
    Perspective: _ClassVar[PerspectiveMode]

class PadRotationAxisType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PlaneParallel: _ClassVar[PadRotationAxisType]
    PlanePerpendicular: _ClassVar[PadRotationAxisType]

class PadColorSelectionPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Square: _ClassVar[PadColorSelectionPreference]
    Circle: _ClassVar[PadColorSelectionPreference]

class MP4ExportStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MP4ExportStyleUnset: _ClassVar[MP4ExportStyle]
    MP4ExportStyleTurntable: _ClassVar[MP4ExportStyle]
    MP4ExportStyleTimelapse: _ClassVar[MP4ExportStyle]
    MP4ExportStyleViewpointFlythrough: _ClassVar[MP4ExportStyle]

class DiscretizationResolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DiscretizationResolutionInvalid: _ClassVar[DiscretizationResolution]
    DiscretizationViewLODMin: _ClassVar[DiscretizationResolution]
    DiscretizationViewLODMid: _ClassVar[DiscretizationResolution]
    DiscretizationViewLODMax: _ClassVar[DiscretizationResolution]
    DiscretizationExportMin: _ClassVar[DiscretizationResolution]
    DiscretizationExportMid: _ClassVar[DiscretizationResolution]
    DiscretizationExportHigh: _ClassVar[DiscretizationResolution]
    DiscretizationExportExtreme: _ClassVar[DiscretizationResolution]
    DiscretizationConvertToSubD: _ClassVar[DiscretizationResolution]

class InteractionPanelTab(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InteractionTriggerPanelTab: _ClassVar[InteractionPanelTab]
    InteractionActionPanelTab: _ClassVar[InteractionPanelTab]

class StartupPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LoadLobby: _ClassVar[StartupPreference]
    LoadNewSketch: _ClassVar[StartupPreference]
    LoadRecentSketch: _ClassVar[StartupPreference]

class PresetMaterialsIteration(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoPresetMaterials: _ClassVar[PresetMaterialsIteration]
    PresetMaterialsV0Unreleased: _ClassVar[PresetMaterialsIteration]
    PresetMaterialsV1: _ClassVar[PresetMaterialsIteration]
TriBoolUndefined: TriBool
TriBoolFalse: TriBool
TriBoolTrue: TriBool
YUpZMirror: BaseAxisConfiguration
ZUpYMirror: BaseAxisConfiguration
ZUpXMirror: BaseAxisConfiguration
YUpXMirror: BaseAxisConfiguration
ScaleMM: ScaleSetting
ScaleCM: ScaleSetting
ScaleM: ScaleSetting
ScaleInch: ScaleSetting
SmartMoveDisabled: SmartMoveSetting
SmartMoveAxisOnly: SmartMoveSetting
SmartMoveAnyDirection: SmartMoveSetting
SurfaceContoursAlwaysOff: SurfaceContourSetting
SurfaceContoursOnInEditMode: SurfaceContourSetting
SurfaceContoursAlwaysOn: SurfaceContourSetting
ControllerLookSimple: ControllerLook
ControllerLookSeeThrough: ControllerLook
ControllerLookWireframe: ControllerLook
ControllerLookNone: ControllerLook
MirrorInvisible: MirrorVisualisationType
MirrorStatic: MirrorVisualisationType
MirrorAutoScale: MirrorVisualisationType
WorldAxisInvisible: WorldAxisType
WorldAxisVisible: WorldAxisType
WorldAxisDeprecated: WorldAxisType
StageFloorInvisible: StageFloorType
StageFloorRoundStage: StageFloorType
StageFloorRectangleStage: StageFloorType
StageFloorGrid: StageFloorType
ScaleSnapNone: ScaleSnapType
ScaleSnapConstantRatio: ScaleSnapType
ScaleSnapFreeScale: ScaleSnapType
ScaleSnapNoneScaling: ScaleSnapType
GrabSphere: GrabShapeType
GrabCube: GrabShapeType
EditSnapNone: EditSnapType
EditSnapObjects: EditSnapType
EditSnapNodes: EditSnapType
MicrophoneOff: MicrophonePreference
MicrophoneHoldUp: MicrophonePreference
MicrophoneAlwaysOn: MicrophonePreference
TwoHandsFreeMove: PrimitiveDrawingPreference
CentralLine: PrimitiveDrawingPreference
OneHandScale: PrimitiveDrawingPreference
ComfortLevelUndefined: ComfortLevel
ComfortLevelBlink: ComfortLevel
ComfortLevelSmooth: ComfortLevel
OBJ: ExportFileType
FBX: ExportFileType
IGES: ExportFileType
USDZ: ExportFileType
GLB: ExportFileType
TurntableMP4: ExportFileType
Thumbnail: ExportFileType
GRS: ExportFileType
Thumbnail360: ExportFileType
PreProcessedGrsImport: ExportFileType
TurntableGif: ExportFileType
Blend: ExportFileType
UnknownStorageType: LocalStorageType
InternalStorage: LocalStorageType
USBAccessibleStorage: LocalStorageType
FbxMesh: FbxExportNurbsPreference
FbxNURBS: FbxExportNurbsPreference
FbxFullData: FbxExportNurbsPreference
TwelveHour: ClockDisplayPreference
TwentyFourHour: ClockDisplayPreference
Off: TimeReminderFrequency
Hourly: TimeReminderFrequency
EveryThirtyMinutes: TimeReminderFrequency
EveryFifteenMinutes: TimeReminderFrequency
ObservationModeOnly: UIVisibilityPolicy
AlwaysHide: UIVisibilityPolicy
AlwaysShow: UIVisibilityPolicy
Maximised: WindowMode
NotMaximised: WindowMode
FullScreen: WindowMode
ratio16To9: AspectRatioType
ratio1To1: AspectRatioType
InvalidSelectionMode: SelectionToolMode
CursorPaintSelect: SelectionToolMode
BoxSelect: SelectionToolMode
DrawPlaneCamera: PadCameraType
FreeCamera: PadCameraType
Orthographic: PerspectiveMode
Perspective: PerspectiveMode
PlaneParallel: PadRotationAxisType
PlanePerpendicular: PadRotationAxisType
Square: PadColorSelectionPreference
Circle: PadColorSelectionPreference
MP4ExportStyleUnset: MP4ExportStyle
MP4ExportStyleTurntable: MP4ExportStyle
MP4ExportStyleTimelapse: MP4ExportStyle
MP4ExportStyleViewpointFlythrough: MP4ExportStyle
DiscretizationResolutionInvalid: DiscretizationResolution
DiscretizationViewLODMin: DiscretizationResolution
DiscretizationViewLODMid: DiscretizationResolution
DiscretizationViewLODMax: DiscretizationResolution
DiscretizationExportMin: DiscretizationResolution
DiscretizationExportMid: DiscretizationResolution
DiscretizationExportHigh: DiscretizationResolution
DiscretizationExportExtreme: DiscretizationResolution
DiscretizationConvertToSubD: DiscretizationResolution
InteractionTriggerPanelTab: InteractionPanelTab
InteractionActionPanelTab: InteractionPanelTab
LoadLobby: StartupPreference
LoadNewSketch: StartupPreference
LoadRecentSketch: StartupPreference
NoPresetMaterials: PresetMaterialsIteration
PresetMaterialsV0Unreleased: PresetMaterialsIteration
PresetMaterialsV1: PresetMaterialsIteration

class UserSavedPreferencesTO(_message.Message):
    __slots__ = ("userId", "language", "leftHandedMode", "ghostMove", "returnAfterDuplicate", "orientationLock", "smartMove", "highQualityRendering", "textPopups", "disableHaptics", "isSeated", "videoTips", "preferredDisplayFrequency", "controllerModel", "deprecatedSurfaceContours", "surfaceContourSetting", "passthroughEnvironment", "useSystemLanguage", "saveToCloud", "cosketchNickname", "cosketchColorR", "cosketchColorG", "cosketchColorB", "cosketchColorA", "microphonePreference", "microphoneDeviceName", "shareUI", "hideUserEmail", "defaultToLocalSave", "mirrorVisualisationType", "worldAxisType", "stageFloorType", "scaleSnapType", "contextualMeasurements", "readoutUnit", "overrideUnit", "onboardingToolsEnabled", "grabShapeType", "comfortLevel", "orthoGraphicPanelsVisible", "orthoGraphicBoundsVisible", "clockDisplayPreference", "timeReminderFrequency", "editPanelDefaultOpen", "importPreviewerPreferences", "exportPreferences", "externalCamX", "externalCamY", "externalCamZ", "externalCamQX", "externalCamQY", "externalCamQZ", "externalCamQW", "externalCamFocal", "fileVersion", "opaqueUI", "lastUserEmail", "padPreferences", "autoOpenLocalFilesWindow", "screenshotPreferencesTO", "usageHintStates", "usageStatistics", "useOculusAvatar", "windowMode", "selectionSettings", "deprecatedSpatialAnchorsUserEnabledBeta", "startupPreference", "brushProfiles", "materialProfiles", "materialProfileScopeIdType", "materialProfileScopeId", "mostRecentlySelectedExportPresetId", "watchedVideos", "mirror", "useGrid", "gridDensity", "disableTimeout", "uiVisibilityPolicy")
    USERID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LEFTHANDEDMODE_FIELD_NUMBER: _ClassVar[int]
    GHOSTMOVE_FIELD_NUMBER: _ClassVar[int]
    RETURNAFTERDUPLICATE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATIONLOCK_FIELD_NUMBER: _ClassVar[int]
    SMARTMOVE_FIELD_NUMBER: _ClassVar[int]
    HIGHQUALITYRENDERING_FIELD_NUMBER: _ClassVar[int]
    TEXTPOPUPS_FIELD_NUMBER: _ClassVar[int]
    DISABLEHAPTICS_FIELD_NUMBER: _ClassVar[int]
    ISSEATED_FIELD_NUMBER: _ClassVar[int]
    VIDEOTIPS_FIELD_NUMBER: _ClassVar[int]
    PREFERREDDISPLAYFREQUENCY_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERMODEL_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDSURFACECONTOURS_FIELD_NUMBER: _ClassVar[int]
    SURFACECONTOURSETTING_FIELD_NUMBER: _ClassVar[int]
    PASSTHROUGHENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    USESYSTEMLANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SAVETOCLOUD_FIELD_NUMBER: _ClassVar[int]
    COSKETCHNICKNAME_FIELD_NUMBER: _ClassVar[int]
    COSKETCHCOLORR_FIELD_NUMBER: _ClassVar[int]
    COSKETCHCOLORG_FIELD_NUMBER: _ClassVar[int]
    COSKETCHCOLORB_FIELD_NUMBER: _ClassVar[int]
    COSKETCHCOLORA_FIELD_NUMBER: _ClassVar[int]
    MICROPHONEPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    MICROPHONEDEVICENAME_FIELD_NUMBER: _ClassVar[int]
    SHAREUI_FIELD_NUMBER: _ClassVar[int]
    HIDEUSEREMAIL_FIELD_NUMBER: _ClassVar[int]
    DEFAULTTOLOCALSAVE_FIELD_NUMBER: _ClassVar[int]
    MIRRORVISUALISATIONTYPE_FIELD_NUMBER: _ClassVar[int]
    WORLDAXISTYPE_FIELD_NUMBER: _ClassVar[int]
    STAGEFLOORTYPE_FIELD_NUMBER: _ClassVar[int]
    SCALESNAPTYPE_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUALMEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
    READOUTUNIT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDEUNIT_FIELD_NUMBER: _ClassVar[int]
    ONBOARDINGTOOLSENABLED_FIELD_NUMBER: _ClassVar[int]
    GRABSHAPETYPE_FIELD_NUMBER: _ClassVar[int]
    COMFORTLEVEL_FIELD_NUMBER: _ClassVar[int]
    ORTHOGRAPHICPANELSVISIBLE_FIELD_NUMBER: _ClassVar[int]
    ORTHOGRAPHICBOUNDSVISIBLE_FIELD_NUMBER: _ClassVar[int]
    CLOCKDISPLAYPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    TIMEREMINDERFREQUENCY_FIELD_NUMBER: _ClassVar[int]
    EDITPANELDEFAULTOPEN_FIELD_NUMBER: _ClassVar[int]
    IMPORTPREVIEWERPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    EXPORTPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMX_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMY_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMZ_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMQX_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMQY_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMQZ_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMQW_FIELD_NUMBER: _ClassVar[int]
    EXTERNALCAMFOCAL_FIELD_NUMBER: _ClassVar[int]
    FILEVERSION_FIELD_NUMBER: _ClassVar[int]
    OPAQUEUI_FIELD_NUMBER: _ClassVar[int]
    LASTUSEREMAIL_FIELD_NUMBER: _ClassVar[int]
    PADPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    AUTOOPENLOCALFILESWINDOW_FIELD_NUMBER: _ClassVar[int]
    SCREENSHOTPREFERENCESTO_FIELD_NUMBER: _ClassVar[int]
    USAGEHINTSTATES_FIELD_NUMBER: _ClassVar[int]
    USAGESTATISTICS_FIELD_NUMBER: _ClassVar[int]
    USEOCULUSAVATAR_FIELD_NUMBER: _ClassVar[int]
    WINDOWMODE_FIELD_NUMBER: _ClassVar[int]
    SELECTIONSETTINGS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDSPATIALANCHORSUSERENABLEDBETA_FIELD_NUMBER: _ClassVar[int]
    STARTUPPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    BRUSHPROFILES_FIELD_NUMBER: _ClassVar[int]
    MATERIALPROFILES_FIELD_NUMBER: _ClassVar[int]
    MATERIALPROFILESCOPEIDTYPE_FIELD_NUMBER: _ClassVar[int]
    MATERIALPROFILESCOPEID_FIELD_NUMBER: _ClassVar[int]
    MOSTRECENTLYSELECTEDEXPORTPRESETID_FIELD_NUMBER: _ClassVar[int]
    WATCHEDVIDEOS_FIELD_NUMBER: _ClassVar[int]
    MIRROR_FIELD_NUMBER: _ClassVar[int]
    USEGRID_FIELD_NUMBER: _ClassVar[int]
    GRIDDENSITY_FIELD_NUMBER: _ClassVar[int]
    DISABLETIMEOUT_FIELD_NUMBER: _ClassVar[int]
    UIVISIBILITYPOLICY_FIELD_NUMBER: _ClassVar[int]
    userId: str
    language: _localization_pb2.LocalLang
    leftHandedMode: bool
    ghostMove: bool
    returnAfterDuplicate: bool
    orientationLock: bool
    smartMove: SmartMoveSetting
    highQualityRendering: bool
    textPopups: bool
    disableHaptics: bool
    isSeated: bool
    videoTips: bool
    preferredDisplayFrequency: float
    controllerModel: ControllerLook
    deprecatedSurfaceContours: bool
    surfaceContourSetting: SurfaceContourSetting
    passthroughEnvironment: bool
    useSystemLanguage: bool
    saveToCloud: bool
    cosketchNickname: str
    cosketchColorR: int
    cosketchColorG: int
    cosketchColorB: int
    cosketchColorA: int
    microphonePreference: MicrophonePreference
    microphoneDeviceName: str
    shareUI: TriBool
    hideUserEmail: bool
    defaultToLocalSave: bool
    mirrorVisualisationType: MirrorVisualisationType
    worldAxisType: WorldAxisType
    stageFloorType: StageFloorType
    scaleSnapType: ScaleSnapType
    contextualMeasurements: bool
    readoutUnit: _sketch_common_pb2.ReadoutUnit
    overrideUnit: _sketch_common_pb2.OverrideUnit
    onboardingToolsEnabled: bool
    grabShapeType: GrabShapeType
    comfortLevel: ComfortLevel
    orthoGraphicPanelsVisible: bool
    orthoGraphicBoundsVisible: bool
    clockDisplayPreference: ClockDisplayPreference
    timeReminderFrequency: TimeReminderFrequency
    editPanelDefaultOpen: bool
    importPreviewerPreferences: ImportPreviewerPreferencesTO
    exportPreferences: ExportPreferencesTO
    externalCamX: float
    externalCamY: float
    externalCamZ: float
    externalCamQX: float
    externalCamQY: float
    externalCamQZ: float
    externalCamQW: float
    externalCamFocal: float
    fileVersion: int
    opaqueUI: bool
    lastUserEmail: str
    padPreferences: PadPreferencesTO
    autoOpenLocalFilesWindow: bool
    screenshotPreferencesTO: ScreenshotPreferencesTO
    usageHintStates: _containers.RepeatedCompositeFieldContainer[UsageHintState]
    usageStatistics: UsageStatistics
    useOculusAvatar: bool
    windowMode: WindowMode
    selectionSettings: SelectionSettingsTO
    deprecatedSpatialAnchorsUserEnabledBeta: bool
    startupPreference: StartupPreference
    brushProfiles: _containers.RepeatedCompositeFieldContainer[BrushProfileTO]
    materialProfiles: _containers.RepeatedCompositeFieldContainer[MaterialProfile]
    materialProfileScopeIdType: _gravi_model_pb2.IdType
    materialProfileScopeId: str
    mostRecentlySelectedExportPresetId: _sketch_common_pb2.GSDataID
    watchedVideos: _containers.RepeatedCompositeFieldContainer[VideoWatchedProgress]
    mirror: bool
    useGrid: bool
    gridDensity: int
    disableTimeout: bool
    uiVisibilityPolicy: UIVisibilityPolicy
    def __init__(self, userId: _Optional[str] = ..., language: _Optional[_Union[_localization_pb2.LocalLang, str]] = ..., leftHandedMode: bool = ..., ghostMove: bool = ..., returnAfterDuplicate: bool = ..., orientationLock: bool = ..., smartMove: _Optional[_Union[SmartMoveSetting, str]] = ..., highQualityRendering: bool = ..., textPopups: bool = ..., disableHaptics: bool = ..., isSeated: bool = ..., videoTips: bool = ..., preferredDisplayFrequency: _Optional[float] = ..., controllerModel: _Optional[_Union[ControllerLook, str]] = ..., deprecatedSurfaceContours: bool = ..., surfaceContourSetting: _Optional[_Union[SurfaceContourSetting, str]] = ..., passthroughEnvironment: bool = ..., useSystemLanguage: bool = ..., saveToCloud: bool = ..., cosketchNickname: _Optional[str] = ..., cosketchColorR: _Optional[int] = ..., cosketchColorG: _Optional[int] = ..., cosketchColorB: _Optional[int] = ..., cosketchColorA: _Optional[int] = ..., microphonePreference: _Optional[_Union[MicrophonePreference, str]] = ..., microphoneDeviceName: _Optional[str] = ..., shareUI: _Optional[_Union[TriBool, str]] = ..., hideUserEmail: bool = ..., defaultToLocalSave: bool = ..., mirrorVisualisationType: _Optional[_Union[MirrorVisualisationType, str]] = ..., worldAxisType: _Optional[_Union[WorldAxisType, str]] = ..., stageFloorType: _Optional[_Union[StageFloorType, str]] = ..., scaleSnapType: _Optional[_Union[ScaleSnapType, str]] = ..., contextualMeasurements: bool = ..., readoutUnit: _Optional[_Union[_sketch_common_pb2.ReadoutUnit, str]] = ..., overrideUnit: _Optional[_Union[_sketch_common_pb2.OverrideUnit, str]] = ..., onboardingToolsEnabled: bool = ..., grabShapeType: _Optional[_Union[GrabShapeType, str]] = ..., comfortLevel: _Optional[_Union[ComfortLevel, str]] = ..., orthoGraphicPanelsVisible: bool = ..., orthoGraphicBoundsVisible: bool = ..., clockDisplayPreference: _Optional[_Union[ClockDisplayPreference, str]] = ..., timeReminderFrequency: _Optional[_Union[TimeReminderFrequency, str]] = ..., editPanelDefaultOpen: bool = ..., importPreviewerPreferences: _Optional[_Union[ImportPreviewerPreferencesTO, _Mapping]] = ..., exportPreferences: _Optional[_Union[ExportPreferencesTO, _Mapping]] = ..., externalCamX: _Optional[float] = ..., externalCamY: _Optional[float] = ..., externalCamZ: _Optional[float] = ..., externalCamQX: _Optional[float] = ..., externalCamQY: _Optional[float] = ..., externalCamQZ: _Optional[float] = ..., externalCamQW: _Optional[float] = ..., externalCamFocal: _Optional[float] = ..., fileVersion: _Optional[int] = ..., opaqueUI: bool = ..., lastUserEmail: _Optional[str] = ..., padPreferences: _Optional[_Union[PadPreferencesTO, _Mapping]] = ..., autoOpenLocalFilesWindow: bool = ..., screenshotPreferencesTO: _Optional[_Union[ScreenshotPreferencesTO, _Mapping]] = ..., usageHintStates: _Optional[_Iterable[_Union[UsageHintState, _Mapping]]] = ..., usageStatistics: _Optional[_Union[UsageStatistics, _Mapping]] = ..., useOculusAvatar: bool = ..., windowMode: _Optional[_Union[WindowMode, str]] = ..., selectionSettings: _Optional[_Union[SelectionSettingsTO, _Mapping]] = ..., deprecatedSpatialAnchorsUserEnabledBeta: bool = ..., startupPreference: _Optional[_Union[StartupPreference, str]] = ..., brushProfiles: _Optional[_Iterable[_Union[BrushProfileTO, _Mapping]]] = ..., materialProfiles: _Optional[_Iterable[_Union[MaterialProfile, _Mapping]]] = ..., materialProfileScopeIdType: _Optional[_Union[_gravi_model_pb2.IdType, str]] = ..., materialProfileScopeId: _Optional[str] = ..., mostRecentlySelectedExportPresetId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., watchedVideos: _Optional[_Iterable[_Union[VideoWatchedProgress, _Mapping]]] = ..., mirror: bool = ..., useGrid: bool = ..., gridDensity: _Optional[int] = ..., disableTimeout: bool = ..., uiVisibilityPolicy: _Optional[_Union[UIVisibilityPolicy, str]] = ...) -> None: ...

class ScreenshotPreferencesTO(_message.Message):
    __slots__ = ("isAddAsReferenceImage", "isPreviewDof", "isTransparent", "isRender", "isVerticalLock", "isMakeViewpointDEPRECATED", "advancedSettingsOn", "focalLength", "aspectRatioType")
    ISADDASREFERENCEIMAGE_FIELD_NUMBER: _ClassVar[int]
    ISPREVIEWDOF_FIELD_NUMBER: _ClassVar[int]
    ISTRANSPARENT_FIELD_NUMBER: _ClassVar[int]
    ISRENDER_FIELD_NUMBER: _ClassVar[int]
    ISVERTICALLOCK_FIELD_NUMBER: _ClassVar[int]
    ISMAKEVIEWPOINTDEPRECATED_FIELD_NUMBER: _ClassVar[int]
    ADVANCEDSETTINGSON_FIELD_NUMBER: _ClassVar[int]
    FOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    ASPECTRATIOTYPE_FIELD_NUMBER: _ClassVar[int]
    isAddAsReferenceImage: bool
    isPreviewDof: bool
    isTransparent: bool
    isRender: bool
    isVerticalLock: bool
    isMakeViewpointDEPRECATED: bool
    advancedSettingsOn: bool
    focalLength: float
    aspectRatioType: AspectRatioType
    def __init__(self, isAddAsReferenceImage: bool = ..., isPreviewDof: bool = ..., isTransparent: bool = ..., isRender: bool = ..., isVerticalLock: bool = ..., isMakeViewpointDEPRECATED: bool = ..., advancedSettingsOn: bool = ..., focalLength: _Optional[float] = ..., aspectRatioType: _Optional[_Union[AspectRatioType, str]] = ...) -> None: ...

class SelectionSettingsTO(_message.Message):
    __slots__ = ("selectionToolMode", "respectGroupsWhenSelecting", "showGumball", "showBoundingBox", "restrictToMirror")
    SELECTIONTOOLMODE_FIELD_NUMBER: _ClassVar[int]
    RESPECTGROUPSWHENSELECTING_FIELD_NUMBER: _ClassVar[int]
    SHOWGUMBALL_FIELD_NUMBER: _ClassVar[int]
    SHOWBOUNDINGBOX_FIELD_NUMBER: _ClassVar[int]
    RESTRICTTOMIRROR_FIELD_NUMBER: _ClassVar[int]
    selectionToolMode: SelectionToolMode
    respectGroupsWhenSelecting: bool
    showGumball: bool
    showBoundingBox: bool
    restrictToMirror: bool
    def __init__(self, selectionToolMode: _Optional[_Union[SelectionToolMode, str]] = ..., respectGroupsWhenSelecting: bool = ..., showGumball: bool = ..., showBoundingBox: bool = ..., restrictToMirror: bool = ...) -> None: ...

class ColorSwatchTO(_message.Message):
    __slots__ = ("r", "g", "b", "index")
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    r: float
    g: float
    b: float
    index: int
    def __init__(self, r: _Optional[float] = ..., g: _Optional[float] = ..., b: _Optional[float] = ..., index: _Optional[int] = ...) -> None: ...

class PadSelectionModeOptions(_message.Message):
    __slots__ = ("deprecatedEditModeEnabled", "gumballEnabled", "planarityBroken")
    DEPRECATEDEDITMODEENABLED_FIELD_NUMBER: _ClassVar[int]
    GUMBALLENABLED_FIELD_NUMBER: _ClassVar[int]
    PLANARITYBROKEN_FIELD_NUMBER: _ClassVar[int]
    deprecatedEditModeEnabled: bool
    gumballEnabled: bool
    planarityBroken: bool
    def __init__(self, deprecatedEditModeEnabled: bool = ..., gumballEnabled: bool = ..., planarityBroken: bool = ...) -> None: ...

class PadNavigationPreferences(_message.Message):
    __slots__ = ("orbitSnapbackThreshold", "rotationThreshold", "zoomThreshold", "zoomSpeed", "freeCameraPanThreshold", "deprecatedInitialisedToDefaults")
    ORBITSNAPBACKTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ROTATIONTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ZOOMTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ZOOMSPEED_FIELD_NUMBER: _ClassVar[int]
    FREECAMERAPANTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDINITIALISEDTODEFAULTS_FIELD_NUMBER: _ClassVar[int]
    orbitSnapbackThreshold: float
    rotationThreshold: float
    zoomThreshold: float
    zoomSpeed: float
    freeCameraPanThreshold: float
    deprecatedInitialisedToDefaults: bool
    def __init__(self, orbitSnapbackThreshold: _Optional[float] = ..., rotationThreshold: _Optional[float] = ..., zoomThreshold: _Optional[float] = ..., zoomSpeed: _Optional[float] = ..., freeCameraPanThreshold: _Optional[float] = ..., deprecatedInitialisedToDefaults: bool = ...) -> None: ...

class PadPreferencesTO(_message.Message):
    __slots__ = ("cameraType", "drawPlaneCameraMode", "freeCameraMode", "drawPlaneCameraFocalLength", "freeCameraFocalLength", "verticalLock", "penMode", "rightHanded", "worldAxis", "floorGrid", "navigationCube", "navigationArrows", "rotationAxisType", "selectionModeOptions", "colorSelectionPreference", "navigationPreferences", "colorSwatches", "visibleCursor", "planeShadows", "initialisedToDefaults", "penOnceDetected")
    CAMERATYPE_FIELD_NUMBER: _ClassVar[int]
    DRAWPLANECAMERAMODE_FIELD_NUMBER: _ClassVar[int]
    FREECAMERAMODE_FIELD_NUMBER: _ClassVar[int]
    DRAWPLANECAMERAFOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    FREECAMERAFOCALLENGTH_FIELD_NUMBER: _ClassVar[int]
    VERTICALLOCK_FIELD_NUMBER: _ClassVar[int]
    PENMODE_FIELD_NUMBER: _ClassVar[int]
    RIGHTHANDED_FIELD_NUMBER: _ClassVar[int]
    WORLDAXIS_FIELD_NUMBER: _ClassVar[int]
    FLOORGRID_FIELD_NUMBER: _ClassVar[int]
    NAVIGATIONCUBE_FIELD_NUMBER: _ClassVar[int]
    NAVIGATIONARROWS_FIELD_NUMBER: _ClassVar[int]
    ROTATIONAXISTYPE_FIELD_NUMBER: _ClassVar[int]
    SELECTIONMODEOPTIONS_FIELD_NUMBER: _ClassVar[int]
    COLORSELECTIONPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    NAVIGATIONPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    COLORSWATCHES_FIELD_NUMBER: _ClassVar[int]
    VISIBLECURSOR_FIELD_NUMBER: _ClassVar[int]
    PLANESHADOWS_FIELD_NUMBER: _ClassVar[int]
    INITIALISEDTODEFAULTS_FIELD_NUMBER: _ClassVar[int]
    PENONCEDETECTED_FIELD_NUMBER: _ClassVar[int]
    cameraType: PadCameraType
    drawPlaneCameraMode: PerspectiveMode
    freeCameraMode: PerspectiveMode
    drawPlaneCameraFocalLength: float
    freeCameraFocalLength: float
    verticalLock: bool
    penMode: bool
    rightHanded: bool
    worldAxis: bool
    floorGrid: bool
    navigationCube: bool
    navigationArrows: bool
    rotationAxisType: PadRotationAxisType
    selectionModeOptions: PadSelectionModeOptions
    colorSelectionPreference: PadColorSelectionPreference
    navigationPreferences: PadNavigationPreferences
    colorSwatches: _containers.RepeatedCompositeFieldContainer[ColorSwatchTO]
    visibleCursor: bool
    planeShadows: bool
    initialisedToDefaults: bool
    penOnceDetected: bool
    def __init__(self, cameraType: _Optional[_Union[PadCameraType, str]] = ..., drawPlaneCameraMode: _Optional[_Union[PerspectiveMode, str]] = ..., freeCameraMode: _Optional[_Union[PerspectiveMode, str]] = ..., drawPlaneCameraFocalLength: _Optional[float] = ..., freeCameraFocalLength: _Optional[float] = ..., verticalLock: bool = ..., penMode: bool = ..., rightHanded: bool = ..., worldAxis: bool = ..., floorGrid: bool = ..., navigationCube: bool = ..., navigationArrows: bool = ..., rotationAxisType: _Optional[_Union[PadRotationAxisType, str]] = ..., selectionModeOptions: _Optional[_Union[PadSelectionModeOptions, _Mapping]] = ..., colorSelectionPreference: _Optional[_Union[PadColorSelectionPreference, str]] = ..., navigationPreferences: _Optional[_Union[PadNavigationPreferences, _Mapping]] = ..., colorSwatches: _Optional[_Iterable[_Union[ColorSwatchTO, _Mapping]]] = ..., visibleCursor: bool = ..., planeShadows: bool = ..., initialisedToDefaults: bool = ..., penOnceDetected: bool = ...) -> None: ...

class UsageHintState(_message.Message):
    __slots__ = ("hintType", "isFreshHint", "timesTriggered")
    HINTTYPE_FIELD_NUMBER: _ClassVar[int]
    ISFRESHHINT_FIELD_NUMBER: _ClassVar[int]
    TIMESTRIGGERED_FIELD_NUMBER: _ClassVar[int]
    hintType: _sketch_common_pb2.UsageHint
    isFreshHint: bool
    timesTriggered: int
    def __init__(self, hintType: _Optional[_Union[_sketch_common_pb2.UsageHint, str]] = ..., isFreshHint: bool = ..., timesTriggered: _Optional[int] = ...) -> None: ...

class UsageStatistics(_message.Message):
    __slots__ = ("cumulativeMinsSpentSketching", "numEditModeSessions")
    CUMULATIVEMINSSPENTSKETCHING_FIELD_NUMBER: _ClassVar[int]
    NUMEDITMODESESSIONS_FIELD_NUMBER: _ClassVar[int]
    cumulativeMinsSpentSketching: int
    numEditModeSessions: int
    def __init__(self, cumulativeMinsSpentSketching: _Optional[int] = ..., numEditModeSessions: _Optional[int] = ...) -> None: ...

class UserDefaultsProfileCollectionTO(_message.Message):
    __slots__ = ("currentProfName", "profiles")
    CURRENTPROFNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILES_FIELD_NUMBER: _ClassVar[int]
    currentProfName: str
    profiles: _containers.RepeatedCompositeFieldContainer[UserDefaultsProfileTO]
    def __init__(self, currentProfName: _Optional[str] = ..., profiles: _Optional[_Iterable[_Union[UserDefaultsProfileTO, _Mapping]]] = ...) -> None: ...

class UserDefaultsProfileTO(_message.Message):
    __slots__ = ("profileName", "mirror", "useGrid", "gridDensity", "fileVersion")
    PROFILENAME_FIELD_NUMBER: _ClassVar[int]
    MIRROR_FIELD_NUMBER: _ClassVar[int]
    USEGRID_FIELD_NUMBER: _ClassVar[int]
    GRIDDENSITY_FIELD_NUMBER: _ClassVar[int]
    FILEVERSION_FIELD_NUMBER: _ClassVar[int]
    profileName: str
    mirror: bool
    useGrid: bool
    gridDensity: int
    fileVersion: int
    def __init__(self, profileName: _Optional[str] = ..., mirror: bool = ..., useGrid: bool = ..., gridDensity: _Optional[int] = ..., fileVersion: _Optional[int] = ...) -> None: ...

class BrushProfileTO(_message.Message):
    __slots__ = ("brushProfileId", "brushProfileName", "hasBrushNameBeenUserModifiedFromDefault", "SplineType", "brushShape", "strokeSizeX", "strokeSizeY", "lowPoly", "capEnds", "SelectedBrushShape", "roundCorners", "inputMode", "projectionMode", "pressureMode", "primitiveInputMode", "inputSmoothing", "snapDrawing", "polarSymmetryDuplicateCount", "repeatingUVs", "autoScale", "surfaceCurveTension", "fullSurfaceCurve", "fourPointSurface", "surfaceCurveSize", "revolveThickness", "revolveRotation", "revolveChosenRepeats", "primitiveDrawnAsSubD", "primitiveCustomiseSubD", "textFontName", "NonStretched", "nonPolyCap")
    BRUSHPROFILEID_FIELD_NUMBER: _ClassVar[int]
    BRUSHPROFILENAME_FIELD_NUMBER: _ClassVar[int]
    HASBRUSHNAMEBEENUSERMODIFIEDFROMDEFAULT_FIELD_NUMBER: _ClassVar[int]
    SPLINETYPE_FIELD_NUMBER: _ClassVar[int]
    BRUSHSHAPE_FIELD_NUMBER: _ClassVar[int]
    STROKESIZEX_FIELD_NUMBER: _ClassVar[int]
    STROKESIZEY_FIELD_NUMBER: _ClassVar[int]
    LOWPOLY_FIELD_NUMBER: _ClassVar[int]
    CAPENDS_FIELD_NUMBER: _ClassVar[int]
    SELECTEDBRUSHSHAPE_FIELD_NUMBER: _ClassVar[int]
    ROUNDCORNERS_FIELD_NUMBER: _ClassVar[int]
    INPUTMODE_FIELD_NUMBER: _ClassVar[int]
    PROJECTIONMODE_FIELD_NUMBER: _ClassVar[int]
    PRESSUREMODE_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVEINPUTMODE_FIELD_NUMBER: _ClassVar[int]
    INPUTSMOOTHING_FIELD_NUMBER: _ClassVar[int]
    SNAPDRAWING_FIELD_NUMBER: _ClassVar[int]
    POLARSYMMETRYDUPLICATECOUNT_FIELD_NUMBER: _ClassVar[int]
    REPEATINGUVS_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALE_FIELD_NUMBER: _ClassVar[int]
    SURFACECURVETENSION_FIELD_NUMBER: _ClassVar[int]
    FULLSURFACECURVE_FIELD_NUMBER: _ClassVar[int]
    FOURPOINTSURFACE_FIELD_NUMBER: _ClassVar[int]
    SURFACECURVESIZE_FIELD_NUMBER: _ClassVar[int]
    REVOLVETHICKNESS_FIELD_NUMBER: _ClassVar[int]
    REVOLVEROTATION_FIELD_NUMBER: _ClassVar[int]
    REVOLVECHOSENREPEATS_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVEDRAWNASSUBD_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVECUSTOMISESUBD_FIELD_NUMBER: _ClassVar[int]
    TEXTFONTNAME_FIELD_NUMBER: _ClassVar[int]
    NONSTRETCHED_FIELD_NUMBER: _ClassVar[int]
    NONPOLYCAP_FIELD_NUMBER: _ClassVar[int]
    brushProfileId: _sketch_common_pb2.GSDataID
    brushProfileName: str
    hasBrushNameBeenUserModifiedFromDefault: bool
    SplineType: _sketch_common_pb2.SplineType
    brushShape: _sketch_common_pb2.BrushShape
    strokeSizeX: float
    strokeSizeY: float
    lowPoly: bool
    capEnds: bool
    SelectedBrushShape: _sketch_common_pb2.BrushShape
    roundCorners: bool
    inputMode: _sketch_inputs_pb2.InputMode
    projectionMode: _sketch_inputs_pb2.ProjectionMode
    pressureMode: _sketch_inputs_pb2.PressureMode
    primitiveInputMode: PrimitiveDrawingPreference
    inputSmoothing: float
    snapDrawing: bool
    polarSymmetryDuplicateCount: int
    repeatingUVs: bool
    autoScale: bool
    surfaceCurveTension: float
    fullSurfaceCurve: bool
    fourPointSurface: bool
    surfaceCurveSize: float
    revolveThickness: float
    revolveRotation: int
    revolveChosenRepeats: int
    primitiveDrawnAsSubD: bool
    primitiveCustomiseSubD: bool
    textFontName: str
    NonStretched: bool
    nonPolyCap: bool
    def __init__(self, brushProfileId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., brushProfileName: _Optional[str] = ..., hasBrushNameBeenUserModifiedFromDefault: bool = ..., SplineType: _Optional[_Union[_sketch_common_pb2.SplineType, str]] = ..., brushShape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., strokeSizeX: _Optional[float] = ..., strokeSizeY: _Optional[float] = ..., lowPoly: bool = ..., capEnds: bool = ..., SelectedBrushShape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., roundCorners: bool = ..., inputMode: _Optional[_Union[_sketch_inputs_pb2.InputMode, str]] = ..., projectionMode: _Optional[_Union[_sketch_inputs_pb2.ProjectionMode, str]] = ..., pressureMode: _Optional[_Union[_sketch_inputs_pb2.PressureMode, str]] = ..., primitiveInputMode: _Optional[_Union[PrimitiveDrawingPreference, str]] = ..., inputSmoothing: _Optional[float] = ..., snapDrawing: bool = ..., polarSymmetryDuplicateCount: _Optional[int] = ..., repeatingUVs: bool = ..., autoScale: bool = ..., surfaceCurveTension: _Optional[float] = ..., fullSurfaceCurve: bool = ..., fourPointSurface: bool = ..., surfaceCurveSize: _Optional[float] = ..., revolveThickness: _Optional[float] = ..., revolveRotation: _Optional[int] = ..., revolveChosenRepeats: _Optional[int] = ..., primitiveDrawnAsSubD: bool = ..., primitiveCustomiseSubD: bool = ..., textFontName: _Optional[str] = ..., NonStretched: bool = ..., nonPolyCap: bool = ...) -> None: ...

class ImportPreviewerPreferencesTO(_message.Message):
    __slots__ = ("units", "OrientationQx", "OrientationQy", "OrientationQz", "OrientationQw", "addToNewLayer")
    UNITS_FIELD_NUMBER: _ClassVar[int]
    ORIENTATIONQX_FIELD_NUMBER: _ClassVar[int]
    ORIENTATIONQY_FIELD_NUMBER: _ClassVar[int]
    ORIENTATIONQZ_FIELD_NUMBER: _ClassVar[int]
    ORIENTATIONQW_FIELD_NUMBER: _ClassVar[int]
    ADDTONEWLAYER_FIELD_NUMBER: _ClassVar[int]
    units: int
    OrientationQx: float
    OrientationQy: float
    OrientationQz: float
    OrientationQw: float
    addToNewLayer: bool
    def __init__(self, units: _Optional[int] = ..., OrientationQx: _Optional[float] = ..., OrientationQy: _Optional[float] = ..., OrientationQz: _Optional[float] = ..., OrientationQw: _Optional[float] = ..., addToNewLayer: bool = ...) -> None: ...

class ExportPreferenceHint(_message.Message):
    __slots__ = ("presetId", "presetDescription", "presetUsageInfo")
    PRESETID_FIELD_NUMBER: _ClassVar[int]
    PRESETDESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRESETUSAGEINFO_FIELD_NUMBER: _ClassVar[int]
    presetId: _sketch_common_pb2.GSDataID
    presetDescription: str
    presetUsageInfo: str
    def __init__(self, presetId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., presetDescription: _Optional[str] = ..., presetUsageInfo: _Optional[str] = ...) -> None: ...

class ExportPresetListTO(_message.Message):
    __slots__ = ("orderedExportPresetsTO", "usageHintStates")
    ORDEREDEXPORTPRESETSTO_FIELD_NUMBER: _ClassVar[int]
    USAGEHINTSTATES_FIELD_NUMBER: _ClassVar[int]
    orderedExportPresetsTO: _containers.RepeatedCompositeFieldContainer[ExportPreferencesTO]
    usageHintStates: _containers.RepeatedCompositeFieldContainer[ExportPreferenceHint]
    def __init__(self, orderedExportPresetsTO: _Optional[_Iterable[_Union[ExportPreferencesTO, _Mapping]]] = ..., usageHintStates: _Optional[_Iterable[_Union[ExportPreferenceHint, _Mapping]]] = ...) -> None: ...

class ExportPreferencesTO(_message.Message):
    __slots__ = ("baseAxes", "scaleSetting", "singleSided", "useSubDControlMesh", "weldVertices", "fileType", "discretizationResolution", "bakeTransforms", "nurbsPreference", "collectGroups", "mp4ExportStyle", "preferenceId", "preferenceDisplayName")
    BASEAXES_FIELD_NUMBER: _ClassVar[int]
    SCALESETTING_FIELD_NUMBER: _ClassVar[int]
    SINGLESIDED_FIELD_NUMBER: _ClassVar[int]
    USESUBDCONTROLMESH_FIELD_NUMBER: _ClassVar[int]
    WELDVERTICES_FIELD_NUMBER: _ClassVar[int]
    FILETYPE_FIELD_NUMBER: _ClassVar[int]
    DISCRETIZATIONRESOLUTION_FIELD_NUMBER: _ClassVar[int]
    BAKETRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    NURBSPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    COLLECTGROUPS_FIELD_NUMBER: _ClassVar[int]
    MP4EXPORTSTYLE_FIELD_NUMBER: _ClassVar[int]
    PREFERENCEID_FIELD_NUMBER: _ClassVar[int]
    PREFERENCEDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    baseAxes: BaseAxisConfiguration
    scaleSetting: ScaleSetting
    singleSided: bool
    useSubDControlMesh: bool
    weldVertices: bool
    fileType: ExportFileType
    discretizationResolution: DiscretizationResolution
    bakeTransforms: bool
    nurbsPreference: FbxExportNurbsPreference
    collectGroups: bool
    mp4ExportStyle: MP4ExportStyle
    preferenceId: _sketch_common_pb2.GSDataID
    preferenceDisplayName: str
    def __init__(self, baseAxes: _Optional[_Union[BaseAxisConfiguration, str]] = ..., scaleSetting: _Optional[_Union[ScaleSetting, str]] = ..., singleSided: bool = ..., useSubDControlMesh: bool = ..., weldVertices: bool = ..., fileType: _Optional[_Union[ExportFileType, str]] = ..., discretizationResolution: _Optional[_Union[DiscretizationResolution, str]] = ..., bakeTransforms: bool = ..., nurbsPreference: _Optional[_Union[FbxExportNurbsPreference, str]] = ..., collectGroups: bool = ..., mp4ExportStyle: _Optional[_Union[MP4ExportStyle, str]] = ..., preferenceId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., preferenceDisplayName: _Optional[str] = ...) -> None: ...

class BrowserCookieTO(_message.Message):
    __slots__ = ("domain", "expirationDate", "httpOnly", "isValid", "name", "path", "secure", "value")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    HTTPONLY_FIELD_NUMBER: _ClassVar[int]
    ISVALID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    domain: str
    expirationDate: int
    httpOnly: bool
    isValid: bool
    name: str
    path: str
    secure: bool
    value: str
    def __init__(self, domain: _Optional[str] = ..., expirationDate: _Optional[int] = ..., httpOnly: bool = ..., isValid: bool = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., secure: bool = ..., value: _Optional[str] = ...) -> None: ...

class MaterialProfile(_message.Message):
    __slots__ = ("material", "isDefault")
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    ISDEFAULT_FIELD_NUMBER: _ClassVar[int]
    material: _sketch_common_pb2.DrawMaterial
    isDefault: bool
    def __init__(self, material: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ..., isDefault: bool = ...) -> None: ...

class VideoWatchedProgress(_message.Message):
    __slots__ = ("videoId", "reachedEnd", "secondsRemaining")
    VIDEOID_FIELD_NUMBER: _ClassVar[int]
    REACHEDEND_FIELD_NUMBER: _ClassVar[int]
    SECONDSREMAINING_FIELD_NUMBER: _ClassVar[int]
    videoId: str
    reachedEnd: bool
    secondsRemaining: int
    def __init__(self, videoId: _Optional[str] = ..., reachedEnd: bool = ..., secondsRemaining: _Optional[int] = ...) -> None: ...

class SavedMaterialsFile(_message.Message):
    __slots__ = ("materials", "materialVersion", "presetMaterialsIteration")
    MATERIALS_FIELD_NUMBER: _ClassVar[int]
    MATERIALVERSION_FIELD_NUMBER: _ClassVar[int]
    PRESETMATERIALSITERATION_FIELD_NUMBER: _ClassVar[int]
    materials: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    materialVersion: int
    presetMaterialsIteration: PresetMaterialsIteration
    def __init__(self, materials: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., materialVersion: _Optional[int] = ..., presetMaterialsIteration: _Optional[_Union[PresetMaterialsIteration, str]] = ...) -> None: ...
