import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeviceInfo: _ClassVar[AuthType]
    EmailPass: _ClassVar[AuthType]
    UserName: _ClassVar[AuthType]

class LoginResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LoginUnknown: _ClassVar[LoginResult]
    LoginSuccess: _ClassVar[LoginResult]
    LoginIncorrectEmailOrPassword: _ClassVar[LoginResult]
    LoginFailure: _ClassVar[LoginResult]
    Login3rdPartyAccountAlreadyLinkedToAnotherLpAccount: _ClassVar[LoginResult]
    LoginSuspendedAccount: _ClassVar[LoginResult]
    LoginEmailAlreadyLinked: _ClassVar[LoginResult]
    LoginAccountLocked: _ClassVar[LoginResult]
    LoginAccountEmailNotActivated: _ClassVar[LoginResult]
    Login3rdPartyAccountNotLinkedToAnyLpAccount: _ClassVar[LoginResult]
    LoginLpAccountAlreadyLinkedToAnother3rdPartyAccount: _ClassVar[LoginResult]
    LoginViveStoreSuccess: _ClassVar[LoginResult]
    LoginMfaRequired: _ClassVar[LoginResult]
    LoginMfaCodeSecretMismatch: _ClassVar[LoginResult]
    LoginResultMfaAlreadyConfigured: _ClassVar[LoginResult]
    LoginSSOLoginRequired: _ClassVar[LoginResult]
    LoginUnityUserIdConflict: _ClassVar[LoginResult]
    LoginExceedSeatCount: _ClassVar[LoginResult]
    LoginAccountLockedToOrg: _ClassVar[LoginResult]
    LoginSSONonceExpired: _ClassVar[LoginResult]
    LoginSSOErrorFromIdentityProvider: _ClassVar[LoginResult]
    LoginSSOUserInMultipleOrgs: _ClassVar[LoginResult]
    LoginSSOUserInNoOrgs: _ClassVar[LoginResult]
    LoginSSOOrgDoesNotUseSSO: _ClassVar[LoginResult]
    LoginSSONoLPAccountWithMatchingEmailToBindTo: _ClassVar[LoginResult]
    LoginSSONeedToCreateAccount: _ClassVar[LoginResult]
    LoginSSOClientTookTooLongBetweenRequests: _ClassVar[LoginResult]
    LoginNoConnection: _ClassVar[LoginResult]
    LoginInvalidPairingCode: _ClassVar[LoginResult]
    LoginUserAlreadyHasPairedDevice: _ClassVar[LoginResult]
    LoginDeviceIdAlreadyPairedToAnotherUser: _ClassVar[LoginResult]
    LoginOrgSecPolicyMfaEnforcement: _ClassVar[LoginResult]
DeviceInfo: AuthType
EmailPass: AuthType
UserName: AuthType
LoginUnknown: LoginResult
LoginSuccess: LoginResult
LoginIncorrectEmailOrPassword: LoginResult
LoginFailure: LoginResult
Login3rdPartyAccountAlreadyLinkedToAnotherLpAccount: LoginResult
LoginSuspendedAccount: LoginResult
LoginEmailAlreadyLinked: LoginResult
LoginAccountLocked: LoginResult
LoginAccountEmailNotActivated: LoginResult
Login3rdPartyAccountNotLinkedToAnyLpAccount: LoginResult
LoginLpAccountAlreadyLinkedToAnother3rdPartyAccount: LoginResult
LoginViveStoreSuccess: LoginResult
LoginMfaRequired: LoginResult
LoginMfaCodeSecretMismatch: LoginResult
LoginResultMfaAlreadyConfigured: LoginResult
LoginSSOLoginRequired: LoginResult
LoginUnityUserIdConflict: LoginResult
LoginExceedSeatCount: LoginResult
LoginAccountLockedToOrg: LoginResult
LoginSSONonceExpired: LoginResult
LoginSSOErrorFromIdentityProvider: LoginResult
LoginSSOUserInMultipleOrgs: LoginResult
LoginSSOUserInNoOrgs: LoginResult
LoginSSOOrgDoesNotUseSSO: LoginResult
LoginSSONoLPAccountWithMatchingEmailToBindTo: LoginResult
LoginSSONeedToCreateAccount: LoginResult
LoginSSOClientTookTooLongBetweenRequests: LoginResult
LoginNoConnection: LoginResult
LoginInvalidPairingCode: LoginResult
LoginUserAlreadyHasPairedDevice: LoginResult
LoginDeviceIdAlreadyPairedToAnotherUser: LoginResult
LoginOrgSecPolicyMfaEnforcement: LoginResult

class LoginRequest(_message.Message):
    __slots__ = ("loginType", "userName", "encryptedPassword", "userId", "deviceInfo", "email", "rememberMe")
    LOGINTYPE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    REMEMBERME_FIELD_NUMBER: _ClassVar[int]
    loginType: AuthType
    userName: str
    encryptedPassword: bytes
    userId: str
    deviceInfo: _gravi_model_pb2.DeviceInfo
    email: str
    rememberMe: bool
    def __init__(self, loginType: _Optional[_Union[AuthType, str]] = ..., userName: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ..., userId: _Optional[str] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., email: _Optional[str] = ..., rememberMe: bool = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("result", "ticket", "authDetail", "mfaSecretKey")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    AUTHDETAIL_FIELD_NUMBER: _ClassVar[int]
    MFASECRETKEY_FIELD_NUMBER: _ClassVar[int]
    result: LoginResult
    ticket: _gravi_model_pb2.IDTicket
    authDetail: _gravi_model_pb2.AuthDetail
    mfaSecretKey: str
    def __init__(self, result: _Optional[_Union[LoginResult, str]] = ..., ticket: _Optional[_Union[_gravi_model_pb2.IDTicket, _Mapping]] = ..., authDetail: _Optional[_Union[_gravi_model_pb2.AuthDetail, _Mapping]] = ..., mfaSecretKey: _Optional[str] = ...) -> None: ...
