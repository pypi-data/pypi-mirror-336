import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DecimateResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DecimateResultUnknown: _ClassVar[DecimateResult]
    DecimateResultSuccess: _ClassVar[DecimateResult]
    DecimateResultFailed: _ClassVar[DecimateResult]
    DecimateResultNoResource: _ClassVar[DecimateResult]
    DecimateResultProcessing: _ClassVar[DecimateResult]
DecimateResultUnknown: DecimateResult
DecimateResultSuccess: DecimateResult
DecimateResultFailed: DecimateResult
DecimateResultNoResource: DecimateResult
DecimateResultProcessing: DecimateResult

class RhinoRequest(_message.Message):
    __slots__ = ("processId", "decimateRequest")
    PROCESSID_FIELD_NUMBER: _ClassVar[int]
    DECIMATEREQUEST_FIELD_NUMBER: _ClassVar[int]
    processId: str
    decimateRequest: DecimateRequest
    def __init__(self, processId: _Optional[str] = ..., decimateRequest: _Optional[_Union[DecimateRequest, _Mapping]] = ...) -> None: ...

class RhinoResponse(_message.Message):
    __slots__ = ("processId", "decimateResponse")
    PROCESSID_FIELD_NUMBER: _ClassVar[int]
    DECIMATERESPONSE_FIELD_NUMBER: _ClassVar[int]
    processId: str
    decimateResponse: DecimateResponse
    def __init__(self, processId: _Optional[str] = ..., decimateResponse: _Optional[_Union[DecimateResponse, _Mapping]] = ...) -> None: ...

class DecimateRequest(_message.Message):
    __slots__ = ("sourceFilePath", "postfix", "targetFaceCount", "exportPath")
    SOURCEFILEPATH_FIELD_NUMBER: _ClassVar[int]
    POSTFIX_FIELD_NUMBER: _ClassVar[int]
    TARGETFACECOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPORTPATH_FIELD_NUMBER: _ClassVar[int]
    sourceFilePath: str
    postfix: str
    targetFaceCount: int
    exportPath: str
    def __init__(self, sourceFilePath: _Optional[str] = ..., postfix: _Optional[str] = ..., targetFaceCount: _Optional[int] = ..., exportPath: _Optional[str] = ...) -> None: ...

class DecimateResponse(_message.Message):
    __slots__ = ("result", "exportPath")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EXPORTPATH_FIELD_NUMBER: _ClassVar[int]
    result: DecimateResult
    exportPath: str
    def __init__(self, result: _Optional[_Union[DecimateResult, str]] = ..., exportPath: _Optional[str] = ...) -> None: ...
