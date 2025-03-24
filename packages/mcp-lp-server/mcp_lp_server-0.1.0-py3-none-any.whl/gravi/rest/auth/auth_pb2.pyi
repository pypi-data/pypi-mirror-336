from gravi.models import gravi_model_pb2 as _gravi_model_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.rest.org import team_pb2 as _team_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SignUpWithSSOResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    success: _ClassVar[SignUpWithSSOResponseCode]
    AddedUserToOrg: _ClassVar[SignUpWithSSOResponseCode]
    RejectedUserAlreadyInOrg: _ClassVar[SignUpWithSSOResponseCode]
    RejectedInvalidEmail: _ClassVar[SignUpWithSSOResponseCode]
    RejectedNoSeatsAvailable: _ClassVar[SignUpWithSSOResponseCode]
    AddedInactiveUserToOrg: _ClassVar[SignUpWithSSOResponseCode]
    RejectedOrgAccountDueToExists: _ClassVar[SignUpWithSSOResponseCode]
    SSONonceExpired: _ClassVar[SignUpWithSSOResponseCode]
    SSOIdentityProviderError: _ClassVar[SignUpWithSSOResponseCode]
    SSONoOrgUsingEmailDomain: _ClassVar[SignUpWithSSOResponseCode]
    SSOOrgDisallowsSSOSignUp: _ClassVar[SignUpWithSSOResponseCode]
    SSOEmailAlreadyInUse: _ClassVar[SignUpWithSSOResponseCode]
    SSOOidcIDAlreadyInUse: _ClassVar[SignUpWithSSOResponseCode]

class ChangeEmailResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ChangeEmailResponseCode_Success: _ClassVar[ChangeEmailResponseCode]
    ChangeEmailResponseCode_EmailAlreadyInUse: _ClassVar[ChangeEmailResponseCode]
    ChangeEmailResponseCode_InvalidEmail: _ClassVar[ChangeEmailResponseCode]

class ChangePasswordResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ChangePasswordResponseCode_Success: _ClassVar[ChangePasswordResponseCode]
    ChangePasswordResponseCode_SameOldNewPassword: _ClassVar[ChangePasswordResponseCode]
    ChangePasswordResponseCode_InvalidPassword: _ClassVar[ChangePasswordResponseCode]
    ChangePasswordResponseCode_IncorrectPassword: _ClassVar[ChangePasswordResponseCode]

class CompleteSignUpByCodeResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CompleteSignUpByCodeResponseCode_Success: _ClassVar[CompleteSignUpByCodeResponseCode]
    CompleteSignUpByCodeResponseCode_InvalidPasswordCombination: _ClassVar[CompleteSignUpByCodeResponseCode]
    CompleteSignUpByCodeResponseCode_MagicLinkNotFoundOrExpired: _ClassVar[CompleteSignUpByCodeResponseCode]
    CompleteSignUpByCodeResponseCode_FailedPrecondition: _ClassVar[CompleteSignUpByCodeResponseCode]

class SecurityEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SecurityEventUnknown: _ClassVar[SecurityEventType]
    SecurityEventWebChangedPassword: _ClassVar[SecurityEventType]
    SecurityEventWebChangedEmail: _ClassVar[SecurityEventType]
    SecurityEventWebResetPassword: _ClassVar[SecurityEventType]
    SecurityEventWebEnabled2FA: _ClassVar[SecurityEventType]
    SecurityEventWebDisabled2FA: _ClassVar[SecurityEventType]
    SecurityEventTypeChangedUserName: _ClassVar[SecurityEventType]
    SecurityEventTypeChangedUserCompany: _ClassVar[SecurityEventType]
    SecurityEventTypeChangedOrgUserStatus: _ClassVar[SecurityEventType]
    SecurityEventTypeChangedOrgUserRole: _ClassVar[SecurityEventType]
    SecurityEventTypeInvitedOrgUsers: _ClassVar[SecurityEventType]
    SecurityEventTypeDeletedOrgUser: _ClassVar[SecurityEventType]
    SecurityEventTypeUserJoinedOrg: _ClassVar[SecurityEventType]
    SecurityEventTypeUserSetRoomPass: _ClassVar[SecurityEventType]
    SecurityEventTypeCreatedOrgTeam: _ClassVar[SecurityEventType]
    SecurityEventTypeDeletedOrgTeam: _ClassVar[SecurityEventType]
    SecurityEventTypeUpdatedOrgTeam: _ClassVar[SecurityEventType]
    SecurityEventTypeLogin: _ClassVar[SecurityEventType]
    SecurityDocEventCreateDoc: _ClassVar[SecurityEventType]
    SecurityDocEventUpdateDoc: _ClassVar[SecurityEventType]
    SecurityDocEventDownloadDoc: _ClassVar[SecurityEventType]
    SecurityDocEventExportDoc: _ClassVar[SecurityEventType]
    SecurityDocEventShareDoc: _ClassVar[SecurityEventType]
    SecurityDocEventTrashDoc: _ClassVar[SecurityEventType]
    SecurityDocEventRestoreDoc: _ClassVar[SecurityEventType]
    SecurityDocEventDeleteDoc: _ClassVar[SecurityEventType]
    SecurityDocEventSendDoc: _ClassVar[SecurityEventType]
    SecurityDocEventAcceptDoc: _ClassVar[SecurityEventType]
    SecurityDocEventSetPassword: _ClassVar[SecurityEventType]
    SecurityDocEventChangeUserCollabRole: _ClassVar[SecurityEventType]
    SecurityDocEventRemoveUserAccess: _ClassVar[SecurityEventType]
    SecurityEventTypeAttachDevice: _ClassVar[SecurityEventType]
    SecurityEventTypeDetachDevice: _ClassVar[SecurityEventType]
    SecurityEventTypeApproveOrDenyJoinOrg: _ClassVar[SecurityEventType]

class StoreSignupResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    StoreSignupResult_UnknownError: _ClassVar[StoreSignupResult]
    StoreSignupResult_Success: _ClassVar[StoreSignupResult]
    StoreSignupResult_CodeNotFound: _ClassVar[StoreSignupResult]
    StoreSignupResult_AccountNotFound: _ClassVar[StoreSignupResult]
    StoreSignupResult_InvalidPassword: _ClassVar[StoreSignupResult]

class DetachDeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownDevice: _ClassVar[DetachDeviceType]
    OculusRiftDevice: _ClassVar[DetachDeviceType]
    OculusQuestDevice: _ClassVar[DetachDeviceType]
    SteamDevice: _ClassVar[DetachDeviceType]
    AppleId: _ClassVar[DetachDeviceType]
success: SignUpWithSSOResponseCode
AddedUserToOrg: SignUpWithSSOResponseCode
RejectedUserAlreadyInOrg: SignUpWithSSOResponseCode
RejectedInvalidEmail: SignUpWithSSOResponseCode
RejectedNoSeatsAvailable: SignUpWithSSOResponseCode
AddedInactiveUserToOrg: SignUpWithSSOResponseCode
RejectedOrgAccountDueToExists: SignUpWithSSOResponseCode
SSONonceExpired: SignUpWithSSOResponseCode
SSOIdentityProviderError: SignUpWithSSOResponseCode
SSONoOrgUsingEmailDomain: SignUpWithSSOResponseCode
SSOOrgDisallowsSSOSignUp: SignUpWithSSOResponseCode
SSOEmailAlreadyInUse: SignUpWithSSOResponseCode
SSOOidcIDAlreadyInUse: SignUpWithSSOResponseCode
ChangeEmailResponseCode_Success: ChangeEmailResponseCode
ChangeEmailResponseCode_EmailAlreadyInUse: ChangeEmailResponseCode
ChangeEmailResponseCode_InvalidEmail: ChangeEmailResponseCode
ChangePasswordResponseCode_Success: ChangePasswordResponseCode
ChangePasswordResponseCode_SameOldNewPassword: ChangePasswordResponseCode
ChangePasswordResponseCode_InvalidPassword: ChangePasswordResponseCode
ChangePasswordResponseCode_IncorrectPassword: ChangePasswordResponseCode
CompleteSignUpByCodeResponseCode_Success: CompleteSignUpByCodeResponseCode
CompleteSignUpByCodeResponseCode_InvalidPasswordCombination: CompleteSignUpByCodeResponseCode
CompleteSignUpByCodeResponseCode_MagicLinkNotFoundOrExpired: CompleteSignUpByCodeResponseCode
CompleteSignUpByCodeResponseCode_FailedPrecondition: CompleteSignUpByCodeResponseCode
SecurityEventUnknown: SecurityEventType
SecurityEventWebChangedPassword: SecurityEventType
SecurityEventWebChangedEmail: SecurityEventType
SecurityEventWebResetPassword: SecurityEventType
SecurityEventWebEnabled2FA: SecurityEventType
SecurityEventWebDisabled2FA: SecurityEventType
SecurityEventTypeChangedUserName: SecurityEventType
SecurityEventTypeChangedUserCompany: SecurityEventType
SecurityEventTypeChangedOrgUserStatus: SecurityEventType
SecurityEventTypeChangedOrgUserRole: SecurityEventType
SecurityEventTypeInvitedOrgUsers: SecurityEventType
SecurityEventTypeDeletedOrgUser: SecurityEventType
SecurityEventTypeUserJoinedOrg: SecurityEventType
SecurityEventTypeUserSetRoomPass: SecurityEventType
SecurityEventTypeCreatedOrgTeam: SecurityEventType
SecurityEventTypeDeletedOrgTeam: SecurityEventType
SecurityEventTypeUpdatedOrgTeam: SecurityEventType
SecurityEventTypeLogin: SecurityEventType
SecurityDocEventCreateDoc: SecurityEventType
SecurityDocEventUpdateDoc: SecurityEventType
SecurityDocEventDownloadDoc: SecurityEventType
SecurityDocEventExportDoc: SecurityEventType
SecurityDocEventShareDoc: SecurityEventType
SecurityDocEventTrashDoc: SecurityEventType
SecurityDocEventRestoreDoc: SecurityEventType
SecurityDocEventDeleteDoc: SecurityEventType
SecurityDocEventSendDoc: SecurityEventType
SecurityDocEventAcceptDoc: SecurityEventType
SecurityDocEventSetPassword: SecurityEventType
SecurityDocEventChangeUserCollabRole: SecurityEventType
SecurityDocEventRemoveUserAccess: SecurityEventType
SecurityEventTypeAttachDevice: SecurityEventType
SecurityEventTypeDetachDevice: SecurityEventType
SecurityEventTypeApproveOrDenyJoinOrg: SecurityEventType
StoreSignupResult_UnknownError: StoreSignupResult
StoreSignupResult_Success: StoreSignupResult
StoreSignupResult_CodeNotFound: StoreSignupResult
StoreSignupResult_AccountNotFound: StoreSignupResult
StoreSignupResult_InvalidPassword: StoreSignupResult
UnknownDevice: DetachDeviceType
OculusRiftDevice: DetachDeviceType
OculusQuestDevice: DetachDeviceType
SteamDevice: DetachDeviceType
AppleId: DetachDeviceType

class EnableMfaRequest(_message.Message):
    __slots__ = ("email", "encryptedPassword", "mfaSecret", "mfaTotpCode", "deviceInfo")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    MFASECRET_FIELD_NUMBER: _ClassVar[int]
    MFATOTPCODE_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    email: str
    encryptedPassword: bytes
    mfaSecret: str
    mfaTotpCode: str
    deviceInfo: _gravi_model_pb2.DeviceInfo
    def __init__(self, email: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ..., mfaSecret: _Optional[str] = ..., mfaTotpCode: _Optional[str] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ...) -> None: ...

class ListSSOProvidersForEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class ListSSOProvidersForEmailResponse(_message.Message):
    __slots__ = ("ssoProviders", "ownerIds")
    SSOPROVIDERS_FIELD_NUMBER: _ClassVar[int]
    OWNERIDS_FIELD_NUMBER: _ClassVar[int]
    ssoProviders: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.SSOProvider]
    ownerIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ssoProviders: _Optional[_Iterable[_Union[_gravi_model_pb2.SSOProvider, str]]] = ..., ownerIds: _Optional[_Iterable[str]] = ...) -> None: ...

class InitiateOidcSSOLoginRequest(_message.Message):
    __slots__ = ("afterAuthRedirectUrl", "ssoProvider", "ownerId")
    AFTERAUTHREDIRECTURL_FIELD_NUMBER: _ClassVar[int]
    SSOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    afterAuthRedirectUrl: str
    ssoProvider: _gravi_model_pb2.SSOProvider
    ownerId: str
    def __init__(self, afterAuthRedirectUrl: _Optional[str] = ..., ssoProvider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., ownerId: _Optional[str] = ...) -> None: ...

class InitiateOidcSSOLoginResponse(_message.Message):
    __slots__ = ("providerRedirectUrl", "nonce", "state", "ssoProvider", "ownerId")
    PROVIDERREDIRECTURL_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SSOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    providerRedirectUrl: str
    nonce: str
    state: str
    ssoProvider: _gravi_model_pb2.SSOProvider
    ownerId: str
    def __init__(self, providerRedirectUrl: _Optional[str] = ..., nonce: _Optional[str] = ..., state: _Optional[str] = ..., ssoProvider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., ownerId: _Optional[str] = ...) -> None: ...

class CompleteOidcSSOLoginRequest(_message.Message):
    __slots__ = ("authCode", "provider", "nonce", "deviceInfo", "ownerId")
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    authCode: str
    provider: _gravi_model_pb2.SSOProvider
    nonce: str
    deviceInfo: _gravi_model_pb2.DeviceInfo
    ownerId: str
    def __init__(self, authCode: _Optional[str] = ..., provider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., nonce: _Optional[str] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., ownerId: _Optional[str] = ...) -> None: ...

class GetSSOProviderForSignupRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetSSOProviderForSignupResponse(_message.Message):
    __slots__ = ("provider", "ownerId")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    provider: _gravi_model_pb2.SSOProvider
    ownerId: str
    def __init__(self, provider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., ownerId: _Optional[str] = ...) -> None: ...

class SignUpWithSSORequest(_message.Message):
    __slots__ = ("ssoCredentials",)
    SSOCREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ssoCredentials: CompleteOidcSSOLoginRequest
    def __init__(self, ssoCredentials: _Optional[_Union[CompleteOidcSSOLoginRequest, _Mapping]] = ...) -> None: ...

class SignUpWithSSOResponse(_message.Message):
    __slots__ = ("responseCode", "invitationSentToEmail")
    RESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    INVITATIONSENTTOEMAIL_FIELD_NUMBER: _ClassVar[int]
    responseCode: SignUpWithSSOResponseCode
    invitationSentToEmail: str
    def __init__(self, responseCode: _Optional[_Union[SignUpWithSSOResponseCode, str]] = ..., invitationSentToEmail: _Optional[str] = ...) -> None: ...

class LoginByEmailRequest(_message.Message):
    __slots__ = ("email", "base64EncodedEncryptedPwd", "rememberMe", "totpCode", "os", "browser", "deviceId", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    BASE64ENCODEDENCRYPTEDPWD_FIELD_NUMBER: _ClassVar[int]
    REMEMBERME_FIELD_NUMBER: _ClassVar[int]
    TOTPCODE_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    BROWSER_FIELD_NUMBER: _ClassVar[int]
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    base64EncodedEncryptedPwd: bytes
    rememberMe: bool
    totpCode: str
    os: str
    browser: str
    deviceId: str
    password: str
    def __init__(self, email: _Optional[str] = ..., base64EncodedEncryptedPwd: _Optional[bytes] = ..., rememberMe: bool = ..., totpCode: _Optional[str] = ..., os: _Optional[str] = ..., browser: _Optional[str] = ..., deviceId: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ChangeEmailRequest(_message.Message):
    __slots__ = ("newEmail",)
    NEWEMAIL_FIELD_NUMBER: _ClassVar[int]
    newEmail: str
    def __init__(self, newEmail: _Optional[str] = ...) -> None: ...

class ChangeEmailResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ChangeEmailResponseCode
    def __init__(self, code: _Optional[_Union[ChangeEmailResponseCode, str]] = ...) -> None: ...

class ChangePasswordRequest(_message.Message):
    __slots__ = ("oldBase64EncodedEncryptedPwd", "newBase64EncodedEncryptedPwd")
    OLDBASE64ENCODEDENCRYPTEDPWD_FIELD_NUMBER: _ClassVar[int]
    NEWBASE64ENCODEDENCRYPTEDPWD_FIELD_NUMBER: _ClassVar[int]
    oldBase64EncodedEncryptedPwd: bytes
    newBase64EncodedEncryptedPwd: bytes
    def __init__(self, oldBase64EncodedEncryptedPwd: _Optional[bytes] = ..., newBase64EncodedEncryptedPwd: _Optional[bytes] = ...) -> None: ...

class ChangePasswordResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ChangePasswordResponseCode
    def __init__(self, code: _Optional[_Union[ChangePasswordResponseCode, str]] = ...) -> None: ...

class EnableTwoFactorAuthRequest(_message.Message):
    __slots__ = ("totopCode",)
    TOTOPCODE_FIELD_NUMBER: _ClassVar[int]
    totopCode: str
    def __init__(self, totopCode: _Optional[str] = ...) -> None: ...

class EnableTwoFactorAuthResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class SendPasswordResetEmailRequest(_message.Message):
    __slots__ = ("email", "reCaptchaToken")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    RECAPTCHATOKEN_FIELD_NUMBER: _ClassVar[int]
    email: str
    reCaptchaToken: str
    def __init__(self, email: _Optional[str] = ..., reCaptchaToken: _Optional[str] = ...) -> None: ...

class ResetPasswordRequest(_message.Message):
    __slots__ = ("resetId", "base64EncodedEncryptedPwd", "reCaptchaToken")
    RESETID_FIELD_NUMBER: _ClassVar[int]
    BASE64ENCODEDENCRYPTEDPWD_FIELD_NUMBER: _ClassVar[int]
    RECAPTCHATOKEN_FIELD_NUMBER: _ClassVar[int]
    resetId: str
    base64EncodedEncryptedPwd: bytes
    reCaptchaToken: str
    def __init__(self, resetId: _Optional[str] = ..., base64EncodedEncryptedPwd: _Optional[bytes] = ..., reCaptchaToken: _Optional[str] = ...) -> None: ...

class CompleteSignUpByCodeRequest(_message.Message):
    __slots__ = ("base64EncodedEncryptedPwd", "magicLinkCode", "firstName", "lastName")
    BASE64ENCODEDENCRYPTEDPWD_FIELD_NUMBER: _ClassVar[int]
    MAGICLINKCODE_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    base64EncodedEncryptedPwd: bytes
    magicLinkCode: str
    firstName: str
    lastName: str
    def __init__(self, base64EncodedEncryptedPwd: _Optional[bytes] = ..., magicLinkCode: _Optional[str] = ..., firstName: _Optional[str] = ..., lastName: _Optional[str] = ...) -> None: ...

class CompleteSignUpByCodeResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: CompleteSignUpByCodeResponseCode
    def __init__(self, code: _Optional[_Union[CompleteSignUpByCodeResponseCode, str]] = ...) -> None: ...

class ListUserLoginAuditsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUserLoginAuditsResponse(_message.Message):
    __slots__ = ("securityAudits",)
    SECURITYAUDITS_FIELD_NUMBER: _ClassVar[int]
    securityAudits: _containers.RepeatedCompositeFieldContainer[UserSecurityAudit]
    def __init__(self, securityAudits: _Optional[_Iterable[_Union[UserSecurityAudit, _Mapping]]] = ...) -> None: ...

class GenerateSecretKeyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenerateSecretKeyResponse(_message.Message):
    __slots__ = ("secretKey",)
    SECRETKEY_FIELD_NUMBER: _ClassVar[int]
    secretKey: str
    def __init__(self, secretKey: _Optional[str] = ...) -> None: ...

class UserSecurityAudit(_message.Message):
    __slots__ = ("userId", "userDeviceId", "userName", "userEmail", "deviceName", "userIp", "timestamp", "eventType", "eventDetail", "eventTypeName")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERDEVICEID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    DEVICENAME_FIELD_NUMBER: _ClassVar[int]
    USERIP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENTTYPE_FIELD_NUMBER: _ClassVar[int]
    EVENTDETAIL_FIELD_NUMBER: _ClassVar[int]
    EVENTTYPENAME_FIELD_NUMBER: _ClassVar[int]
    userId: str
    userDeviceId: str
    userName: str
    userEmail: str
    deviceName: str
    userIp: str
    timestamp: int
    eventType: SecurityEventType
    eventDetail: SecurityEventDetail
    eventTypeName: str
    def __init__(self, userId: _Optional[str] = ..., userDeviceId: _Optional[str] = ..., userName: _Optional[str] = ..., userEmail: _Optional[str] = ..., deviceName: _Optional[str] = ..., userIp: _Optional[str] = ..., timestamp: _Optional[int] = ..., eventType: _Optional[_Union[SecurityEventType, str]] = ..., eventDetail: _Optional[_Union[SecurityEventDetail, _Mapping]] = ..., eventTypeName: _Optional[str] = ...) -> None: ...

class SecurityEventDetail(_message.Message):
    __slots__ = ("changedOrgUserStatus", "changedOrgUserRole", "invitedOrgUsers", "deletedOrgUser", "userJoinedOrg", "setRoomPass", "createdOrgTeam", "deletedOrgTeam", "updatedOrgTeam", "createdDoc", "updatedDoc", "downloadedDoc", "exportedDoc", "sharedDoc", "trashedDoc", "restoredDoc", "deletedDoc", "sentDoc", "acceptedDoc", "setDocPassword", "changeUserCollabRole", "removeUserAccess", "attachDevice", "detachDevice", "securityEventApproveOrDenyJoinOrg")
    CHANGEDORGUSERSTATUS_FIELD_NUMBER: _ClassVar[int]
    CHANGEDORGUSERROLE_FIELD_NUMBER: _ClassVar[int]
    INVITEDORGUSERS_FIELD_NUMBER: _ClassVar[int]
    DELETEDORGUSER_FIELD_NUMBER: _ClassVar[int]
    USERJOINEDORG_FIELD_NUMBER: _ClassVar[int]
    SETROOMPASS_FIELD_NUMBER: _ClassVar[int]
    CREATEDORGTEAM_FIELD_NUMBER: _ClassVar[int]
    DELETEDORGTEAM_FIELD_NUMBER: _ClassVar[int]
    UPDATEDORGTEAM_FIELD_NUMBER: _ClassVar[int]
    CREATEDDOC_FIELD_NUMBER: _ClassVar[int]
    UPDATEDDOC_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADEDDOC_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDDOC_FIELD_NUMBER: _ClassVar[int]
    SHAREDDOC_FIELD_NUMBER: _ClassVar[int]
    TRASHEDDOC_FIELD_NUMBER: _ClassVar[int]
    RESTOREDDOC_FIELD_NUMBER: _ClassVar[int]
    DELETEDDOC_FIELD_NUMBER: _ClassVar[int]
    SENTDOC_FIELD_NUMBER: _ClassVar[int]
    ACCEPTEDDOC_FIELD_NUMBER: _ClassVar[int]
    SETDOCPASSWORD_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERCOLLABROLE_FIELD_NUMBER: _ClassVar[int]
    REMOVEUSERACCESS_FIELD_NUMBER: _ClassVar[int]
    ATTACHDEVICE_FIELD_NUMBER: _ClassVar[int]
    DETACHDEVICE_FIELD_NUMBER: _ClassVar[int]
    SECURITYEVENTAPPROVEORDENYJOINORG_FIELD_NUMBER: _ClassVar[int]
    changedOrgUserStatus: ChangedOrgUserStatus
    changedOrgUserRole: ChangedOrgUserRole
    invitedOrgUsers: InvitedOrgUsers
    deletedOrgUser: DeletedOrgUser
    userJoinedOrg: UserJoinedOrg
    setRoomPass: SecurityEventSetRoomPass
    createdOrgTeam: SecurityEventDetailCreatedOrgTeam
    deletedOrgTeam: SecurityEventDetailDeletedOrgTeam
    updatedOrgTeam: SecurityEventDetailUpdatedOrgTeam
    createdDoc: SecurityDocEventDetailCreateDoc
    updatedDoc: SecurityDocEventDetailUpdateDoc
    downloadedDoc: SecurityDocEventDetailDownloadDoc
    exportedDoc: SecurityDocEventDetailExportDoc
    sharedDoc: SecurityDocEventDetailShareDoc
    trashedDoc: SecurityDocEventDetailTrashDoc
    restoredDoc: SecurityDocEventDetailRestoreDoc
    deletedDoc: SecurityDocEventDetailDeleteDoc
    sentDoc: SecurityDocEventDetailSendDoc
    acceptedDoc: SecurityDocEventDetailAcceptDoc
    setDocPassword: SecurityDocEventDetailSetPassword
    changeUserCollabRole: SecurityDocEventDetailChangeUserCollabRole
    removeUserAccess: SecurityDocEventDetailRemoveUserAccess
    attachDevice: SecurityEventAttachDevice
    detachDevice: SecurityEventDetachDevice
    securityEventApproveOrDenyJoinOrg: SecurityEventApproveOrDenyJoinOrg
    def __init__(self, changedOrgUserStatus: _Optional[_Union[ChangedOrgUserStatus, _Mapping]] = ..., changedOrgUserRole: _Optional[_Union[ChangedOrgUserRole, _Mapping]] = ..., invitedOrgUsers: _Optional[_Union[InvitedOrgUsers, _Mapping]] = ..., deletedOrgUser: _Optional[_Union[DeletedOrgUser, _Mapping]] = ..., userJoinedOrg: _Optional[_Union[UserJoinedOrg, _Mapping]] = ..., setRoomPass: _Optional[_Union[SecurityEventSetRoomPass, _Mapping]] = ..., createdOrgTeam: _Optional[_Union[SecurityEventDetailCreatedOrgTeam, _Mapping]] = ..., deletedOrgTeam: _Optional[_Union[SecurityEventDetailDeletedOrgTeam, _Mapping]] = ..., updatedOrgTeam: _Optional[_Union[SecurityEventDetailUpdatedOrgTeam, _Mapping]] = ..., createdDoc: _Optional[_Union[SecurityDocEventDetailCreateDoc, _Mapping]] = ..., updatedDoc: _Optional[_Union[SecurityDocEventDetailUpdateDoc, _Mapping]] = ..., downloadedDoc: _Optional[_Union[SecurityDocEventDetailDownloadDoc, _Mapping]] = ..., exportedDoc: _Optional[_Union[SecurityDocEventDetailExportDoc, _Mapping]] = ..., sharedDoc: _Optional[_Union[SecurityDocEventDetailShareDoc, _Mapping]] = ..., trashedDoc: _Optional[_Union[SecurityDocEventDetailTrashDoc, _Mapping]] = ..., restoredDoc: _Optional[_Union[SecurityDocEventDetailRestoreDoc, _Mapping]] = ..., deletedDoc: _Optional[_Union[SecurityDocEventDetailDeleteDoc, _Mapping]] = ..., sentDoc: _Optional[_Union[SecurityDocEventDetailSendDoc, _Mapping]] = ..., acceptedDoc: _Optional[_Union[SecurityDocEventDetailAcceptDoc, _Mapping]] = ..., setDocPassword: _Optional[_Union[SecurityDocEventDetailSetPassword, _Mapping]] = ..., changeUserCollabRole: _Optional[_Union[SecurityDocEventDetailChangeUserCollabRole, _Mapping]] = ..., removeUserAccess: _Optional[_Union[SecurityDocEventDetailRemoveUserAccess, _Mapping]] = ..., attachDevice: _Optional[_Union[SecurityEventAttachDevice, _Mapping]] = ..., detachDevice: _Optional[_Union[SecurityEventDetachDevice, _Mapping]] = ..., securityEventApproveOrDenyJoinOrg: _Optional[_Union[SecurityEventApproveOrDenyJoinOrg, _Mapping]] = ...) -> None: ...

class AuditUserInfoSnapshot(_message.Message):
    __slots__ = ("userId", "userDisplayName", "userEmail")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    userId: str
    userDisplayName: str
    userEmail: str
    def __init__(self, userId: _Optional[str] = ..., userDisplayName: _Optional[str] = ..., userEmail: _Optional[str] = ...) -> None: ...

class ChangedOrgUserStatus(_message.Message):
    __slots__ = ("objectUser", "oldStatus", "newStatus")
    OBJECTUSER_FIELD_NUMBER: _ClassVar[int]
    OLDSTATUS_FIELD_NUMBER: _ClassVar[int]
    NEWSTATUS_FIELD_NUMBER: _ClassVar[int]
    objectUser: AuditUserInfoSnapshot
    oldStatus: _gravi_model_pb2.OrgMemberStatus
    newStatus: _gravi_model_pb2.OrgMemberStatus
    def __init__(self, objectUser: _Optional[_Union[AuditUserInfoSnapshot, _Mapping]] = ..., oldStatus: _Optional[_Union[_gravi_model_pb2.OrgMemberStatus, str]] = ..., newStatus: _Optional[_Union[_gravi_model_pb2.OrgMemberStatus, str]] = ...) -> None: ...

class ChangedOrgUserRole(_message.Message):
    __slots__ = ("objectUser", "oldRole", "newRole")
    OBJECTUSER_FIELD_NUMBER: _ClassVar[int]
    OLDROLE_FIELD_NUMBER: _ClassVar[int]
    NEWROLE_FIELD_NUMBER: _ClassVar[int]
    objectUser: AuditUserInfoSnapshot
    oldRole: _gravi_model_pb2.OrgMemberRole
    newRole: _gravi_model_pb2.OrgMemberRole
    def __init__(self, objectUser: _Optional[_Union[AuditUserInfoSnapshot, _Mapping]] = ..., oldRole: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., newRole: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ...) -> None: ...

class InvitedOrgUsers(_message.Message):
    __slots__ = ("invitedEmails", "invitedAsOrgAccounts")
    INVITEDEMAILS_FIELD_NUMBER: _ClassVar[int]
    INVITEDASORGACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    invitedEmails: _containers.RepeatedScalarFieldContainer[str]
    invitedAsOrgAccounts: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, invitedEmails: _Optional[_Iterable[str]] = ..., invitedAsOrgAccounts: _Optional[_Iterable[bool]] = ...) -> None: ...

class DeletedOrgUser(_message.Message):
    __slots__ = ("objectUser",)
    OBJECTUSER_FIELD_NUMBER: _ClassVar[int]
    objectUser: AuditUserInfoSnapshot
    def __init__(self, objectUser: _Optional[_Union[AuditUserInfoSnapshot, _Mapping]] = ...) -> None: ...

class UserJoinedOrg(_message.Message):
    __slots__ = ("isOrgAccount",)
    ISORGACCOUNT_FIELD_NUMBER: _ClassVar[int]
    isOrgAccount: bool
    def __init__(self, isOrgAccount: bool = ...) -> None: ...

class SecurityEventSetRoomPass(_message.Message):
    __slots__ = ("roomId", "roomName")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMNAME_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    roomName: str
    def __init__(self, roomId: _Optional[str] = ..., roomName: _Optional[str] = ...) -> None: ...

class SecurityEventDetailCreatedOrgTeam(_message.Message):
    __slots__ = ("teamId", "teamName", "usersAdded", "userRolesWhenAdded")
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    TEAMNAME_FIELD_NUMBER: _ClassVar[int]
    USERSADDED_FIELD_NUMBER: _ClassVar[int]
    USERROLESWHENADDED_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    teamName: str
    usersAdded: _containers.RepeatedCompositeFieldContainer[AuditUserInfoSnapshot]
    userRolesWhenAdded: _containers.RepeatedScalarFieldContainer[_team_pb2.OrgTeamRole]
    def __init__(self, teamId: _Optional[str] = ..., teamName: _Optional[str] = ..., usersAdded: _Optional[_Iterable[_Union[AuditUserInfoSnapshot, _Mapping]]] = ..., userRolesWhenAdded: _Optional[_Iterable[_Union[_team_pb2.OrgTeamRole, str]]] = ...) -> None: ...

class SecurityEventDetailDeletedOrgTeam(_message.Message):
    __slots__ = ("teamId", "teamName")
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    TEAMNAME_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    teamName: str
    def __init__(self, teamId: _Optional[str] = ..., teamName: _Optional[str] = ...) -> None: ...

class SecurityEventDetailUpdatedOrgTeam(_message.Message):
    __slots__ = ("teamId", "oldTeamName", "newTeamName", "usersRemoved", "usersAdded", "userRolesWhenAdded", "updatedAllowExternalMembers")
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    OLDTEAMNAME_FIELD_NUMBER: _ClassVar[int]
    NEWTEAMNAME_FIELD_NUMBER: _ClassVar[int]
    USERSREMOVED_FIELD_NUMBER: _ClassVar[int]
    USERSADDED_FIELD_NUMBER: _ClassVar[int]
    USERROLESWHENADDED_FIELD_NUMBER: _ClassVar[int]
    UPDATEDALLOWEXTERNALMEMBERS_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    oldTeamName: str
    newTeamName: str
    usersRemoved: _containers.RepeatedCompositeFieldContainer[AuditUserInfoSnapshot]
    usersAdded: _containers.RepeatedCompositeFieldContainer[AuditUserInfoSnapshot]
    userRolesWhenAdded: _containers.RepeatedScalarFieldContainer[_team_pb2.OrgTeamRole]
    updatedAllowExternalMembers: _wrappers_pb2.OptionalBool
    def __init__(self, teamId: _Optional[str] = ..., oldTeamName: _Optional[str] = ..., newTeamName: _Optional[str] = ..., usersRemoved: _Optional[_Iterable[_Union[AuditUserInfoSnapshot, _Mapping]]] = ..., usersAdded: _Optional[_Iterable[_Union[AuditUserInfoSnapshot, _Mapping]]] = ..., userRolesWhenAdded: _Optional[_Iterable[_Union[_team_pb2.OrgTeamRole, str]]] = ..., updatedAllowExternalMembers: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ...) -> None: ...

class SecurityAuditInfo(_message.Message):
    __slots__ = ("os", "browser")
    OS_FIELD_NUMBER: _ClassVar[int]
    BROWSER_FIELD_NUMBER: _ClassVar[int]
    os: str
    browser: str
    def __init__(self, os: _Optional[str] = ..., browser: _Optional[str] = ...) -> None: ...

class SignupByOculusPlatformResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: StoreSignupResult
    def __init__(self, result: _Optional[_Union[StoreSignupResult, str]] = ...) -> None: ...

class SignupBySteamPlatformResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: StoreSignupResult
    def __init__(self, result: _Optional[_Union[StoreSignupResult, str]] = ...) -> None: ...

class SecurityDocEventDetailCreateDoc(_message.Message):
    __slots__ = ("docInfo",)
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ...) -> None: ...

class SecurityDocEventDetailUpdateDoc(_message.Message):
    __slots__ = ("docInfo", "newDocName", "newSpaceName")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    NEWDOCNAME_FIELD_NUMBER: _ClassVar[int]
    NEWSPACENAME_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    newDocName: str
    newSpaceName: str
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., newDocName: _Optional[str] = ..., newSpaceName: _Optional[str] = ...) -> None: ...

class SecurityDocEventDetailDownloadDoc(_message.Message):
    __slots__ = ("docInfo",)
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ...) -> None: ...

class SecurityDocEventDetailExportDoc(_message.Message):
    __slots__ = ("docInfo", "exportedDocName", "exportedDocType")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDDOCNAME_FIELD_NUMBER: _ClassVar[int]
    EXPORTEDDOCTYPE_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    exportedDocName: str
    exportedDocType: _gravi_model_pb2.DocumentType
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., exportedDocName: _Optional[str] = ..., exportedDocType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ...) -> None: ...

class SecurityDocEventDetailShareDoc(_message.Message):
    __slots__ = ("docInfo", "receiverEmail", "collabRole")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    RECEIVEREMAIL_FIELD_NUMBER: _ClassVar[int]
    COLLABROLE_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    receiverEmail: str
    collabRole: _gravi_model_pb2.CollaborationRole
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., receiverEmail: _Optional[str] = ..., collabRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class SecurityDocEventDetailTrashDoc(_message.Message):
    __slots__ = ("docInfo",)
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ...) -> None: ...

class SecurityDocEventDetailRestoreDoc(_message.Message):
    __slots__ = ("docInfo", "restoredDocPath")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    RESTOREDDOCPATH_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    restoredDocPath: str
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., restoredDocPath: _Optional[str] = ...) -> None: ...

class SecurityDocEventDetailDeleteDoc(_message.Message):
    __slots__ = ("docInfo",)
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ...) -> None: ...

class SecurityDocEventDetailSendDoc(_message.Message):
    __slots__ = ("docInfo", "receiverEmail")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    RECEIVEREMAIL_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    receiverEmail: str
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., receiverEmail: _Optional[str] = ...) -> None: ...

class SecurityDocEventDetailAcceptDoc(_message.Message):
    __slots__ = ("docInfo", "senderEmail")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    SENDEREMAIL_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    senderEmail: str
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., senderEmail: _Optional[str] = ...) -> None: ...

class SecurityDocEventDetailSetPassword(_message.Message):
    __slots__ = ("docInfo",)
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ...) -> None: ...

class SecurityDocEventDetailBasicDoc(_message.Message):
    __slots__ = ("docName", "docType", "spaceName", "docId")
    DOCNAME_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    SPACENAME_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docName: str
    docType: _gravi_model_pb2.DocumentType
    spaceName: str
    docId: str
    def __init__(self, docName: _Optional[str] = ..., docType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., spaceName: _Optional[str] = ..., docId: _Optional[str] = ...) -> None: ...

class SecurityDocEventDetailChangeUserCollabRole(_message.Message):
    __slots__ = ("docInfo", "targetUserEmail", "oldRole", "newRole")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    TARGETUSEREMAIL_FIELD_NUMBER: _ClassVar[int]
    OLDROLE_FIELD_NUMBER: _ClassVar[int]
    NEWROLE_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    targetUserEmail: str
    oldRole: _gravi_model_pb2.CollaborationRole
    newRole: _gravi_model_pb2.CollaborationRole
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., targetUserEmail: _Optional[str] = ..., oldRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., newRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class SecurityDocEventDetailRemoveUserAccess(_message.Message):
    __slots__ = ("docInfo", "targetUserEmail")
    DOCINFO_FIELD_NUMBER: _ClassVar[int]
    TARGETUSEREMAIL_FIELD_NUMBER: _ClassVar[int]
    docInfo: SecurityDocEventDetailBasicDoc
    targetUserEmail: str
    def __init__(self, docInfo: _Optional[_Union[SecurityDocEventDetailBasicDoc, _Mapping]] = ..., targetUserEmail: _Optional[str] = ...) -> None: ...

class SecurityEventAttachDevice(_message.Message):
    __slots__ = ("deviceName", "deviceType")
    DEVICENAME_FIELD_NUMBER: _ClassVar[int]
    DEVICETYPE_FIELD_NUMBER: _ClassVar[int]
    deviceName: str
    deviceType: DetachDeviceType
    def __init__(self, deviceName: _Optional[str] = ..., deviceType: _Optional[_Union[DetachDeviceType, str]] = ...) -> None: ...

class SecurityEventDetachDevice(_message.Message):
    __slots__ = ("deviceName", "deviceType")
    DEVICENAME_FIELD_NUMBER: _ClassVar[int]
    DEVICETYPE_FIELD_NUMBER: _ClassVar[int]
    deviceName: str
    deviceType: DetachDeviceType
    def __init__(self, deviceName: _Optional[str] = ..., deviceType: _Optional[_Union[DetachDeviceType, str]] = ...) -> None: ...

class SecurityEventApproveOrDenyJoinOrg(_message.Message):
    __slots__ = ("orgId", "email", "role", "orgAccountInvite", "approve")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ORGACCOUNTINVITE_FIELD_NUMBER: _ClassVar[int]
    APPROVE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    email: str
    role: _gravi_model_pb2.OrgMemberRole
    orgAccountInvite: bool
    approve: bool
    def __init__(self, orgId: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., orgAccountInvite: bool = ..., approve: bool = ...) -> None: ...
