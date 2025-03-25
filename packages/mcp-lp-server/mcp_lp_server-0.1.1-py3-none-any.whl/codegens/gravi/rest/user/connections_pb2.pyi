import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompleteOidcAuthorisationResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CompleteOidcAuthorisationResponseCode_Success: _ClassVar[CompleteOidcAuthorisationResponseCode]
    CompleteOidcAuthorisationResponseCode_AuthorisedToDifferentAccount: _ClassVar[CompleteOidcAuthorisationResponseCode]
    CompleteOidcAuthorisationResponseCode_ThirdPartyIdentityNotRetrieved: _ClassVar[CompleteOidcAuthorisationResponseCode]

class SearchPublicUserResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SearchUserResult_Success: _ClassVar[SearchPublicUserResult]
    SearchUserResult_UserNotFound: _ClassVar[SearchPublicUserResult]

class UserOnlineStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UserOnlineStatusOnline: _ClassVar[UserOnlineStatus]
    UserOnlineStatusOffline: _ClassVar[UserOnlineStatus]

class CreateConnectionInvitationResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateConnectionInvitationResponseCodeSuccess: _ClassVar[CreateConnectionInvitationResponseCode]
    CreateConnectionInvitationResponseCodeInviteeNotFound: _ClassVar[CreateConnectionInvitationResponseCode]
    CreateConnectionInvitationResponseCodeOrgAccountInviteeNotAllowed: _ClassVar[CreateConnectionInvitationResponseCode]
    CreateConnectionInvitationResponseCodeInvitationAlreadyExists: _ClassVar[CreateConnectionInvitationResponseCode]
    CreateConnectionInvitationResponseCodeInvitationPendingOrAccepted: _ClassVar[CreateConnectionInvitationResponseCode]

class UpdateConnectionInvitationResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateConnectionInvitationResponseCode_Success: _ClassVar[UpdateConnectionInvitationResponseCode]
    UpdateConnectionInvitationResponseCode_InvitationNotFound: _ClassVar[UpdateConnectionInvitationResponseCode]
    UpdateConnectionInvitationResponseCode_InvitationUpdateNotAllowed: _ClassVar[UpdateConnectionInvitationResponseCode]
    UpdateConnectionInvitationResponseCode_InvitationUpdateFailure: _ClassVar[UpdateConnectionInvitationResponseCode]
CompleteOidcAuthorisationResponseCode_Success: CompleteOidcAuthorisationResponseCode
CompleteOidcAuthorisationResponseCode_AuthorisedToDifferentAccount: CompleteOidcAuthorisationResponseCode
CompleteOidcAuthorisationResponseCode_ThirdPartyIdentityNotRetrieved: CompleteOidcAuthorisationResponseCode
SearchUserResult_Success: SearchPublicUserResult
SearchUserResult_UserNotFound: SearchPublicUserResult
UserOnlineStatusOnline: UserOnlineStatus
UserOnlineStatusOffline: UserOnlineStatus
CreateConnectionInvitationResponseCodeSuccess: CreateConnectionInvitationResponseCode
CreateConnectionInvitationResponseCodeInviteeNotFound: CreateConnectionInvitationResponseCode
CreateConnectionInvitationResponseCodeOrgAccountInviteeNotAllowed: CreateConnectionInvitationResponseCode
CreateConnectionInvitationResponseCodeInvitationAlreadyExists: CreateConnectionInvitationResponseCode
CreateConnectionInvitationResponseCodeInvitationPendingOrAccepted: CreateConnectionInvitationResponseCode
UpdateConnectionInvitationResponseCode_Success: UpdateConnectionInvitationResponseCode
UpdateConnectionInvitationResponseCode_InvitationNotFound: UpdateConnectionInvitationResponseCode
UpdateConnectionInvitationResponseCode_InvitationUpdateNotAllowed: UpdateConnectionInvitationResponseCode
UpdateConnectionInvitationResponseCode_InvitationUpdateFailure: UpdateConnectionInvitationResponseCode

class InitiateOidcAuthorisationRequest(_message.Message):
    __slots__ = ("userId", "afterAuthRedirectUrl", "oidcResourceProvider")
    USERID_FIELD_NUMBER: _ClassVar[int]
    AFTERAUTHREDIRECTURL_FIELD_NUMBER: _ClassVar[int]
    OIDCRESOURCEPROVIDER_FIELD_NUMBER: _ClassVar[int]
    userId: str
    afterAuthRedirectUrl: str
    oidcResourceProvider: _gravi_model_pb2.OIDCResourceProvider
    def __init__(self, userId: _Optional[str] = ..., afterAuthRedirectUrl: _Optional[str] = ..., oidcResourceProvider: _Optional[_Union[_gravi_model_pb2.OIDCResourceProvider, str]] = ...) -> None: ...

class InitiateOidcAuthorisationResponse(_message.Message):
    __slots__ = ("providerRedirectUrl", "nonce", "state", "oidcResourceProvider")
    PROVIDERREDIRECTURL_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    OIDCRESOURCEPROVIDER_FIELD_NUMBER: _ClassVar[int]
    providerRedirectUrl: str
    nonce: str
    state: str
    oidcResourceProvider: _gravi_model_pb2.OIDCResourceProvider
    def __init__(self, providerRedirectUrl: _Optional[str] = ..., nonce: _Optional[str] = ..., state: _Optional[str] = ..., oidcResourceProvider: _Optional[_Union[_gravi_model_pb2.OIDCResourceProvider, str]] = ...) -> None: ...

class CompleteOidcAuthorisationRequest(_message.Message):
    __slots__ = ("userId", "authCode", "oidcResourceProvider", "nonce", "deviceInfo")
    USERID_FIELD_NUMBER: _ClassVar[int]
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    OIDCRESOURCEPROVIDER_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    userId: str
    authCode: str
    oidcResourceProvider: _gravi_model_pb2.OIDCResourceProvider
    nonce: str
    deviceInfo: _gravi_model_pb2.DeviceInfo
    def __init__(self, userId: _Optional[str] = ..., authCode: _Optional[str] = ..., oidcResourceProvider: _Optional[_Union[_gravi_model_pb2.OIDCResourceProvider, str]] = ..., nonce: _Optional[str] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ...) -> None: ...

class CompleteOidcAuthorisationResponse(_message.Message):
    __slots__ = ("socialInfo", "code")
    SOCIALINFO_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    socialInfo: _gravi_model_pb2.UserPublicSocialInfo
    code: CompleteOidcAuthorisationResponseCode
    def __init__(self, socialInfo: _Optional[_Union[_gravi_model_pb2.UserPublicSocialInfo, _Mapping]] = ..., code: _Optional[_Union[CompleteOidcAuthorisationResponseCode, str]] = ...) -> None: ...

class RevokeOidcAuthorisationRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class RevokeOidcAuthorisationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SearchPublicUserRequest(_message.Message):
    __slots__ = ("userHandle",)
    USERHANDLE_FIELD_NUMBER: _ClassVar[int]
    userHandle: str
    def __init__(self, userHandle: _Optional[str] = ...) -> None: ...

class SearchPublicUserResponse(_message.Message):
    __slots__ = ("userPublicInfo", "searchPublicUserResult", "userId")
    USERPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    SEARCHPUBLICUSERRESULT_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    userPublicInfo: _gravi_model_pb2.UserPublicTO
    searchPublicUserResult: SearchPublicUserResult
    userId: str
    def __init__(self, userPublicInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ..., searchPublicUserResult: _Optional[_Union[SearchPublicUserResult, str]] = ..., userId: _Optional[str] = ...) -> None: ...

class ConnectionTO(_message.Message):
    __slots__ = ("userId", "onlineStatus", "userPublicInfo", "email")
    USERID_FIELD_NUMBER: _ClassVar[int]
    ONLINESTATUS_FIELD_NUMBER: _ClassVar[int]
    USERPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    userId: str
    onlineStatus: UserOnlineStatus
    userPublicInfo: _gravi_model_pb2.UserPublicTO
    email: str
    def __init__(self, userId: _Optional[str] = ..., onlineStatus: _Optional[_Union[UserOnlineStatus, str]] = ..., userPublicInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ..., email: _Optional[str] = ...) -> None: ...

class ListConnectionsRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class ListConnectionsResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ConnectionTO]
    def __init__(self, connections: _Optional[_Iterable[_Union[ConnectionTO, _Mapping]]] = ...) -> None: ...

class CreateConnectionInvitationRequest(_message.Message):
    __slots__ = ("inviterUserId", "inviteeUserId", "inviterPublicProfileLink")
    INVITERUSERID_FIELD_NUMBER: _ClassVar[int]
    INVITEEUSERID_FIELD_NUMBER: _ClassVar[int]
    INVITERPUBLICPROFILELINK_FIELD_NUMBER: _ClassVar[int]
    inviterUserId: str
    inviteeUserId: str
    inviterPublicProfileLink: str
    def __init__(self, inviterUserId: _Optional[str] = ..., inviteeUserId: _Optional[str] = ..., inviterPublicProfileLink: _Optional[str] = ...) -> None: ...

class CreateConnectionInvitationResponse(_message.Message):
    __slots__ = ("connectionInvitation", "code")
    CONNECTIONINVITATION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    connectionInvitation: _gravi_model_pb2.ConnectionInvitationTO
    code: CreateConnectionInvitationResponseCode
    def __init__(self, connectionInvitation: _Optional[_Union[_gravi_model_pb2.ConnectionInvitationTO, _Mapping]] = ..., code: _Optional[_Union[CreateConnectionInvitationResponseCode, str]] = ...) -> None: ...

class ListConnectionInvitationsRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class ListConnectionInvitationsResponse(_message.Message):
    __slots__ = ("connectionInvitations",)
    CONNECTIONINVITATIONS_FIELD_NUMBER: _ClassVar[int]
    connectionInvitations: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.ConnectionInvitationTO]
    def __init__(self, connectionInvitations: _Optional[_Iterable[_Union[_gravi_model_pb2.ConnectionInvitationTO, _Mapping]]] = ...) -> None: ...

class UpdateConnectionInvitationRequest(_message.Message):
    __slots__ = ("invitationId", "invitationStatus", "inviterPublicProfileLink")
    INVITATIONID_FIELD_NUMBER: _ClassVar[int]
    INVITATIONSTATUS_FIELD_NUMBER: _ClassVar[int]
    INVITERPUBLICPROFILELINK_FIELD_NUMBER: _ClassVar[int]
    invitationId: str
    invitationStatus: _gravi_model_pb2.ConnectionInvitationStatus
    inviterPublicProfileLink: str
    def __init__(self, invitationId: _Optional[str] = ..., invitationStatus: _Optional[_Union[_gravi_model_pb2.ConnectionInvitationStatus, str]] = ..., inviterPublicProfileLink: _Optional[str] = ...) -> None: ...

class UpdateConnectionInvitationResponse(_message.Message):
    __slots__ = ("connectionInvitation", "code")
    CONNECTIONINVITATION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    connectionInvitation: _gravi_model_pb2.ConnectionInvitationTO
    code: UpdateConnectionInvitationResponseCode
    def __init__(self, connectionInvitation: _Optional[_Union[_gravi_model_pb2.ConnectionInvitationTO, _Mapping]] = ..., code: _Optional[_Union[UpdateConnectionInvitationResponseCode, str]] = ...) -> None: ...
