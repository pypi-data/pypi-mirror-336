import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VRNotificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NotificationTypeUnknown: _ClassVar[VRNotificationType]
    InviteToCollab: _ClassVar[VRNotificationType]
    EnterRoomDirectly: _ClassVar[VRNotificationType]
    VRConnectionInvitation: _ClassVar[VRNotificationType]
    VRNotificationType_AdminEnterRoomDirectlyViaDeeplink: _ClassVar[VRNotificationType]

class WebNotificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WebNotificationTypeUnknown: _ClassVar[WebNotificationType]
    VRLoginNotification: _ClassVar[WebNotificationType]
    FreeCollabShowQuickFeedbackWeb: _ClassVar[WebNotificationType]
    WebConnectionInvitation: _ClassVar[WebNotificationType]

class NotificationServiceRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NotificationServiceRequestType_Unknown: _ClassVar[NotificationServiceRequestType]
    NotificationServiceRequestType_DeliveredNotificationsAck: _ClassVar[NotificationServiceRequestType]
    NotificationServiceRequestType_ListUndeliveredNotification: _ClassVar[NotificationServiceRequestType]
NotificationTypeUnknown: VRNotificationType
InviteToCollab: VRNotificationType
EnterRoomDirectly: VRNotificationType
VRConnectionInvitation: VRNotificationType
VRNotificationType_AdminEnterRoomDirectlyViaDeeplink: VRNotificationType
WebNotificationTypeUnknown: WebNotificationType
VRLoginNotification: WebNotificationType
FreeCollabShowQuickFeedbackWeb: WebNotificationType
WebConnectionInvitation: WebNotificationType
NotificationServiceRequestType_Unknown: NotificationServiceRequestType
NotificationServiceRequestType_DeliveredNotificationsAck: NotificationServiceRequestType
NotificationServiceRequestType_ListUndeliveredNotification: NotificationServiceRequestType

class NotificationTO(_message.Message):
    __slots__ = ("notificationId", "requiredConsumeConfirm", "activeTime", "notificationContent")
    NOTIFICATIONID_FIELD_NUMBER: _ClassVar[int]
    REQUIREDCONSUMECONFIRM_FIELD_NUMBER: _ClassVar[int]
    ACTIVETIME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONCONTENT_FIELD_NUMBER: _ClassVar[int]
    notificationId: str
    requiredConsumeConfirm: bool
    activeTime: int
    notificationContent: NotificationContentTO
    def __init__(self, notificationId: _Optional[str] = ..., requiredConsumeConfirm: bool = ..., activeTime: _Optional[int] = ..., notificationContent: _Optional[_Union[NotificationContentTO, _Mapping]] = ...) -> None: ...

class NotificationContentTO(_message.Message):
    __slots__ = ("vrNotification", "webNotification")
    VRNOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    WEBNOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    vrNotification: VRNotificationContentTO
    webNotification: WebNotificationContentTO
    def __init__(self, vrNotification: _Optional[_Union[VRNotificationContentTO, _Mapping]] = ..., webNotification: _Optional[_Union[WebNotificationContentTO, _Mapping]] = ...) -> None: ...

class VRNotificationContentTO(_message.Message):
    __slots__ = ("notificationType", "inviteToCollab", "enterRoomDirectly", "connectionInvitation", "adminEnterRoomDirectly")
    NOTIFICATIONTYPE_FIELD_NUMBER: _ClassVar[int]
    INVITETOCOLLAB_FIELD_NUMBER: _ClassVar[int]
    ENTERROOMDIRECTLY_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONINVITATION_FIELD_NUMBER: _ClassVar[int]
    ADMINENTERROOMDIRECTLY_FIELD_NUMBER: _ClassVar[int]
    notificationType: VRNotificationType
    inviteToCollab: InviteToCollabPayload
    enterRoomDirectly: EnterRoomDirectlyPayload
    connectionInvitation: _gravi_model_pb2.ConnectionInvitationTO
    adminEnterRoomDirectly: AdminEnterRoomDirectlyViaDeeplink
    def __init__(self, notificationType: _Optional[_Union[VRNotificationType, str]] = ..., inviteToCollab: _Optional[_Union[InviteToCollabPayload, _Mapping]] = ..., enterRoomDirectly: _Optional[_Union[EnterRoomDirectlyPayload, _Mapping]] = ..., connectionInvitation: _Optional[_Union[_gravi_model_pb2.ConnectionInvitationTO, _Mapping]] = ..., adminEnterRoomDirectly: _Optional[_Union[AdminEnterRoomDirectlyViaDeeplink, _Mapping]] = ...) -> None: ...

class InviteToCollabPayload(_message.Message):
    __slots__ = ("docId", "inviter", "docName")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    INVITER_FIELD_NUMBER: _ClassVar[int]
    DOCNAME_FIELD_NUMBER: _ClassVar[int]
    docId: str
    inviter: _gravi_model_pb2.SharableUserInfo
    docName: str
    def __init__(self, docId: _Optional[str] = ..., inviter: _Optional[_Union[_gravi_model_pb2.SharableUserInfo, _Mapping]] = ..., docName: _Optional[str] = ...) -> None: ...

class EnterRoomDirectlyPayload(_message.Message):
    __slots__ = ("docId", "isPublic")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ISPUBLIC_FIELD_NUMBER: _ClassVar[int]
    docId: str
    isPublic: bool
    def __init__(self, docId: _Optional[str] = ..., isPublic: bool = ...) -> None: ...

class AdminEnterRoomDirectlyViaDeeplink(_message.Message):
    __slots__ = ("deeplinkId",)
    DEEPLINKID_FIELD_NUMBER: _ClassVar[int]
    deeplinkId: str
    def __init__(self, deeplinkId: _Optional[str] = ...) -> None: ...

class WebNotificationContentTO(_message.Message):
    __slots__ = ("notificationType", "vrLoginNotification", "connectionInvitation")
    NOTIFICATIONTYPE_FIELD_NUMBER: _ClassVar[int]
    VRLOGINNOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONINVITATION_FIELD_NUMBER: _ClassVar[int]
    notificationType: WebNotificationType
    vrLoginNotification: VRLoginNotificationTO
    connectionInvitation: _gravi_model_pb2.ConnectionInvitationTO
    def __init__(self, notificationType: _Optional[_Union[WebNotificationType, str]] = ..., vrLoginNotification: _Optional[_Union[VRLoginNotificationTO, _Mapping]] = ..., connectionInvitation: _Optional[_Union[_gravi_model_pb2.ConnectionInvitationTO, _Mapping]] = ...) -> None: ...

class VRLoginNotificationTO(_message.Message):
    __slots__ = ("magicLinkLoginIdCode",)
    MAGICLINKLOGINIDCODE_FIELD_NUMBER: _ClassVar[int]
    magicLinkLoginIdCode: str
    def __init__(self, magicLinkLoginIdCode: _Optional[str] = ...) -> None: ...

class NotificationList(_message.Message):
    __slots__ = ("notifications",)
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    notifications: _containers.RepeatedCompositeFieldContainer[NotificationTO]
    def __init__(self, notifications: _Optional[_Iterable[_Union[NotificationTO, _Mapping]]] = ...) -> None: ...

class AckDeliveredNotificationsRequest(_message.Message):
    __slots__ = ("notificationIds",)
    NOTIFICATIONIDS_FIELD_NUMBER: _ClassVar[int]
    notificationIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, notificationIds: _Optional[_Iterable[str]] = ...) -> None: ...

class AckDeliveredNotificationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUndeliveredNotificationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUndeliveredNotificationResponse(_message.Message):
    __slots__ = ("notificationList",)
    NOTIFICATIONLIST_FIELD_NUMBER: _ClassVar[int]
    notificationList: NotificationList
    def __init__(self, notificationList: _Optional[_Union[NotificationList, _Mapping]] = ...) -> None: ...

class NotificationServiceTicket(_message.Message):
    __slots__ = ("stoken",)
    STOKEN_FIELD_NUMBER: _ClassVar[int]
    stoken: str
    def __init__(self, stoken: _Optional[str] = ...) -> None: ...

class NotificationServiceRequest(_message.Message):
    __slots__ = ("requestType", "ticket", "ackDeliveredNotifsRequest", "listUndeliveredNotificationRequest")
    REQUESTTYPE_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    ACKDELIVEREDNOTIFSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTUNDELIVEREDNOTIFICATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    requestType: NotificationServiceRequestType
    ticket: NotificationServiceTicket
    ackDeliveredNotifsRequest: AckDeliveredNotificationsRequest
    listUndeliveredNotificationRequest: ListUndeliveredNotificationRequest
    def __init__(self, requestType: _Optional[_Union[NotificationServiceRequestType, str]] = ..., ticket: _Optional[_Union[NotificationServiceTicket, _Mapping]] = ..., ackDeliveredNotifsRequest: _Optional[_Union[AckDeliveredNotificationsRequest, _Mapping]] = ..., listUndeliveredNotificationRequest: _Optional[_Union[ListUndeliveredNotificationRequest, _Mapping]] = ...) -> None: ...

class NotificationServiceResponse(_message.Message):
    __slots__ = ("ackDeliveredNotifsResponse", "listUndeliveredNotificationResponse")
    ACKDELIVEREDNOTIFSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTUNDELIVEREDNOTIFICATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ackDeliveredNotifsResponse: AckDeliveredNotificationResponse
    listUndeliveredNotificationResponse: ListUndeliveredNotificationResponse
    def __init__(self, ackDeliveredNotifsResponse: _Optional[_Union[AckDeliveredNotificationResponse, _Mapping]] = ..., listUndeliveredNotificationResponse: _Optional[_Union[ListUndeliveredNotificationResponse, _Mapping]] = ...) -> None: ...
