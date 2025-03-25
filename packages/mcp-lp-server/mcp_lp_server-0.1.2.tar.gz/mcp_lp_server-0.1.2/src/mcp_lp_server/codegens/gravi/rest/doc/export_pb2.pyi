from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rest.doc import doc_rest_pb2 as _doc_rest_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExportStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ExportStatusQueued: _ClassVar[ExportStatus]
    ExportStatusInProgress: _ClassVar[ExportStatus]
    ExportStatusCompleted: _ClassVar[ExportStatus]
    ExportStatusFailed: _ClassVar[ExportStatus]
    ExportStatusFailedByExportTakingTooLong: _ClassVar[ExportStatus]

class ExportProcessMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ExportProcessModeCloud: _ClassVar[ExportProcessMode]
    ExportProcessModeOnDevice: _ClassVar[ExportProcessMode]

class CreateDocExportEntryResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateExportDocEntryResponseCodeSuccess: _ClassVar[CreateDocExportEntryResponseCode]
    CreateExportDocEntryResponseCodeExportDocNotFound: _ClassVar[CreateDocExportEntryResponseCode]

class ExportDocSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ExportDocSourceUnset: _ClassVar[ExportDocSource]
    ExportDocSourceCloudSketch: _ClassVar[ExportDocSource]
    ExportDocSourceNewUpload: _ClassVar[ExportDocSource]

class PostExportActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PostExportActionTypeUnset: _ClassVar[PostExportActionType]
    PostExportActionTypeSaveAsDoc: _ClassVar[PostExportActionType]
    PostExportActionTypeSaveAsDocThumbnail: _ClassVar[PostExportActionType]
    PostExportActionTypeSaveAsPreProcessedGrs: _ClassVar[PostExportActionType]
    PostExportActionTypeSaveAs360Thumbnail: _ClassVar[PostExportActionType]

class ExportDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ExportDocResponseCodeSuccess: _ClassVar[ExportDocResponseCode]
    ExportDocResponseCodeUnsupportedFileFormat: _ClassVar[ExportDocResponseCode]
    ExportDocResponseCodeDocNotFoundOrHaveChanged: _ClassVar[ExportDocResponseCode]

class GetDocExportResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetDocExportResponseCodeSuccess: _ClassVar[GetDocExportResponseCode]
    GetDocExportResponseCodeDocExportExpiredOrNotFound: _ClassVar[GetDocExportResponseCode]

class DownloadDocExportResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DownloadDocExportResponseCodeSuccess: _ClassVar[DownloadDocExportResponseCode]
    DownloadDocExportResponseCodeExportNotFoundOrExpired: _ClassVar[DownloadDocExportResponseCode]
ExportStatusQueued: ExportStatus
ExportStatusInProgress: ExportStatus
ExportStatusCompleted: ExportStatus
ExportStatusFailed: ExportStatus
ExportStatusFailedByExportTakingTooLong: ExportStatus
ExportProcessModeCloud: ExportProcessMode
ExportProcessModeOnDevice: ExportProcessMode
CreateExportDocEntryResponseCodeSuccess: CreateDocExportEntryResponseCode
CreateExportDocEntryResponseCodeExportDocNotFound: CreateDocExportEntryResponseCode
ExportDocSourceUnset: ExportDocSource
ExportDocSourceCloudSketch: ExportDocSource
ExportDocSourceNewUpload: ExportDocSource
PostExportActionTypeUnset: PostExportActionType
PostExportActionTypeSaveAsDoc: PostExportActionType
PostExportActionTypeSaveAsDocThumbnail: PostExportActionType
PostExportActionTypeSaveAsPreProcessedGrs: PostExportActionType
PostExportActionTypeSaveAs360Thumbnail: PostExportActionType
ExportDocResponseCodeSuccess: ExportDocResponseCode
ExportDocResponseCodeUnsupportedFileFormat: ExportDocResponseCode
ExportDocResponseCodeDocNotFoundOrHaveChanged: ExportDocResponseCode
GetDocExportResponseCodeSuccess: GetDocExportResponseCode
GetDocExportResponseCodeDocExportExpiredOrNotFound: GetDocExportResponseCode
DownloadDocExportResponseCodeSuccess: DownloadDocExportResponseCode
DownloadDocExportResponseCodeExportNotFoundOrExpired: DownloadDocExportResponseCode

class DocExport(_message.Message):
    __slots__ = ("ownerId", "uid", "expiry", "status", "createdOn", "preference", "updatedOn", "exportFileFullPath", "saveToMyFilesOnCompletion", "exportedFileDocId", "processMode", "exportId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    UPDATEDON_FIELD_NUMBER: _ClassVar[int]
    EXPORTFILEFULLPATH_FIELD_NUMBER: _ClassVar[int]
    SAVETOMYFILESONCOMPLETION_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDFILEDOCID_FIELD_NUMBER: _ClassVar[int]
    PROCESSMODE_FIELD_NUMBER: _ClassVar[int]
    EXPORTID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    uid: str
    expiry: int
    status: ExportStatus
    createdOn: int
    preference: _preferences_pb2.ExportPreferencesTO
    updatedOn: int
    exportFileFullPath: str
    saveToMyFilesOnCompletion: bool
    exportedFileDocId: str
    processMode: ExportProcessMode
    exportId: str
    def __init__(self, ownerId: _Optional[str] = ..., uid: _Optional[str] = ..., expiry: _Optional[int] = ..., status: _Optional[_Union[ExportStatus, str]] = ..., createdOn: _Optional[int] = ..., preference: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ..., updatedOn: _Optional[int] = ..., exportFileFullPath: _Optional[str] = ..., saveToMyFilesOnCompletion: bool = ..., exportedFileDocId: _Optional[str] = ..., processMode: _Optional[_Union[ExportProcessMode, str]] = ..., exportId: _Optional[str] = ...) -> None: ...

class CreateDocExportEntryRequest(_message.Message):
    __slots__ = ("exportedFileDocId", "exportStartedOn", "exportFinishedOn", "processMode", "preference")
    EXPORTEDFILEDOCID_FIELD_NUMBER: _ClassVar[int]
    EXPORTSTARTEDON_FIELD_NUMBER: _ClassVar[int]
    EXPORTFINISHEDON_FIELD_NUMBER: _ClassVar[int]
    PROCESSMODE_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    exportedFileDocId: str
    exportStartedOn: int
    exportFinishedOn: int
    processMode: ExportProcessMode
    preference: _preferences_pb2.ExportPreferencesTO
    def __init__(self, exportedFileDocId: _Optional[str] = ..., exportStartedOn: _Optional[int] = ..., exportFinishedOn: _Optional[int] = ..., processMode: _Optional[_Union[ExportProcessMode, str]] = ..., preference: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ...) -> None: ...

class CreateDocExportEntryResponse(_message.Message):
    __slots__ = ("code", "export")
    CODE_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    code: CreateDocExportEntryResponseCode
    export: DocExport
    def __init__(self, code: _Optional[_Union[CreateDocExportEntryResponseCode, str]] = ..., export: _Optional[_Union[DocExport, _Mapping]] = ...) -> None: ...

class PostExportActionSaveAsDoc(_message.Message):
    __slots__ = ("docTypeToSaveAs", "destinationFolderDocId", "destinationSpaceId")
    DOCTYPETOSAVEAS_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONFOLDERDOCID_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONSPACEID_FIELD_NUMBER: _ClassVar[int]
    docTypeToSaveAs: _gravi_model_pb2.DocumentType
    destinationFolderDocId: str
    destinationSpaceId: _gravi_model_pb2.SpaceId
    def __init__(self, docTypeToSaveAs: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., destinationFolderDocId: _Optional[str] = ..., destinationSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class PostExportActionSaveAsDocThumbnail(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class PostExportActionSaveAsPreProcessedGrs(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class PostExportActionSaveAs360Thumbnail(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class PostExportAction(_message.Message):
    __slots__ = ("actionType", "saveAsDoc", "saveAsDocThumbnail", "saveAsPreProcessedGrs", "saveas360Thumbnail")
    ACTIONTYPE_FIELD_NUMBER: _ClassVar[int]
    SAVEASDOC_FIELD_NUMBER: _ClassVar[int]
    SAVEASDOCTHUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    SAVEASPREPROCESSEDGRS_FIELD_NUMBER: _ClassVar[int]
    SAVEAS360THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    actionType: PostExportActionType
    saveAsDoc: PostExportActionSaveAsDoc
    saveAsDocThumbnail: PostExportActionSaveAsDocThumbnail
    saveAsPreProcessedGrs: PostExportActionSaveAsPreProcessedGrs
    saveas360Thumbnail: PostExportActionSaveAs360Thumbnail
    def __init__(self, actionType: _Optional[_Union[PostExportActionType, str]] = ..., saveAsDoc: _Optional[_Union[PostExportActionSaveAsDoc, _Mapping]] = ..., saveAsDocThumbnail: _Optional[_Union[PostExportActionSaveAsDocThumbnail, _Mapping]] = ..., saveAsPreProcessedGrs: _Optional[_Union[PostExportActionSaveAsPreProcessedGrs, _Mapping]] = ..., saveas360Thumbnail: _Optional[_Union[PostExportActionSaveAs360Thumbnail, _Mapping]] = ...) -> None: ...

class ExportDocRequest(_message.Message):
    __slots__ = ("docOwnerId", "docId", "docContentHash", "preference", "exportedFileName", "docSource", "uploadId", "contentId", "docSpaceId", "saveToMyFilesOnCompletion", "docTypeToSaveAs", "exportDestinationFolderDocId", "exportDestinationSpaceId", "postExportAction", "sourceOrgId")
    DOCOWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    DOCCONTENTHASH_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDFILENAME_FIELD_NUMBER: _ClassVar[int]
    DOCSOURCE_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    CONTENTID_FIELD_NUMBER: _ClassVar[int]
    DOCSPACEID_FIELD_NUMBER: _ClassVar[int]
    SAVETOMYFILESONCOMPLETION_FIELD_NUMBER: _ClassVar[int]
    DOCTYPETOSAVEAS_FIELD_NUMBER: _ClassVar[int]
    EXPORTDESTINATIONFOLDERDOCID_FIELD_NUMBER: _ClassVar[int]
    EXPORTDESTINATIONSPACEID_FIELD_NUMBER: _ClassVar[int]
    POSTEXPORTACTION_FIELD_NUMBER: _ClassVar[int]
    SOURCEORGID_FIELD_NUMBER: _ClassVar[int]
    docOwnerId: str
    docId: str
    docContentHash: str
    preference: _preferences_pb2.ExportPreferencesTO
    exportedFileName: str
    docSource: ExportDocSource
    uploadId: str
    contentId: str
    docSpaceId: _gravi_model_pb2.SpaceId
    saveToMyFilesOnCompletion: bool
    docTypeToSaveAs: _gravi_model_pb2.DocumentType
    exportDestinationFolderDocId: str
    exportDestinationSpaceId: _gravi_model_pb2.SpaceId
    postExportAction: PostExportAction
    sourceOrgId: str
    def __init__(self, docOwnerId: _Optional[str] = ..., docId: _Optional[str] = ..., docContentHash: _Optional[str] = ..., preference: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ..., exportedFileName: _Optional[str] = ..., docSource: _Optional[_Union[ExportDocSource, str]] = ..., uploadId: _Optional[str] = ..., contentId: _Optional[str] = ..., docSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., saveToMyFilesOnCompletion: bool = ..., docTypeToSaveAs: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., exportDestinationFolderDocId: _Optional[str] = ..., exportDestinationSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., postExportAction: _Optional[_Union[PostExportAction, _Mapping]] = ..., sourceOrgId: _Optional[str] = ...) -> None: ...

class ExportDocResponse(_message.Message):
    __slots__ = ("code", "export")
    CODE_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    code: ExportDocResponseCode
    export: DocExport
    def __init__(self, code: _Optional[_Union[ExportDocResponseCode, str]] = ..., export: _Optional[_Union[DocExport, _Mapping]] = ...) -> None: ...

class GetDocExportRequest(_message.Message):
    __slots__ = ("ownerId", "exportId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    EXPORTID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    exportId: str
    def __init__(self, ownerId: _Optional[str] = ..., exportId: _Optional[str] = ...) -> None: ...

class GetDocExportResponse(_message.Message):
    __slots__ = ("export", "code")
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    export: DocExport
    code: GetDocExportResponseCode
    def __init__(self, export: _Optional[_Union[DocExport, _Mapping]] = ..., code: _Optional[_Union[GetDocExportResponseCode, str]] = ...) -> None: ...

class ListDocExportsRequest(_message.Message):
    __slots__ = ("ownerId",)
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    def __init__(self, ownerId: _Optional[str] = ...) -> None: ...

class ListDocExportsResponse(_message.Message):
    __slots__ = ("exports",)
    EXPORTS_FIELD_NUMBER: _ClassVar[int]
    exports: _containers.RepeatedCompositeFieldContainer[DocExport]
    def __init__(self, exports: _Optional[_Iterable[_Union[DocExport, _Mapping]]] = ...) -> None: ...

class UploadDocExportRequest(_message.Message):
    __slots__ = ("uploadParts",)
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    uploadParts: _containers.RepeatedCompositeFieldContainer[_doc_rest_pb2.UploadPart]
    def __init__(self, uploadParts: _Optional[_Iterable[_Union[_doc_rest_pb2.UploadPart, _Mapping]]] = ...) -> None: ...

class UploadDocExportResponse(_message.Message):
    __slots__ = ("partUploadUrls", "uploadId", "contentId")
    PARTUPLOADURLS_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    CONTENTID_FIELD_NUMBER: _ClassVar[int]
    partUploadUrls: _containers.RepeatedScalarFieldContainer[str]
    uploadId: str
    contentId: str
    def __init__(self, partUploadUrls: _Optional[_Iterable[str]] = ..., uploadId: _Optional[str] = ..., contentId: _Optional[str] = ...) -> None: ...

class DownloadDocExportRequest(_message.Message):
    __slots__ = ("ownerId", "exportId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    EXPORTID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    exportId: str
    def __init__(self, ownerId: _Optional[str] = ..., exportId: _Optional[str] = ...) -> None: ...

class DownloadDocExportResponse(_message.Message):
    __slots__ = ("downloadUrl", "code")
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    downloadUrl: str
    code: DownloadDocExportResponseCode
    def __init__(self, downloadUrl: _Optional[str] = ..., code: _Optional[_Union[DownloadDocExportResponseCode, str]] = ...) -> None: ...
