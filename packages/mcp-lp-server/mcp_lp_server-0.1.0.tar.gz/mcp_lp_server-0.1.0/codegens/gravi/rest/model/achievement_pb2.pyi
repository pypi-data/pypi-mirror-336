import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AchievementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AchievementUnset: _ClassVar[AchievementType]
    AchievementNewSketch: _ClassVar[AchievementType]
    AchievementTutorialVideo: _ClassVar[AchievementType]
    AchievementUseCreationTool: _ClassVar[AchievementType]
    AchievementOpenToolBelt: _ClassVar[AchievementType]
    AchievementChangeEnvironment: _ClassVar[AchievementType]
    AchievementScaleAvatar: _ClassVar[AchievementType]
    AchievementUseEditMode: _ClassVar[AchievementType]
    AchievementUseColourPicker: _ClassVar[AchievementType]
    AchievementDeleteObject: _ClassVar[AchievementType]
    AchievementUseInk1: _ClassVar[AchievementType]
    AchievementUseInk20: _ClassVar[AchievementType]
    AchievementUseRevolve1: _ClassVar[AchievementType]
    AchievementUseRevolve20: _ClassVar[AchievementType]
    AchievementUseVolume1: _ClassVar[AchievementType]
    AchievementUseVolume20: _ClassVar[AchievementType]
    AchievementUseStroke1: _ClassVar[AchievementType]
    AchievementUseStroke20: _ClassVar[AchievementType]
    AchievementUseSurface1: _ClassVar[AchievementType]
    AchievementUseSurface20: _ClassVar[AchievementType]
    AchievementPrimitive1: _ClassVar[AchievementType]
    AchievementPrimitive20: _ClassVar[AchievementType]
    AchievementSubd1: _ClassVar[AchievementType]
    AchievementSubd20: _ClassVar[AchievementType]
    AchievementGrabObject: _ClassVar[AchievementType]
    AchievementNavigate: _ClassVar[AchievementType]
    AchievementBringInMannequin: _ClassVar[AchievementType]
    AchievementUseMirror: _ClassVar[AchievementType]
    AchievementDimensionLine1: _ClassVar[AchievementType]
    AchievementDimensionLine20: _ClassVar[AchievementType]
    AchievementSubmitLPEmail: _ClassVar[AchievementType]
    AchievementLPAccount: _ClassVar[AchievementType]
    AchievementSetupPassword: _ClassVar[AchievementType]
    AchievementFinishSurvey: _ClassVar[AchievementType]
    AchievementSaveSketch: _ClassVar[AchievementType]
    AchievementExportSketch: _ClassVar[AchievementType]
    AchievementTakeScreenshot: _ClassVar[AchievementType]
    AchievementImportRefImage: _ClassVar[AchievementType]
    AchievementOpenGallerySketch: _ClassVar[AchievementType]
    AchievementImportPrefab: _ClassVar[AchievementType]
    AchievementSketchWithinFirst48Hours: _ClassVar[AchievementType]
    AchievementSketchBetweenDay2And7: _ClassVar[AchievementType]
    AchievementSubDBugRepair: _ClassVar[AchievementType]
    AchievementCompleteFirstSketch: _ClassVar[AchievementType]
AchievementUnset: AchievementType
AchievementNewSketch: AchievementType
AchievementTutorialVideo: AchievementType
AchievementUseCreationTool: AchievementType
AchievementOpenToolBelt: AchievementType
AchievementChangeEnvironment: AchievementType
AchievementScaleAvatar: AchievementType
AchievementUseEditMode: AchievementType
AchievementUseColourPicker: AchievementType
AchievementDeleteObject: AchievementType
AchievementUseInk1: AchievementType
AchievementUseInk20: AchievementType
AchievementUseRevolve1: AchievementType
AchievementUseRevolve20: AchievementType
AchievementUseVolume1: AchievementType
AchievementUseVolume20: AchievementType
AchievementUseStroke1: AchievementType
AchievementUseStroke20: AchievementType
AchievementUseSurface1: AchievementType
AchievementUseSurface20: AchievementType
AchievementPrimitive1: AchievementType
AchievementPrimitive20: AchievementType
AchievementSubd1: AchievementType
AchievementSubd20: AchievementType
AchievementGrabObject: AchievementType
AchievementNavigate: AchievementType
AchievementBringInMannequin: AchievementType
AchievementUseMirror: AchievementType
AchievementDimensionLine1: AchievementType
AchievementDimensionLine20: AchievementType
AchievementSubmitLPEmail: AchievementType
AchievementLPAccount: AchievementType
AchievementSetupPassword: AchievementType
AchievementFinishSurvey: AchievementType
AchievementSaveSketch: AchievementType
AchievementExportSketch: AchievementType
AchievementTakeScreenshot: AchievementType
AchievementImportRefImage: AchievementType
AchievementOpenGallerySketch: AchievementType
AchievementImportPrefab: AchievementType
AchievementSketchWithinFirst48Hours: AchievementType
AchievementSketchBetweenDay2And7: AchievementType
AchievementSubDBugRepair: AchievementType
AchievementCompleteFirstSketch: AchievementType

class AchievementRecord(_message.Message):
    __slots__ = ("achievementType", "targetCounter", "targetActions", "achievedOn")
    class TargetActionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ACHIEVEMENTTYPE_FIELD_NUMBER: _ClassVar[int]
    TARGETCOUNTER_FIELD_NUMBER: _ClassVar[int]
    TARGETACTIONS_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEDON_FIELD_NUMBER: _ClassVar[int]
    achievementType: AchievementType
    targetCounter: int
    targetActions: _containers.ScalarMap[str, int]
    achievedOn: int
    def __init__(self, achievementType: _Optional[_Union[AchievementType, str]] = ..., targetCounter: _Optional[int] = ..., targetActions: _Optional[_Mapping[str, int]] = ..., achievedOn: _Optional[int] = ...) -> None: ...
