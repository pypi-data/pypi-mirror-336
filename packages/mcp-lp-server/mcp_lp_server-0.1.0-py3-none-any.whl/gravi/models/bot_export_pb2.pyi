from gravi.models import preferences_pb2 as _preferences_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BotExportPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BotExportUnknown: _ClassVar[BotExportPhase]
    BotExportQueueing: _ClassVar[BotExportPhase]
    BotExportDownloadFile: _ClassVar[BotExportPhase]
    BotExportExporting: _ClassVar[BotExportPhase]
    BotExportFinished: _ClassVar[BotExportPhase]
    BotExportFailed: _ClassVar[BotExportPhase]
    BotExportUploadFile: _ClassVar[BotExportPhase]

class BotExportResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BotExportUnknownResult: _ClassVar[BotExportResultCode]
    BotExportSuccess: _ClassVar[BotExportResultCode]
    BotExportFailedExport: _ClassVar[BotExportResultCode]
BotExportUnknown: BotExportPhase
BotExportQueueing: BotExportPhase
BotExportDownloadFile: BotExportPhase
BotExportExporting: BotExportPhase
BotExportFinished: BotExportPhase
BotExportFailed: BotExportPhase
BotExportUploadFile: BotExportPhase
BotExportUnknownResult: BotExportResultCode
BotExportSuccess: BotExportResultCode
BotExportFailedExport: BotExportResultCode

class BotExportConfig(_message.Message):
    __slots__ = ("ownerId", "exportRequestId", "filePath", "originalDocName", "exportPreferencesTO", "levelsOfDetail")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    EXPORTREQUESTID_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    ORIGINALDOCNAME_FIELD_NUMBER: _ClassVar[int]
    EXPORTPREFERENCESTO_FIELD_NUMBER: _ClassVar[int]
    LEVELSOFDETAIL_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    exportRequestId: str
    filePath: str
    originalDocName: str
    exportPreferencesTO: _preferences_pb2.ExportPreferencesTO
    levelsOfDetail: _containers.RepeatedScalarFieldContainer[_sketch_common_pb2.LevelOfDetail]
    def __init__(self, ownerId: _Optional[str] = ..., exportRequestId: _Optional[str] = ..., filePath: _Optional[str] = ..., originalDocName: _Optional[str] = ..., exportPreferencesTO: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ..., levelsOfDetail: _Optional[_Iterable[_Union[_sketch_common_pb2.LevelOfDetail, str]]] = ...) -> None: ...

class BotExportStatus(_message.Message):
    __slots__ = ("exporting", "exportConfig", "exportPhase", "latestExportResult")
    EXPORTING_FIELD_NUMBER: _ClassVar[int]
    EXPORTCONFIG_FIELD_NUMBER: _ClassVar[int]
    EXPORTPHASE_FIELD_NUMBER: _ClassVar[int]
    LATESTEXPORTRESULT_FIELD_NUMBER: _ClassVar[int]
    exporting: bool
    exportConfig: BotExportConfig
    exportPhase: BotExportPhase
    latestExportResult: BotExportResult
    def __init__(self, exporting: bool = ..., exportConfig: _Optional[_Union[BotExportConfig, _Mapping]] = ..., exportPhase: _Optional[_Union[BotExportPhase, str]] = ..., latestExportResult: _Optional[_Union[BotExportResult, _Mapping]] = ...) -> None: ...

class BotExportResult(_message.Message):
    __slots__ = ("ownerId", "exportRequestId", "result", "exportedFilePath")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    EXPORTREQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDFILEPATH_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    exportRequestId: str
    result: BotExportResultCode
    exportedFilePath: str
    def __init__(self, ownerId: _Optional[str] = ..., exportRequestId: _Optional[str] = ..., result: _Optional[_Union[BotExportResultCode, str]] = ..., exportedFilePath: _Optional[str] = ...) -> None: ...
