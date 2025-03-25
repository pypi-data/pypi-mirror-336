from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rpc import cosketch_serverpush_pb2 as _cosketch_serverpush_pb2
from gravi.rpc.model.extra import sketch_extra_pb2 as _sketch_extra_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.rpc.model.incremental import sketch_incremental_pb2 as _sketch_incremental_pb2
from gravi.gsfile.metadata.persistence import metadata_pb2 as _metadata_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RpcErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoError: _ClassVar[RpcErrorCode]
    Unknown: _ClassVar[RpcErrorCode]
    RejoinRoom: _ClassVar[RpcErrorCode]
    ServerError: _ClassVar[RpcErrorCode]
    MultiJoinError: _ClassVar[RpcErrorCode]
    ActorIsCreating: _ClassVar[RpcErrorCode]
    ActorCreationError: _ClassVar[RpcErrorCode]
    RoomNotExist: _ClassVar[RpcErrorCode]
    ActorAskTimeout: _ClassVar[RpcErrorCode]
    RpcTypeNotFound: _ClassVar[RpcErrorCode]
    RoomIdMissing: _ClassVar[RpcErrorCode]
    ClientIdMissing: _ClassVar[RpcErrorCode]
    InvalidTicket: _ClassVar[RpcErrorCode]
    UserIdMissing: _ClassVar[RpcErrorCode]
    RoomIsFull: _ClassVar[RpcErrorCode]
    RoomIsLocked: _ClassVar[RpcErrorCode]
    ExpiredTicket: _ClassVar[RpcErrorCode]
    ExpiredTCPChannel: _ClassVar[RpcErrorCode]
    DuplicatedRpc: _ClassVar[RpcErrorCode]
    DiscardedRpc: _ClassVar[RpcErrorCode]

class RpcType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownType: _ClassVar[RpcType]
    ConnHandshake: _ClassVar[RpcType]
    JoinRoom: _ClassVar[RpcType]
    LeaveRoom: _ClassVar[RpcType]
    HeartBeat: _ClassVar[RpcType]
    SketchAction: _ClassVar[RpcType]
    PollSketch: _ClassVar[RpcType]
    PollFinalSketches: _ClassVar[RpcType]
    SyncFinalSketches: _ClassVar[RpcType]
    SyncFinalGroups: _ClassVar[RpcType]
    AddLayer: _ClassVar[RpcType]
    DeleteLayer: _ClassVar[RpcType]
    GetLayer: _ClassVar[RpcType]
    ModifyLayer: _ClassVar[RpcType]
    PreviewLayer: _ClassVar[RpcType]
    ChangeStrokeLayer: _ClassVar[RpcType]
    PlaceDeleteLayerLock: _ClassVar[RpcType]
    CancelDeleteLayerLock: _ClassVar[RpcType]
    ModifyLayerGroup: _ClassVar[RpcType]
    GroupingObjects: _ClassVar[RpcType]
    UnGroupingObjects: _ClassVar[RpcType]
    AddImportedGroup: _ClassVar[RpcType]
    CreateDuplicatedGroups: _ClassVar[RpcType]
    ConvertToSubD: _ClassVar[RpcType]
    ReverseSubDConversion: _ClassVar[RpcType]
    MergeSubDObjects: _ClassVar[RpcType]
    UpdateMaterial: _ClassVar[RpcType]
    PreviewMaterial: _ClassVar[RpcType]
    SyncTransform: _ClassVar[RpcType]
    SyncUserState: _ClassVar[RpcType]
    AssetsReady: _ClassVar[RpcType]
    ChangeRoomCoordinator: _ClassVar[RpcType]
    ChangeEnvironment: _ClassVar[RpcType]
    SyncRoomExtraData: _ClassVar[RpcType]
    LockWholeRoom: _ClassVar[RpcType]
    UpdateCoSketchUser: _ClassVar[RpcType]
    RequestToFollow: _ClassVar[RpcType]
    UpdateSectionView: _ClassVar[RpcType]
    PreviewIncrementalData: _ClassVar[RpcType]
    ConfirmIncrementalData: _ClassVar[RpcType]
    GetMissingConfirmIncrementalData: _ClassVar[RpcType]
    RepairSubD: _ClassVar[RpcType]
    SubmitSketchStateChanges: _ClassVar[RpcType]
    ClientRelayData: _ClassVar[RpcType]
    ListPlayers: _ClassVar[RpcType]
    BroadcastRelayData: _ClassVar[RpcType]
    SyncUI: _ClassVar[RpcType]
    SendMessageBroadcast: _ClassVar[RpcType]
    GetMissingMessage: _ClassVar[RpcType]
    SyncUserPreferences: _ClassVar[RpcType]
    SyncUserDefaults: _ClassVar[RpcType]
    AuthorizeJoiner: _ClassVar[RpcType]
    SketchStateChange: _ClassVar[RpcType]
    ServerPush: _ClassVar[RpcType]

class SingleSketchObjectChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SingleSketchObjectChangeTypeUnset: _ClassVar[SingleSketchObjectChangeType]
    SingleSketchObjectChangeTypeCreate: _ClassVar[SingleSketchObjectChangeType]
    SingleSketchObjectChangeTypeUpdate: _ClassVar[SingleSketchObjectChangeType]
    SingleSketchObjectChangeTypeDelete: _ClassVar[SingleSketchObjectChangeType]

class CollaborationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Success: _ClassVar[CollaborationResult]
    NoPermission: _ClassVar[CollaborationResult]

class StrokeActionResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    StrokeActionSuccess: _ClassVar[StrokeActionResult]
    StrokeRevisionOutOfDate: _ClassVar[StrokeActionResult]
    StrokeLayerNotExists: _ClassVar[StrokeActionResult]
    SeqIdOutOfDate: _ClassVar[StrokeActionResult]
    StrokeDeleted: _ClassVar[StrokeActionResult]
    StrokeUsedByOthers: _ClassVar[StrokeActionResult]
    StrokeMissingLayerId: _ClassVar[StrokeActionResult]
    StrokeMissingMaterial: _ClassVar[StrokeActionResult]
    OutOfDateStroke: _ClassVar[StrokeActionResult]
    MissingFinalStroke: _ClassVar[StrokeActionResult]
    DataIntegrityError: _ClassVar[StrokeActionResult]
    TolerableEdgeCase: _ClassVar[StrokeActionResult]

class LayerActionResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LayerActionSuccess: _ClassVar[LayerActionResult]
    LayerRevisionOutOfDate: _ClassVar[LayerActionResult]
    NotLayerOwner: _ClassVar[LayerActionResult]
    LayerSettingReject: _ClassVar[LayerActionResult]
    NewLayerIdExists: _ClassVar[LayerActionResult]
    LayerNotExists: _ClassVar[LayerActionResult]
    LayerInUse: _ClassVar[LayerActionResult]
    LayerClientIDIsMissing: _ClassVar[LayerActionResult]

class PlaceDeleteLayerLockResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PlaceLayerLockUnknown: _ClassVar[PlaceDeleteLayerLockResult]
    PlaceLayerLockSuccess: _ClassVar[PlaceDeleteLayerLockResult]
    PlaceLayerLockHashFailure: _ClassVar[PlaceDeleteLayerLockResult]
    PlaceLayerLockUnknownFailure: _ClassVar[PlaceDeleteLayerLockResult]
    PlaceLayerLockStrokeFailure: _ClassVar[PlaceDeleteLayerLockResult]

class ModifyLayerGroupResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ModifyLayerGroupUnknown: _ClassVar[ModifyLayerGroupResult]
    ModifyLayerGroupSuccess: _ClassVar[ModifyLayerGroupResult]
    ModifyLayerGroupBadClientRequest: _ClassVar[ModifyLayerGroupResult]

class PreviewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Color: _ClassVar[PreviewType]
    MaterialType: _ClassVar[PreviewType]
    Guid: _ClassVar[PreviewType]
    AlphaTransparency: _ClassVar[PreviewType]
    ResetMaterial: _ClassVar[PreviewType]
    TextureTransform: _ClassVar[PreviewType]
    Roughness: _ClassVar[PreviewType]
    Metallic: _ClassVar[PreviewType]
    HueShift: _ClassVar[PreviewType]
    ShadowSoftness: _ClassVar[PreviewType]
    OutlineWidth: _ClassVar[PreviewType]
    OutlineColor: _ClassVar[PreviewType]

class ConfirmIncrementalResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ConfirmIncrementalUnknown: _ClassVar[ConfirmIncrementalResult]
    ConfirmIncrementalSuccess: _ClassVar[ConfirmIncrementalResult]
    ConfirmIncrementalStrokeMissing: _ClassVar[ConfirmIncrementalResult]
    ConfirmIncrementalStrokeDeleted: _ClassVar[ConfirmIncrementalResult]
    ConfirmIncrementalStrokeNotLocked: _ClassVar[ConfirmIncrementalResult]

class RepairSubDResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RepairSubDResultUnknown: _ClassVar[RepairSubDResult]
    RepairSubDResultSuccess: _ClassVar[RepairSubDResult]
    RepairSubDCorruptObjectMissing: _ClassVar[RepairSubDResult]
    RepairSubDCorruptObjectAlreadyRepaired: _ClassVar[RepairSubDResult]

class LockWholeRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LockWholeRoomUnknown: _ClassVar[LockWholeRoomResult]
    LockWholeRoomSuccess: _ClassVar[LockWholeRoomResult]
    LockWholeRoomNoPermission: _ClassVar[LockWholeRoomResult]

class UpdateCoSketchUserResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateCoSketchUserUnknown: _ClassVar[UpdateCoSketchUserResult]
    UpdateCoSketchUserSuccess: _ClassVar[UpdateCoSketchUserResult]
    UpdateCoSketchUserInvalidName: _ClassVar[UpdateCoSketchUserResult]
    UpdateCoSketchUserDuplicatedName: _ClassVar[UpdateCoSketchUserResult]

class PresetMessage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PresetMessageUnknown: _ClassVar[PresetMessage]
    PresetMessageHandUp: _ClassVar[PresetMessage]
    PresetMessageHandDown: _ClassVar[PresetMessage]

class GetMissingMessageResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetMissingMessageResultUnknown: _ClassVar[GetMissingMessageResult]
    GetMissingMessageResultOK: _ClassVar[GetMissingMessageResult]
    GetMissingMessageResultMissing: _ClassVar[GetMissingMessageResult]
    GetMissingMessageResultExceeding: _ClassVar[GetMissingMessageResult]

class ConvertToSubDResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ConvertToSubDResultUnknown: _ClassVar[ConvertToSubDResult]
    ConvertToSubDResultSuccess: _ClassVar[ConvertToSubDResult]
    ConvertToSubDResultStrokeOutOfSync: _ClassVar[ConvertToSubDResult]

class MergeSubDObjectsResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MergeSubDObjectsResultUnknown: _ClassVar[MergeSubDObjectsResult]
    MergeSubDObjectsResultSuccess: _ClassVar[MergeSubDObjectsResult]
    MergeSubDObjectsStrokeOutOfSync: _ClassVar[MergeSubDObjectsResult]

class UpdateSectionViewResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateSectionViewUnknown: _ClassVar[UpdateSectionViewResult]
    UpdateSectionViewSuccess: _ClassVar[UpdateSectionViewResult]
    UpdateSectionViewFailed: _ClassVar[UpdateSectionViewResult]
NoError: RpcErrorCode
Unknown: RpcErrorCode
RejoinRoom: RpcErrorCode
ServerError: RpcErrorCode
MultiJoinError: RpcErrorCode
ActorIsCreating: RpcErrorCode
ActorCreationError: RpcErrorCode
RoomNotExist: RpcErrorCode
ActorAskTimeout: RpcErrorCode
RpcTypeNotFound: RpcErrorCode
RoomIdMissing: RpcErrorCode
ClientIdMissing: RpcErrorCode
InvalidTicket: RpcErrorCode
UserIdMissing: RpcErrorCode
RoomIsFull: RpcErrorCode
RoomIsLocked: RpcErrorCode
ExpiredTicket: RpcErrorCode
ExpiredTCPChannel: RpcErrorCode
DuplicatedRpc: RpcErrorCode
DiscardedRpc: RpcErrorCode
UnknownType: RpcType
ConnHandshake: RpcType
JoinRoom: RpcType
LeaveRoom: RpcType
HeartBeat: RpcType
SketchAction: RpcType
PollSketch: RpcType
PollFinalSketches: RpcType
SyncFinalSketches: RpcType
SyncFinalGroups: RpcType
AddLayer: RpcType
DeleteLayer: RpcType
GetLayer: RpcType
ModifyLayer: RpcType
PreviewLayer: RpcType
ChangeStrokeLayer: RpcType
PlaceDeleteLayerLock: RpcType
CancelDeleteLayerLock: RpcType
ModifyLayerGroup: RpcType
GroupingObjects: RpcType
UnGroupingObjects: RpcType
AddImportedGroup: RpcType
CreateDuplicatedGroups: RpcType
ConvertToSubD: RpcType
ReverseSubDConversion: RpcType
MergeSubDObjects: RpcType
UpdateMaterial: RpcType
PreviewMaterial: RpcType
SyncTransform: RpcType
SyncUserState: RpcType
AssetsReady: RpcType
ChangeRoomCoordinator: RpcType
ChangeEnvironment: RpcType
SyncRoomExtraData: RpcType
LockWholeRoom: RpcType
UpdateCoSketchUser: RpcType
RequestToFollow: RpcType
UpdateSectionView: RpcType
PreviewIncrementalData: RpcType
ConfirmIncrementalData: RpcType
GetMissingConfirmIncrementalData: RpcType
RepairSubD: RpcType
SubmitSketchStateChanges: RpcType
ClientRelayData: RpcType
ListPlayers: RpcType
BroadcastRelayData: RpcType
SyncUI: RpcType
SendMessageBroadcast: RpcType
GetMissingMessage: RpcType
SyncUserPreferences: RpcType
SyncUserDefaults: RpcType
AuthorizeJoiner: RpcType
SketchStateChange: RpcType
ServerPush: RpcType
SingleSketchObjectChangeTypeUnset: SingleSketchObjectChangeType
SingleSketchObjectChangeTypeCreate: SingleSketchObjectChangeType
SingleSketchObjectChangeTypeUpdate: SingleSketchObjectChangeType
SingleSketchObjectChangeTypeDelete: SingleSketchObjectChangeType
Success: CollaborationResult
NoPermission: CollaborationResult
StrokeActionSuccess: StrokeActionResult
StrokeRevisionOutOfDate: StrokeActionResult
StrokeLayerNotExists: StrokeActionResult
SeqIdOutOfDate: StrokeActionResult
StrokeDeleted: StrokeActionResult
StrokeUsedByOthers: StrokeActionResult
StrokeMissingLayerId: StrokeActionResult
StrokeMissingMaterial: StrokeActionResult
OutOfDateStroke: StrokeActionResult
MissingFinalStroke: StrokeActionResult
DataIntegrityError: StrokeActionResult
TolerableEdgeCase: StrokeActionResult
LayerActionSuccess: LayerActionResult
LayerRevisionOutOfDate: LayerActionResult
NotLayerOwner: LayerActionResult
LayerSettingReject: LayerActionResult
NewLayerIdExists: LayerActionResult
LayerNotExists: LayerActionResult
LayerInUse: LayerActionResult
LayerClientIDIsMissing: LayerActionResult
PlaceLayerLockUnknown: PlaceDeleteLayerLockResult
PlaceLayerLockSuccess: PlaceDeleteLayerLockResult
PlaceLayerLockHashFailure: PlaceDeleteLayerLockResult
PlaceLayerLockUnknownFailure: PlaceDeleteLayerLockResult
PlaceLayerLockStrokeFailure: PlaceDeleteLayerLockResult
ModifyLayerGroupUnknown: ModifyLayerGroupResult
ModifyLayerGroupSuccess: ModifyLayerGroupResult
ModifyLayerGroupBadClientRequest: ModifyLayerGroupResult
Color: PreviewType
MaterialType: PreviewType
Guid: PreviewType
AlphaTransparency: PreviewType
ResetMaterial: PreviewType
TextureTransform: PreviewType
Roughness: PreviewType
Metallic: PreviewType
HueShift: PreviewType
ShadowSoftness: PreviewType
OutlineWidth: PreviewType
OutlineColor: PreviewType
ConfirmIncrementalUnknown: ConfirmIncrementalResult
ConfirmIncrementalSuccess: ConfirmIncrementalResult
ConfirmIncrementalStrokeMissing: ConfirmIncrementalResult
ConfirmIncrementalStrokeDeleted: ConfirmIncrementalResult
ConfirmIncrementalStrokeNotLocked: ConfirmIncrementalResult
RepairSubDResultUnknown: RepairSubDResult
RepairSubDResultSuccess: RepairSubDResult
RepairSubDCorruptObjectMissing: RepairSubDResult
RepairSubDCorruptObjectAlreadyRepaired: RepairSubDResult
LockWholeRoomUnknown: LockWholeRoomResult
LockWholeRoomSuccess: LockWholeRoomResult
LockWholeRoomNoPermission: LockWholeRoomResult
UpdateCoSketchUserUnknown: UpdateCoSketchUserResult
UpdateCoSketchUserSuccess: UpdateCoSketchUserResult
UpdateCoSketchUserInvalidName: UpdateCoSketchUserResult
UpdateCoSketchUserDuplicatedName: UpdateCoSketchUserResult
PresetMessageUnknown: PresetMessage
PresetMessageHandUp: PresetMessage
PresetMessageHandDown: PresetMessage
GetMissingMessageResultUnknown: GetMissingMessageResult
GetMissingMessageResultOK: GetMissingMessageResult
GetMissingMessageResultMissing: GetMissingMessageResult
GetMissingMessageResultExceeding: GetMissingMessageResult
ConvertToSubDResultUnknown: ConvertToSubDResult
ConvertToSubDResultSuccess: ConvertToSubDResult
ConvertToSubDResultStrokeOutOfSync: ConvertToSubDResult
MergeSubDObjectsResultUnknown: MergeSubDObjectsResult
MergeSubDObjectsResultSuccess: MergeSubDObjectsResult
MergeSubDObjectsStrokeOutOfSync: MergeSubDObjectsResult
UpdateSectionViewUnknown: UpdateSectionViewResult
UpdateSectionViewSuccess: UpdateSectionViewResult
UpdateSectionViewFailed: UpdateSectionViewResult

class ClientSessionState(_message.Message):
    __slots__ = ("userPreference", "components", "userState", "uiStates")
    class ComponentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SyncTransformBroadcast
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SyncTransformBroadcast, _Mapping]] = ...) -> None: ...
    class UiStatesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    USERPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    USERSTATE_FIELD_NUMBER: _ClassVar[int]
    UISTATES_FIELD_NUMBER: _ClassVar[int]
    userPreference: _preferences_pb2.UserSavedPreferencesTO
    components: _containers.MessageMap[str, SyncTransformBroadcast]
    userState: _sketch_model_pb2.CoSketchUserState
    uiStates: _containers.ScalarMap[str, bytes]
    def __init__(self, userPreference: _Optional[_Union[_preferences_pb2.UserSavedPreferencesTO, _Mapping]] = ..., components: _Optional[_Mapping[str, SyncTransformBroadcast]] = ..., userState: _Optional[_Union[_sketch_model_pb2.CoSketchUserState, _Mapping]] = ..., uiStates: _Optional[_Mapping[str, bytes]] = ...) -> None: ...

class RpcRequest(_message.Message):
    __slots__ = ("requestType", "rpcId", "ticket", "connectionID", "requestSendTime", "updatedEntityID", "authenticatedSenderId", "lastReceiveTime", "retryCount", "joinRoomRequest", "sketchActionRequest", "pollSketchRequest", "pollFinalSketchesRequest", "syncFinalSketchesRequest", "syncFinalGroupsRequest", "addLayerRequest", "deleteLayerRequest", "getLayerRequest", "modifyLayerRequest", "previewLayerRequest", "changeLayerRequest", "placeDeleteLayerLockRequest", "cancelDeleteLayerLockRequest", "modifyLayerGroupRequest", "groupingObjectsRequest", "unGroupObjectsRequest", "addImportedGroupRequest", "CreateDuplicatedGroupsRequest", "convertToSubDRequest", "reverseSubDConversionRequest", "mergeSubDObjectsRequest", "updateMaterialRequest", "previewMaterialBroadcast", "syncTransformBroadcast", "userStateBroadcast", "assetsReadyRequest", "changeCoordinatorBroadcast", "changeEnvironmentBroadcast", "syncRoomExtraDataRequest", "lockWholeRoomRequest", "updateCoSketchUserRequest", "requestToFollowRequest", "updateSectionViewRequest", "previewIncrementalDataRequest", "confirmIncrementalDataRequest", "getMissingConfirmIncrementalDataRequest", "repairSubDRequest", "submitSketchStateChangesRequest", "relayData", "listPlayersRequest", "syncUIBroadcast", "messageBroadcast", "getMissingMessageRequest", "syncUserPreferencesBroadcast", "syncUserDefaultsBroadcast", "authorizeJoinerRequest")
    REQUESTTYPE_FIELD_NUMBER: _ClassVar[int]
    RPCID_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONID_FIELD_NUMBER: _ClassVar[int]
    REQUESTSENDTIME_FIELD_NUMBER: _ClassVar[int]
    UPDATEDENTITYID_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATEDSENDERID_FIELD_NUMBER: _ClassVar[int]
    LASTRECEIVETIME_FIELD_NUMBER: _ClassVar[int]
    RETRYCOUNT_FIELD_NUMBER: _ClassVar[int]
    JOINROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    SKETCHACTIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    POLLSKETCHREQUEST_FIELD_NUMBER: _ClassVar[int]
    POLLFINALSKETCHESREQUEST_FIELD_NUMBER: _ClassVar[int]
    SYNCFINALSKETCHESREQUEST_FIELD_NUMBER: _ClassVar[int]
    SYNCFINALGROUPSREQUEST_FIELD_NUMBER: _ClassVar[int]
    ADDLAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETELAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETLAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    PREVIEWLAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGELAYERREQUEST_FIELD_NUMBER: _ClassVar[int]
    PLACEDELETELAYERLOCKREQUEST_FIELD_NUMBER: _ClassVar[int]
    CANCELDELETELAYERLOCKREQUEST_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERGROUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    GROUPINGOBJECTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    UNGROUPOBJECTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    ADDIMPORTEDGROUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEDUPLICATEDGROUPSREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONVERTTOSUBDREQUEST_FIELD_NUMBER: _ClassVar[int]
    REVERSESUBDCONVERSIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    MERGESUBDOBJECTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEMATERIALREQUEST_FIELD_NUMBER: _ClassVar[int]
    PREVIEWMATERIALBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SYNCTRANSFORMBROADCAST_FIELD_NUMBER: _ClassVar[int]
    USERSTATEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    ASSETSREADYREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGECOORDINATORBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGEENVIRONMENTBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SYNCROOMEXTRADATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    LOCKWHOLEROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATECOSKETCHUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUESTTOFOLLOWREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATESECTIONVIEWREQUEST_FIELD_NUMBER: _ClassVar[int]
    PREVIEWINCREMENTALDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONFIRMINCREMENTALDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETMISSINGCONFIRMINCREMENTALDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    REPAIRSUBDREQUEST_FIELD_NUMBER: _ClassVar[int]
    SUBMITSKETCHSTATECHANGESREQUEST_FIELD_NUMBER: _ClassVar[int]
    RELAYDATA_FIELD_NUMBER: _ClassVar[int]
    LISTPLAYERSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SYNCUIBROADCAST_FIELD_NUMBER: _ClassVar[int]
    MESSAGEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    GETMISSINGMESSAGEREQUEST_FIELD_NUMBER: _ClassVar[int]
    SYNCUSERPREFERENCESBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SYNCUSERDEFAULTSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZEJOINERREQUEST_FIELD_NUMBER: _ClassVar[int]
    requestType: RpcType
    rpcId: int
    ticket: _gravi_model_pb2.CoSketchTicket
    connectionID: str
    requestSendTime: int
    updatedEntityID: int
    authenticatedSenderId: int
    lastReceiveTime: int
    retryCount: int
    joinRoomRequest: JoinRoomRequest
    sketchActionRequest: SketchActionRequest
    pollSketchRequest: PollSketchRequest
    pollFinalSketchesRequest: PollFinalSketchesRequest
    syncFinalSketchesRequest: SyncFinalSketchesRequest
    syncFinalGroupsRequest: SyncFinalGroupsRequest
    addLayerRequest: AddLayerRequest
    deleteLayerRequest: DeleteLayerRequest
    getLayerRequest: GetLayerRequest
    modifyLayerRequest: ModifyLayerRequest
    previewLayerRequest: PreviewLayerBroadcast
    changeLayerRequest: ChangeLayerRequest
    placeDeleteLayerLockRequest: PlaceDeleteLayerLockRequest
    cancelDeleteLayerLockRequest: CancelDeleteLayerLockRequest
    modifyLayerGroupRequest: ModifyLayerGroupRequest
    groupingObjectsRequest: GroupingObjectsRequest
    unGroupObjectsRequest: UnGroupObjectsRequest
    addImportedGroupRequest: AddImportedGroupRequest
    CreateDuplicatedGroupsRequest: CreateDuplicatedGroupsRequest
    convertToSubDRequest: ConvertToSubDRequest
    reverseSubDConversionRequest: ReverseSubDConversionRequest
    mergeSubDObjectsRequest: MergeSubDObjectsRequest
    updateMaterialRequest: UpdateMaterialRequest
    previewMaterialBroadcast: PreviewMaterialBroadcast
    syncTransformBroadcast: SyncTransformBroadcast
    userStateBroadcast: UserStateBroadcast
    assetsReadyRequest: AssetsReadyRequest
    changeCoordinatorBroadcast: ChangeCoordinatorBroadcast
    changeEnvironmentBroadcast: ChangeEnvironmentBroadcast
    syncRoomExtraDataRequest: SyncRoomExtraDataRequest
    lockWholeRoomRequest: LockWholeRoomRequest
    updateCoSketchUserRequest: UpdateCoSketchUserRequest
    requestToFollowRequest: RequestToFollowRequest
    updateSectionViewRequest: UpdateSectionViewRequest
    previewIncrementalDataRequest: PreviewIncrementalDataRequest
    confirmIncrementalDataRequest: ConfirmIncrementalDataRequest
    getMissingConfirmIncrementalDataRequest: GetMissingConfirmIncrementalDataRequest
    repairSubDRequest: RepairSubDRequest
    submitSketchStateChangesRequest: SubmitSketchStateChangesRequest
    relayData: RelayData
    listPlayersRequest: ListPlayersRequest
    syncUIBroadcast: SyncUIBroadcast
    messageBroadcast: MessageBroadcast
    getMissingMessageRequest: GetMissingMessageRequest
    syncUserPreferencesBroadcast: SyncUserPreferencesBroadcast
    syncUserDefaultsBroadcast: SyncUserDefaultsBroadcast
    authorizeJoinerRequest: AuthorizeJoinerRequest
    def __init__(self, requestType: _Optional[_Union[RpcType, str]] = ..., rpcId: _Optional[int] = ..., ticket: _Optional[_Union[_gravi_model_pb2.CoSketchTicket, _Mapping]] = ..., connectionID: _Optional[str] = ..., requestSendTime: _Optional[int] = ..., updatedEntityID: _Optional[int] = ..., authenticatedSenderId: _Optional[int] = ..., lastReceiveTime: _Optional[int] = ..., retryCount: _Optional[int] = ..., joinRoomRequest: _Optional[_Union[JoinRoomRequest, _Mapping]] = ..., sketchActionRequest: _Optional[_Union[SketchActionRequest, _Mapping]] = ..., pollSketchRequest: _Optional[_Union[PollSketchRequest, _Mapping]] = ..., pollFinalSketchesRequest: _Optional[_Union[PollFinalSketchesRequest, _Mapping]] = ..., syncFinalSketchesRequest: _Optional[_Union[SyncFinalSketchesRequest, _Mapping]] = ..., syncFinalGroupsRequest: _Optional[_Union[SyncFinalGroupsRequest, _Mapping]] = ..., addLayerRequest: _Optional[_Union[AddLayerRequest, _Mapping]] = ..., deleteLayerRequest: _Optional[_Union[DeleteLayerRequest, _Mapping]] = ..., getLayerRequest: _Optional[_Union[GetLayerRequest, _Mapping]] = ..., modifyLayerRequest: _Optional[_Union[ModifyLayerRequest, _Mapping]] = ..., previewLayerRequest: _Optional[_Union[PreviewLayerBroadcast, _Mapping]] = ..., changeLayerRequest: _Optional[_Union[ChangeLayerRequest, _Mapping]] = ..., placeDeleteLayerLockRequest: _Optional[_Union[PlaceDeleteLayerLockRequest, _Mapping]] = ..., cancelDeleteLayerLockRequest: _Optional[_Union[CancelDeleteLayerLockRequest, _Mapping]] = ..., modifyLayerGroupRequest: _Optional[_Union[ModifyLayerGroupRequest, _Mapping]] = ..., groupingObjectsRequest: _Optional[_Union[GroupingObjectsRequest, _Mapping]] = ..., unGroupObjectsRequest: _Optional[_Union[UnGroupObjectsRequest, _Mapping]] = ..., addImportedGroupRequest: _Optional[_Union[AddImportedGroupRequest, _Mapping]] = ..., CreateDuplicatedGroupsRequest: _Optional[_Union[CreateDuplicatedGroupsRequest, _Mapping]] = ..., convertToSubDRequest: _Optional[_Union[ConvertToSubDRequest, _Mapping]] = ..., reverseSubDConversionRequest: _Optional[_Union[ReverseSubDConversionRequest, _Mapping]] = ..., mergeSubDObjectsRequest: _Optional[_Union[MergeSubDObjectsRequest, _Mapping]] = ..., updateMaterialRequest: _Optional[_Union[UpdateMaterialRequest, _Mapping]] = ..., previewMaterialBroadcast: _Optional[_Union[PreviewMaterialBroadcast, _Mapping]] = ..., syncTransformBroadcast: _Optional[_Union[SyncTransformBroadcast, _Mapping]] = ..., userStateBroadcast: _Optional[_Union[UserStateBroadcast, _Mapping]] = ..., assetsReadyRequest: _Optional[_Union[AssetsReadyRequest, _Mapping]] = ..., changeCoordinatorBroadcast: _Optional[_Union[ChangeCoordinatorBroadcast, _Mapping]] = ..., changeEnvironmentBroadcast: _Optional[_Union[ChangeEnvironmentBroadcast, _Mapping]] = ..., syncRoomExtraDataRequest: _Optional[_Union[SyncRoomExtraDataRequest, _Mapping]] = ..., lockWholeRoomRequest: _Optional[_Union[LockWholeRoomRequest, _Mapping]] = ..., updateCoSketchUserRequest: _Optional[_Union[UpdateCoSketchUserRequest, _Mapping]] = ..., requestToFollowRequest: _Optional[_Union[RequestToFollowRequest, _Mapping]] = ..., updateSectionViewRequest: _Optional[_Union[UpdateSectionViewRequest, _Mapping]] = ..., previewIncrementalDataRequest: _Optional[_Union[PreviewIncrementalDataRequest, _Mapping]] = ..., confirmIncrementalDataRequest: _Optional[_Union[ConfirmIncrementalDataRequest, _Mapping]] = ..., getMissingConfirmIncrementalDataRequest: _Optional[_Union[GetMissingConfirmIncrementalDataRequest, _Mapping]] = ..., repairSubDRequest: _Optional[_Union[RepairSubDRequest, _Mapping]] = ..., submitSketchStateChangesRequest: _Optional[_Union[SubmitSketchStateChangesRequest, _Mapping]] = ..., relayData: _Optional[_Union[RelayData, _Mapping]] = ..., listPlayersRequest: _Optional[_Union[ListPlayersRequest, _Mapping]] = ..., syncUIBroadcast: _Optional[_Union[SyncUIBroadcast, _Mapping]] = ..., messageBroadcast: _Optional[_Union[MessageBroadcast, _Mapping]] = ..., getMissingMessageRequest: _Optional[_Union[GetMissingMessageRequest, _Mapping]] = ..., syncUserPreferencesBroadcast: _Optional[_Union[SyncUserPreferencesBroadcast, _Mapping]] = ..., syncUserDefaultsBroadcast: _Optional[_Union[SyncUserDefaultsBroadcast, _Mapping]] = ..., authorizeJoinerRequest: _Optional[_Union[AuthorizeJoinerRequest, _Mapping]] = ...) -> None: ...

class SubmitSketchStateChangesRequest(_message.Message):
    __slots__ = ("changes",)
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    changes: _containers.RepeatedCompositeFieldContainer[SingleSketchObjectChange]
    def __init__(self, changes: _Optional[_Iterable[_Union[SingleSketchObjectChange, _Mapping]]] = ...) -> None: ...

class SubmitSketchStateChangesResponse(_message.Message):
    __slots__ = ("isAccepted", "latestObjects")
    ISACCEPTED_FIELD_NUMBER: _ClassVar[int]
    LATESTOBJECTS_FIELD_NUMBER: _ClassVar[int]
    isAccepted: bool
    latestObjects: _containers.RepeatedCompositeFieldContainer[SketchObject]
    def __init__(self, isAccepted: bool = ..., latestObjects: _Optional[_Iterable[_Union[SketchObject, _Mapping]]] = ...) -> None: ...

class SingleSketchObjectChange(_message.Message):
    __slots__ = ("parentRevisionId", "type", "object")
    PARENTREVISIONID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    parentRevisionId: int
    type: SingleSketchObjectChangeType
    object: SketchObject
    def __init__(self, parentRevisionId: _Optional[int] = ..., type: _Optional[_Union[SingleSketchObjectChangeType, str]] = ..., object: _Optional[_Union[SketchObject, _Mapping]] = ...) -> None: ...

class SketchObject(_message.Message):
    __slots__ = ("id", "revisionId", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    revisionId: int
    metadata: _metadata_pb2.SketchMetadataModel
    def __init__(self, id: _Optional[str] = ..., revisionId: _Optional[int] = ..., metadata: _Optional[_Union[_metadata_pb2.SketchMetadataModel, _Mapping]] = ...) -> None: ...

class RpcResponse(_message.Message):
    __slots__ = ("rpcType", "rpcId", "errorCode", "timestamp", "broadcast", "fromClientId", "requestSendTime", "joinRoomResponse", "joinRoomBroadcast", "leaveRoomBroadcast", "sketchActionResponse", "sketchActionBroadcast", "pollSketchResponse", "pollFinalSketchesResponse", "syncFinalSketchesResponse", "syncFinalGroupsResponse", "addLayerBroadcast", "addLayerResponse", "deleteLayerBroadcast", "deleteLayerResponse", "getLayerResponse", "modifyLayerResponse", "previewLayerBroadcast", "changeLayerBroadcast", "changeLayerResponse", "importLayersResponse", "placeDeleteLayerLockResponse", "placeDeleteLayerLockBroadcast", "cancelDeleteLayerLockResponse", "cancelDeleteLayerLockBroadcast", "modifyLayerGroupResponse", "modifyLayerGroupBroadcast", "groupingObjectsBroadcast", "groupingObjectsResponse", "unGroupObjectsBroadcast", "unGroupObjectsResponse", "addImportedGroupBroadcast", "CreateDuplicatedGroupsBroadcast", "CreateDuplicatedGroupsResponse", "convertToSubDResponse", "convertToSubDBroadcast", "reverseSubDConversionResponse", "reverseSubDConversionBroadcast", "mergeSubDObjectsResponse", "mergeSubDObjectsBroadcast", "updateMaterialBroadcast", "previewMaterialBroadcast", "syncTransformBroadcast", "userStateBroadcast", "assetsReadyBroadcast", "changeCoordinatorBroadcast", "changeCoordinatorResponse", "changeEnvironmentBroadcast", "changeEnvironmentResponse", "syncRoomExtraDataResponse", "lockWholeRoomResponse", "LockWholeRoomBroadcast", "updateCoSketchUserResponse", "updateCoSketchUserBroadcast", "updateSectionViewResponse", "updateSectionViewBroadcast", "previewIncrementalDataBroadcast", "confirmIncrementalDataBroadcast", "getMissingConfirmIncrementalDataResponse", "confirmIncrementalDataResponse", "repairSubDBroadcast", "repairSubDResponse", "submitSketchStateChangesResponse", "relayData", "listPlayersResponse", "syncUIBroadcast", "messageBroadcast", "messageBroadcastResponse", "getMissingMessageResponse", "syncUserPreferencesBroadcast", "syncUserDefaultsBroadcast", "authorizeJoinerBroadcast", "sketchStateChangeBroadcast", "serverPushBroadcast")
    RPCTYPE_FIELD_NUMBER: _ClassVar[int]
    RPCID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    FROMCLIENTID_FIELD_NUMBER: _ClassVar[int]
    REQUESTSENDTIME_FIELD_NUMBER: _ClassVar[int]
    JOINROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    JOINROOMBROADCAST_FIELD_NUMBER: _ClassVar[int]
    LEAVEROOMBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SKETCHACTIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SKETCHACTIONBROADCAST_FIELD_NUMBER: _ClassVar[int]
    POLLSKETCHRESPONSE_FIELD_NUMBER: _ClassVar[int]
    POLLFINALSKETCHESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCFINALSKETCHESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCFINALGROUPSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ADDLAYERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    ADDLAYERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETELAYERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    DELETELAYERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETLAYERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    PREVIEWLAYERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGELAYERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGELAYERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    IMPORTLAYERSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    PLACEDELETELAYERLOCKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    PLACEDELETELAYERLOCKBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CANCELDELETELAYERLOCKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CANCELDELETELAYERLOCKBROADCAST_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERGROUPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERGROUPBROADCAST_FIELD_NUMBER: _ClassVar[int]
    GROUPINGOBJECTSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    GROUPINGOBJECTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UNGROUPOBJECTSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    UNGROUPOBJECTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ADDIMPORTEDGROUPBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CREATEDUPLICATEDGROUPSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CREATEDUPLICATEDGROUPSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONVERTTOSUBDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONVERTTOSUBDBROADCAST_FIELD_NUMBER: _ClassVar[int]
    REVERSESUBDCONVERSIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REVERSESUBDCONVERSIONBROADCAST_FIELD_NUMBER: _ClassVar[int]
    MERGESUBDOBJECTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MERGESUBDOBJECTSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    UPDATEMATERIALBROADCAST_FIELD_NUMBER: _ClassVar[int]
    PREVIEWMATERIALBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SYNCTRANSFORMBROADCAST_FIELD_NUMBER: _ClassVar[int]
    USERSTATEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    ASSETSREADYBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGECOORDINATORBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGECOORDINATORRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANGEENVIRONMENTBROADCAST_FIELD_NUMBER: _ClassVar[int]
    CHANGEENVIRONMENTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCROOMEXTRADATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    LOCKWHOLEROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LOCKWHOLEROOMBROADCAST_FIELD_NUMBER: _ClassVar[int]
    UPDATECOSKETCHUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATECOSKETCHUSERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    UPDATESECTIONVIEWRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATESECTIONVIEWBROADCAST_FIELD_NUMBER: _ClassVar[int]
    PREVIEWINCREMENTALDATABROADCAST_FIELD_NUMBER: _ClassVar[int]
    CONFIRMINCREMENTALDATABROADCAST_FIELD_NUMBER: _ClassVar[int]
    GETMISSINGCONFIRMINCREMENTALDATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONFIRMINCREMENTALDATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    REPAIRSUBDBROADCAST_FIELD_NUMBER: _ClassVar[int]
    REPAIRSUBDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SUBMITSKETCHSTATECHANGESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    RELAYDATA_FIELD_NUMBER: _ClassVar[int]
    LISTPLAYERSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCUIBROADCAST_FIELD_NUMBER: _ClassVar[int]
    MESSAGEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    MESSAGEBROADCASTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETMISSINGMESSAGERESPONSE_FIELD_NUMBER: _ClassVar[int]
    SYNCUSERPREFERENCESBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SYNCUSERDEFAULTSBROADCAST_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZEJOINERBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SKETCHSTATECHANGEBROADCAST_FIELD_NUMBER: _ClassVar[int]
    SERVERPUSHBROADCAST_FIELD_NUMBER: _ClassVar[int]
    rpcType: RpcType
    rpcId: int
    errorCode: RpcErrorCode
    timestamp: int
    broadcast: bool
    fromClientId: int
    requestSendTime: int
    joinRoomResponse: JoinRoomResponse
    joinRoomBroadcast: JoinRoomBroadcast
    leaveRoomBroadcast: LeaveRoomBroadcast
    sketchActionResponse: SketchActionResponse
    sketchActionBroadcast: SketchActionRequest
    pollSketchResponse: PollSketchResponse
    pollFinalSketchesResponse: PollFinalSketchesResponse
    syncFinalSketchesResponse: SyncFinalSketchesResponse
    syncFinalGroupsResponse: SyncFinalGroupsResponse
    addLayerBroadcast: AddLayerBroadcast
    addLayerResponse: AddLayerResponse
    deleteLayerBroadcast: DeleteLayerRequest
    deleteLayerResponse: DeleteLayerResponse
    getLayerResponse: GetLayerResponse
    modifyLayerResponse: ModifyLayerResponse
    previewLayerBroadcast: PreviewLayerBroadcast
    changeLayerBroadcast: ChangeLayerBroadcast
    changeLayerResponse: ChangeLayerResponse
    importLayersResponse: ImportLayersResponse
    placeDeleteLayerLockResponse: PlaceDeleteLayerLockResponse
    placeDeleteLayerLockBroadcast: PlaceDeleteLayerLockRequest
    cancelDeleteLayerLockResponse: CancelDeleteLayerLockResponse
    cancelDeleteLayerLockBroadcast: CancelDeleteLayerLockRequest
    modifyLayerGroupResponse: ModifyLayerGroupResponse
    modifyLayerGroupBroadcast: ModifyLayerGroupRequest
    groupingObjectsBroadcast: GroupingObjectsRequest
    groupingObjectsResponse: GroupResponse
    unGroupObjectsBroadcast: UnGroupObjectsRequest
    unGroupObjectsResponse: GroupResponse
    addImportedGroupBroadcast: AddImportedGroupRequest
    CreateDuplicatedGroupsBroadcast: CreateDuplicatedGroupsRequest
    CreateDuplicatedGroupsResponse: GroupResponse
    convertToSubDResponse: ConvertToSubDResponse
    convertToSubDBroadcast: ConvertToSubDRequest
    reverseSubDConversionResponse: ReverseSubDConversionResponse
    reverseSubDConversionBroadcast: ReverseSubDConversionRequest
    mergeSubDObjectsResponse: MergeSubDObjectsResponse
    mergeSubDObjectsBroadcast: MergeSubDObjectsRequest
    updateMaterialBroadcast: UpdateMaterialBroadcast
    previewMaterialBroadcast: PreviewMaterialBroadcast
    syncTransformBroadcast: SyncTransformBroadcast
    userStateBroadcast: UserStateBroadcast
    assetsReadyBroadcast: AssetsReadyBroadcast
    changeCoordinatorBroadcast: ChangeCoordinatorBroadcast
    changeCoordinatorResponse: ChangeCoordinatorResponse
    changeEnvironmentBroadcast: ChangeEnvironmentBroadcast
    changeEnvironmentResponse: ChangeEnvironmentResponse
    syncRoomExtraDataResponse: SyncRoomExtraDataResponse
    lockWholeRoomResponse: LockWholeRoomResponse
    LockWholeRoomBroadcast: LockWholeRoomRequest
    updateCoSketchUserResponse: UpdateCoSketchUserResponse
    updateCoSketchUserBroadcast: UpdateCoSketchUserRequest
    updateSectionViewResponse: UpdateSectionViewResponse
    updateSectionViewBroadcast: UpdateSectionViewRequest
    previewIncrementalDataBroadcast: PreviewIncrementalDataBroadcast
    confirmIncrementalDataBroadcast: ConfirmIncrementalDataBroadcast
    getMissingConfirmIncrementalDataResponse: GetMissingConfirmIncrementalDataResponse
    confirmIncrementalDataResponse: ConfirmIncrementalDataResponse
    repairSubDBroadcast: RepairSubDBroadcast
    repairSubDResponse: RepairSubDResponse
    submitSketchStateChangesResponse: SubmitSketchStateChangesResponse
    relayData: RelayData
    listPlayersResponse: ListPlayersResponse
    syncUIBroadcast: SyncUIBroadcast
    messageBroadcast: MessageBroadcast
    messageBroadcastResponse: MessageBroadcastResponse
    getMissingMessageResponse: GetMissingMessageResponse
    syncUserPreferencesBroadcast: SyncUserPreferencesBroadcast
    syncUserDefaultsBroadcast: SyncUserDefaultsBroadcast
    authorizeJoinerBroadcast: AuthorizeJoinerRequest
    sketchStateChangeBroadcast: SketchStateChangeBroadcast
    serverPushBroadcast: _containers.RepeatedCompositeFieldContainer[_cosketch_serverpush_pb2.ServerPushBroadcast]
    def __init__(self, rpcType: _Optional[_Union[RpcType, str]] = ..., rpcId: _Optional[int] = ..., errorCode: _Optional[_Union[RpcErrorCode, str]] = ..., timestamp: _Optional[int] = ..., broadcast: bool = ..., fromClientId: _Optional[int] = ..., requestSendTime: _Optional[int] = ..., joinRoomResponse: _Optional[_Union[JoinRoomResponse, _Mapping]] = ..., joinRoomBroadcast: _Optional[_Union[JoinRoomBroadcast, _Mapping]] = ..., leaveRoomBroadcast: _Optional[_Union[LeaveRoomBroadcast, _Mapping]] = ..., sketchActionResponse: _Optional[_Union[SketchActionResponse, _Mapping]] = ..., sketchActionBroadcast: _Optional[_Union[SketchActionRequest, _Mapping]] = ..., pollSketchResponse: _Optional[_Union[PollSketchResponse, _Mapping]] = ..., pollFinalSketchesResponse: _Optional[_Union[PollFinalSketchesResponse, _Mapping]] = ..., syncFinalSketchesResponse: _Optional[_Union[SyncFinalSketchesResponse, _Mapping]] = ..., syncFinalGroupsResponse: _Optional[_Union[SyncFinalGroupsResponse, _Mapping]] = ..., addLayerBroadcast: _Optional[_Union[AddLayerBroadcast, _Mapping]] = ..., addLayerResponse: _Optional[_Union[AddLayerResponse, _Mapping]] = ..., deleteLayerBroadcast: _Optional[_Union[DeleteLayerRequest, _Mapping]] = ..., deleteLayerResponse: _Optional[_Union[DeleteLayerResponse, _Mapping]] = ..., getLayerResponse: _Optional[_Union[GetLayerResponse, _Mapping]] = ..., modifyLayerResponse: _Optional[_Union[ModifyLayerResponse, _Mapping]] = ..., previewLayerBroadcast: _Optional[_Union[PreviewLayerBroadcast, _Mapping]] = ..., changeLayerBroadcast: _Optional[_Union[ChangeLayerBroadcast, _Mapping]] = ..., changeLayerResponse: _Optional[_Union[ChangeLayerResponse, _Mapping]] = ..., importLayersResponse: _Optional[_Union[ImportLayersResponse, _Mapping]] = ..., placeDeleteLayerLockResponse: _Optional[_Union[PlaceDeleteLayerLockResponse, _Mapping]] = ..., placeDeleteLayerLockBroadcast: _Optional[_Union[PlaceDeleteLayerLockRequest, _Mapping]] = ..., cancelDeleteLayerLockResponse: _Optional[_Union[CancelDeleteLayerLockResponse, _Mapping]] = ..., cancelDeleteLayerLockBroadcast: _Optional[_Union[CancelDeleteLayerLockRequest, _Mapping]] = ..., modifyLayerGroupResponse: _Optional[_Union[ModifyLayerGroupResponse, _Mapping]] = ..., modifyLayerGroupBroadcast: _Optional[_Union[ModifyLayerGroupRequest, _Mapping]] = ..., groupingObjectsBroadcast: _Optional[_Union[GroupingObjectsRequest, _Mapping]] = ..., groupingObjectsResponse: _Optional[_Union[GroupResponse, _Mapping]] = ..., unGroupObjectsBroadcast: _Optional[_Union[UnGroupObjectsRequest, _Mapping]] = ..., unGroupObjectsResponse: _Optional[_Union[GroupResponse, _Mapping]] = ..., addImportedGroupBroadcast: _Optional[_Union[AddImportedGroupRequest, _Mapping]] = ..., CreateDuplicatedGroupsBroadcast: _Optional[_Union[CreateDuplicatedGroupsRequest, _Mapping]] = ..., CreateDuplicatedGroupsResponse: _Optional[_Union[GroupResponse, _Mapping]] = ..., convertToSubDResponse: _Optional[_Union[ConvertToSubDResponse, _Mapping]] = ..., convertToSubDBroadcast: _Optional[_Union[ConvertToSubDRequest, _Mapping]] = ..., reverseSubDConversionResponse: _Optional[_Union[ReverseSubDConversionResponse, _Mapping]] = ..., reverseSubDConversionBroadcast: _Optional[_Union[ReverseSubDConversionRequest, _Mapping]] = ..., mergeSubDObjectsResponse: _Optional[_Union[MergeSubDObjectsResponse, _Mapping]] = ..., mergeSubDObjectsBroadcast: _Optional[_Union[MergeSubDObjectsRequest, _Mapping]] = ..., updateMaterialBroadcast: _Optional[_Union[UpdateMaterialBroadcast, _Mapping]] = ..., previewMaterialBroadcast: _Optional[_Union[PreviewMaterialBroadcast, _Mapping]] = ..., syncTransformBroadcast: _Optional[_Union[SyncTransformBroadcast, _Mapping]] = ..., userStateBroadcast: _Optional[_Union[UserStateBroadcast, _Mapping]] = ..., assetsReadyBroadcast: _Optional[_Union[AssetsReadyBroadcast, _Mapping]] = ..., changeCoordinatorBroadcast: _Optional[_Union[ChangeCoordinatorBroadcast, _Mapping]] = ..., changeCoordinatorResponse: _Optional[_Union[ChangeCoordinatorResponse, _Mapping]] = ..., changeEnvironmentBroadcast: _Optional[_Union[ChangeEnvironmentBroadcast, _Mapping]] = ..., changeEnvironmentResponse: _Optional[_Union[ChangeEnvironmentResponse, _Mapping]] = ..., syncRoomExtraDataResponse: _Optional[_Union[SyncRoomExtraDataResponse, _Mapping]] = ..., lockWholeRoomResponse: _Optional[_Union[LockWholeRoomResponse, _Mapping]] = ..., LockWholeRoomBroadcast: _Optional[_Union[LockWholeRoomRequest, _Mapping]] = ..., updateCoSketchUserResponse: _Optional[_Union[UpdateCoSketchUserResponse, _Mapping]] = ..., updateCoSketchUserBroadcast: _Optional[_Union[UpdateCoSketchUserRequest, _Mapping]] = ..., updateSectionViewResponse: _Optional[_Union[UpdateSectionViewResponse, _Mapping]] = ..., updateSectionViewBroadcast: _Optional[_Union[UpdateSectionViewRequest, _Mapping]] = ..., previewIncrementalDataBroadcast: _Optional[_Union[PreviewIncrementalDataBroadcast, _Mapping]] = ..., confirmIncrementalDataBroadcast: _Optional[_Union[ConfirmIncrementalDataBroadcast, _Mapping]] = ..., getMissingConfirmIncrementalDataResponse: _Optional[_Union[GetMissingConfirmIncrementalDataResponse, _Mapping]] = ..., confirmIncrementalDataResponse: _Optional[_Union[ConfirmIncrementalDataResponse, _Mapping]] = ..., repairSubDBroadcast: _Optional[_Union[RepairSubDBroadcast, _Mapping]] = ..., repairSubDResponse: _Optional[_Union[RepairSubDResponse, _Mapping]] = ..., submitSketchStateChangesResponse: _Optional[_Union[SubmitSketchStateChangesResponse, _Mapping]] = ..., relayData: _Optional[_Union[RelayData, _Mapping]] = ..., listPlayersResponse: _Optional[_Union[ListPlayersResponse, _Mapping]] = ..., syncUIBroadcast: _Optional[_Union[SyncUIBroadcast, _Mapping]] = ..., messageBroadcast: _Optional[_Union[MessageBroadcast, _Mapping]] = ..., messageBroadcastResponse: _Optional[_Union[MessageBroadcastResponse, _Mapping]] = ..., getMissingMessageResponse: _Optional[_Union[GetMissingMessageResponse, _Mapping]] = ..., syncUserPreferencesBroadcast: _Optional[_Union[SyncUserPreferencesBroadcast, _Mapping]] = ..., syncUserDefaultsBroadcast: _Optional[_Union[SyncUserDefaultsBroadcast, _Mapping]] = ..., authorizeJoinerBroadcast: _Optional[_Union[AuthorizeJoinerRequest, _Mapping]] = ..., sketchStateChangeBroadcast: _Optional[_Union[SketchStateChangeBroadcast, _Mapping]] = ..., serverPushBroadcast: _Optional[_Iterable[_Union[_cosketch_serverpush_pb2.ServerPushBroadcast, _Mapping]]] = ...) -> None: ...

class SketchStateChangeBroadcast(_message.Message):
    __slots__ = ("globalRevisionId", "fromClientId", "objects")
    GLOBALREVISIONID_FIELD_NUMBER: _ClassVar[int]
    FROMCLIENTID_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    globalRevisionId: int
    fromClientId: int
    objects: _containers.RepeatedCompositeFieldContainer[SketchObject]
    def __init__(self, globalRevisionId: _Optional[int] = ..., fromClientId: _Optional[int] = ..., objects: _Optional[_Iterable[_Union[SketchObject, _Mapping]]] = ...) -> None: ...

class JoinRoomRequest(_message.Message):
    __slots__ = ("user", "joinRoomToken")
    USER_FIELD_NUMBER: _ClassVar[int]
    JOINROOMTOKEN_FIELD_NUMBER: _ClassVar[int]
    user: _sketch_model_pb2.CoSketchUser
    joinRoomToken: str
    def __init__(self, user: _Optional[_Union[_sketch_model_pb2.CoSketchUser, _Mapping]] = ..., joinRoomToken: _Optional[str] = ...) -> None: ...

class JoinRoomBroadcast(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _sketch_model_pb2.CoSketchUser
    def __init__(self, user: _Optional[_Union[_sketch_model_pb2.CoSketchUser, _Mapping]] = ...) -> None: ...

class JoinRoomResponse(_message.Message):
    __slots__ = ("others", "roomExtraData", "roomInMemoryStates", "otherUsersInitialTransforms", "spawnPoint")
    class OtherUsersInitialTransformsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: SyncTransformBroadcasts
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[SyncTransformBroadcasts, _Mapping]] = ...) -> None: ...
    OTHERS_FIELD_NUMBER: _ClassVar[int]
    ROOMEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    ROOMINMEMORYSTATES_FIELD_NUMBER: _ClassVar[int]
    OTHERUSERSINITIALTRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    SPAWNPOINT_FIELD_NUMBER: _ClassVar[int]
    others: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.CoSketchUser]
    roomExtraData: _sketch_model_pb2.CoSketchRoomExtraData
    roomInMemoryStates: RoomInMemoryStates
    otherUsersInitialTransforms: _containers.MessageMap[int, SyncTransformBroadcasts]
    spawnPoint: _sketch_model_pb2.StrokeActionData
    def __init__(self, others: _Optional[_Iterable[_Union[_sketch_model_pb2.CoSketchUser, _Mapping]]] = ..., roomExtraData: _Optional[_Union[_sketch_model_pb2.CoSketchRoomExtraData, _Mapping]] = ..., roomInMemoryStates: _Optional[_Union[RoomInMemoryStates, _Mapping]] = ..., otherUsersInitialTransforms: _Optional[_Mapping[int, SyncTransformBroadcasts]] = ..., spawnPoint: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ...) -> None: ...

class SyncTransformBroadcasts(_message.Message):
    __slots__ = ("transforms",)
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    transforms: _containers.RepeatedCompositeFieldContainer[SyncTransformBroadcast]
    def __init__(self, transforms: _Optional[_Iterable[_Union[SyncTransformBroadcast, _Mapping]]] = ...) -> None: ...

class LeaveRoomBroadcast(_message.Message):
    __slots__ = ("leaverUserId", "roomId", "leaverClientId")
    LEAVERUSERID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    LEAVERCLIENTID_FIELD_NUMBER: _ClassVar[int]
    leaverUserId: str
    roomId: str
    leaverClientId: int
    def __init__(self, leaverUserId: _Optional[str] = ..., roomId: _Optional[str] = ..., leaverClientId: _Optional[int] = ...) -> None: ...

class UserStateBroadcast(_message.Message):
    __slots__ = ("userState",)
    USERSTATE_FIELD_NUMBER: _ClassVar[int]
    userState: _sketch_model_pb2.CoSketchUserState
    def __init__(self, userState: _Optional[_Union[_sketch_model_pb2.CoSketchUserState, _Mapping]] = ...) -> None: ...

class SketchActionRequest(_message.Message):
    __slots__ = ("actionData", "mergedActions", "skipMeshUpdate")
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    MERGEDACTIONS_FIELD_NUMBER: _ClassVar[int]
    SKIPMESHUPDATE_FIELD_NUMBER: _ClassVar[int]
    actionData: _sketch_model_pb2.StrokeActionData
    mergedActions: _containers.RepeatedScalarFieldContainer[_sketch_model_pb2.SplineAction]
    skipMeshUpdate: bool
    def __init__(self, actionData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ..., mergedActions: _Optional[_Iterable[_Union[_sketch_model_pb2.SplineAction, str]]] = ..., skipMeshUpdate: bool = ...) -> None: ...

class SketchActionResponse(_message.Message):
    __slots__ = ("newerActionData", "requestAction", "rejectedInvalidStrokeName", "result")
    NEWERACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    REQUESTACTION_FIELD_NUMBER: _ClassVar[int]
    REJECTEDINVALIDSTROKENAME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    newerActionData: _sketch_model_pb2.StrokeActionData
    requestAction: _sketch_model_pb2.SplineAction
    rejectedInvalidStrokeName: str
    result: StrokeActionResult
    def __init__(self, newerActionData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ..., requestAction: _Optional[_Union[_sketch_model_pb2.SplineAction, str]] = ..., rejectedInvalidStrokeName: _Optional[str] = ..., result: _Optional[_Union[StrokeActionResult, str]] = ...) -> None: ...

class PollSketchRequest(_message.Message):
    __slots__ = ("fromStrokeUpdateSeqId", "retrieveUpdateSeqIdCapTo", "fromFinalGroupUpdateSeqId", "fromFinalLayerGroupUpdateSeqId")
    FROMSTROKEUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    RETRIEVEUPDATESEQIDCAPTO_FIELD_NUMBER: _ClassVar[int]
    FROMFINALGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    FROMFINALLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    fromStrokeUpdateSeqId: int
    retrieveUpdateSeqIdCapTo: int
    fromFinalGroupUpdateSeqId: int
    fromFinalLayerGroupUpdateSeqId: int
    def __init__(self, fromStrokeUpdateSeqId: _Optional[int] = ..., retrieveUpdateSeqIdCapTo: _Optional[int] = ..., fromFinalGroupUpdateSeqId: _Optional[int] = ..., fromFinalLayerGroupUpdateSeqId: _Optional[int] = ...) -> None: ...

class PollSketchResponse(_message.Message):
    __slots__ = ("toStrokeUpdateSeqId", "actionData", "drawMaterial", "maxUpdateSeqId", "layer", "deprecatedConfirmIncrementalEditSketchObjectId", "deprecatedConfirmIncrementalEditSeqId", "toGroupUpdateSeqId", "groupData", "toLayerGroupUpdateSeqId", "layerGroupUpdates", "fromStrokeUpdateSeqId", "fromGroupUpdateSeqId", "fromLayerGroupUpdateSeqId", "mostRecentForceDestroyedThisSessionId")
    TOSTROKEUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    MAXUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDCONFIRMINCREMENTALEDITSKETCHOBJECTID_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDCONFIRMINCREMENTALEDITSEQID_FIELD_NUMBER: _ClassVar[int]
    TOGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    GROUPDATA_FIELD_NUMBER: _ClassVar[int]
    TOLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPUPDATES_FIELD_NUMBER: _ClassVar[int]
    FROMSTROKEUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    FROMGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    FROMLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    MOSTRECENTFORCEDESTROYEDTHISSESSIONID_FIELD_NUMBER: _ClassVar[int]
    toStrokeUpdateSeqId: int
    actionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    drawMaterial: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    maxUpdateSeqId: int
    layer: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.LayerModelTO]
    deprecatedConfirmIncrementalEditSketchObjectId: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    deprecatedConfirmIncrementalEditSeqId: _containers.RepeatedScalarFieldContainer[int]
    toGroupUpdateSeqId: int
    groupData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupTO]
    toLayerGroupUpdateSeqId: int
    layerGroupUpdates: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.NestedLayerRelationship]
    fromStrokeUpdateSeqId: int
    fromGroupUpdateSeqId: int
    fromLayerGroupUpdateSeqId: int
    mostRecentForceDestroyedThisSessionId: _sketch_common_pb2.GSDataID
    def __init__(self, toStrokeUpdateSeqId: _Optional[int] = ..., actionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., drawMaterial: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., maxUpdateSeqId: _Optional[int] = ..., layer: _Optional[_Iterable[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]]] = ..., deprecatedConfirmIncrementalEditSketchObjectId: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., deprecatedConfirmIncrementalEditSeqId: _Optional[_Iterable[int]] = ..., toGroupUpdateSeqId: _Optional[int] = ..., groupData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]]] = ..., toLayerGroupUpdateSeqId: _Optional[int] = ..., layerGroupUpdates: _Optional[_Iterable[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]]] = ..., fromStrokeUpdateSeqId: _Optional[int] = ..., fromGroupUpdateSeqId: _Optional[int] = ..., fromLayerGroupUpdateSeqId: _Optional[int] = ..., mostRecentForceDestroyedThisSessionId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class PollFinalSketchesRequest(_message.Message):
    __slots__ = ("fromFinalActionUpdateSeqId", "groupHash", "fromGroupUpdateSeqId", "mostRecentForceDestroyedThisSessionId", "fromLayerGroupUpdateSeqId")
    FROMFINALACTIONUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    GROUPHASH_FIELD_NUMBER: _ClassVar[int]
    FROMGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    MOSTRECENTFORCEDESTROYEDTHISSESSIONID_FIELD_NUMBER: _ClassVar[int]
    FROMLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    fromFinalActionUpdateSeqId: int
    groupHash: int
    fromGroupUpdateSeqId: int
    mostRecentForceDestroyedThisSessionId: _sketch_common_pb2.GSDataID
    fromLayerGroupUpdateSeqId: int
    def __init__(self, fromFinalActionUpdateSeqId: _Optional[int] = ..., groupHash: _Optional[int] = ..., fromGroupUpdateSeqId: _Optional[int] = ..., mostRecentForceDestroyedThisSessionId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., fromLayerGroupUpdateSeqId: _Optional[int] = ...) -> None: ...

class StrokeChecksum(_message.Message):
    __slots__ = ("strokeId", "seqId")
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    strokeId: _sketch_common_pb2.GSDataID
    seqId: int
    def __init__(self, strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., seqId: _Optional[int] = ...) -> None: ...

class PollFinalSketchesResponse(_message.Message):
    __slots__ = ("fromFinalActionUpdateSeqId", "toFinalActionUpdateSeqId", "strokeChecksums", "maxUpdateSeqId", "fromGroupUpdateSeqId", "toGroupUpdateSeqId", "changedGroups", "missedForceDestroysThisSession", "fromLayerGroupUpdateSeqId", "toLayerGroupUpdateSeqId", "layerGroupUpdates", "lastMessageSeqId")
    FROMFINALACTIONUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    TOFINALACTIONUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    STROKECHECKSUMS_FIELD_NUMBER: _ClassVar[int]
    MAXUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    FROMGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    TOGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    CHANGEDGROUPS_FIELD_NUMBER: _ClassVar[int]
    MISSEDFORCEDESTROYSTHISSESSION_FIELD_NUMBER: _ClassVar[int]
    FROMLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    TOLAYERGROUPUPDATESEQID_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPUPDATES_FIELD_NUMBER: _ClassVar[int]
    LASTMESSAGESEQID_FIELD_NUMBER: _ClassVar[int]
    fromFinalActionUpdateSeqId: int
    toFinalActionUpdateSeqId: int
    strokeChecksums: _containers.RepeatedCompositeFieldContainer[StrokeChecksum]
    maxUpdateSeqId: int
    fromGroupUpdateSeqId: int
    toGroupUpdateSeqId: int
    changedGroups: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupTO]
    missedForceDestroysThisSession: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    fromLayerGroupUpdateSeqId: int
    toLayerGroupUpdateSeqId: int
    layerGroupUpdates: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.NestedLayerRelationship]
    lastMessageSeqId: int
    def __init__(self, fromFinalActionUpdateSeqId: _Optional[int] = ..., toFinalActionUpdateSeqId: _Optional[int] = ..., strokeChecksums: _Optional[_Iterable[_Union[StrokeChecksum, _Mapping]]] = ..., maxUpdateSeqId: _Optional[int] = ..., fromGroupUpdateSeqId: _Optional[int] = ..., toGroupUpdateSeqId: _Optional[int] = ..., changedGroups: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]]] = ..., missedForceDestroysThisSession: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., fromLayerGroupUpdateSeqId: _Optional[int] = ..., toLayerGroupUpdateSeqId: _Optional[int] = ..., layerGroupUpdates: _Optional[_Iterable[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]]] = ..., lastMessageSeqId: _Optional[int] = ...) -> None: ...

class SyncFinalSketchesRequest(_message.Message):
    __slots__ = ("strokeIds",)
    STROKEIDS_FIELD_NUMBER: _ClassVar[int]
    strokeIds: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    def __init__(self, strokeIds: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ...) -> None: ...

class SyncFinalSketchesResponse(_message.Message):
    __slots__ = ("actionData", "drawMaterial")
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    actionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    drawMaterial: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    def __init__(self, actionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., drawMaterial: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ...) -> None: ...

class SyncFinalGroupsRequest(_message.Message):
    __slots__ = ("groupIds",)
    GROUPIDS_FIELD_NUMBER: _ClassVar[int]
    groupIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, groupIds: _Optional[_Iterable[str]] = ...) -> None: ...

class SyncFinalGroupsResponse(_message.Message):
    __slots__ = ("groupTOs",)
    GROUPTOS_FIELD_NUMBER: _ClassVar[int]
    groupTOs: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupTO]
    def __init__(self, groupTOs: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]]] = ...) -> None: ...

class SyncTransformBroadcast(_message.Message):
    __slots__ = ("componentId", "positionX", "positionY", "positionZ", "rotationX", "rotationY", "rotationZ", "rotationW", "scale", "disabled", "avatarId", "avatarData", "colocationSessionData", "cameraState")
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    POSITIONX_FIELD_NUMBER: _ClassVar[int]
    POSITIONY_FIELD_NUMBER: _ClassVar[int]
    POSITIONZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONX_FIELD_NUMBER: _ClassVar[int]
    ROTATIONY_FIELD_NUMBER: _ClassVar[int]
    ROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONW_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    AVATARID_FIELD_NUMBER: _ClassVar[int]
    AVATARDATA_FIELD_NUMBER: _ClassVar[int]
    COLOCATIONSESSIONDATA_FIELD_NUMBER: _ClassVar[int]
    CAMERASTATE_FIELD_NUMBER: _ClassVar[int]
    componentId: str
    positionX: float
    positionY: float
    positionZ: float
    rotationX: float
    rotationY: float
    rotationZ: float
    rotationW: float
    scale: float
    disabled: bool
    avatarId: int
    avatarData: bytes
    colocationSessionData: ColocationSessionData
    cameraState: _sketch_model_pb2.CameraState
    def __init__(self, componentId: _Optional[str] = ..., positionX: _Optional[float] = ..., positionY: _Optional[float] = ..., positionZ: _Optional[float] = ..., rotationX: _Optional[float] = ..., rotationY: _Optional[float] = ..., rotationZ: _Optional[float] = ..., rotationW: _Optional[float] = ..., scale: _Optional[float] = ..., disabled: bool = ..., avatarId: _Optional[int] = ..., avatarData: _Optional[bytes] = ..., colocationSessionData: _Optional[_Union[ColocationSessionData, _Mapping]] = ..., cameraState: _Optional[_Union[_sketch_model_pb2.CameraState, _Mapping]] = ...) -> None: ...

class ColocationSessionData(_message.Message):
    __slots__ = ("userMetaId", "hostAnchorGuid", "hostClientIDSharedWith")
    USERMETAID_FIELD_NUMBER: _ClassVar[int]
    HOSTANCHORGUID_FIELD_NUMBER: _ClassVar[int]
    HOSTCLIENTIDSHAREDWITH_FIELD_NUMBER: _ClassVar[int]
    userMetaId: int
    hostAnchorGuid: str
    hostClientIDSharedWith: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, userMetaId: _Optional[int] = ..., hostAnchorGuid: _Optional[str] = ..., hostClientIDSharedWith: _Optional[_Iterable[int]] = ...) -> None: ...

class AddLayerRequest(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class AddLayerResponse(_message.Message):
    __slots__ = ("result", "failureLayerGuid")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    FAILURELAYERGUID_FIELD_NUMBER: _ClassVar[int]
    result: LayerActionResult
    failureLayerGuid: str
    def __init__(self, result: _Optional[_Union[LayerActionResult, str]] = ..., failureLayerGuid: _Optional[str] = ...) -> None: ...

class AddLayerBroadcast(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class LayerDeletionLock(_message.Message):
    __slots__ = ("layerGuid", "strokesHash")
    LAYERGUID_FIELD_NUMBER: _ClassVar[int]
    STROKESHASH_FIELD_NUMBER: _ClassVar[int]
    layerGuid: str
    strokesHash: int
    def __init__(self, layerGuid: _Optional[str] = ..., strokesHash: _Optional[int] = ...) -> None: ...

class PlaceDeleteLayerLockRequest(_message.Message):
    __slots__ = ("layerLocks",)
    LAYERLOCKS_FIELD_NUMBER: _ClassVar[int]
    layerLocks: _containers.RepeatedCompositeFieldContainer[LayerDeletionLock]
    def __init__(self, layerLocks: _Optional[_Iterable[_Union[LayerDeletionLock, _Mapping]]] = ...) -> None: ...

class PlaceDeleteLayerLockResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: PlaceDeleteLayerLockResult
    def __init__(self, result: _Optional[_Union[PlaceDeleteLayerLockResult, str]] = ...) -> None: ...

class CancelDeleteLayerLockRequest(_message.Message):
    __slots__ = ("layerGuid",)
    LAYERGUID_FIELD_NUMBER: _ClassVar[int]
    layerGuid: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, layerGuid: _Optional[_Iterable[str]] = ...) -> None: ...

class ModifyLayerRequest(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class CancelDeleteLayerLockResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteLayerRequest(_message.Message):
    __slots__ = ("layerLocks",)
    LAYERLOCKS_FIELD_NUMBER: _ClassVar[int]
    layerLocks: _containers.RepeatedCompositeFieldContainer[LayerDeletionLock]
    def __init__(self, layerLocks: _Optional[_Iterable[_Union[LayerDeletionLock, _Mapping]]] = ...) -> None: ...

class DeleteLayerResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: LayerActionResult
    def __init__(self, result: _Optional[_Union[LayerActionResult, str]] = ...) -> None: ...

class GetLayerRequest(_message.Message):
    __slots__ = ("layerGuid",)
    LAYERGUID_FIELD_NUMBER: _ClassVar[int]
    layerGuid: str
    def __init__(self, layerGuid: _Optional[str] = ...) -> None: ...

class GetLayerResponse(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class ModifyLayerResponse(_message.Message):
    __slots__ = ("result", "layer")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    result: LayerActionResult
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, result: _Optional[_Union[LayerActionResult, str]] = ..., layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class PreviewLayerBroadcast(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _sketch_common_pb2.LayerModelTO
    def __init__(self, layer: _Optional[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]] = ...) -> None: ...

class ChangeLayerRequest(_message.Message):
    __slots__ = ("actionData", "toLayerGuid")
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    TOLAYERGUID_FIELD_NUMBER: _ClassVar[int]
    actionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    toLayerGuid: str
    def __init__(self, actionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., toLayerGuid: _Optional[str] = ...) -> None: ...

class ChangeLayerBroadcast(_message.Message):
    __slots__ = ("actionData", "lastLayerRevisionId", "toLayerGuid")
    ACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    LASTLAYERREVISIONID_FIELD_NUMBER: _ClassVar[int]
    TOLAYERGUID_FIELD_NUMBER: _ClassVar[int]
    actionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    lastLayerRevisionId: int
    toLayerGuid: str
    def __init__(self, actionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., lastLayerRevisionId: _Optional[int] = ..., toLayerGuid: _Optional[str] = ...) -> None: ...

class ChangeLayerResponse(_message.Message):
    __slots__ = ("result", "newerActionData", "lastLayerRevisionId")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    NEWERACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    LASTLAYERREVISIONID_FIELD_NUMBER: _ClassVar[int]
    result: StrokeActionResult
    newerActionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    lastLayerRevisionId: int
    def __init__(self, result: _Optional[_Union[StrokeActionResult, str]] = ..., newerActionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., lastLayerRevisionId: _Optional[int] = ...) -> None: ...

class ImportLayersResponse(_message.Message):
    __slots__ = ("layers",)
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.LayerModelTO]
    def __init__(self, layers: _Optional[_Iterable[_Union[_sketch_common_pb2.LayerModelTO, _Mapping]]] = ...) -> None: ...

class ModifyLayerGroupRequest(_message.Message):
    __slots__ = ("modifications",)
    MODIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    modifications: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.NestedLayerRelationship]
    def __init__(self, modifications: _Optional[_Iterable[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]]] = ...) -> None: ...

class ModifyLayerGroupResponse(_message.Message):
    __slots__ = ("result", "layerGroup")
    class LayerGroupEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUP_FIELD_NUMBER: _ClassVar[int]
    result: ModifyLayerGroupResult
    layerGroup: _containers.ScalarMap[str, str]
    def __init__(self, result: _Optional[_Union[ModifyLayerGroupResult, str]] = ..., layerGroup: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateMaterialRequest(_message.Message):
    __slots__ = ("drawMaterial",)
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    drawMaterial: _sketch_common_pb2.DrawMaterial
    def __init__(self, drawMaterial: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...

class UpdateMaterialBroadcast(_message.Message):
    __slots__ = ("drawMaterial",)
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    drawMaterial: _sketch_common_pb2.DrawMaterial
    def __init__(self, drawMaterial: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...

class PreviewMaterialBroadcast(_message.Message):
    __slots__ = ("sketchObjectId", "previewType", "color", "materialType", "textureTransform", "roughness", "metallic", "specularHueShift", "shadowSoftness", "guid", "outlineWidth", "outlineColor")
    SKETCHOBJECTID_FIELD_NUMBER: _ClassVar[int]
    PREVIEWTYPE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    MATERIALTYPE_FIELD_NUMBER: _ClassVar[int]
    TEXTURETRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ROUGHNESS_FIELD_NUMBER: _ClassVar[int]
    METALLIC_FIELD_NUMBER: _ClassVar[int]
    SPECULARHUESHIFT_FIELD_NUMBER: _ClassVar[int]
    SHADOWSOFTNESS_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    OUTLINEWIDTH_FIELD_NUMBER: _ClassVar[int]
    OUTLINECOLOR_FIELD_NUMBER: _ClassVar[int]
    sketchObjectId: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    previewType: PreviewType
    color: int
    materialType: _sketch_common_pb2.BaseMaterialType
    textureTransform: _sketch_common_pb2.MainTextureTransform
    roughness: float
    metallic: float
    specularHueShift: float
    shadowSoftness: float
    guid: str
    outlineWidth: float
    outlineColor: int
    def __init__(self, sketchObjectId: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., previewType: _Optional[_Union[PreviewType, str]] = ..., color: _Optional[int] = ..., materialType: _Optional[_Union[_sketch_common_pb2.BaseMaterialType, str]] = ..., textureTransform: _Optional[_Union[_sketch_common_pb2.MainTextureTransform, _Mapping]] = ..., roughness: _Optional[float] = ..., metallic: _Optional[float] = ..., specularHueShift: _Optional[float] = ..., shadowSoftness: _Optional[float] = ..., guid: _Optional[str] = ..., outlineWidth: _Optional[float] = ..., outlineColor: _Optional[int] = ...) -> None: ...

class PreviewIncrementalDataRequest(_message.Message):
    __slots__ = ("incrementalData",)
    INCREMENTALDATA_FIELD_NUMBER: _ClassVar[int]
    incrementalData: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, incrementalData: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class PreviewIncrementalDataBroadcast(_message.Message):
    __slots__ = ("incrementalData",)
    INCREMENTALDATA_FIELD_NUMBER: _ClassVar[int]
    incrementalData: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, incrementalData: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class ConfirmIncrementalDataRequest(_message.Message):
    __slots__ = ("incrementalData",)
    INCREMENTALDATA_FIELD_NUMBER: _ClassVar[int]
    incrementalData: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, incrementalData: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class ConfirmIncrementalDataResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ConfirmIncrementalResult
    def __init__(self, result: _Optional[_Union[ConfirmIncrementalResult, str]] = ...) -> None: ...

class GetMissingConfirmIncrementalDataRequest(_message.Message):
    __slots__ = ("strokeId", "missingDataSeqID")
    STROKEID_FIELD_NUMBER: _ClassVar[int]
    MISSINGDATASEQID_FIELD_NUMBER: _ClassVar[int]
    strokeId: _sketch_common_pb2.GSDataID
    missingDataSeqID: int
    def __init__(self, strokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., missingDataSeqID: _Optional[int] = ...) -> None: ...

class GetMissingConfirmIncrementalDataResponse(_message.Message):
    __slots__ = ("incrementalData",)
    INCREMENTALDATA_FIELD_NUMBER: _ClassVar[int]
    incrementalData: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, incrementalData: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class ConfirmIncrementalDataBroadcast(_message.Message):
    __slots__ = ("incrementalData",)
    INCREMENTALDATA_FIELD_NUMBER: _ClassVar[int]
    incrementalData: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, incrementalData: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class RepairSubDRequest(_message.Message):
    __slots__ = ("corruptSubDStrokeId", "idForNewlyRepairedSubD")
    CORRUPTSUBDSTROKEID_FIELD_NUMBER: _ClassVar[int]
    IDFORNEWLYREPAIREDSUBD_FIELD_NUMBER: _ClassVar[int]
    corruptSubDStrokeId: _sketch_common_pb2.GSDataID
    idForNewlyRepairedSubD: _sketch_common_pb2.GSDataID
    def __init__(self, corruptSubDStrokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., idForNewlyRepairedSubD: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class RepairSubDResponse(_message.Message):
    __slots__ = ("repairSubDResult", "corruptSubDStrokeId")
    REPAIRSUBDRESULT_FIELD_NUMBER: _ClassVar[int]
    CORRUPTSUBDSTROKEID_FIELD_NUMBER: _ClassVar[int]
    repairSubDResult: RepairSubDResult
    corruptSubDStrokeId: _sketch_common_pb2.GSDataID
    def __init__(self, repairSubDResult: _Optional[_Union[RepairSubDResult, str]] = ..., corruptSubDStrokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class RepairSubDBroadcast(_message.Message):
    __slots__ = ("corruptSubDStrokeId", "repairedActionData")
    CORRUPTSUBDSTROKEID_FIELD_NUMBER: _ClassVar[int]
    REPAIREDACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    corruptSubDStrokeId: _sketch_common_pb2.GSDataID
    repairedActionData: _sketch_model_pb2.StrokeActionData
    def __init__(self, corruptSubDStrokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., repairedActionData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ...) -> None: ...

class ChangeCoordinatorBroadcast(_message.Message):
    __slots__ = ("newCoordinatorId",)
    NEWCOORDINATORID_FIELD_NUMBER: _ClassVar[int]
    newCoordinatorId: int
    def __init__(self, newCoordinatorId: _Optional[int] = ...) -> None: ...

class ChangeCoordinatorResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CollaborationResult
    def __init__(self, result: _Optional[_Union[CollaborationResult, str]] = ...) -> None: ...

class ChangeEnvironmentBroadcast(_message.Message):
    __slots__ = ("settings", "presetIndex")
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PRESETINDEX_FIELD_NUMBER: _ClassVar[int]
    settings: _gravi_model_pb2.EnvironmentSettingTO
    presetIndex: int
    def __init__(self, settings: _Optional[_Union[_gravi_model_pb2.EnvironmentSettingTO, _Mapping]] = ..., presetIndex: _Optional[int] = ...) -> None: ...

class ChangeEnvironmentResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CollaborationResult
    def __init__(self, result: _Optional[_Union[CollaborationResult, str]] = ...) -> None: ...

class SyncRoomExtraDataRequest(_message.Message):
    __slots__ = ("includeEnvironment",)
    INCLUDEENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    includeEnvironment: bool
    def __init__(self, includeEnvironment: bool = ...) -> None: ...

class SyncRoomExtraDataResponse(_message.Message):
    __slots__ = ("roomExtraData",)
    ROOMEXTRADATA_FIELD_NUMBER: _ClassVar[int]
    roomExtraData: _sketch_model_pb2.CoSketchRoomExtraData
    def __init__(self, roomExtraData: _Optional[_Union[_sketch_model_pb2.CoSketchRoomExtraData, _Mapping]] = ...) -> None: ...

class RoomInMemoryStates(_message.Message):
    __slots__ = ("blockJoining", "blockSketch", "shutdownRoom")
    BLOCKJOINING_FIELD_NUMBER: _ClassVar[int]
    BLOCKSKETCH_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWNROOM_FIELD_NUMBER: _ClassVar[int]
    blockJoining: bool
    blockSketch: bool
    shutdownRoom: bool
    def __init__(self, blockJoining: bool = ..., blockSketch: bool = ..., shutdownRoom: bool = ...) -> None: ...

class LockWholeRoomRequest(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: RoomInMemoryStates
    def __init__(self, states: _Optional[_Union[RoomInMemoryStates, _Mapping]] = ...) -> None: ...

class LockWholeRoomResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: LockWholeRoomResult
    def __init__(self, result: _Optional[_Union[LockWholeRoomResult, str]] = ...) -> None: ...

class UpdateCoSketchUserRequest(_message.Message):
    __slots__ = ("newUserName",)
    NEWUSERNAME_FIELD_NUMBER: _ClassVar[int]
    newUserName: str
    def __init__(self, newUserName: _Optional[str] = ...) -> None: ...

class UpdateCoSketchUserResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: UpdateCoSketchUserResult
    def __init__(self, result: _Optional[_Union[UpdateCoSketchUserResult, str]] = ...) -> None: ...

class RelayData(_message.Message):
    __slots__ = ("toClientId", "data")
    TOCLIENTID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    toClientId: int
    data: bytes
    def __init__(self, toClientId: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class ListPlayersRequest(_message.Message):
    __slots__ = ("voicePlayerName",)
    VOICEPLAYERNAME_FIELD_NUMBER: _ClassVar[int]
    voicePlayerName: str
    def __init__(self, voicePlayerName: _Optional[str] = ...) -> None: ...

class ListPlayersResponse(_message.Message):
    __slots__ = ("clientIds",)
    class ClientIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    CLIENTIDS_FIELD_NUMBER: _ClassVar[int]
    clientIds: _containers.ScalarMap[int, str]
    def __init__(self, clientIds: _Optional[_Mapping[int, str]] = ...) -> None: ...

class AssetPermit(_message.Message):
    __slots__ = ("assetName", "secretCode")
    ASSETNAME_FIELD_NUMBER: _ClassVar[int]
    SECRETCODE_FIELD_NUMBER: _ClassVar[int]
    assetName: str
    secretCode: str
    def __init__(self, assetName: _Optional[str] = ..., secretCode: _Optional[str] = ...) -> None: ...

class AssetsReadyRequest(_message.Message):
    __slots__ = ("downloadFileName",)
    DOWNLOADFILENAME_FIELD_NUMBER: _ClassVar[int]
    downloadFileName: str
    def __init__(self, downloadFileName: _Optional[str] = ...) -> None: ...

class AssetsReadyBroadcast(_message.Message):
    __slots__ = ("downloadFileName", "secretCode")
    DOWNLOADFILENAME_FIELD_NUMBER: _ClassVar[int]
    SECRETCODE_FIELD_NUMBER: _ClassVar[int]
    downloadFileName: str
    secretCode: str
    def __init__(self, downloadFileName: _Optional[str] = ..., secretCode: _Optional[str] = ...) -> None: ...

class SyncUIBroadcast(_message.Message):
    __slots__ = ("uiId", "uiStates")
    UIID_FIELD_NUMBER: _ClassVar[int]
    UISTATES_FIELD_NUMBER: _ClassVar[int]
    uiId: str
    uiStates: bytes
    def __init__(self, uiId: _Optional[str] = ..., uiStates: _Optional[bytes] = ...) -> None: ...

class MessageBroadcast(_message.Message):
    __slots__ = ("clientId", "seqId", "presetMessage", "message")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    SEQID_FIELD_NUMBER: _ClassVar[int]
    PRESETMESSAGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    clientId: int
    seqId: int
    presetMessage: PresetMessage
    message: str
    def __init__(self, clientId: _Optional[int] = ..., seqId: _Optional[int] = ..., presetMessage: _Optional[_Union[PresetMessage, str]] = ..., message: _Optional[str] = ...) -> None: ...

class MessageBroadcastResponse(_message.Message):
    __slots__ = ("seqId",)
    SEQID_FIELD_NUMBER: _ClassVar[int]
    seqId: int
    def __init__(self, seqId: _Optional[int] = ...) -> None: ...

class GetMissingMessageRequest(_message.Message):
    __slots__ = ("seqId",)
    SEQID_FIELD_NUMBER: _ClassVar[int]
    seqId: int
    def __init__(self, seqId: _Optional[int] = ...) -> None: ...

class GetMissingMessageResponse(_message.Message):
    __slots__ = ("result", "message")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    result: GetMissingMessageResult
    message: MessageBroadcast
    def __init__(self, result: _Optional[_Union[GetMissingMessageResult, str]] = ..., message: _Optional[_Union[MessageBroadcast, _Mapping]] = ...) -> None: ...

class SyncUserPreferencesBroadcast(_message.Message):
    __slots__ = ("userPreferences",)
    USERPREFERENCES_FIELD_NUMBER: _ClassVar[int]
    userPreferences: _preferences_pb2.UserSavedPreferencesTO
    def __init__(self, userPreferences: _Optional[_Union[_preferences_pb2.UserSavedPreferencesTO, _Mapping]] = ...) -> None: ...

class SyncUserDefaultsBroadcast(_message.Message):
    __slots__ = ("userDefaults",)
    USERDEFAULTS_FIELD_NUMBER: _ClassVar[int]
    userDefaults: _preferences_pb2.UserDefaultsProfileTO
    def __init__(self, userDefaults: _Optional[_Union[_preferences_pb2.UserDefaultsProfileTO, _Mapping]] = ...) -> None: ...

class GroupingObjectsRequest(_message.Message):
    __slots__ = ("newGroupId", "strokeIdsWithoutGroup", "subGroupIds", "subGroupSeqIds")
    NEWGROUPID_FIELD_NUMBER: _ClassVar[int]
    STROKEIDSWITHOUTGROUP_FIELD_NUMBER: _ClassVar[int]
    SUBGROUPIDS_FIELD_NUMBER: _ClassVar[int]
    SUBGROUPSEQIDS_FIELD_NUMBER: _ClassVar[int]
    newGroupId: str
    strokeIdsWithoutGroup: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.GSDataID]
    subGroupIds: _containers.RepeatedScalarFieldContainer[str]
    subGroupSeqIds: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, newGroupId: _Optional[str] = ..., strokeIdsWithoutGroup: _Optional[_Iterable[_Union[_sketch_common_pb2.GSDataID, _Mapping]]] = ..., subGroupIds: _Optional[_Iterable[str]] = ..., subGroupSeqIds: _Optional[_Iterable[int]] = ...) -> None: ...

class GroupResponse(_message.Message):
    __slots__ = ("success", "newerActionData", "drawMaterial", "newerGroups")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NEWERACTIONDATA_FIELD_NUMBER: _ClassVar[int]
    DRAWMATERIAL_FIELD_NUMBER: _ClassVar[int]
    NEWERGROUPS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    newerActionData: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeActionData]
    drawMaterial: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    newerGroups: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupTO]
    def __init__(self, success: bool = ..., newerActionData: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]]] = ..., drawMaterial: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., newerGroups: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]]] = ...) -> None: ...

class UnGroupObjectsRequest(_message.Message):
    __slots__ = ("groupId", "groupSeqId")
    GROUPID_FIELD_NUMBER: _ClassVar[int]
    GROUPSEQID_FIELD_NUMBER: _ClassVar[int]
    groupId: str
    groupSeqId: int
    def __init__(self, groupId: _Optional[str] = ..., groupSeqId: _Optional[int] = ...) -> None: ...

class AddImportedGroupRequest(_message.Message):
    __slots__ = ("importedGroup",)
    IMPORTEDGROUP_FIELD_NUMBER: _ClassVar[int]
    importedGroup: _sketch_model_pb2.StrokeGroupTO
    def __init__(self, importedGroup: _Optional[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]] = ...) -> None: ...

class CreateDuplicatedGroupsRequest(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _containers.RepeatedCompositeFieldContainer[_sketch_model_pb2.StrokeGroupTO]
    def __init__(self, group: _Optional[_Iterable[_Union[_sketch_model_pb2.StrokeGroupTO, _Mapping]]] = ...) -> None: ...

class ConvertToSubDRequest(_message.Message):
    __slots__ = ("originalStrokeId", "originalStrokeMetaData", "subDData")
    ORIGINALSTROKEID_FIELD_NUMBER: _ClassVar[int]
    ORIGINALSTROKEMETADATA_FIELD_NUMBER: _ClassVar[int]
    SUBDDATA_FIELD_NUMBER: _ClassVar[int]
    originalStrokeId: _sketch_common_pb2.GSDataID
    originalStrokeMetaData: _sketch_model_pb2.StrokeActionMetaData
    subDData: _sketch_model_pb2.StrokeActionData
    def __init__(self, originalStrokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., originalStrokeMetaData: _Optional[_Union[_sketch_model_pb2.StrokeActionMetaData, _Mapping]] = ..., subDData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ...) -> None: ...

class ConvertToSubDResponse(_message.Message):
    __slots__ = ("result", "subDStrokeId")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SUBDSTROKEID_FIELD_NUMBER: _ClassVar[int]
    result: ConvertToSubDResult
    subDStrokeId: _sketch_common_pb2.GSDataID
    def __init__(self, result: _Optional[_Union[ConvertToSubDResult, str]] = ..., subDStrokeId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ...) -> None: ...

class ReverseSubDConversionRequest(_message.Message):
    __slots__ = ("subDId", "subDMetaData", "originalStrokeData")
    SUBDID_FIELD_NUMBER: _ClassVar[int]
    SUBDMETADATA_FIELD_NUMBER: _ClassVar[int]
    ORIGINALSTROKEDATA_FIELD_NUMBER: _ClassVar[int]
    subDId: _sketch_common_pb2.GSDataID
    subDMetaData: _sketch_model_pb2.StrokeActionMetaData
    originalStrokeData: _sketch_model_pb2.StrokeActionData
    def __init__(self, subDId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., subDMetaData: _Optional[_Union[_sketch_model_pb2.StrokeActionMetaData, _Mapping]] = ..., originalStrokeData: _Optional[_Union[_sketch_model_pb2.StrokeActionData, _Mapping]] = ...) -> None: ...

class ReverseSubDConversionResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ConvertToSubDResult
    def __init__(self, result: _Optional[_Union[ConvertToSubDResult, str]] = ...) -> None: ...

class MergeSubDObjectsRequest(_message.Message):
    __slots__ = ("objectToDeleteId", "objectToDeleteMetaData", "incrementalDataToMerge")
    OBJECTTODELETEID_FIELD_NUMBER: _ClassVar[int]
    OBJECTTODELETEMETADATA_FIELD_NUMBER: _ClassVar[int]
    INCREMENTALDATATOMERGE_FIELD_NUMBER: _ClassVar[int]
    objectToDeleteId: _sketch_common_pb2.GSDataID
    objectToDeleteMetaData: _sketch_model_pb2.StrokeActionMetaData
    incrementalDataToMerge: _sketch_incremental_pb2.StrokeIncrementalData
    def __init__(self, objectToDeleteId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., objectToDeleteMetaData: _Optional[_Union[_sketch_model_pb2.StrokeActionMetaData, _Mapping]] = ..., incrementalDataToMerge: _Optional[_Union[_sketch_incremental_pb2.StrokeIncrementalData, _Mapping]] = ...) -> None: ...

class MergeSubDObjectsResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: MergeSubDObjectsResult
    def __init__(self, result: _Optional[_Union[MergeSubDObjectsResult, str]] = ...) -> None: ...

class AuthorizeJoinerRequest(_message.Message):
    __slots__ = ("joinerClientId", "allowed")
    JOINERCLIENTID_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    joinerClientId: int
    allowed: bool
    def __init__(self, joinerClientId: _Optional[int] = ..., allowed: bool = ...) -> None: ...

class RequestToFollowRequest(_message.Message):
    __slots__ = ("toClientId",)
    TOCLIENTID_FIELD_NUMBER: _ClassVar[int]
    toClientId: int
    def __init__(self, toClientId: _Optional[int] = ...) -> None: ...

class UpdateSectionViewRequest(_message.Message):
    __slots__ = ("sectionViewData",)
    SECTIONVIEWDATA_FIELD_NUMBER: _ClassVar[int]
    sectionViewData: _sketch_common_pb2.SectionViewData
    def __init__(self, sectionViewData: _Optional[_Union[_sketch_common_pb2.SectionViewData, _Mapping]] = ...) -> None: ...

class UpdateSectionViewResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: UpdateSectionViewResult
    def __init__(self, result: _Optional[_Union[UpdateSectionViewResult, str]] = ...) -> None: ...
