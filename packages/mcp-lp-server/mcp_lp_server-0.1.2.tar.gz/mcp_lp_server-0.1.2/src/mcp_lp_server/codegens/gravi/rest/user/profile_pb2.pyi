import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSubscriptionResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateSubscriptionResponseCodeUnknown: _ClassVar[CreateSubscriptionResponseCode]
    CreateSubscriptionResponseCodeSuccess: _ClassVar[CreateSubscriptionResponseCode]
    CreateSubscriptionResponseCodeInternalError: _ClassVar[CreateSubscriptionResponseCode]
    CreateSubscriptionResponseCodeUnsupportedCountry: _ClassVar[CreateSubscriptionResponseCode]
    CreateSubscriptionResponseCodeUserAlreadyProTier: _ClassVar[CreateSubscriptionResponseCode]

class SubscriptionBillingPeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SubscriptionBillingPeriodMonthly: _ClassVar[SubscriptionBillingPeriod]
    SubscriptionBillingPeriodYearly: _ClassVar[SubscriptionBillingPeriod]

class SubscriptionPlan(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SubscriptionPlanPro: _ClassVar[SubscriptionPlan]

class GetStripeCustomerPortalLinkResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetStripeCustomerPortalLinkResponseCodeUnknown: _ClassVar[GetStripeCustomerPortalLinkResponseCode]
    GetStripeCustomerPortalLinkResponseCodeSuccess: _ClassVar[GetStripeCustomerPortalLinkResponseCode]
    GetStripeCustomerPortalLinkResponseCodeInternalError: _ClassVar[GetStripeCustomerPortalLinkResponseCode]
    GetStripeCustomerPortalLinkResponseCodeCustomerNotFound: _ClassVar[GetStripeCustomerPortalLinkResponseCode]

class GetSubscriptionPriceResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetSubscriptionPriceResponseCodeUnknown: _ClassVar[GetSubscriptionPriceResponseCode]
    GetSubscriptionPriceResponseCodeSuccess: _ClassVar[GetSubscriptionPriceResponseCode]
    GetSubscriptionPriceResponseCodeInternalError: _ClassVar[GetSubscriptionPriceResponseCode]

class Currency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USD: _ClassVar[Currency]
    GBP: _ClassVar[Currency]
    EUR: _ClassVar[Currency]
CreateSubscriptionResponseCodeUnknown: CreateSubscriptionResponseCode
CreateSubscriptionResponseCodeSuccess: CreateSubscriptionResponseCode
CreateSubscriptionResponseCodeInternalError: CreateSubscriptionResponseCode
CreateSubscriptionResponseCodeUnsupportedCountry: CreateSubscriptionResponseCode
CreateSubscriptionResponseCodeUserAlreadyProTier: CreateSubscriptionResponseCode
SubscriptionBillingPeriodMonthly: SubscriptionBillingPeriod
SubscriptionBillingPeriodYearly: SubscriptionBillingPeriod
SubscriptionPlanPro: SubscriptionPlan
GetStripeCustomerPortalLinkResponseCodeUnknown: GetStripeCustomerPortalLinkResponseCode
GetStripeCustomerPortalLinkResponseCodeSuccess: GetStripeCustomerPortalLinkResponseCode
GetStripeCustomerPortalLinkResponseCodeInternalError: GetStripeCustomerPortalLinkResponseCode
GetStripeCustomerPortalLinkResponseCodeCustomerNotFound: GetStripeCustomerPortalLinkResponseCode
GetSubscriptionPriceResponseCodeUnknown: GetSubscriptionPriceResponseCode
GetSubscriptionPriceResponseCodeSuccess: GetSubscriptionPriceResponseCode
GetSubscriptionPriceResponseCodeInternalError: GetSubscriptionPriceResponseCode
USD: Currency
GBP: Currency
EUR: Currency

class UpdateUserInfoRequest(_message.Message):
    __slots__ = ("userId", "newFirstName", "newLastName", "newCompanyName", "newDisplayName", "newBio", "newPublicProfileStatus")
    USERID_FIELD_NUMBER: _ClassVar[int]
    NEWFIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    NEWLASTNAME_FIELD_NUMBER: _ClassVar[int]
    NEWCOMPANYNAME_FIELD_NUMBER: _ClassVar[int]
    NEWDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    NEWBIO_FIELD_NUMBER: _ClassVar[int]
    NEWPUBLICPROFILESTATUS_FIELD_NUMBER: _ClassVar[int]
    userId: str
    newFirstName: _wrappers_pb2.OptionalString
    newLastName: _wrappers_pb2.OptionalString
    newCompanyName: _wrappers_pb2.OptionalString
    newDisplayName: _wrappers_pb2.OptionalString
    newBio: _wrappers_pb2.OptionalString
    newPublicProfileStatus: _gravi_model_pb2.PublicProfileStatus
    def __init__(self, userId: _Optional[str] = ..., newFirstName: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., newLastName: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., newCompanyName: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., newDisplayName: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., newBio: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., newPublicProfileStatus: _Optional[_Union[_gravi_model_pb2.PublicProfileStatus, str]] = ...) -> None: ...

class UpdateUserInfoResponse(_message.Message):
    __slots__ = ("user", "userPublicInfo")
    USER_FIELD_NUMBER: _ClassVar[int]
    USERPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    user: _gravi_model_pb2.UserTO
    userPublicInfo: _gravi_model_pb2.UserPublicTO
    def __init__(self, user: _Optional[_Union[_gravi_model_pb2.UserTO, _Mapping]] = ..., userPublicInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ...) -> None: ...

class CreateUserSurveyRequest(_message.Message):
    __slots__ = ("userSurvey",)
    USERSURVEY_FIELD_NUMBER: _ClassVar[int]
    userSurvey: UserSurvey
    def __init__(self, userSurvey: _Optional[_Union[UserSurvey, _Mapping]] = ...) -> None: ...

class CreateUserSurveyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UserSurvey(_message.Message):
    __slots__ = ("industry", "companyName", "role", "jobTitle", "useCase", "discoverySource", "isFromDeeplink")
    INDUSTRY_FIELD_NUMBER: _ClassVar[int]
    COMPANYNAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    JOBTITLE_FIELD_NUMBER: _ClassVar[int]
    USECASE_FIELD_NUMBER: _ClassVar[int]
    DISCOVERYSOURCE_FIELD_NUMBER: _ClassVar[int]
    ISFROMDEEPLINK_FIELD_NUMBER: _ClassVar[int]
    industry: str
    companyName: str
    role: str
    jobTitle: _wrappers_pb2.OptionalString
    useCase: str
    discoverySource: str
    isFromDeeplink: bool
    def __init__(self, industry: _Optional[str] = ..., companyName: _Optional[str] = ..., role: _Optional[str] = ..., jobTitle: _Optional[_Union[_wrappers_pb2.OptionalString, _Mapping]] = ..., useCase: _Optional[str] = ..., discoverySource: _Optional[str] = ..., isFromDeeplink: bool = ...) -> None: ...

class UserInfo(_message.Message):
    __slots__ = ("userId", "userName", "joinedDate", "lastLoggedInEpochMs", "isOrgAccount", "role", "status", "email", "pairedDeviceId", "isDevicePairingEnforced")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    JOINEDDATE_FIELD_NUMBER: _ClassVar[int]
    LASTLOGGEDINEPOCHMS_FIELD_NUMBER: _ClassVar[int]
    ISORGACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PAIREDDEVICEID_FIELD_NUMBER: _ClassVar[int]
    ISDEVICEPAIRINGENFORCED_FIELD_NUMBER: _ClassVar[int]
    userId: str
    userName: str
    joinedDate: int
    lastLoggedInEpochMs: int
    isOrgAccount: bool
    role: _gravi_model_pb2.OrgMemberRole
    status: _gravi_model_pb2.OrgMemberStatus
    email: str
    pairedDeviceId: str
    isDevicePairingEnforced: bool
    def __init__(self, userId: _Optional[str] = ..., userName: _Optional[str] = ..., joinedDate: _Optional[int] = ..., lastLoggedInEpochMs: _Optional[int] = ..., isOrgAccount: bool = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., status: _Optional[_Union[_gravi_model_pb2.OrgMemberStatus, str]] = ..., email: _Optional[str] = ..., pairedDeviceId: _Optional[str] = ..., isDevicePairingEnforced: bool = ...) -> None: ...

class CreateSubscriptionRequest(_message.Message):
    __slots__ = ("subscriptionBillingPeriod", "subscriptionPlan", "successRedirectLink", "cancelRedirectLink")
    SUBSCRIPTIONBILLINGPERIOD_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONPLAN_FIELD_NUMBER: _ClassVar[int]
    SUCCESSREDIRECTLINK_FIELD_NUMBER: _ClassVar[int]
    CANCELREDIRECTLINK_FIELD_NUMBER: _ClassVar[int]
    subscriptionBillingPeriod: SubscriptionBillingPeriod
    subscriptionPlan: SubscriptionPlan
    successRedirectLink: str
    cancelRedirectLink: str
    def __init__(self, subscriptionBillingPeriod: _Optional[_Union[SubscriptionBillingPeriod, str]] = ..., subscriptionPlan: _Optional[_Union[SubscriptionPlan, str]] = ..., successRedirectLink: _Optional[str] = ..., cancelRedirectLink: _Optional[str] = ...) -> None: ...

class CreateSubscriptionResponse(_message.Message):
    __slots__ = ("stripeCheckoutLink", "createSubscriptionResponseCode")
    STRIPECHECKOUTLINK_FIELD_NUMBER: _ClassVar[int]
    CREATESUBSCRIPTIONRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    stripeCheckoutLink: str
    createSubscriptionResponseCode: CreateSubscriptionResponseCode
    def __init__(self, stripeCheckoutLink: _Optional[str] = ..., createSubscriptionResponseCode: _Optional[_Union[CreateSubscriptionResponseCode, str]] = ...) -> None: ...

class GetStripeCustomerPortalLinkRequest(_message.Message):
    __slots__ = ("redirectLink",)
    REDIRECTLINK_FIELD_NUMBER: _ClassVar[int]
    redirectLink: str
    def __init__(self, redirectLink: _Optional[str] = ...) -> None: ...

class GetStripeCustomerPortalLinkResponse(_message.Message):
    __slots__ = ("stripeCustomerPortalLink", "getStripeCustomerPortalLinkResponseCode")
    STRIPECUSTOMERPORTALLINK_FIELD_NUMBER: _ClassVar[int]
    GETSTRIPECUSTOMERPORTALLINKRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    stripeCustomerPortalLink: str
    getStripeCustomerPortalLinkResponseCode: GetStripeCustomerPortalLinkResponseCode
    def __init__(self, stripeCustomerPortalLink: _Optional[str] = ..., getStripeCustomerPortalLinkResponseCode: _Optional[_Union[GetStripeCustomerPortalLinkResponseCode, str]] = ...) -> None: ...

class GetSubscriptionPriceRequest(_message.Message):
    __slots__ = ("subscriptionBillingPeriod", "subscriptionPlan")
    SUBSCRIPTIONBILLINGPERIOD_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONPLAN_FIELD_NUMBER: _ClassVar[int]
    subscriptionBillingPeriod: SubscriptionBillingPeriod
    subscriptionPlan: SubscriptionPlan
    def __init__(self, subscriptionBillingPeriod: _Optional[_Union[SubscriptionBillingPeriod, str]] = ..., subscriptionPlan: _Optional[_Union[SubscriptionPlan, str]] = ...) -> None: ...

class GetSubscriptionPriceResponse(_message.Message):
    __slots__ = ("price", "currency", "getSubscriptionPriceResponseCode")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    GETSUBSCRIPTIONPRICERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    price: int
    currency: Currency
    getSubscriptionPriceResponseCode: GetSubscriptionPriceResponseCode
    def __init__(self, price: _Optional[int] = ..., currency: _Optional[_Union[Currency, str]] = ..., getSubscriptionPriceResponseCode: _Optional[_Union[GetSubscriptionPriceResponseCode, str]] = ...) -> None: ...
