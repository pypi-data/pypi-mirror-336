import gs_options_pb2 as _gs_options_pb2
from gravi.rest.common import async_pb2 as _async_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageResolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ImageResolution1024x576: _ClassVar[ImageResolution]
    ImageResolution1280x720: _ClassVar[ImageResolution]
    ImageResolution2720x1520: _ClassVar[ImageResolution]

class GenerateImagesResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GenerateImageResponseSuccess: _ClassVar[GenerateImagesResponseCode]
    GenerateImagesResponseCodeFailure: _ClassVar[GenerateImagesResponseCode]

class Generate3DModelResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Generate3DModelResponseCodeSuccess: _ClassVar[Generate3DModelResponseCode]
    Generate3DModelResponseCodeFailure: _ClassVar[Generate3DModelResponseCode]

class ModelFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ModelFormatGLB: _ClassVar[ModelFormat]
    ModelFormatOBJ: _ClassVar[ModelFormat]
ImageResolution1024x576: ImageResolution
ImageResolution1280x720: ImageResolution
ImageResolution2720x1520: ImageResolution
GenerateImageResponseSuccess: GenerateImagesResponseCode
GenerateImagesResponseCodeFailure: GenerateImagesResponseCode
Generate3DModelResponseCodeSuccess: Generate3DModelResponseCode
Generate3DModelResponseCodeFailure: Generate3DModelResponseCode
ModelFormatGLB: ModelFormat
ModelFormatOBJ: ModelFormat

class GenerateImagesRequest(_message.Message):
    __slots__ = ("prompt", "controlImage", "controlStrength", "targetResolution")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    CONTROLIMAGE_FIELD_NUMBER: _ClassVar[int]
    CONTROLSTRENGTH_FIELD_NUMBER: _ClassVar[int]
    TARGETRESOLUTION_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    controlImage: bytes
    controlStrength: float
    targetResolution: ImageResolution
    def __init__(self, prompt: _Optional[str] = ..., controlImage: _Optional[bytes] = ..., controlStrength: _Optional[float] = ..., targetResolution: _Optional[_Union[ImageResolution, str]] = ...) -> None: ...

class GenerateImagesResponse(_message.Message):
    __slots__ = ("code", "images")
    CODE_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    code: GenerateImagesResponseCode
    images: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, code: _Optional[_Union[GenerateImagesResponseCode, str]] = ..., images: _Optional[_Iterable[bytes]] = ...) -> None: ...

class Generate3DModelRequest(_message.Message):
    __slots__ = ("pendingAsyncJob", "req")
    PENDINGASYNCJOB_FIELD_NUMBER: _ClassVar[int]
    REQ_FIELD_NUMBER: _ClassVar[int]
    pendingAsyncJob: _async_pb2.AsyncJob
    req: Generate3DModelRequestPayload
    def __init__(self, pendingAsyncJob: _Optional[_Union[_async_pb2.AsyncJob, _Mapping]] = ..., req: _Optional[_Union[Generate3DModelRequestPayload, _Mapping]] = ...) -> None: ...

class Generate3DModelRequestPayload(_message.Message):
    __slots__ = ("images",)
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, images: _Optional[_Iterable[bytes]] = ...) -> None: ...

class Generate3DModelResponse(_message.Message):
    __slots__ = ("pendingAsyncJob", "resp")
    PENDINGASYNCJOB_FIELD_NUMBER: _ClassVar[int]
    RESP_FIELD_NUMBER: _ClassVar[int]
    pendingAsyncJob: _async_pb2.AsyncJob
    resp: Generate3DModelResponsePayload
    def __init__(self, pendingAsyncJob: _Optional[_Union[_async_pb2.AsyncJob, _Mapping]] = ..., resp: _Optional[_Union[Generate3DModelResponsePayload, _Mapping]] = ...) -> None: ...

class Generate3DModelResponsePayload(_message.Message):
    __slots__ = ("code", "modelUrl", "format")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MODELURL_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    code: Generate3DModelResponseCode
    modelUrl: str
    format: ModelFormat
    def __init__(self, code: _Optional[_Union[Generate3DModelResponseCode, str]] = ..., modelUrl: _Optional[str] = ..., format: _Optional[_Union[ModelFormat, str]] = ...) -> None: ...
