import gs_options_pb2 as _gs_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Texture2DTO(_message.Message):
    __slots__ = ("guid", "width", "height", "format", "mipmap", "originalFilename", "filesize", "isOpaque")
    GUID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    MIPMAP_FIELD_NUMBER: _ClassVar[int]
    ORIGINALFILENAME_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    ISOPAQUE_FIELD_NUMBER: _ClassVar[int]
    guid: str
    width: int
    height: int
    format: int
    mipmap: bool
    originalFilename: str
    filesize: int
    isOpaque: bool
    def __init__(self, guid: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., format: _Optional[int] = ..., mipmap: bool = ..., originalFilename: _Optional[str] = ..., filesize: _Optional[int] = ..., isOpaque: bool = ...) -> None: ...

class TransformTO(_message.Message):
    __slots__ = ("localPositionX", "localPositionY", "localPositionZ", "localRotationX", "localRotationY", "localRotationZ", "localRotationW", "localScaleX", "localScaleY", "localScaleZ")
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
    def __init__(self, localPositionX: _Optional[float] = ..., localPositionY: _Optional[float] = ..., localPositionZ: _Optional[float] = ..., localRotationX: _Optional[float] = ..., localRotationY: _Optional[float] = ..., localRotationZ: _Optional[float] = ..., localRotationW: _Optional[float] = ..., localScaleX: _Optional[float] = ..., localScaleY: _Optional[float] = ..., localScaleZ: _Optional[float] = ...) -> None: ...

class ThumbnailCameraTO(_message.Message):
    __slots__ = ("transform", "fieldOfView")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    FIELDOFVIEW_FIELD_NUMBER: _ClassVar[int]
    transform: TransformTO
    fieldOfView: float
    def __init__(self, transform: _Optional[_Union[TransformTO, _Mapping]] = ..., fieldOfView: _Optional[float] = ...) -> None: ...
