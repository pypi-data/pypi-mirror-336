from gravi.models import gravi_model_pb2 as _gravi_model_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConvertDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ConvertDocResponseCodeSuccess: _ClassVar[ConvertDocResponseCode]
    ConvertDocResponseCodeInvalidSourceDoc: _ClassVar[ConvertDocResponseCode]
    ConvertDocResponseCodeInvalidTargetDocType: _ClassVar[ConvertDocResponseCode]

class SearchPublicContentDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SearchPublicContentDocResponseCode_Invalid: _ClassVar[SearchPublicContentDocResponseCode]
    SearchPublicContentDocResponseCode_Success: _ClassVar[SearchPublicContentDocResponseCode]
    SearchPublicContentDocResponseCode_DocNotFound: _ClassVar[SearchPublicContentDocResponseCode]

class InitiateFileUploadResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InitiateFileUploadResponseCode_Success: _ClassVar[InitiateFileUploadResponseCode]
    InitiateFileUploadResponseCode_StorageAllowanceExceeded: _ClassVar[InitiateFileUploadResponseCode]
    InitiateFileUploadResponseCode_MissingUploadId: _ClassVar[InitiateFileUploadResponseCode]

class DownloadDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DownloadDocResponseCode_Success: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_DocNotFound: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_DocContentNotFound: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_DocBeingZipped: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_UnsupportedDocType: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_ZippingNotSupportedWhileCollabIsLive: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_RevisionHashNotFound: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_RevisionHashNotProvidedForOnlineSketch: _ClassVar[DownloadDocResponseCode]
    DownloadDocResponseCode_PreProcessedImportGenerating: _ClassVar[DownloadDocResponseCode]

class CreateDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateDocResponse_Success: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_InsufficientStorage: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_ContentNotUploaded: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_DocumentAlreadyExists: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_ParentFolderNotFound: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_MaxPersonalCollabRoomExceeded: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_DocBeingUnzipped: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_UnzipJobAlreadyExpired: _ClassVar[CreateDocResponseCode]
    CreateDocResponseCode_DocOwnershipNotAllowed: _ClassVar[CreateDocResponseCode]

class UpdateDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateDocResponseCode_Success: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_DocNotFound: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_OutdatedOldContentHash: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_ContentNotUploaded: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_InsufficientStorage: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_DocBeingUnzipped: _ClassVar[UpdateDocResponseCode]
    UpdateDocResponseCode_UnzipJobAlreadyExpired: _ClassVar[UpdateDocResponseCode]

class DocSortingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Any: _ClassVar[DocSortingType]
    ByLastModifyAsc: _ClassVar[DocSortingType]
    ByCreateTimeAsc: _ClassVar[DocSortingType]
    ByDocNameAsc: _ClassVar[DocSortingType]
    ByFileSizeAsc: _ClassVar[DocSortingType]
    ByDocTypeAsc: _ClassVar[DocSortingType]
    ByLastModifyDesc: _ClassVar[DocSortingType]
    ByCreateTimeDesc: _ClassVar[DocSortingType]
    ByDocNameDesc: _ClassVar[DocSortingType]
    ByFileSizeDesc: _ClassVar[DocSortingType]
    ByDocTypeDesc: _ClassVar[DocSortingType]
    ByTrashedOnDesc: _ClassVar[DocSortingType]
    ByTrashedOnAsc: _ClassVar[DocSortingType]

class ListDocsResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ListDocsResponseCodeUnknown: _ClassVar[ListDocsResponseCode]
    ListDocsResponseCodeSuccess: _ClassVar[ListDocsResponseCode]
    ListDocsResponseCodeNoPermissionToSpaceId: _ClassVar[ListDocsResponseCode]

class DeprecatedGetDocumentsError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetDocumentsError_Unknown: _ClassVar[DeprecatedGetDocumentsError]
    GetDocumentsError_MissingUserLevelPerms: _ClassVar[DeprecatedGetDocumentsError]
    GetDocumentsError_MissingOrgLevelPerms: _ClassVar[DeprecatedGetDocumentsError]
    GetDocumentsError_MissingTeamLevelPerms: _ClassVar[DeprecatedGetDocumentsError]

class GetDocumentError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetDocumentError_Unknown: _ClassVar[GetDocumentError]
    GetDocumentError_NoError: _ClassVar[GetDocumentError]
    GetDocumentError_NoAccessPerm: _ClassVar[GetDocumentError]
    GetDocumentError_NotFound: _ClassVar[GetDocumentError]
    GetDocumentError_NoAccessCannotRequest: _ClassVar[GetDocumentError]

class GetDocumentSpaceNameResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetDocumentSpaceNameResponseCodeUnknown: _ClassVar[GetDocumentSpaceNameResponseCode]
    GetDocumentSpaceNameResponseCodeSuccess: _ClassVar[GetDocumentSpaceNameResponseCode]
    GetDocumentSpaceNameResponseCodeDocNotFound: _ClassVar[GetDocumentSpaceNameResponseCode]
    GetDocumentSpaceNameResponseCodePermissionDenied: _ClassVar[GetDocumentSpaceNameResponseCode]

class SendDocumentResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SendDocumentUnknown: _ClassVar[SendDocumentResult]
    SendDocumentSuccess: _ClassVar[SendDocumentResult]
    SendDocumentFailedSendToSelf: _ClassVar[SendDocumentResult]
    SendDocumentFailedDocNotExist: _ClassVar[SendDocumentResult]

class CreateFolderResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateFolderResponseCodeSuccess: _ClassVar[CreateFolderResponseCode]
    CreateFolderResponseCodeFolderWithSamePathAlreadyExists: _ClassVar[CreateFolderResponseCode]

class TrashDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TrashDocResponseCodeSuccess: _ClassVar[TrashDocResponseCode]
    TrashDocResponseCodeLiveCollabRoom: _ClassVar[TrashDocResponseCode]

class RestoreDocResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RestoreDocResponseCodeSuccess: _ClassVar[RestoreDocResponseCode]
    RestoreDocResponseCodeDocNotFound: _ClassVar[RestoreDocResponseCode]
    RestoreDocResponseCodeParentFolderNotFound: _ClassVar[RestoreDocResponseCode]
    RestoreDocResponseCodeDocAlreadyExists: _ClassVar[RestoreDocResponseCode]
    RestoreDocResponseCodeMaxRoomsReachedCantRestore: _ClassVar[RestoreDocResponseCode]

class DeleteDocsInBinResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeleteDocsInBinResponseCodeUnknown: _ClassVar[DeleteDocsInBinResponseCode]
    DeleteDocsInBinResponseCodeSuccess: _ClassVar[DeleteDocsInBinResponseCode]
    DeleteDocsInBinResponseCodeNoPermissionToSpace: _ClassVar[DeleteDocsInBinResponseCode]

class MoveDocResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MoveDocUnknown: _ClassVar[MoveDocResult]
    MoveDocSuccess: _ClassVar[MoveDocResult]
    MoveDocOutOfDate: _ClassVar[MoveDocResult]
    MoveDocMissing: _ClassVar[MoveDocResult]
    MoveDocToDocExists: _ClassVar[MoveDocResult]
    MoveDocNoPermission: _ClassVar[MoveDocResult]
    MoveDocServerError: _ClassVar[MoveDocResult]
    MoveDocIsFolderError: _ClassVar[MoveDocResult]
    MoveDocWrongFileTypeError: _ClassVar[MoveDocResult]
    MoveDocDestinationParentFolderNotFound: _ClassVar[MoveDocResult]
    MoveDocInsufficientStorage: _ClassVar[MoveDocResult]

class FileContentSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FileContentSourceUnset: _ClassVar[FileContentSource]
    FileContentSourceCloudDoc: _ClassVar[FileContentSource]
    FileContentSourceNewUpload: _ClassVar[FileContentSource]

class CreateDocAssetResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateDocAssetResponseCodeSuccess: _ClassVar[CreateDocAssetResponseCode]
    CreateDocAssetResponseCodeInsufficientStorage: _ClassVar[CreateDocAssetResponseCode]
    CreateDocAssetResponseCodeContentNotUploaded: _ClassVar[CreateDocAssetResponseCode]
    CreateDocAssetResponseCodeAssetAlreadyExists: _ClassVar[CreateDocAssetResponseCode]
    CreateDocAssetResponseCodeSketchNotFound: _ClassVar[CreateDocAssetResponseCode]
    CreateDocAssetResponseCodeContentDocNotFound: _ClassVar[CreateDocAssetResponseCode]

class DownloadDocAssetsResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DownloadDocAssetsResponseCodeSuccess: _ClassVar[DownloadDocAssetsResponseCode]
    DownloadDocAssetsResponseCodeInvalidAssetNames: _ClassVar[DownloadDocAssetsResponseCode]
    DownloadDocAssetsResponseCodeDocNotFound: _ClassVar[DownloadDocAssetsResponseCode]
    DownloadDocAssetsResponseCodeDocAssetsNotFound: _ClassVar[DownloadDocAssetsResponseCode]

class ThumbnailType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ThumbnailTypePng: _ClassVar[ThumbnailType]

class UploadDocThumbnailResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UploadDocThumbnailResponseCodeSuccess: _ClassVar[UploadDocThumbnailResponseCode]
    UploadDocThumbnailResponseCodeDocNotFound: _ClassVar[UploadDocThumbnailResponseCode]
    UploadDocThumbnailResponseCodeContentNotUploaded: _ClassVar[UploadDocThumbnailResponseCode]

class CreateEnterRoomNotificationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateEnterRoomNotificationUnknown: _ClassVar[CreateEnterRoomNotificationResult]
    CreateEnterRoomNotificationSuccess: _ClassVar[CreateEnterRoomNotificationResult]
    CreateEnterRoomNotificationRoomNotFound: _ClassVar[CreateEnterRoomNotificationResult]
    CreateEnterRoomNotificationNoPermission: _ClassVar[CreateEnterRoomNotificationResult]

class CopyDocResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CopyDocResult_Unknown: _ClassVar[CopyDocResult]
    CopyDocResult_Success: _ClassVar[CopyDocResult]
    CopyDocResult_Error_DocInUse: _ClassVar[CopyDocResult]
    CopyDocResult_Error_FullStorage: _ClassVar[CopyDocResult]
    CopyDocResult_Error_MissingPermissions: _ClassVar[CopyDocResult]
    CopyDocResult_Error_MissingDoc: _ClassVar[CopyDocResult]
ConvertDocResponseCodeSuccess: ConvertDocResponseCode
ConvertDocResponseCodeInvalidSourceDoc: ConvertDocResponseCode
ConvertDocResponseCodeInvalidTargetDocType: ConvertDocResponseCode
SearchPublicContentDocResponseCode_Invalid: SearchPublicContentDocResponseCode
SearchPublicContentDocResponseCode_Success: SearchPublicContentDocResponseCode
SearchPublicContentDocResponseCode_DocNotFound: SearchPublicContentDocResponseCode
InitiateFileUploadResponseCode_Success: InitiateFileUploadResponseCode
InitiateFileUploadResponseCode_StorageAllowanceExceeded: InitiateFileUploadResponseCode
InitiateFileUploadResponseCode_MissingUploadId: InitiateFileUploadResponseCode
DownloadDocResponseCode_Success: DownloadDocResponseCode
DownloadDocResponseCode_DocNotFound: DownloadDocResponseCode
DownloadDocResponseCode_DocContentNotFound: DownloadDocResponseCode
DownloadDocResponseCode_DocBeingZipped: DownloadDocResponseCode
DownloadDocResponseCode_UnsupportedDocType: DownloadDocResponseCode
DownloadDocResponseCode_ZippingNotSupportedWhileCollabIsLive: DownloadDocResponseCode
DownloadDocResponseCode_RevisionHashNotFound: DownloadDocResponseCode
DownloadDocResponseCode_RevisionHashNotProvidedForOnlineSketch: DownloadDocResponseCode
DownloadDocResponseCode_PreProcessedImportGenerating: DownloadDocResponseCode
CreateDocResponse_Success: CreateDocResponseCode
CreateDocResponseCode_InsufficientStorage: CreateDocResponseCode
CreateDocResponseCode_ContentNotUploaded: CreateDocResponseCode
CreateDocResponseCode_DocumentAlreadyExists: CreateDocResponseCode
CreateDocResponseCode_ParentFolderNotFound: CreateDocResponseCode
CreateDocResponseCode_MaxPersonalCollabRoomExceeded: CreateDocResponseCode
CreateDocResponseCode_DocBeingUnzipped: CreateDocResponseCode
CreateDocResponseCode_UnzipJobAlreadyExpired: CreateDocResponseCode
CreateDocResponseCode_DocOwnershipNotAllowed: CreateDocResponseCode
UpdateDocResponseCode_Success: UpdateDocResponseCode
UpdateDocResponseCode_DocNotFound: UpdateDocResponseCode
UpdateDocResponseCode_OutdatedOldContentHash: UpdateDocResponseCode
UpdateDocResponseCode_ContentNotUploaded: UpdateDocResponseCode
UpdateDocResponseCode_InsufficientStorage: UpdateDocResponseCode
UpdateDocResponseCode_DocBeingUnzipped: UpdateDocResponseCode
UpdateDocResponseCode_UnzipJobAlreadyExpired: UpdateDocResponseCode
Any: DocSortingType
ByLastModifyAsc: DocSortingType
ByCreateTimeAsc: DocSortingType
ByDocNameAsc: DocSortingType
ByFileSizeAsc: DocSortingType
ByDocTypeAsc: DocSortingType
ByLastModifyDesc: DocSortingType
ByCreateTimeDesc: DocSortingType
ByDocNameDesc: DocSortingType
ByFileSizeDesc: DocSortingType
ByDocTypeDesc: DocSortingType
ByTrashedOnDesc: DocSortingType
ByTrashedOnAsc: DocSortingType
ListDocsResponseCodeUnknown: ListDocsResponseCode
ListDocsResponseCodeSuccess: ListDocsResponseCode
ListDocsResponseCodeNoPermissionToSpaceId: ListDocsResponseCode
GetDocumentsError_Unknown: DeprecatedGetDocumentsError
GetDocumentsError_MissingUserLevelPerms: DeprecatedGetDocumentsError
GetDocumentsError_MissingOrgLevelPerms: DeprecatedGetDocumentsError
GetDocumentsError_MissingTeamLevelPerms: DeprecatedGetDocumentsError
GetDocumentError_Unknown: GetDocumentError
GetDocumentError_NoError: GetDocumentError
GetDocumentError_NoAccessPerm: GetDocumentError
GetDocumentError_NotFound: GetDocumentError
GetDocumentError_NoAccessCannotRequest: GetDocumentError
GetDocumentSpaceNameResponseCodeUnknown: GetDocumentSpaceNameResponseCode
GetDocumentSpaceNameResponseCodeSuccess: GetDocumentSpaceNameResponseCode
GetDocumentSpaceNameResponseCodeDocNotFound: GetDocumentSpaceNameResponseCode
GetDocumentSpaceNameResponseCodePermissionDenied: GetDocumentSpaceNameResponseCode
SendDocumentUnknown: SendDocumentResult
SendDocumentSuccess: SendDocumentResult
SendDocumentFailedSendToSelf: SendDocumentResult
SendDocumentFailedDocNotExist: SendDocumentResult
CreateFolderResponseCodeSuccess: CreateFolderResponseCode
CreateFolderResponseCodeFolderWithSamePathAlreadyExists: CreateFolderResponseCode
TrashDocResponseCodeSuccess: TrashDocResponseCode
TrashDocResponseCodeLiveCollabRoom: TrashDocResponseCode
RestoreDocResponseCodeSuccess: RestoreDocResponseCode
RestoreDocResponseCodeDocNotFound: RestoreDocResponseCode
RestoreDocResponseCodeParentFolderNotFound: RestoreDocResponseCode
RestoreDocResponseCodeDocAlreadyExists: RestoreDocResponseCode
RestoreDocResponseCodeMaxRoomsReachedCantRestore: RestoreDocResponseCode
DeleteDocsInBinResponseCodeUnknown: DeleteDocsInBinResponseCode
DeleteDocsInBinResponseCodeSuccess: DeleteDocsInBinResponseCode
DeleteDocsInBinResponseCodeNoPermissionToSpace: DeleteDocsInBinResponseCode
MoveDocUnknown: MoveDocResult
MoveDocSuccess: MoveDocResult
MoveDocOutOfDate: MoveDocResult
MoveDocMissing: MoveDocResult
MoveDocToDocExists: MoveDocResult
MoveDocNoPermission: MoveDocResult
MoveDocServerError: MoveDocResult
MoveDocIsFolderError: MoveDocResult
MoveDocWrongFileTypeError: MoveDocResult
MoveDocDestinationParentFolderNotFound: MoveDocResult
MoveDocInsufficientStorage: MoveDocResult
FileContentSourceUnset: FileContentSource
FileContentSourceCloudDoc: FileContentSource
FileContentSourceNewUpload: FileContentSource
CreateDocAssetResponseCodeSuccess: CreateDocAssetResponseCode
CreateDocAssetResponseCodeInsufficientStorage: CreateDocAssetResponseCode
CreateDocAssetResponseCodeContentNotUploaded: CreateDocAssetResponseCode
CreateDocAssetResponseCodeAssetAlreadyExists: CreateDocAssetResponseCode
CreateDocAssetResponseCodeSketchNotFound: CreateDocAssetResponseCode
CreateDocAssetResponseCodeContentDocNotFound: CreateDocAssetResponseCode
DownloadDocAssetsResponseCodeSuccess: DownloadDocAssetsResponseCode
DownloadDocAssetsResponseCodeInvalidAssetNames: DownloadDocAssetsResponseCode
DownloadDocAssetsResponseCodeDocNotFound: DownloadDocAssetsResponseCode
DownloadDocAssetsResponseCodeDocAssetsNotFound: DownloadDocAssetsResponseCode
ThumbnailTypePng: ThumbnailType
UploadDocThumbnailResponseCodeSuccess: UploadDocThumbnailResponseCode
UploadDocThumbnailResponseCodeDocNotFound: UploadDocThumbnailResponseCode
UploadDocThumbnailResponseCodeContentNotUploaded: UploadDocThumbnailResponseCode
CreateEnterRoomNotificationUnknown: CreateEnterRoomNotificationResult
CreateEnterRoomNotificationSuccess: CreateEnterRoomNotificationResult
CreateEnterRoomNotificationRoomNotFound: CreateEnterRoomNotificationResult
CreateEnterRoomNotificationNoPermission: CreateEnterRoomNotificationResult
CopyDocResult_Unknown: CopyDocResult
CopyDocResult_Success: CopyDocResult
CopyDocResult_Error_DocInUse: CopyDocResult
CopyDocResult_Error_FullStorage: CopyDocResult
CopyDocResult_Error_MissingPermissions: CopyDocResult
CopyDocResult_Error_MissingDoc: CopyDocResult

class ConvertDocRequest(_message.Message):
    __slots__ = ("docId", "toDocType")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    TODOCTYPE_FIELD_NUMBER: _ClassVar[int]
    docId: str
    toDocType: _gravi_model_pb2.DocumentType
    def __init__(self, docId: _Optional[str] = ..., toDocType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ...) -> None: ...

class ConvertDocResponse(_message.Message):
    __slots__ = ("code", "doc")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    code: ConvertDocResponseCode
    doc: _gravi_model_pb2.DocumentTO
    def __init__(self, code: _Optional[_Union[ConvertDocResponseCode, str]] = ..., doc: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class SearchDocsRequest(_message.Message):
    __slots__ = ("searchPhrase", "pageSize", "pageOffset", "spaceIds", "searchFolderId")
    SEARCHPHRASE_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGEOFFSET_FIELD_NUMBER: _ClassVar[int]
    SPACEIDS_FIELD_NUMBER: _ClassVar[int]
    SEARCHFOLDERID_FIELD_NUMBER: _ClassVar[int]
    searchPhrase: str
    pageSize: int
    pageOffset: int
    spaceIds: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.SpaceId]
    searchFolderId: str
    def __init__(self, searchPhrase: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageOffset: _Optional[int] = ..., spaceIds: _Optional[_Iterable[_Union[_gravi_model_pb2.SpaceId, _Mapping]]] = ..., searchFolderId: _Optional[str] = ...) -> None: ...

class SearchDocsResponse(_message.Message):
    __slots__ = ("docs",)
    DOCS_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ...) -> None: ...

class SearchPublicContentDocByPathRequest(_message.Message):
    __slots__ = ("pathOfDocToFind",)
    PATHOFDOCTOFIND_FIELD_NUMBER: _ClassVar[int]
    pathOfDocToFind: str
    def __init__(self, pathOfDocToFind: _Optional[str] = ...) -> None: ...

class SearchPublicContentDocByPathResponse(_message.Message):
    __slots__ = ("responseCode", "doc")
    RESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    responseCode: SearchPublicContentDocResponseCode
    doc: _gravi_model_pb2.DocumentTO
    def __init__(self, responseCode: _Optional[_Union[SearchPublicContentDocResponseCode, str]] = ..., doc: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class InitiateFileUploadRequest(_message.Message):
    __slots__ = ("ownerId", "uploadParts", "spaceId", "createDocPayload", "createDocAssetPayload", "updateDocPayload", "uploadDocThumbnailPayload")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCASSETPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    UPDATEDOCPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    UPLOADDOCTHUMBNAILPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    uploadParts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    spaceId: _gravi_model_pb2.SpaceId
    createDocPayload: CreateDocPayload
    createDocAssetPayload: CreateDocAssetPayload
    updateDocPayload: UpdateDocPayload
    uploadDocThumbnailPayload: UploadDocThumbnailPayload
    def __init__(self, ownerId: _Optional[str] = ..., uploadParts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., createDocPayload: _Optional[_Union[CreateDocPayload, _Mapping]] = ..., createDocAssetPayload: _Optional[_Union[CreateDocAssetPayload, _Mapping]] = ..., updateDocPayload: _Optional[_Union[UpdateDocPayload, _Mapping]] = ..., uploadDocThumbnailPayload: _Optional[_Union[UploadDocThumbnailPayload, _Mapping]] = ...) -> None: ...

class CreateDocPayload(_message.Message):
    __slots__ = ("docType",)
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    docType: _gravi_model_pb2.DocumentType
    def __init__(self, docType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ...) -> None: ...

class CreateDocAssetPayload(_message.Message):
    __slots__ = ("assetName",)
    ASSETNAME_FIELD_NUMBER: _ClassVar[int]
    assetName: str
    def __init__(self, assetName: _Optional[str] = ...) -> None: ...

class UpdateDocPayload(_message.Message):
    __slots__ = ("docId", "docType")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    docId: str
    docType: _gravi_model_pb2.DocumentType
    def __init__(self, docId: _Optional[str] = ..., docType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ...) -> None: ...

class UploadDocThumbnailPayload(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class UploadPart(_message.Message):
    __slots__ = ("sizeInBytes", "base64EncodedMd5Hash")
    SIZEINBYTES_FIELD_NUMBER: _ClassVar[int]
    BASE64ENCODEDMD5HASH_FIELD_NUMBER: _ClassVar[int]
    sizeInBytes: int
    base64EncodedMd5Hash: str
    def __init__(self, sizeInBytes: _Optional[int] = ..., base64EncodedMd5Hash: _Optional[str] = ...) -> None: ...

class InitiateFileUploadResponse(_message.Message):
    __slots__ = ("code", "partUploadUrls", "uploadId", "contentId", "uploadIdV2")
    CODE_FIELD_NUMBER: _ClassVar[int]
    PARTUPLOADURLS_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    CONTENTID_FIELD_NUMBER: _ClassVar[int]
    UPLOADIDV2_FIELD_NUMBER: _ClassVar[int]
    code: InitiateFileUploadResponseCode
    partUploadUrls: _containers.RepeatedScalarFieldContainer[str]
    uploadId: str
    contentId: str
    uploadIdV2: MultipartUploadId
    def __init__(self, code: _Optional[_Union[InitiateFileUploadResponseCode, str]] = ..., partUploadUrls: _Optional[_Iterable[str]] = ..., uploadId: _Optional[str] = ..., contentId: _Optional[str] = ..., uploadIdV2: _Optional[_Union[MultipartUploadId, _Mapping]] = ...) -> None: ...

class MultipartUploadId(_message.Message):
    __slots__ = ("uploadId", "docId", "docHash")
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    DOCHASH_FIELD_NUMBER: _ClassVar[int]
    uploadId: str
    docId: str
    docHash: str
    def __init__(self, uploadId: _Optional[str] = ..., docId: _Optional[str] = ..., docHash: _Optional[str] = ...) -> None: ...

class DownloadDocRequest(_message.Message):
    __slots__ = ("docId", "assetName", "assetNames", "zipEntireDoc", "revisionHash", "preProcessedGrsImport")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ASSETNAME_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMES_FIELD_NUMBER: _ClassVar[int]
    ZIPENTIREDOC_FIELD_NUMBER: _ClassVar[int]
    REVISIONHASH_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSEDGRSIMPORT_FIELD_NUMBER: _ClassVar[int]
    docId: str
    assetName: str
    assetNames: _containers.RepeatedScalarFieldContainer[str]
    zipEntireDoc: bool
    revisionHash: str
    preProcessedGrsImport: bool
    def __init__(self, docId: _Optional[str] = ..., assetName: _Optional[str] = ..., assetNames: _Optional[_Iterable[str]] = ..., zipEntireDoc: bool = ..., revisionHash: _Optional[str] = ..., preProcessedGrsImport: bool = ...) -> None: ...

class DownloadDocResponse(_message.Message):
    __slots__ = ("code", "downloadUrl", "assetNameAndDownloadUrls", "downloadUrlTTL")
    class AssetNameAndDownloadUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMEANDDOWNLOADURLS_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURLTTL_FIELD_NUMBER: _ClassVar[int]
    code: DownloadDocResponseCode
    downloadUrl: str
    assetNameAndDownloadUrls: _containers.ScalarMap[str, str]
    downloadUrlTTL: int
    def __init__(self, code: _Optional[_Union[DownloadDocResponseCode, str]] = ..., downloadUrl: _Optional[str] = ..., assetNameAndDownloadUrls: _Optional[_Mapping[str, str]] = ..., downloadUrlTTL: _Optional[int] = ...) -> None: ...

class DownloadPublicSpaceDocRequest(_message.Message):
    __slots__ = ("docId", "assetNames", "zipEntireDoc")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMES_FIELD_NUMBER: _ClassVar[int]
    ZIPENTIREDOC_FIELD_NUMBER: _ClassVar[int]
    docId: str
    assetNames: _containers.RepeatedScalarFieldContainer[str]
    zipEntireDoc: bool
    def __init__(self, docId: _Optional[str] = ..., assetNames: _Optional[_Iterable[str]] = ..., zipEntireDoc: bool = ...) -> None: ...

class DownloadPublicSpaceDocResponse(_message.Message):
    __slots__ = ("code", "downloadUrl", "assetNameAndDownloadUrls", "downloadUrlTTL")
    class AssetNameAndDownloadUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMEANDDOWNLOADURLS_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURLTTL_FIELD_NUMBER: _ClassVar[int]
    code: DownloadDocResponseCode
    downloadUrl: str
    assetNameAndDownloadUrls: _containers.ScalarMap[str, str]
    downloadUrlTTL: int
    def __init__(self, code: _Optional[_Union[DownloadDocResponseCode, str]] = ..., downloadUrl: _Optional[str] = ..., assetNameAndDownloadUrls: _Optional[_Mapping[str, str]] = ..., downloadUrlTTL: _Optional[int] = ...) -> None: ...

class CreateDocRequest(_message.Message):
    __slots__ = ("ownerId", "docPath", "uploadParts", "uploadId", "docType", "spaceId", "hasNoInitialContent", "disableServerThumbnailGeneration", "uploadIdV2")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCPATH_FIELD_NUMBER: _ClassVar[int]
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    HASNOINITIALCONTENT_FIELD_NUMBER: _ClassVar[int]
    DISABLESERVERTHUMBNAILGENERATION_FIELD_NUMBER: _ClassVar[int]
    UPLOADIDV2_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docPath: str
    uploadParts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    uploadId: str
    docType: _gravi_model_pb2.DocumentType
    spaceId: _gravi_model_pb2.SpaceId
    hasNoInitialContent: bool
    disableServerThumbnailGeneration: bool
    uploadIdV2: MultipartUploadId
    def __init__(self, ownerId: _Optional[str] = ..., docPath: _Optional[str] = ..., uploadParts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., uploadId: _Optional[str] = ..., docType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., hasNoInitialContent: bool = ..., disableServerThumbnailGeneration: bool = ..., uploadIdV2: _Optional[_Union[MultipartUploadId, _Mapping]] = ...) -> None: ...

class CreateDocResponse(_message.Message):
    __slots__ = ("code", "document")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    code: CreateDocResponseCode
    document: _gravi_model_pb2.DocumentTO
    def __init__(self, code: _Optional[_Union[CreateDocResponseCode, str]] = ..., document: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class UpdateDocRequest(_message.Message):
    __slots__ = ("ownerId", "docId", "uploadParts", "uploadId", "uploadIdV2", "oldContentHash", "spaceId", "disableServerThumbnailGeneration")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    UPLOADIDV2_FIELD_NUMBER: _ClassVar[int]
    OLDCONTENTHASH_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    DISABLESERVERTHUMBNAILGENERATION_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docId: str
    uploadParts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    uploadId: str
    uploadIdV2: MultipartUploadId
    oldContentHash: str
    spaceId: _gravi_model_pb2.SpaceId
    disableServerThumbnailGeneration: bool
    def __init__(self, ownerId: _Optional[str] = ..., docId: _Optional[str] = ..., uploadParts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., uploadId: _Optional[str] = ..., uploadIdV2: _Optional[_Union[MultipartUploadId, _Mapping]] = ..., oldContentHash: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., disableServerThumbnailGeneration: bool = ...) -> None: ...

class UpdateDocResponse(_message.Message):
    __slots__ = ("code", "document")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    code: UpdateDocResponseCode
    document: _gravi_model_pb2.DocumentTO
    def __init__(self, code: _Optional[_Union[UpdateDocResponseCode, str]] = ..., document: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class ListDocsRequest(_message.Message):
    __slots__ = ("ownerId", "documentType", "offset", "pageSize", "sortingType", "folder", "documentTypes", "spaceId", "sortingTypes", "docNameContainsString")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTTYPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    SORTINGTYPE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTTYPES_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SORTINGTYPES_FIELD_NUMBER: _ClassVar[int]
    DOCNAMECONTAINSSTRING_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    documentType: _gravi_model_pb2.DocumentType
    offset: int
    pageSize: int
    sortingType: DocSortingType
    folder: str
    documentTypes: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.DocumentType]
    spaceId: _gravi_model_pb2.SpaceId
    sortingTypes: _containers.RepeatedScalarFieldContainer[DocSortingType]
    docNameContainsString: str
    def __init__(self, ownerId: _Optional[str] = ..., documentType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., offset: _Optional[int] = ..., pageSize: _Optional[int] = ..., sortingType: _Optional[_Union[DocSortingType, str]] = ..., folder: _Optional[str] = ..., documentTypes: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentType, str]]] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., sortingTypes: _Optional[_Iterable[_Union[DocSortingType, str]]] = ..., docNameContainsString: _Optional[str] = ...) -> None: ...

class ListDocsResponse(_message.Message):
    __slots__ = ("docs", "code")
    DOCS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    code: ListDocsResponseCode
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ..., code: _Optional[_Union[ListDocsResponseCode, str]] = ...) -> None: ...

class ListPublicSpaceDocsRequest(_message.Message):
    __slots__ = ("offset", "pageSize", "folder", "documentTypes", "sortingTypes", "docNameContainsString")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTTYPES_FIELD_NUMBER: _ClassVar[int]
    SORTINGTYPES_FIELD_NUMBER: _ClassVar[int]
    DOCNAMECONTAINSSTRING_FIELD_NUMBER: _ClassVar[int]
    offset: int
    pageSize: int
    folder: str
    documentTypes: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.DocumentType]
    sortingTypes: _containers.RepeatedScalarFieldContainer[DocSortingType]
    docNameContainsString: str
    def __init__(self, offset: _Optional[int] = ..., pageSize: _Optional[int] = ..., folder: _Optional[str] = ..., documentTypes: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentType, str]]] = ..., sortingTypes: _Optional[_Iterable[_Union[DocSortingType, str]]] = ..., docNameContainsString: _Optional[str] = ...) -> None: ...

class ListPublicSpaceDocsResponse(_message.Message):
    __slots__ = ("docs",)
    DOCS_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ...) -> None: ...

class ListRecentDocsRequest(_message.Message):
    __slots__ = ("pageToken", "pageSize")
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    pageToken: str
    pageSize: int
    def __init__(self, pageToken: _Optional[str] = ..., pageSize: _Optional[int] = ...) -> None: ...

class ListRecentDocsResponse(_message.Message):
    __slots__ = ("docs", "nextPageToken")
    DOCS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    nextPageToken: str
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class ListSharedDocsRequest(_message.Message):
    __slots__ = ("pageToken", "pageSize")
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    pageToken: str
    pageSize: int
    def __init__(self, pageToken: _Optional[str] = ..., pageSize: _Optional[int] = ...) -> None: ...

class ListSharedDocsResponse(_message.Message):
    __slots__ = ("docs", "roles", "nextPageToken")
    DOCS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    roles: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.CollaborationRole]
    nextPageToken: str
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ..., roles: _Optional[_Iterable[_Union[_gravi_model_pb2.CollaborationRole, str]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class ListDocsInBinRequest(_message.Message):
    __slots__ = ("ownerId", "pageSize", "pageOffset", "spaceId", "sortingTypes")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGEOFFSET_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SORTINGTYPES_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    pageSize: int
    pageOffset: int
    spaceId: _gravi_model_pb2.SpaceId
    sortingTypes: _containers.RepeatedScalarFieldContainer[DocSortingType]
    def __init__(self, ownerId: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageOffset: _Optional[int] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., sortingTypes: _Optional[_Iterable[_Union[DocSortingType, str]]] = ...) -> None: ...

class ListDocsInBinResponse(_message.Message):
    __slots__ = ("docs",)
    DOCS_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ...) -> None: ...

class DeprecatedDocumentIdAndError(_message.Message):
    __slots__ = ("error", "docId")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    error: DeprecatedGetDocumentsError
    docId: str
    def __init__(self, error: _Optional[_Union[DeprecatedGetDocumentsError, str]] = ..., docId: _Optional[str] = ...) -> None: ...

class DeprecatedGetDocumentsRequest(_message.Message):
    __slots__ = ("docIds", "spaceId", "docFullPath", "returnErrors")
    DOCIDS_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    DOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    RETURNERRORS_FIELD_NUMBER: _ClassVar[int]
    docIds: _containers.RepeatedScalarFieldContainer[str]
    spaceId: _gravi_model_pb2.SpaceId
    docFullPath: str
    returnErrors: bool
    def __init__(self, docIds: _Optional[_Iterable[str]] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., docFullPath: _Optional[str] = ..., returnErrors: bool = ...) -> None: ...

class GetDocumentByIdRequest(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class GetDocumentByPathRequest(_message.Message):
    __slots__ = ("spaceId", "docFullPath")
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    DOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    spaceId: _gravi_model_pb2.SpaceId
    docFullPath: str
    def __init__(self, spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., docFullPath: _Optional[str] = ...) -> None: ...

class DeprecatedGetDocumentsResponse(_message.Message):
    __slots__ = ("docs", "errors")
    DOCS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    docs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    errors: _containers.RepeatedCompositeFieldContainer[DeprecatedDocumentIdAndError]
    def __init__(self, docs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[DeprecatedDocumentIdAndError, _Mapping]]] = ...) -> None: ...

class GetDocumentResponse(_message.Message):
    __slots__ = ("doc", "error")
    DOC_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    doc: _gravi_model_pb2.DocumentTO
    error: GetDocumentError
    def __init__(self, doc: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ..., error: _Optional[_Union[GetDocumentError, str]] = ...) -> None: ...

class GetDocumentSpaceNameRequest(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class GetDocumentSpaceNameResponse(_message.Message):
    __slots__ = ("ownerIdName", "partitionIdName", "getDocumentSpaceNameResponseCode")
    OWNERIDNAME_FIELD_NUMBER: _ClassVar[int]
    PARTITIONIDNAME_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTSPACENAMERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    ownerIdName: str
    partitionIdName: str
    getDocumentSpaceNameResponseCode: GetDocumentSpaceNameResponseCode
    def __init__(self, ownerIdName: _Optional[str] = ..., partitionIdName: _Optional[str] = ..., getDocumentSpaceNameResponseCode: _Optional[_Union[GetDocumentSpaceNameResponseCode, str]] = ...) -> None: ...

class SendDocumentRequest(_message.Message):
    __slots__ = ("ownerId", "docId", "email", "senderMessage", "spaceId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SENDERMESSAGE_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docId: str
    email: str
    senderMessage: str
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, ownerId: _Optional[str] = ..., docId: _Optional[str] = ..., email: _Optional[str] = ..., senderMessage: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class SendDocumentResponse(_message.Message):
    __slots__ = ("success", "result", "sendId")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SENDID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: SendDocumentResult
    sendId: str
    def __init__(self, success: bool = ..., result: _Optional[_Union[SendDocumentResult, str]] = ..., sendId: _Optional[str] = ...) -> None: ...

class CreateFolderRequest(_message.Message):
    __slots__ = ("docFullPath", "ownerId", "spaceId")
    DOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    docFullPath: str
    ownerId: str
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, docFullPath: _Optional[str] = ..., ownerId: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class CreateFolderResponse(_message.Message):
    __slots__ = ("resultCode", "latestFolder", "code")
    RESULTCODE_FIELD_NUMBER: _ClassVar[int]
    LATESTFOLDER_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    resultCode: int
    latestFolder: _gravi_model_pb2.DocumentTO
    code: CreateFolderResponseCode
    def __init__(self, resultCode: _Optional[int] = ..., latestFolder: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ..., code: _Optional[_Union[CreateFolderResponseCode, str]] = ...) -> None: ...

class TrashDocRequest(_message.Message):
    __slots__ = ("ownerId", "docId", "docHash", "spaceId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    DOCHASH_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docId: str
    docHash: str
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, ownerId: _Optional[str] = ..., docId: _Optional[str] = ..., docHash: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class TrashDocResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: TrashDocResponseCode
    def __init__(self, code: _Optional[_Union[TrashDocResponseCode, str]] = ...) -> None: ...

class RestoreDocRequest(_message.Message):
    __slots__ = ("ownerId", "docId", "pathToRestoreTo", "spaceId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    PATHTORESTORETO_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docId: str
    pathToRestoreTo: str
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, ownerId: _Optional[str] = ..., docId: _Optional[str] = ..., pathToRestoreTo: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class RestoreDocResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: RestoreDocResponseCode
    def __init__(self, code: _Optional[_Union[RestoreDocResponseCode, str]] = ...) -> None: ...

class DeleteDocsInBinRequest(_message.Message):
    __slots__ = ("ownerId", "docIds", "spaceId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCIDS_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    docIds: _containers.RepeatedScalarFieldContainer[str]
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, ownerId: _Optional[str] = ..., docIds: _Optional[_Iterable[str]] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class DeleteDocsInBinResponse(_message.Message):
    __slots__ = ("code", "deletedDocs")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DELETEDDOCS_FIELD_NUMBER: _ClassVar[int]
    code: DeleteDocsInBinResponseCode
    deletedDocs: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.DocumentTO]
    def __init__(self, code: _Optional[_Union[DeleteDocsInBinResponseCode, str]] = ..., deletedDocs: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentTO, _Mapping]]] = ...) -> None: ...

class MoveDocumentRequest(_message.Message):
    __slots__ = ("docId", "docHash", "toDocFullPath", "fromSpaceId", "toSpaceId")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    DOCHASH_FIELD_NUMBER: _ClassVar[int]
    TODOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    FROMSPACEID_FIELD_NUMBER: _ClassVar[int]
    TOSPACEID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    docHash: str
    toDocFullPath: str
    fromSpaceId: _gravi_model_pb2.SpaceId
    toSpaceId: _gravi_model_pb2.SpaceId
    def __init__(self, docId: _Optional[str] = ..., docHash: _Optional[str] = ..., toDocFullPath: _Optional[str] = ..., fromSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., toSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class MoveDocumentResponse(_message.Message):
    __slots__ = ("result", "movedDocument")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MOVEDDOCUMENT_FIELD_NUMBER: _ClassVar[int]
    result: MoveDocResult
    movedDocument: _gravi_model_pb2.DocumentTO
    def __init__(self, result: _Optional[_Union[MoveDocResult, str]] = ..., movedDocument: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class GetUsedSpaceSizeRequest(_message.Message):
    __slots__ = ("ownerId", "spaceId")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    spaceId: _gravi_model_pb2.SpaceId
    def __init__(self, ownerId: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class GetUsedSpaceSizeResponse(_message.Message):
    __slots__ = ("usedSize", "freeSize")
    USEDSIZE_FIELD_NUMBER: _ClassVar[int]
    FREESIZE_FIELD_NUMBER: _ClassVar[int]
    usedSize: int
    freeSize: int
    def __init__(self, usedSize: _Optional[int] = ..., freeSize: _Optional[int] = ...) -> None: ...

class CreateDocAssetRequest(_message.Message):
    __slots__ = ("docId", "assetName", "contentSource", "uploadId", "uploadParts", "contentDocSpaceId", "contentDocId", "uploadIdV2")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ASSETNAME_FIELD_NUMBER: _ClassVar[int]
    CONTENTSOURCE_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    CONTENTDOCSPACEID_FIELD_NUMBER: _ClassVar[int]
    CONTENTDOCID_FIELD_NUMBER: _ClassVar[int]
    UPLOADIDV2_FIELD_NUMBER: _ClassVar[int]
    docId: str
    assetName: str
    contentSource: FileContentSource
    uploadId: str
    uploadParts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    contentDocSpaceId: _gravi_model_pb2.SpaceId
    contentDocId: str
    uploadIdV2: MultipartUploadId
    def __init__(self, docId: _Optional[str] = ..., assetName: _Optional[str] = ..., contentSource: _Optional[_Union[FileContentSource, str]] = ..., uploadId: _Optional[str] = ..., uploadParts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., contentDocSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., contentDocId: _Optional[str] = ..., uploadIdV2: _Optional[_Union[MultipartUploadId, _Mapping]] = ...) -> None: ...

class CreateDocAssetResponse(_message.Message):
    __slots__ = ("code", "doc")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    code: CreateDocAssetResponseCode
    doc: _gravi_model_pb2.DocumentTO
    def __init__(self, code: _Optional[_Union[CreateDocAssetResponseCode, str]] = ..., doc: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ...) -> None: ...

class DownloadDocAssetsRequest(_message.Message):
    __slots__ = ("docId", "assetNames")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMES_FIELD_NUMBER: _ClassVar[int]
    docId: str
    assetNames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, docId: _Optional[str] = ..., assetNames: _Optional[_Iterable[str]] = ...) -> None: ...

class DownloadDocAssetsResponse(_message.Message):
    __slots__ = ("code", "assetNameAndDownloadUrls")
    class AssetNameAndDownloadUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    ASSETNAMEANDDOWNLOADURLS_FIELD_NUMBER: _ClassVar[int]
    code: DownloadDocAssetsResponseCode
    assetNameAndDownloadUrls: _containers.ScalarMap[str, str]
    def __init__(self, code: _Optional[_Union[DownloadDocAssetsResponseCode, str]] = ..., assetNameAndDownloadUrls: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UploadDocThumbnailRequest(_message.Message):
    __slots__ = ("docId", "thumbnailType", "uploadParts", "uploadId", "uploadIdV2")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILTYPE_FIELD_NUMBER: _ClassVar[int]
    UPLOADPARTS_FIELD_NUMBER: _ClassVar[int]
    UPLOADID_FIELD_NUMBER: _ClassVar[int]
    UPLOADIDV2_FIELD_NUMBER: _ClassVar[int]
    docId: str
    thumbnailType: ThumbnailType
    uploadParts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    uploadId: str
    uploadIdV2: MultipartUploadId
    def __init__(self, docId: _Optional[str] = ..., thumbnailType: _Optional[_Union[ThumbnailType, str]] = ..., uploadParts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., uploadId: _Optional[str] = ..., uploadIdV2: _Optional[_Union[MultipartUploadId, _Mapping]] = ...) -> None: ...

class UploadDocThumbnailResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: UploadDocThumbnailResponseCode
    def __init__(self, code: _Optional[_Union[UploadDocThumbnailResponseCode, str]] = ...) -> None: ...

class CreateEnterRoomNotificationRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class CreateEnterRoomNotificationResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CreateEnterRoomNotificationResult
    def __init__(self, result: _Optional[_Union[CreateEnterRoomNotificationResult, str]] = ...) -> None: ...

class ListAllUsersWithAccessToDocRequest(_message.Message):
    __slots__ = ("docId", "lastPageToken", "pageSize")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    LASTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    docId: str
    lastPageToken: str
    pageSize: int
    def __init__(self, docId: _Optional[str] = ..., lastPageToken: _Optional[str] = ..., pageSize: _Optional[int] = ...) -> None: ...

class ListAllUsersWithAccessToDocResponse(_message.Message):
    __slots__ = ("users", "pageToken")
    USERS_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserWithAccessToDoc]
    pageToken: str
    def __init__(self, users: _Optional[_Iterable[_Union[UserWithAccessToDoc, _Mapping]]] = ..., pageToken: _Optional[str] = ...) -> None: ...

class UserWithAccessToDoc(_message.Message):
    __slots__ = ("displayName", "email", "userId", "sharedOrChangedRole", "role")
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SHAREDORCHANGEDROLE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    displayName: str
    email: str
    userId: str
    sharedOrChangedRole: bool
    role: _gravi_model_pb2.CollaborationRole
    def __init__(self, displayName: _Optional[str] = ..., email: _Optional[str] = ..., userId: _Optional[str] = ..., sharedOrChangedRole: bool = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class CopyDocRequest(_message.Message):
    __slots__ = ("docId", "toSpaceId", "newDocPath")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    TOSPACEID_FIELD_NUMBER: _ClassVar[int]
    NEWDOCPATH_FIELD_NUMBER: _ClassVar[int]
    docId: str
    toSpaceId: _gravi_model_pb2.SpaceId
    newDocPath: str
    def __init__(self, docId: _Optional[str] = ..., toSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., newDocPath: _Optional[str] = ...) -> None: ...

class CopyDocResponse(_message.Message):
    __slots__ = ("res",)
    RES_FIELD_NUMBER: _ClassVar[int]
    res: CopyDocResult
    def __init__(self, res: _Optional[_Union[CopyDocResult, str]] = ...) -> None: ...
