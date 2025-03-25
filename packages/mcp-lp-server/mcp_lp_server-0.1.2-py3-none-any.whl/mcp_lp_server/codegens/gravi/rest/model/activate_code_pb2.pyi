import gs_options_pb2 as _gs_options_pb2
from gravi.rest.auth import auth_pb2 as _auth_pb2
from gravi.rest.model import login_pb2 as _login_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActivateCodeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ActivateCodeType_Unknown: _ClassVar[ActivateCodeType]
    ActivateCodeType_SteamSignup: _ClassVar[ActivateCodeType]
    ActivateCodeType_OculusSignup: _ClassVar[ActivateCodeType]
    ActivateCodeType_ActivateAccount: _ClassVar[ActivateCodeType]
    ActivateCodeType_OrgInv: _ClassVar[ActivateCodeType]
    ActivateCodeType_OneTimeLogin: _ClassVar[ActivateCodeType]
    ActivateCodeType_InitiateSignUp: _ClassVar[ActivateCodeType]
    ActivateCodeType_BindOidcUniqueId: _ClassVar[ActivateCodeType]
    ActivateCodeType_ChangeEmail: _ClassVar[ActivateCodeType]
    ActivateCodeType_SendDocument: _ClassVar[ActivateCodeType]
    ActivateCodeType_ShareRoom: _ClassVar[ActivateCodeType]

class ActivateCodeResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ActivateCodeResult_Success: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_LinkNotFoundOrExpired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_SendDocSignupRequired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_SendDocNoLongerExists: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_InvalidCodeType: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_UserAddedToOrg: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_SSOSignupRequired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_EmailAccountAlreadyExists: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_ShareRoomNoLongerExists: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_OIDCIDAlreadyInUse: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_OIDCEmailDoesntMatchActivationLink: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_OIDCSSOFailure: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_ReCaptchaFailure: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_NotEnoughSeats: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_CodeAlreadyActivated: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_ActivationFailed: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_SSOLoginRequired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_MfaSetupRequired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_MfaLoginRequired: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_TeamNotFoundOrDeleted: _ClassVar[ActivateCodeResult]
    ActivateCodeResult_AccountAlreadyExistsInAnotherOrg: _ClassVar[ActivateCodeResult]
ActivateCodeType_Unknown: ActivateCodeType
ActivateCodeType_SteamSignup: ActivateCodeType
ActivateCodeType_OculusSignup: ActivateCodeType
ActivateCodeType_ActivateAccount: ActivateCodeType
ActivateCodeType_OrgInv: ActivateCodeType
ActivateCodeType_OneTimeLogin: ActivateCodeType
ActivateCodeType_InitiateSignUp: ActivateCodeType
ActivateCodeType_BindOidcUniqueId: ActivateCodeType
ActivateCodeType_ChangeEmail: ActivateCodeType
ActivateCodeType_SendDocument: ActivateCodeType
ActivateCodeType_ShareRoom: ActivateCodeType
ActivateCodeResult_Success: ActivateCodeResult
ActivateCodeResult_LinkNotFoundOrExpired: ActivateCodeResult
ActivateCodeResult_SendDocSignupRequired: ActivateCodeResult
ActivateCodeResult_SendDocNoLongerExists: ActivateCodeResult
ActivateCodeResult_InvalidCodeType: ActivateCodeResult
ActivateCodeResult_UserAddedToOrg: ActivateCodeResult
ActivateCodeResult_SSOSignupRequired: ActivateCodeResult
ActivateCodeResult_EmailAccountAlreadyExists: ActivateCodeResult
ActivateCodeResult_ShareRoomNoLongerExists: ActivateCodeResult
ActivateCodeResult_OIDCIDAlreadyInUse: ActivateCodeResult
ActivateCodeResult_OIDCEmailDoesntMatchActivationLink: ActivateCodeResult
ActivateCodeResult_OIDCSSOFailure: ActivateCodeResult
ActivateCodeResult_ReCaptchaFailure: ActivateCodeResult
ActivateCodeResult_NotEnoughSeats: ActivateCodeResult
ActivateCodeResult_CodeAlreadyActivated: ActivateCodeResult
ActivateCodeResult_ActivationFailed: ActivateCodeResult
ActivateCodeResult_SSOLoginRequired: ActivateCodeResult
ActivateCodeResult_MfaSetupRequired: ActivateCodeResult
ActivateCodeResult_MfaLoginRequired: ActivateCodeResult
ActivateCodeResult_TeamNotFoundOrDeleted: ActivateCodeResult
ActivateCodeResult_AccountAlreadyExistsInAnotherOrg: ActivateCodeResult

class ActivateCodeRequest(_message.Message):
    __slots__ = ("activateCodeType", "linkCode", "deactivateCode", "completeOidcSSOLoginRequest", "totpCode", "autoLogin")
    ACTIVATECODETYPE_FIELD_NUMBER: _ClassVar[int]
    LINKCODE_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATECODE_FIELD_NUMBER: _ClassVar[int]
    COMPLETEOIDCSSOLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    TOTPCODE_FIELD_NUMBER: _ClassVar[int]
    AUTOLOGIN_FIELD_NUMBER: _ClassVar[int]
    activateCodeType: ActivateCodeType
    linkCode: str
    deactivateCode: bool
    completeOidcSSOLoginRequest: _auth_pb2.CompleteOidcSSOLoginRequest
    totpCode: str
    autoLogin: bool
    def __init__(self, activateCodeType: _Optional[_Union[ActivateCodeType, str]] = ..., linkCode: _Optional[str] = ..., deactivateCode: bool = ..., completeOidcSSOLoginRequest: _Optional[_Union[_auth_pb2.CompleteOidcSSOLoginRequest, _Mapping]] = ..., totpCode: _Optional[str] = ..., autoLogin: bool = ...) -> None: ...

class ActivateCodeResponse(_message.Message):
    __slots__ = ("result", "email", "newDocId", "ssoProvider", "loginResponse", "newDocSpaceId", "isSSOSetupMissingForOrgDNS", "isMFASetupMissingForOrgDNS", "ownerIdForSso")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NEWDOCID_FIELD_NUMBER: _ClassVar[int]
    SSOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    LOGINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    NEWDOCSPACEID_FIELD_NUMBER: _ClassVar[int]
    ISSSOSETUPMISSINGFORORGDNS_FIELD_NUMBER: _ClassVar[int]
    ISMFASETUPMISSINGFORORGDNS_FIELD_NUMBER: _ClassVar[int]
    OWNERIDFORSSO_FIELD_NUMBER: _ClassVar[int]
    result: ActivateCodeResult
    email: str
    newDocId: str
    ssoProvider: _gravi_model_pb2.SSOProvider
    loginResponse: _login_pb2.LoginResponse
    newDocSpaceId: _gravi_model_pb2.SpaceId
    isSSOSetupMissingForOrgDNS: bool
    isMFASetupMissingForOrgDNS: bool
    ownerIdForSso: str
    def __init__(self, result: _Optional[_Union[ActivateCodeResult, str]] = ..., email: _Optional[str] = ..., newDocId: _Optional[str] = ..., ssoProvider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., loginResponse: _Optional[_Union[_login_pb2.LoginResponse, _Mapping]] = ..., newDocSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., isSSOSetupMissingForOrgDNS: bool = ..., isMFASetupMissingForOrgDNS: bool = ..., ownerIdForSso: _Optional[str] = ...) -> None: ...
