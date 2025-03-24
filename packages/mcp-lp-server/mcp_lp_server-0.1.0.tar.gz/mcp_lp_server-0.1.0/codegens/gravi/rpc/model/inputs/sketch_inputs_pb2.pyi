import gs_options_pb2 as _gs_options_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Mixed: _ClassVar[InputMode]
    Points: _ClassVar[InputMode]
    ConnectCurves: _ClassVar[InputMode]
    SurfaceFromSpline: _ClassVar[InputMode]

class ProjectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidProjection: _ClassVar[ProjectionMode]
    NoProjection: _ClassVar[ProjectionMode]
    DefaultProjection: _ClassVar[ProjectionMode]
    PlanarProjection: _ClassVar[ProjectionMode]

class PressureMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    None: _ClassVar[PressureMode]
    Speed: _ClassVar[PressureMode]
    Pressure: _ClassVar[PressureMode]
    SpeedInverted: _ClassVar[PressureMode]
    PressureInverted: _ClassVar[PressureMode]
    Taper: _ClassVar[PressureMode]
    TaperInverted: _ClassVar[PressureMode]

class ToolModeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidToolMode: _ClassVar[ToolModeType]
    Idle: _ClassVar[ToolModeType]
    Drawing: _ClassVar[ToolModeType]
    Grabbing: _ClassVar[ToolModeType]
    Screenshot: _ClassVar[ToolModeType]
    ControlPoint: _ClassVar[ToolModeType]
    UIUsing: _ClassVar[ToolModeType]
    Keyboard: _ClassVar[ToolModeType]
    SubDCustomisePrimitive: _ClassVar[ToolModeType]
    Export: _ClassVar[ToolModeType]
    MiniMap: _ClassVar[ToolModeType]
    ViewPointEdit: _ClassVar[ToolModeType]
    ViewerMode: _ClassVar[ToolModeType]
    Import: _ClassVar[ToolModeType]

class SketchTool(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidSketchTool: _ClassVar[SketchTool]
    NoSketchTool: _ClassVar[SketchTool]
    Draw: _ClassVar[SketchTool]
    Selection: _ClassVar[SketchTool]
    ColourPicker: _ClassVar[SketchTool]
    Laser: _ClassVar[SketchTool]
    Measurement: _ClassVar[SketchTool]
    Viewpoint: _ClassVar[SketchTool]
    Teleporter: _ClassVar[SketchTool]
    Paintbrush: _ClassVar[SketchTool]
    CrossSection: _ClassVar[SketchTool]
    FlipNormals: _ClassVar[SketchTool]

class EditTool(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidEditTool: _ClassVar[EditTool]
    NoEditTool: _ClassVar[EditTool]
    StandardEdit: _ClassVar[EditTool]
    EditSelection: _ClassVar[EditTool]
    SubDEdit: _ClassVar[EditTool]

class ExportTool(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidExportTool: _ClassVar[ExportTool]
    NoExportTool: _ClassVar[ExportTool]
Mixed: InputMode
Points: InputMode
ConnectCurves: InputMode
SurfaceFromSpline: InputMode
InvalidProjection: ProjectionMode
NoProjection: ProjectionMode
DefaultProjection: ProjectionMode
PlanarProjection: ProjectionMode
None: PressureMode
Speed: PressureMode
Pressure: PressureMode
SpeedInverted: PressureMode
PressureInverted: PressureMode
Taper: PressureMode
TaperInverted: PressureMode
InvalidToolMode: ToolModeType
Idle: ToolModeType
Drawing: ToolModeType
Grabbing: ToolModeType
Screenshot: ToolModeType
ControlPoint: ToolModeType
UIUsing: ToolModeType
Keyboard: ToolModeType
SubDCustomisePrimitive: ToolModeType
Export: ToolModeType
MiniMap: ToolModeType
ViewPointEdit: ToolModeType
ViewerMode: ToolModeType
Import: ToolModeType
InvalidSketchTool: SketchTool
NoSketchTool: SketchTool
Draw: SketchTool
Selection: SketchTool
ColourPicker: SketchTool
Laser: SketchTool
Measurement: SketchTool
Viewpoint: SketchTool
Teleporter: SketchTool
Paintbrush: SketchTool
CrossSection: SketchTool
FlipNormals: SketchTool
InvalidEditTool: EditTool
NoEditTool: EditTool
StandardEdit: EditTool
EditSelection: EditTool
SubDEdit: EditTool
InvalidExportTool: ExportTool
NoExportTool: ExportTool

class UserToolModeStates(_message.Message):
    __slots__ = ("currentToolMode", "exitBackToolMode", "baseToolMode")
    CURRENTTOOLMODE_FIELD_NUMBER: _ClassVar[int]
    EXITBACKTOOLMODE_FIELD_NUMBER: _ClassVar[int]
    BASETOOLMODE_FIELD_NUMBER: _ClassVar[int]
    currentToolMode: ToolModeType
    exitBackToolMode: ToolModeType
    baseToolMode: ToolModeType
    def __init__(self, currentToolMode: _Optional[_Union[ToolModeType, str]] = ..., exitBackToolMode: _Optional[_Union[ToolModeType, str]] = ..., baseToolMode: _Optional[_Union[ToolModeType, str]] = ...) -> None: ...

class UserToolStates(_message.Message):
    __slots__ = ("sketchTool", "editTool", "exportTool")
    SKETCHTOOL_FIELD_NUMBER: _ClassVar[int]
    EDITTOOL_FIELD_NUMBER: _ClassVar[int]
    EXPORTTOOL_FIELD_NUMBER: _ClassVar[int]
    sketchTool: SketchTool
    editTool: EditTool
    exportTool: ExportTool
    def __init__(self, sketchTool: _Optional[_Union[SketchTool, str]] = ..., editTool: _Optional[_Union[EditTool, str]] = ..., exportTool: _Optional[_Union[ExportTool, str]] = ...) -> None: ...

class UserRestrictionStates(_message.Message):
    __slots__ = ("activeLocks",)
    ACTIVELOCKS_FIELD_NUMBER: _ClassVar[int]
    activeLocks: _containers.RepeatedScalarFieldContainer[_sketch_interactions_pb2.UserRestrictionLockType]
    def __init__(self, activeLocks: _Optional[_Iterable[_Union[_sketch_interactions_pb2.UserRestrictionLockType, str]]] = ...) -> None: ...

class UserPencilModeStates(_message.Message):
    __slots__ = ("mainHandPencilMode", "offHandPencilMode")
    MAINHANDPENCILMODE_FIELD_NUMBER: _ClassVar[int]
    OFFHANDPENCILMODE_FIELD_NUMBER: _ClassVar[int]
    mainHandPencilMode: bool
    offHandPencilMode: bool
    def __init__(self, mainHandPencilMode: bool = ..., offHandPencilMode: bool = ...) -> None: ...

class UserDrawingStates(_message.Message):
    __slots__ = ("brushChosenAtScale",)
    BRUSHCHOSENATSCALE_FIELD_NUMBER: _ClassVar[int]
    brushChosenAtScale: float
    def __init__(self, brushChosenAtScale: _Optional[float] = ...) -> None: ...

class SelectionDrawingStates(_message.Message):
    __slots__ = ("isDrawingBox",)
    ISDRAWINGBOX_FIELD_NUMBER: _ClassVar[int]
    isDrawingBox: bool
    def __init__(self, isDrawingBox: bool = ...) -> None: ...

class UserUIInputType(_message.Message):
    __slots__ = ("inputType",)
    INPUTTYPE_FIELD_NUMBER: _ClassVar[int]
    inputType: str
    def __init__(self, inputType: _Optional[str] = ...) -> None: ...
