import gs_options_pb2 as _gs_options_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteOrgMembershipInvitationResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeleteOrgMembershipInvitationResponseCodeUnknown: _ClassVar[DeleteOrgMembershipInvitationResponseCode]
    DeleteOrgMembershipInvitationResponseCodeSuccess: _ClassVar[DeleteOrgMembershipInvitationResponseCode]
    DeleteOrgMembershipInvitationResponseCodeNotFound: _ClassVar[DeleteOrgMembershipInvitationResponseCode]
    DeleteOrgMembershipInvitationResponseCodeNotAllowed: _ClassVar[DeleteOrgMembershipInvitationResponseCode]

class CreateOrgAccountsByOrgAdminResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateOrgAccountsByOrgAdminResponseCode_Unknown: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
    CreateOrgAccountsByOrgAdminResponseCode_Success: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
    CreateOrgAccountsByOrgAdminResponseCode_AccountAlreadyExists: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
    CreateOrgAccountsByOrgAdminResponseCode_NotEnoughSeats: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
    CreateOrgAccountsByOrgAdminResponseCode_InvalidEmail: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
    CreateOrgAccountsByOrgAdminResponseCode_Failure: _ClassVar[CreateOrgAccountsByOrgAdminResponseCode]
DeleteOrgMembershipInvitationResponseCodeUnknown: DeleteOrgMembershipInvitationResponseCode
DeleteOrgMembershipInvitationResponseCodeSuccess: DeleteOrgMembershipInvitationResponseCode
DeleteOrgMembershipInvitationResponseCodeNotFound: DeleteOrgMembershipInvitationResponseCode
DeleteOrgMembershipInvitationResponseCodeNotAllowed: DeleteOrgMembershipInvitationResponseCode
CreateOrgAccountsByOrgAdminResponseCode_Unknown: CreateOrgAccountsByOrgAdminResponseCode
CreateOrgAccountsByOrgAdminResponseCode_Success: CreateOrgAccountsByOrgAdminResponseCode
CreateOrgAccountsByOrgAdminResponseCode_AccountAlreadyExists: CreateOrgAccountsByOrgAdminResponseCode
CreateOrgAccountsByOrgAdminResponseCode_NotEnoughSeats: CreateOrgAccountsByOrgAdminResponseCode
CreateOrgAccountsByOrgAdminResponseCode_InvalidEmail: CreateOrgAccountsByOrgAdminResponseCode
CreateOrgAccountsByOrgAdminResponseCode_Failure: CreateOrgAccountsByOrgAdminResponseCode

class OrgMembershipInvitation(_message.Message):
    __slots__ = ("orgId", "invitedEmail", "invitedOn", "expiresOn", "licenseType", "isOrgAccount", "role")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    INVITEDEMAIL_FIELD_NUMBER: _ClassVar[int]
    INVITEDON_FIELD_NUMBER: _ClassVar[int]
    EXPIRESON_FIELD_NUMBER: _ClassVar[int]
    LICENSETYPE_FIELD_NUMBER: _ClassVar[int]
    ISORGACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    invitedEmail: str
    invitedOn: int
    expiresOn: int
    licenseType: _gravi_model_pb2.OrgLicenseType
    isOrgAccount: bool
    role: _gravi_model_pb2.OrgMemberRole
    def __init__(self, orgId: _Optional[str] = ..., invitedEmail: _Optional[str] = ..., invitedOn: _Optional[int] = ..., expiresOn: _Optional[int] = ..., licenseType: _Optional[_Union[_gravi_model_pb2.OrgLicenseType, str]] = ..., isOrgAccount: bool = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ...) -> None: ...

class ListOrgMembershipInvitationsRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class ListOrgMembershipInvitationsResponse(_message.Message):
    __slots__ = ("invitations",)
    INVITATIONS_FIELD_NUMBER: _ClassVar[int]
    invitations: _containers.RepeatedCompositeFieldContainer[OrgMembershipInvitation]
    def __init__(self, invitations: _Optional[_Iterable[_Union[OrgMembershipInvitation, _Mapping]]] = ...) -> None: ...

class DeleteOrgMembershipInvitationRequest(_message.Message):
    __slots__ = ("orgId", "email")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    email: str
    def __init__(self, orgId: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class DeleteOrgMembershipInvitationResponse(_message.Message):
    __slots__ = ("deleteOrgMembershipInvitationResponseCode",)
    DELETEORGMEMBERSHIPINVITATIONRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    deleteOrgMembershipInvitationResponseCode: DeleteOrgMembershipInvitationResponseCode
    def __init__(self, deleteOrgMembershipInvitationResponseCode: _Optional[_Union[DeleteOrgMembershipInvitationResponseCode, str]] = ...) -> None: ...

class ResendOrgMembershipInvitationRequest(_message.Message):
    __slots__ = ("orgId", "inviteeEmail")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    INVITEEEMAIL_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    inviteeEmail: str
    def __init__(self, orgId: _Optional[str] = ..., inviteeEmail: _Optional[str] = ...) -> None: ...

class ResendOrgMembershipInvitationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateOrgAccountsByOrgAdminRequest(_message.Message):
    __slots__ = ("orgId", "orgAccountCreationPayloads")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ORGACCOUNTCREATIONPAYLOADS_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    orgAccountCreationPayloads: _containers.RepeatedCompositeFieldContainer[OrgAccountCreationPayload]
    def __init__(self, orgId: _Optional[str] = ..., orgAccountCreationPayloads: _Optional[_Iterable[_Union[OrgAccountCreationPayload, _Mapping]]] = ...) -> None: ...

class OrgAccountCreationPayload(_message.Message):
    __slots__ = ("email", "licenseType")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    LICENSETYPE_FIELD_NUMBER: _ClassVar[int]
    email: str
    licenseType: _gravi_model_pb2.OrgLicenseType
    def __init__(self, email: _Optional[str] = ..., licenseType: _Optional[_Union[_gravi_model_pb2.OrgLicenseType, str]] = ...) -> None: ...

class CreateOrgAccountsByOrgAdminResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CreateOrgAccountsByOrgAdminResult]
    def __init__(self, results: _Optional[_Iterable[_Union[CreateOrgAccountsByOrgAdminResult, _Mapping]]] = ...) -> None: ...

class CreateOrgAccountsByOrgAdminResult(_message.Message):
    __slots__ = ("userCreated", "error")
    USERCREATED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    userCreated: _gravi_model_pb2.UserTO
    error: CreateOrgAccountsByOrgAdminResponseCode
    def __init__(self, userCreated: _Optional[_Union[_gravi_model_pb2.UserTO, _Mapping]] = ..., error: _Optional[_Union[CreateOrgAccountsByOrgAdminResponseCode, str]] = ...) -> None: ...
