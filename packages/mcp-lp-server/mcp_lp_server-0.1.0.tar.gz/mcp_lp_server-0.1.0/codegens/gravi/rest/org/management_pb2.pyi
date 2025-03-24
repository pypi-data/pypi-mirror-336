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

class OrgType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgTypeUnknown: _ClassVar[OrgType]
    OrgTypeEdu: _ClassVar[OrgType]
    OrgTypePaid: _ClassVar[OrgType]
    OrgTypePaidSLA: _ClassVar[OrgType]
    OrgTypePartner: _ClassVar[OrgType]
    OrgTypeTrial: _ClassVar[OrgType]
    OrgTypeGSOrgs: _ClassVar[OrgType]
    OrgTypeCommunity: _ClassVar[OrgType]
OrgTypeUnknown: OrgType
OrgTypeEdu: OrgType
OrgTypePaid: OrgType
OrgTypePaidSLA: OrgType
OrgTypePartner: OrgType
OrgTypeTrial: OrgType
OrgTypeGSOrgs: OrgType
OrgTypeCommunity: OrgType

class UpdateOrgRequest(_message.Message):
    __slots__ = ("orgId", "mfaEnforcement")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    MFAENFORCEMENT_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    mfaEnforcement: _wrappers_pb2.OptionalBool
    def __init__(self, orgId: _Optional[str] = ..., mfaEnforcement: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ...) -> None: ...

class UpdateOrgResponse(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: OrganizationTO
    def __init__(self, org: _Optional[_Union[OrganizationTO, _Mapping]] = ...) -> None: ...

class OrgUserInfo(_message.Message):
    __slots__ = ("orgId", "roleId", "statusId", "onPremEnterpise", "orgName")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ROLEID_FIELD_NUMBER: _ClassVar[int]
    STATUSID_FIELD_NUMBER: _ClassVar[int]
    ONPREMENTERPISE_FIELD_NUMBER: _ClassVar[int]
    ORGNAME_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    roleId: int
    statusId: int
    onPremEnterpise: bool
    orgName: str
    def __init__(self, orgId: _Optional[str] = ..., roleId: _Optional[int] = ..., statusId: _Optional[int] = ..., onPremEnterpise: bool = ..., orgName: _Optional[str] = ...) -> None: ...

class OrgDownloadVersions(_message.Message):
    __slots__ = ("cloudClientVersion", "entClientVersion", "entQuestVersion", "entServerVersion", "entRhinoVersion", "entSetupVideoVersion", "entSetupQuestVideoVersion", "entQuestVideosVersion", "entDocumentationVersion", "steamVRVersion")
    CLOUDCLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTCLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTQUESTVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTSERVERVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTRHINOVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTSETUPVIDEOVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTSETUPQUESTVIDEOVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTQUESTVIDEOSVERSION_FIELD_NUMBER: _ClassVar[int]
    ENTDOCUMENTATIONVERSION_FIELD_NUMBER: _ClassVar[int]
    STEAMVRVERSION_FIELD_NUMBER: _ClassVar[int]
    cloudClientVersion: str
    entClientVersion: str
    entQuestVersion: str
    entServerVersion: str
    entRhinoVersion: str
    entSetupVideoVersion: str
    entSetupQuestVideoVersion: str
    entQuestVideosVersion: str
    entDocumentationVersion: str
    steamVRVersion: str
    def __init__(self, cloudClientVersion: _Optional[str] = ..., entClientVersion: _Optional[str] = ..., entQuestVersion: _Optional[str] = ..., entServerVersion: _Optional[str] = ..., entRhinoVersion: _Optional[str] = ..., entSetupVideoVersion: _Optional[str] = ..., entSetupQuestVideoVersion: _Optional[str] = ..., entQuestVideosVersion: _Optional[str] = ..., entDocumentationVersion: _Optional[str] = ..., steamVRVersion: _Optional[str] = ...) -> None: ...

class GetOrgDownloadVersionsRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class GetOrgDownloadVersionsResponse(_message.Message):
    __slots__ = ("orgDownloadVersions",)
    ORGDOWNLOADVERSIONS_FIELD_NUMBER: _ClassVar[int]
    orgDownloadVersions: OrgDownloadVersions
    def __init__(self, orgDownloadVersions: _Optional[_Union[OrgDownloadVersions, _Mapping]] = ...) -> None: ...

class OrganizationTO(_message.Message):
    __slots__ = ("organizationId", "name", "priceTier", "canaryFeatures", "dataLocation", "ssoProvider", "licenseExpiryOn", "totalSeats", "seatsUsed", "totalStorage", "usedStorage", "isOnPrem", "enabledFeatures", "purchasedSeats", "daysToPermanentlyDeleteBinned", "daysToAutoBinDocs", "orgType", "allowedClientVersions", "secPolicyMfaEnforcement")
    ORGANIZATIONID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICETIER_FIELD_NUMBER: _ClassVar[int]
    CANARYFEATURES_FIELD_NUMBER: _ClassVar[int]
    DATALOCATION_FIELD_NUMBER: _ClassVar[int]
    SSOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    LICENSEEXPIRYON_FIELD_NUMBER: _ClassVar[int]
    TOTALSEATS_FIELD_NUMBER: _ClassVar[int]
    SEATSUSED_FIELD_NUMBER: _ClassVar[int]
    TOTALSTORAGE_FIELD_NUMBER: _ClassVar[int]
    USEDSTORAGE_FIELD_NUMBER: _ClassVar[int]
    ISONPREM_FIELD_NUMBER: _ClassVar[int]
    ENABLEDFEATURES_FIELD_NUMBER: _ClassVar[int]
    PURCHASEDSEATS_FIELD_NUMBER: _ClassVar[int]
    DAYSTOPERMANENTLYDELETEBINNED_FIELD_NUMBER: _ClassVar[int]
    DAYSTOAUTOBINDOCS_FIELD_NUMBER: _ClassVar[int]
    ORGTYPE_FIELD_NUMBER: _ClassVar[int]
    ALLOWEDCLIENTVERSIONS_FIELD_NUMBER: _ClassVar[int]
    SECPOLICYMFAENFORCEMENT_FIELD_NUMBER: _ClassVar[int]
    organizationId: str
    name: str
    priceTier: _gravi_model_pb2.PriceTier
    canaryFeatures: bool
    dataLocation: _gravi_model_pb2.DataLocation
    ssoProvider: _gravi_model_pb2.SSOProvider
    licenseExpiryOn: int
    totalSeats: int
    seatsUsed: int
    totalStorage: int
    usedStorage: int
    isOnPrem: bool
    enabledFeatures: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.SubscriptionFeatureFlag]
    purchasedSeats: int
    daysToPermanentlyDeleteBinned: int
    daysToAutoBinDocs: int
    orgType: OrgType
    allowedClientVersions: _containers.RepeatedScalarFieldContainer[str]
    secPolicyMfaEnforcement: bool
    def __init__(self, organizationId: _Optional[str] = ..., name: _Optional[str] = ..., priceTier: _Optional[_Union[_gravi_model_pb2.PriceTier, str]] = ..., canaryFeatures: bool = ..., dataLocation: _Optional[_Union[_gravi_model_pb2.DataLocation, str]] = ..., ssoProvider: _Optional[_Union[_gravi_model_pb2.SSOProvider, str]] = ..., licenseExpiryOn: _Optional[int] = ..., totalSeats: _Optional[int] = ..., seatsUsed: _Optional[int] = ..., totalStorage: _Optional[int] = ..., usedStorage: _Optional[int] = ..., isOnPrem: bool = ..., enabledFeatures: _Optional[_Iterable[_Union[_gravi_model_pb2.SubscriptionFeatureFlag, str]]] = ..., purchasedSeats: _Optional[int] = ..., daysToPermanentlyDeleteBinned: _Optional[int] = ..., daysToAutoBinDocs: _Optional[int] = ..., orgType: _Optional[_Union[OrgType, str]] = ..., allowedClientVersions: _Optional[_Iterable[str]] = ..., secPolicyMfaEnforcement: bool = ...) -> None: ...
