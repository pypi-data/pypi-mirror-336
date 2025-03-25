import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShareRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ShareRoomResult_ShareRoomInvalid: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomSuccess: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomInvalidEmail: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomNoPermission: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomWithSelf: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomNeedSeat: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomCantInviteOrgUser: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomRoleMustNotBeHigherThanLicenseCap: _ClassVar[ShareRoomResult]
    ShareRoomResult_ShareRoomRoleMustNotBeHigherThanActorRole: _ClassVar[ShareRoomResult]

class RemoveAccessFromRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RemoveAccessFromRoomResult_Unknown: _ClassVar[RemoveAccessFromRoomResult]
    RemoveAccessFromRoomResult_Success: _ClassVar[RemoveAccessFromRoomResult]
    RemoveAccessFromRoomResult_RoleMustBeCreatorToRemoveUser: _ClassVar[RemoveAccessFromRoomResult]
    RemoveAccessFromRoomResult_RoomNotFound: _ClassVar[RemoveAccessFromRoomResult]

class GenerateDeepAccessLinksResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GenerateDeepLinks_Unknown: _ClassVar[GenerateDeepAccessLinksResult]
    GenerateDeepLinks_Success: _ClassVar[GenerateDeepAccessLinksResult]
    GenerateDeepLinks_NoPermission: _ClassVar[GenerateDeepAccessLinksResult]
    GenerateDeepLinks_RoomIsLocked: _ClassVar[GenerateDeepAccessLinksResult]
    GenerateDeepLinks_RoomNotFound: _ClassVar[GenerateDeepAccessLinksResult]
    GenerateDeepLinks_LinkNotFound: _ClassVar[GenerateDeepAccessLinksResult]

class DataUpdateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[DataUpdateType]
    Stroke: _ClassVar[DataUpdateType]
    Layer: _ClassVar[DataUpdateType]
    Material: _ClassVar[DataUpdateType]
    Group: _ClassVar[DataUpdateType]
    AssetReady: _ClassVar[DataUpdateType]
    LayerGroupEntry: _ClassVar[DataUpdateType]

class BookmarkPublicDocResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BookmarkPublicRoomUnknown: _ClassVar[BookmarkPublicDocResult]
    BookmarkPublicRoomSuccess: _ClassVar[BookmarkPublicDocResult]
    BookmarkPublicRoomNoPermission: _ClassVar[BookmarkPublicDocResult]
    BookmarkPublicRoomNotFound: _ClassVar[BookmarkPublicDocResult]

class RequestRoomAccessResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RequestRoomAccessResult_Unknown: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RequestedAccessToOrg: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RequestedAccessToRoom: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_AlreadyHasAccess: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_AlreadyRequestedAccess: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RejectedInvalidEmail: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RoomDoesNotExits: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RequestedAccessToOrgTeam: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RejectedUnauthorized: _ClassVar[RequestRoomAccessResult]
    RequestRoomAccessResult_RejectedUserInAnotherOrg: _ClassVar[RequestRoomAccessResult]

class LaunchStreamingAgentForRoomResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LaunchStreamingAgentForRoomResponseCodeSuccess: _ClassVar[LaunchStreamingAgentForRoomResponseCode]
    LaunchStreamingAgentForRoomResponseCodeRoomNotFound: _ClassVar[LaunchStreamingAgentForRoomResponseCode]

class GetRoomIdByShortCodeResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetRoomIdByShortCodeResponseCodeUnknown: _ClassVar[GetRoomIdByShortCodeResponseCode]
    GetRoomIdByShortCodeResponseCodeRoomNotFound: _ClassVar[GetRoomIdByShortCodeResponseCode]
    GetRoomIdByShortCodeResponseCodeNoPermission: _ClassVar[GetRoomIdByShortCodeResponseCode]
    GetRoomIdByShortCodeResponseCodeMalformedCode: _ClassVar[GetRoomIdByShortCodeResponseCode]
    GetRoomIdByShortCodeResponseCodeSuccess: _ClassVar[GetRoomIdByShortCodeResponseCode]

class GetShortCodeByRoomIdResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetShortCodeByRoomIdResponseCodeUnknown: _ClassVar[GetShortCodeByRoomIdResponseCode]
    GetShortCodeByRoomIdResponseCodeRoomNotFound: _ClassVar[GetShortCodeByRoomIdResponseCode]
    GetShortCodeByRoomIdResponseCodeNoPermission: _ClassVar[GetShortCodeByRoomIdResponseCode]
    GetShortCodeByRoomIdResponseCodeSuccess: _ClassVar[GetShortCodeByRoomIdResponseCode]
ShareRoomResult_ShareRoomInvalid: ShareRoomResult
ShareRoomResult_ShareRoomSuccess: ShareRoomResult
ShareRoomResult_ShareRoomInvalidEmail: ShareRoomResult
ShareRoomResult_ShareRoomNoPermission: ShareRoomResult
ShareRoomResult_ShareRoomWithSelf: ShareRoomResult
ShareRoomResult_ShareRoomNeedSeat: ShareRoomResult
ShareRoomResult_ShareRoomCantInviteOrgUser: ShareRoomResult
ShareRoomResult_ShareRoomRoleMustNotBeHigherThanLicenseCap: ShareRoomResult
ShareRoomResult_ShareRoomRoleMustNotBeHigherThanActorRole: ShareRoomResult
RemoveAccessFromRoomResult_Unknown: RemoveAccessFromRoomResult
RemoveAccessFromRoomResult_Success: RemoveAccessFromRoomResult
RemoveAccessFromRoomResult_RoleMustBeCreatorToRemoveUser: RemoveAccessFromRoomResult
RemoveAccessFromRoomResult_RoomNotFound: RemoveAccessFromRoomResult
GenerateDeepLinks_Unknown: GenerateDeepAccessLinksResult
GenerateDeepLinks_Success: GenerateDeepAccessLinksResult
GenerateDeepLinks_NoPermission: GenerateDeepAccessLinksResult
GenerateDeepLinks_RoomIsLocked: GenerateDeepAccessLinksResult
GenerateDeepLinks_RoomNotFound: GenerateDeepAccessLinksResult
GenerateDeepLinks_LinkNotFound: GenerateDeepAccessLinksResult
Unknown: DataUpdateType
Stroke: DataUpdateType
Layer: DataUpdateType
Material: DataUpdateType
Group: DataUpdateType
AssetReady: DataUpdateType
LayerGroupEntry: DataUpdateType
BookmarkPublicRoomUnknown: BookmarkPublicDocResult
BookmarkPublicRoomSuccess: BookmarkPublicDocResult
BookmarkPublicRoomNoPermission: BookmarkPublicDocResult
BookmarkPublicRoomNotFound: BookmarkPublicDocResult
RequestRoomAccessResult_Unknown: RequestRoomAccessResult
RequestRoomAccessResult_RequestedAccessToOrg: RequestRoomAccessResult
RequestRoomAccessResult_RequestedAccessToRoom: RequestRoomAccessResult
RequestRoomAccessResult_AlreadyHasAccess: RequestRoomAccessResult
RequestRoomAccessResult_AlreadyRequestedAccess: RequestRoomAccessResult
RequestRoomAccessResult_RejectedInvalidEmail: RequestRoomAccessResult
RequestRoomAccessResult_RoomDoesNotExits: RequestRoomAccessResult
RequestRoomAccessResult_RequestedAccessToOrgTeam: RequestRoomAccessResult
RequestRoomAccessResult_RejectedUnauthorized: RequestRoomAccessResult
RequestRoomAccessResult_RejectedUserInAnotherOrg: RequestRoomAccessResult
LaunchStreamingAgentForRoomResponseCodeSuccess: LaunchStreamingAgentForRoomResponseCode
LaunchStreamingAgentForRoomResponseCodeRoomNotFound: LaunchStreamingAgentForRoomResponseCode
GetRoomIdByShortCodeResponseCodeUnknown: GetRoomIdByShortCodeResponseCode
GetRoomIdByShortCodeResponseCodeRoomNotFound: GetRoomIdByShortCodeResponseCode
GetRoomIdByShortCodeResponseCodeNoPermission: GetRoomIdByShortCodeResponseCode
GetRoomIdByShortCodeResponseCodeMalformedCode: GetRoomIdByShortCodeResponseCode
GetRoomIdByShortCodeResponseCodeSuccess: GetRoomIdByShortCodeResponseCode
GetShortCodeByRoomIdResponseCodeUnknown: GetShortCodeByRoomIdResponseCode
GetShortCodeByRoomIdResponseCodeRoomNotFound: GetShortCodeByRoomIdResponseCode
GetShortCodeByRoomIdResponseCodeNoPermission: GetShortCodeByRoomIdResponseCode
GetShortCodeByRoomIdResponseCodeSuccess: GetShortCodeByRoomIdResponseCode

class ShareRoomWithUserRequest(_message.Message):
    __slots__ = ("roomId", "shareWithEmail", "role")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SHAREWITHEMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    shareWithEmail: str
    role: _gravi_model_pb2.CollaborationRole
    def __init__(self, roomId: _Optional[str] = ..., shareWithEmail: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class ShareRoomWithUserResponse(_message.Message):
    __slots__ = ("result", "userId", "magicLinkId")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    MAGICLINKID_FIELD_NUMBER: _ClassVar[int]
    result: ShareRoomResult
    userId: str
    magicLinkId: str
    def __init__(self, result: _Optional[_Union[ShareRoomResult, str]] = ..., userId: _Optional[str] = ..., magicLinkId: _Optional[str] = ...) -> None: ...

class UpdateUserRoomAccessRequest(_message.Message):
    __slots__ = ("roomId", "sharedWithEmail", "role")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SHAREDWITHEMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    sharedWithEmail: str
    role: _gravi_model_pb2.CollaborationRole
    def __init__(self, roomId: _Optional[str] = ..., sharedWithEmail: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class ListRoomAccessesRequest(_message.Message):
    __slots__ = ("roomId", "lastIdentityId", "amount")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    LASTIDENTITYID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    lastIdentityId: str
    amount: int
    def __init__(self, roomId: _Optional[str] = ..., lastIdentityId: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class ListRoomAccessesResponse(_message.Message):
    __slots__ = ("identities",)
    IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    identities: _containers.RepeatedCompositeFieldContainer[IdentityAccess]
    def __init__(self, identities: _Optional[_Iterable[_Union[IdentityAccess, _Mapping]]] = ...) -> None: ...

class IdentityAccess(_message.Message):
    __slots__ = ("identityId", "identityName", "userEmail", "role")
    IDENTITYID_FIELD_NUMBER: _ClassVar[int]
    IDENTITYNAME_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    identityId: str
    identityName: str
    userEmail: str
    role: _gravi_model_pb2.CollaborationRole
    def __init__(self, identityId: _Optional[str] = ..., identityName: _Optional[str] = ..., userEmail: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class RemoveAccessFromRoomRequest(_message.Message):
    __slots__ = ("roomId", "identityId", "isSharedRoom")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    IDENTITYID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    identityId: str
    isSharedRoom: bool
    def __init__(self, roomId: _Optional[str] = ..., identityId: _Optional[str] = ..., isSharedRoom: bool = ...) -> None: ...

class StopRoomSharingRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class StopRoomSharingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveAccessFromRoomResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RemoveAccessFromRoomResult
    def __init__(self, result: _Optional[_Union[RemoveAccessFromRoomResult, str]] = ...) -> None: ...

class SetCoSketchRoomPassRequest(_message.Message):
    __slots__ = ("roomId", "currentPass", "newPass")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    CURRENTPASS_FIELD_NUMBER: _ClassVar[int]
    NEWPASS_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    currentPass: str
    newPass: str
    def __init__(self, roomId: _Optional[str] = ..., currentPass: _Optional[str] = ..., newPass: _Optional[str] = ...) -> None: ...

class SetCoSketchRoomPassResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GenerateDeepAccessLinkRequest(_message.Message):
    __slots__ = ("deepLink", "roomId")
    DEEPLINK_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    deepLink: str
    roomId: str
    def __init__(self, deepLink: _Optional[str] = ..., roomId: _Optional[str] = ...) -> None: ...

class GenerateDeepAccessLinkResponse(_message.Message):
    __slots__ = ("result", "responseContent", "oneTimeAuthToken")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RESPONSECONTENT_FIELD_NUMBER: _ClassVar[int]
    ONETIMEAUTHTOKEN_FIELD_NUMBER: _ClassVar[int]
    result: GenerateDeepAccessLinksResult
    responseContent: _gravi_model_pb2.GSDeepLinkTO
    oneTimeAuthToken: str
    def __init__(self, result: _Optional[_Union[GenerateDeepAccessLinksResult, str]] = ..., responseContent: _Optional[_Union[_gravi_model_pb2.GSDeepLinkTO, _Mapping]] = ..., oneTimeAuthToken: _Optional[str] = ...) -> None: ...

class GetSketchRoomUpdatesRequest(_message.Message):
    __slots__ = ("roomId", "lastSeqStamp")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    LASTSEQSTAMP_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    lastSeqStamp: int
    def __init__(self, roomId: _Optional[str] = ..., lastSeqStamp: _Optional[int] = ...) -> None: ...

class GetSketchRoomUpdatesResponse(_message.Message):
    __slots__ = ("lastSeqStamp", "updates", "ccLiveInstance")
    LASTSEQSTAMP_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    CCLIVEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    lastSeqStamp: int
    updates: _containers.RepeatedCompositeFieldContainer[DataUpdate]
    ccLiveInstance: _gravi_model_pb2.CoCreationLiveInstance
    def __init__(self, lastSeqStamp: _Optional[int] = ..., updates: _Optional[_Iterable[_Union[DataUpdate, _Mapping]]] = ..., ccLiveInstance: _Optional[_Union[_gravi_model_pb2.CoCreationLiveInstance, _Mapping]] = ...) -> None: ...

class DataUpdate(_message.Message):
    __slots__ = ("deleted", "updateType", "strokeId", "strokeData", "layer", "drawMaterial", "group", "assetName", "layerGroupEntry")
    DELETED_FIELD_NUMBER: _ClassVar[int]
    UPDATETYPE_FIELD_NUMBER: _ClassVar[int]
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    STROKEDATA_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    ASSETNAME_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPENTRY_FIELD_NUMBER: _ClassVar[int]
    deleted: bool
    updateType: DataUpdateType
    strokeId: _sketch_common_pb2.GSDataID
    strokeData: _sketch_model_pb2.StrokeDataSnapshot
    layer: _sketch_common_pb2.LayerModelTO
    drawMaterial: _sketch_common_pb2.DrawMaterial
    group: _sketch_model_pb2.StrokeGroupTO
    assetName: str
    layerGroupEntry: _sketch_common_pb2.NestedLayerRelationship
    def __init__(self, deleted: bool = ..., updateType: _Optional[_Union[DataUpdateType, str]] = ..., strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., strokeData: _Optional[_Union[_sketch_model_pb2.StrokeDataSnapshot, _Mapping]] = ..., layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ..., drawMaterial: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ..., group: _Optional[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]] = ..., assetName: _Optional[str] = ..., layerGroupEntry: _Optional[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]] = ...) -> None: ...

class SetPublicDocRequest(_message.Message):
    __slots__ = ("docId", "isPublicAccessible", "joinerRequestEnabled")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ISPUBLICACCESSIBLE_FIELD_NUMBER: _ClassVar[int]
    JOINERREQUESTENABLED_FIELD_NUMBER: _ClassVar[int]
    docId: str
    isPublicAccessible: bool
    joinerRequestEnabled: bool
    def __init__(self, docId: _Optional[str] = ..., isPublicAccessible: bool = ..., joinerRequestEnabled: bool = ...) -> None: ...

class SetPublicDocResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class BookmarkPublicDocRequest(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: str
    def __init__(self, docId: _Optional[str] = ...) -> None: ...

class BookmarkPublicDocResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: BookmarkPublicDocResult
    def __init__(self, result: _Optional[_Union[BookmarkPublicDocResult, str]] = ...) -> None: ...

class ListPublicRoomRequest(_message.Message):
    __slots__ = ("numPerPage", "pageToken")
    NUMPERPAGE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    numPerPage: int
    pageToken: str
    def __init__(self, numPerPage: _Optional[int] = ..., pageToken: _Optional[str] = ...) -> None: ...

class RequestRoomAccessRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class RequestRoomAccessResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestRoomAccessResult
    def __init__(self, result: _Optional[_Union[RequestRoomAccessResult, str]] = ...) -> None: ...

class RoomAccessRequest(_message.Message):
    __slots__ = ("roomId", "email", "role", "requestedOn", "userId")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    REQUESTEDON_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    email: str
    role: _gravi_model_pb2.CollaborationRole
    requestedOn: int
    userId: str
    def __init__(self, roomId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., requestedOn: _Optional[int] = ..., userId: _Optional[str] = ...) -> None: ...

class ListRoomAccessRequestsRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class ListRoomAccessRequestsResponse(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[RoomAccessRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[RoomAccessRequest, _Mapping]]] = ...) -> None: ...

class ApproveRoomAccessRequest(_message.Message):
    __slots__ = ("roomId", "email", "role", "approve")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    APPROVE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    email: str
    role: _gravi_model_pb2.CollaborationRole
    approve: bool
    def __init__(self, roomId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., approve: bool = ...) -> None: ...

class ApproveRoomAccessResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ShareRoomResult
    def __init__(self, result: _Optional[_Union[ShareRoomResult, str]] = ...) -> None: ...

class LaunchStreamingAgentForRoomRequest(_message.Message):
    __slots__ = ("roomId", "deeplink")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    DEEPLINK_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    deeplink: str
    def __init__(self, roomId: _Optional[str] = ..., deeplink: _Optional[str] = ...) -> None: ...

class LaunchStreamingAgentForRoomResponse(_message.Message):
    __slots__ = ("code", "embeddableStreamingUrl")
    CODE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDABLESTREAMINGURL_FIELD_NUMBER: _ClassVar[int]
    code: LaunchStreamingAgentForRoomResponseCode
    embeddableStreamingUrl: str
    def __init__(self, code: _Optional[_Union[LaunchStreamingAgentForRoomResponseCode, str]] = ..., embeddableStreamingUrl: _Optional[str] = ...) -> None: ...

class EnterRoomViaAdminNotificationDeeplinkRequest(_message.Message):
    __slots__ = ("deeplink", "grsVersion")
    DEEPLINK_FIELD_NUMBER: _ClassVar[int]
    GRSVERSION_FIELD_NUMBER: _ClassVar[int]
    deeplink: str
    grsVersion: int
    def __init__(self, deeplink: _Optional[str] = ..., grsVersion: _Optional[int] = ...) -> None: ...

class GetRoomIdByShortCodeRequest(_message.Message):
    __slots__ = ("shortCode",)
    SHORTCODE_FIELD_NUMBER: _ClassVar[int]
    shortCode: str
    def __init__(self, shortCode: _Optional[str] = ...) -> None: ...

class GetRoomIdByShortCodeResponse(_message.Message):
    __slots__ = ("code", "roomId")
    CODE_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    code: GetRoomIdByShortCodeResponseCode
    roomId: str
    def __init__(self, code: _Optional[_Union[GetRoomIdByShortCodeResponseCode, str]] = ..., roomId: _Optional[str] = ...) -> None: ...

class GetShortCodeByRoomIdRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class GetShortCodeByRoomIdResponse(_message.Message):
    __slots__ = ("code", "shortCode")
    CODE_FIELD_NUMBER: _ClassVar[int]
    SHORTCODE_FIELD_NUMBER: _ClassVar[int]
    code: GetShortCodeByRoomIdResponseCode
    shortCode: str
    def __init__(self, code: _Optional[_Union[GetShortCodeByRoomIdResponseCode, str]] = ..., shortCode: _Optional[str] = ...) -> None: ...
