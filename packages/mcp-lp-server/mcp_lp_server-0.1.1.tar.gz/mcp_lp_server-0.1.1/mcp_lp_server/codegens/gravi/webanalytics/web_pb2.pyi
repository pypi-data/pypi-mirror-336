import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rest.model import platform_rest_pb2 as _platform_rest_pb2
from gravi.rest.org import team_pb2 as _team_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WebEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WebEventTypeUnset: _ClassVar[WebEventType]
    WebEventTypeUploadFile: _ClassVar[WebEventType]
    WebEventTypeDownloadFile: _ClassVar[WebEventType]
    WebEventTypeDownloadMultipleFiles: _ClassVar[WebEventType]
    WebEventTypeTrashFile: _ClassVar[WebEventType]
    WebEventTypeClearBin: _ClassVar[WebEventType]
    WebEventTypeViewFile: _ClassVar[WebEventType]
    WebEventTypeCreateFolder: _ClassVar[WebEventType]
    WebEventTypeRenameFile: _ClassVar[WebEventType]
    WebEventTypeOpenExternalSocialMedia: _ClassVar[WebEventType]
    WebEventTypeMoveFile: _ClassVar[WebEventType]
    WebEventTypeSendFile: _ClassVar[WebEventType]
    WebEventTypeReceiveFile: _ClassVar[WebEventType]
    WebEventTypeShareRoom: _ClassVar[WebEventType]
    WebEventTypeDirectDownloadExport: _ClassVar[WebEventType]
    WebEventTypeDownloadGS: _ClassVar[WebEventType]
    WebEventTypeDeeplinkLaunch: _ClassVar[WebEventType]
    WebEventTypeCreateRoom: _ClassVar[WebEventType]
    WebEventTypeAcceptShareRoom: _ClassVar[WebEventType]
    WebEventTypeRequestInviteToAdmin: _ClassVar[WebEventType]
    WebEventTypeApproveRequestInviteToAdmin: _ClassVar[WebEventType]
    WebEventTypeRequestRoomAccess: _ClassVar[WebEventType]
    WebEventTypeApproveRoomAccessRequest: _ClassVar[WebEventType]
    WebEventTypeUpdateProfileBio: _ClassVar[WebEventType]
    WebEventTypeUpdateProfileStatus: _ClassVar[WebEventType]
    WebEventTypeClickViewProfile: _ClassVar[WebEventType]
    WebEventTypeViewProfile: _ClassVar[WebEventType]
    WebEventTypeConnectionInvitation: _ClassVar[WebEventType]
    WebEventTypeClickLinkInstagram: _ClassVar[WebEventType]
    WebEventTypeClickLinkLinkedIn: _ClassVar[WebEventType]
    WebEventTypeLinkInstagramSuccessful: _ClassVar[WebEventType]
    WebEventTypeLinkLinkedInSuccessful: _ClassVar[WebEventType]
    WebEventTypeToggleLayout: _ClassVar[WebEventType]
    WebEventTypeSearch: _ClassVar[WebEventType]
    WebEventTypeToggleAside: _ClassVar[WebEventType]
    WebEventTypeToggleDoNotShowAgain: _ClassVar[WebEventType]
    WebEventTypeFilter: _ClassVar[WebEventType]
    WebEventTypeSortBy: _ClassVar[WebEventType]
    WebEventTypeChangeViewMode: _ClassVar[WebEventType]
    WebEventTypeContextMenuDoc: _ClassVar[WebEventType]
    WebEventTypeDeleteDocuments: _ClassVar[WebEventType]
    WebEventTypeDragAndDropDocuments: _ClassVar[WebEventType]
    WebEventTypeDeleteFromBin: _ClassVar[WebEventType]
    WebEventTypeRestoreFromBin: _ClassVar[WebEventType]
    WebEventJoinViaDeepLink: _ClassVar[WebEventType]
    WebEventTypeDoubleClickDoc: _ClassVar[WebEventType]
    WebEventTypeDocActionTriggered: _ClassVar[WebEventType]
    WebEventTypeContextMenuSidebar: _ClassVar[WebEventType]
    WebEventTypeChangeRoomRole: _ClassVar[WebEventType]
    WebEventTypeRemoveFromRoom: _ClassVar[WebEventType]
    WebEventTypeExportViaPresetModal: _ClassVar[WebEventType]
    WebEventTypeSwitchProfile: _ClassVar[WebEventType]
    WebEventTypeAutogeneratePassword: _ClassVar[WebEventType]
    WebEventTypeOpenSupportMenu: _ClassVar[WebEventType]
    WebEventTypeOpenGravitySketchHelpCenter: _ClassVar[WebEventType]
    WebEventTypeOpenLiveChat: _ClassVar[WebEventType]
    WebEventTypeRequestResetPassword: _ClassVar[WebEventType]
    WebEventTypeRequestChangeEmail: _ClassVar[WebEventType]
    WebEventTypeChangePasword: _ClassVar[WebEventType]
    WebEventTypeChangeUserField: _ClassVar[WebEventType]
    WebEventTypeDeleteAccount: _ClassVar[WebEventType]
    WebEventTypeToggleMFA: _ClassVar[WebEventType]
    WebEventTypeToggleOrgLevelMFA: _ClassVar[WebEventType]
    WebEventTypeInviteOrgMember: _ClassVar[WebEventType]
    WebEventTypeChangeOrgRole: _ClassVar[WebEventType]
    WebEventTypeRemoveOrgUser: _ClassVar[WebEventType]
    WebEventTypeMakeOrgUserInactive: _ClassVar[WebEventType]
    WebEventTypeAddNewTeam: _ClassVar[WebEventType]
    WebEventTypeRenameTeam: _ClassVar[WebEventType]
    WebEventTypeAddTeamMembers: _ClassVar[WebEventType]
    WebEventTypeChangeTeamRole: _ClassVar[WebEventType]
    WebEventTypeRemoveTeamMember: _ClassVar[WebEventType]
    WebEventTypeRemoveAllTeamMembers: _ClassVar[WebEventType]
    WebEventTypeGetHelpForLogin: _ClassVar[WebEventType]
    WebEventTypeResendLoginCode: _ClassVar[WebEventType]
    WebEventTypeOpenEmailForMagicLogin: _ClassVar[WebEventType]
    WebEventTypeSendLoginCode: _ClassVar[WebEventType]
    WebEventTypeReEnterMagicLoginEmail: _ClassVar[WebEventType]
    WebEventTypeLoginViaEmailCode: _ClassVar[WebEventType]
    WebEventTypeClick3DModelOnSignUp: _ClassVar[WebEventType]
    WebEventTypeSwitchToLoginOnSignUp: _ClassVar[WebEventType]
    WebEventTypeSwitchToSignupOnLogin: _ClassVar[WebEventType]
    WebEventTypeSwitchWorkspace: _ClassVar[WebEventType]
    WebEventTypeNavbarNavigate: _ClassVar[WebEventType]
    WebEventTypePaywallTriggered: _ClassVar[WebEventType]
    WebEventTypeDiscoverBusiness: _ClassVar[WebEventType]
    WebEventTypePaywallPersonalUserFlag: _ClassVar[WebEventType]
    WebEventTypePaywallBusinessUserDetailsSubmitted: _ClassVar[WebEventType]
    WebEventTypePaywallPersonalUserDetailsSubmitted: _ClassVar[WebEventType]
    WebEventTypePaywallPersonalUserDetailsClosed: _ClassVar[WebEventType]
    WebEventTypePaywallBusinessUserDetailsClosed: _ClassVar[WebEventType]
    WebEventTypeDiscoverUpgradeToPro: _ClassVar[WebEventType]
    WebEventTypeUserClickUpgradeToPro: _ClassVar[WebEventType]
    WebEventTypeGoToPricingPage: _ClassVar[WebEventType]
    WebEventTypeUpgradeToProRegionNotSupported: _ClassVar[WebEventType]
    WebEventTypeUpgradeToProEncounteredError: _ClassVar[WebEventType]
    WebEventTypeUpgradeToProSuccessful: _ClassVar[WebEventType]
    WebEventTypeTriggerProPaywall: _ClassVar[WebEventType]
    WebEventTypeTriggerProTierCap: _ClassVar[WebEventType]
    WebEventTypeUserClickManageSubscription: _ClassVar[WebEventType]
    WebEventTypeLearnMoreBusiness: _ClassVar[WebEventType]
    WebEventTypeConnectWithAnExpert: _ClassVar[WebEventType]

class DocActionSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DocActionSource_Unknown: _ClassVar[DocActionSource]
    DocActionSource_HeaderBar: _ClassVar[DocActionSource]
    DocActionSource_ContextMenu: _ClassVar[DocActionSource]
    DocActionSource_ViewFilePage: _ClassVar[DocActionSource]

class UserFieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UserFieldType_unknown: _ClassVar[UserFieldType]
    UserFieldType_firstName: _ClassVar[UserFieldType]
    UserFieldType_lastName: _ClassVar[UserFieldType]
    UserFieldType_companyName: _ClassVar[UserFieldType]
    UserFieldType_displayName: _ClassVar[UserFieldType]
    UserFieldType_profileStatus: _ClassVar[UserFieldType]
    UserFieldType_bio: _ClassVar[UserFieldType]

class ImportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UploadFileUnknown: _ClassVar[ImportType]
    UploadFileButton: _ClassVar[ImportType]
    UploadFileDnD: _ClassVar[ImportType]
    UploadFileCopyPaste: _ClassVar[ImportType]

class PublicProfileViewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ViewOwnProfile: _ClassVar[PublicProfileViewType]
    ViewOtherProfileAuthd: _ClassVar[PublicProfileViewType]
    ViewOtherProfileUnauthd: _ClassVar[PublicProfileViewType]

class DownloadMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DownloadMethod_Unknown: _ClassVar[DownloadMethod]
    DownloadMethod_LP_Button: _ClassVar[DownloadMethod]
    DownloadMethod_DragAndDrop: _ClassVar[DownloadMethod]
    DownloadMethod_SaveAs: _ClassVar[DownloadMethod]

class ViewFileSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ViewFileSource_unknown: _ClassVar[ViewFileSource]
    ViewFileSource_contextMenu: _ClassVar[ViewFileSource]
    ViewFileSource_doubleClick: _ClassVar[ViewFileSource]
    ViewFileSource_toolbar: _ClassVar[ViewFileSource]
    ViewFileSource_URL: _ClassVar[ViewFileSource]
    ViewFileSource_shared: _ClassVar[ViewFileSource]

class SocialMediaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SocialMediaTypeUnknown: _ClassVar[SocialMediaType]
    SocialMediaTypeInstagram: _ClassVar[SocialMediaType]
    SocialMediaTypeDiscord: _ClassVar[SocialMediaType]
    SocialMediaTypeYoutube: _ClassVar[SocialMediaType]

class SocialMediaLinkLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SocialMediaLinkLocationUnknown: _ClassVar[SocialMediaLinkLocation]
    SocialMediaLinkLocationTopNav: _ClassVar[SocialMediaLinkLocation]
    SocialMediaLinkLocationPopup: _ClassVar[SocialMediaLinkLocation]

class DownloadGSLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DownloadLocationUnknown: _ClassVar[DownloadGSLocation]
    DownloadLocationSideBar: _ClassVar[DownloadGSLocation]
    DownloadLocationDeepLink: _ClassVar[DownloadGSLocation]
    DownloadLocationDeepLinkLaunch: _ClassVar[DownloadGSLocation]
    DownloadLocationEnterprisePage: _ClassVar[DownloadGSLocation]
    DownloadLocationEnterprisePageVersioned: _ClassVar[DownloadGSLocation]

class DoNotShowAgainSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DoNotShowAgainSource_Unknown: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamRenameFile: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamUploadFile: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamMoveFileByModal: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamMoveFileByDrag: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamNewRoom: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamRestoreFile: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamNewFolder: _ClassVar[DoNotShowAgainSource]
    DoNotShowAgainSource_GuestTeamNewFolderCustomPath: _ClassVar[DoNotShowAgainSource]

class AddTeamMemberLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AddTeamMemberLocation_Unknown: _ClassVar[AddTeamMemberLocation]
    AddTeamMemberLocation_OrgMembersList: _ClassVar[AddTeamMemberLocation]
    AddTeamMemberLocation_TeamMembersList: _ClassVar[AddTeamMemberLocation]
    AddTeamMemberLocation_CreateTeamModal: _ClassVar[AddTeamMemberLocation]

class RecentsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RecentsType_Unknown: _ClassVar[RecentsType]
    RecentsType_Files: _ClassVar[RecentsType]
    RecentsType_Suggested: _ClassVar[RecentsType]
    RecentsType_Recents: _ClassVar[RecentsType]

class RecentsTimePeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RecentsTimePeriod_Unknown: _ClassVar[RecentsTimePeriod]
    RecentsTimePeriod_Today: _ClassVar[RecentsTimePeriod]
    RecentsTimePeriod_ThisWeek: _ClassVar[RecentsTimePeriod]
    RecentsTimePeriod_ThisMonth: _ClassVar[RecentsTimePeriod]
    RecentsTimePeriod_ThisYear: _ClassVar[RecentsTimePeriod]
    RecentsTimePeriod_Earlier: _ClassVar[RecentsTimePeriod]

class SearchScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SearchScope_Unknown: _ClassVar[SearchScope]
    SearchScope_Full: _ClassVar[SearchScope]
    SearchScope_Folder: _ClassVar[SearchScope]

class FilterOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FilterOption_Unknown: _ClassVar[FilterOption]
    FilterOption_Sketches: _ClassVar[FilterOption]
    FilterOption_ReferenceImages: _ClassVar[FilterOption]
    FilterOption_ImportLibrary: _ClassVar[FilterOption]
    FilterOption_Screenshots: _ClassVar[FilterOption]
    FilterOption_Exports: _ClassVar[FilterOption]
    FilterOption_CollabRooms: _ClassVar[FilterOption]

class SortByOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SortByOption_Unknown: _ClassVar[SortByOption]
    SortByOption_Name: _ClassVar[SortByOption]
    SortByOption_Created: _ClassVar[SortByOption]
    SortByOption_Updated: _ClassVar[SortByOption]
    SortByOption_Size: _ClassVar[SortByOption]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SortOrder_Unknown: _ClassVar[SortOrder]
    SortOrder_Ascending: _ClassVar[SortOrder]
    SortOrder_Descending: _ClassVar[SortOrder]

class ViewMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ViewMode_Unknown: _ClassVar[ViewMode]
    ViewMode_Tiled: _ClassVar[ViewMode]
    ViewMode_List: _ClassVar[ViewMode]

class EmailLink(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EmailLink_Unknown: _ClassVar[EmailLink]
    EmailLink_Gmail: _ClassVar[EmailLink]
    EmailLink_Outlook: _ClassVar[EmailLink]

class DocActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[DocActionType]
    JoinRoom: _ClassVar[DocActionType]
    ViewDoc: _ClassVar[DocActionType]
    SetRoomPassword: _ClassVar[DocActionType]
    ShareDoc: _ClassVar[DocActionType]
    CopyInviteLink: _ClassVar[DocActionType]
    MoveDoc: _ClassVar[DocActionType]
    RenameDoc: _ClassVar[DocActionType]
    DeleteDoc: _ClassVar[DocActionType]
    EnterFolder: _ClassVar[DocActionType]
    RemoveAccessToRoom: _ClassVar[DocActionType]
    DownloadDoc: _ClassVar[DocActionType]
    SendDoc: _ClassVar[DocActionType]
    ExportDoc: _ClassVar[DocActionType]

class Workspace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Workspace_unknown: _ClassVar[Workspace]
    Workspace_bonusPack: _ClassVar[Workspace]
    Workspace_personalSpace: _ClassVar[Workspace]
    Workspace_orgSpace: _ClassVar[Workspace]

class NavbarNavigateOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NavbarNavigateOption_unknown: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_personalOrgSpace: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_sharedOrgSpace: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_teamSpace: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_manageOrg: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_manageMembers: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_manageTeams: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_cloudExports: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_recents: _ClassVar[NavbarNavigateOption]
    NavbarNavigateOption_trashBin: _ClassVar[NavbarNavigateOption]
WebEventTypeUnset: WebEventType
WebEventTypeUploadFile: WebEventType
WebEventTypeDownloadFile: WebEventType
WebEventTypeDownloadMultipleFiles: WebEventType
WebEventTypeTrashFile: WebEventType
WebEventTypeClearBin: WebEventType
WebEventTypeViewFile: WebEventType
WebEventTypeCreateFolder: WebEventType
WebEventTypeRenameFile: WebEventType
WebEventTypeOpenExternalSocialMedia: WebEventType
WebEventTypeMoveFile: WebEventType
WebEventTypeSendFile: WebEventType
WebEventTypeReceiveFile: WebEventType
WebEventTypeShareRoom: WebEventType
WebEventTypeDirectDownloadExport: WebEventType
WebEventTypeDownloadGS: WebEventType
WebEventTypeDeeplinkLaunch: WebEventType
WebEventTypeCreateRoom: WebEventType
WebEventTypeAcceptShareRoom: WebEventType
WebEventTypeRequestInviteToAdmin: WebEventType
WebEventTypeApproveRequestInviteToAdmin: WebEventType
WebEventTypeRequestRoomAccess: WebEventType
WebEventTypeApproveRoomAccessRequest: WebEventType
WebEventTypeUpdateProfileBio: WebEventType
WebEventTypeUpdateProfileStatus: WebEventType
WebEventTypeClickViewProfile: WebEventType
WebEventTypeViewProfile: WebEventType
WebEventTypeConnectionInvitation: WebEventType
WebEventTypeClickLinkInstagram: WebEventType
WebEventTypeClickLinkLinkedIn: WebEventType
WebEventTypeLinkInstagramSuccessful: WebEventType
WebEventTypeLinkLinkedInSuccessful: WebEventType
WebEventTypeToggleLayout: WebEventType
WebEventTypeSearch: WebEventType
WebEventTypeToggleAside: WebEventType
WebEventTypeToggleDoNotShowAgain: WebEventType
WebEventTypeFilter: WebEventType
WebEventTypeSortBy: WebEventType
WebEventTypeChangeViewMode: WebEventType
WebEventTypeContextMenuDoc: WebEventType
WebEventTypeDeleteDocuments: WebEventType
WebEventTypeDragAndDropDocuments: WebEventType
WebEventTypeDeleteFromBin: WebEventType
WebEventTypeRestoreFromBin: WebEventType
WebEventJoinViaDeepLink: WebEventType
WebEventTypeDoubleClickDoc: WebEventType
WebEventTypeDocActionTriggered: WebEventType
WebEventTypeContextMenuSidebar: WebEventType
WebEventTypeChangeRoomRole: WebEventType
WebEventTypeRemoveFromRoom: WebEventType
WebEventTypeExportViaPresetModal: WebEventType
WebEventTypeSwitchProfile: WebEventType
WebEventTypeAutogeneratePassword: WebEventType
WebEventTypeOpenSupportMenu: WebEventType
WebEventTypeOpenGravitySketchHelpCenter: WebEventType
WebEventTypeOpenLiveChat: WebEventType
WebEventTypeRequestResetPassword: WebEventType
WebEventTypeRequestChangeEmail: WebEventType
WebEventTypeChangePasword: WebEventType
WebEventTypeChangeUserField: WebEventType
WebEventTypeDeleteAccount: WebEventType
WebEventTypeToggleMFA: WebEventType
WebEventTypeToggleOrgLevelMFA: WebEventType
WebEventTypeInviteOrgMember: WebEventType
WebEventTypeChangeOrgRole: WebEventType
WebEventTypeRemoveOrgUser: WebEventType
WebEventTypeMakeOrgUserInactive: WebEventType
WebEventTypeAddNewTeam: WebEventType
WebEventTypeRenameTeam: WebEventType
WebEventTypeAddTeamMembers: WebEventType
WebEventTypeChangeTeamRole: WebEventType
WebEventTypeRemoveTeamMember: WebEventType
WebEventTypeRemoveAllTeamMembers: WebEventType
WebEventTypeGetHelpForLogin: WebEventType
WebEventTypeResendLoginCode: WebEventType
WebEventTypeOpenEmailForMagicLogin: WebEventType
WebEventTypeSendLoginCode: WebEventType
WebEventTypeReEnterMagicLoginEmail: WebEventType
WebEventTypeLoginViaEmailCode: WebEventType
WebEventTypeClick3DModelOnSignUp: WebEventType
WebEventTypeSwitchToLoginOnSignUp: WebEventType
WebEventTypeSwitchToSignupOnLogin: WebEventType
WebEventTypeSwitchWorkspace: WebEventType
WebEventTypeNavbarNavigate: WebEventType
WebEventTypePaywallTriggered: WebEventType
WebEventTypeDiscoverBusiness: WebEventType
WebEventTypePaywallPersonalUserFlag: WebEventType
WebEventTypePaywallBusinessUserDetailsSubmitted: WebEventType
WebEventTypePaywallPersonalUserDetailsSubmitted: WebEventType
WebEventTypePaywallPersonalUserDetailsClosed: WebEventType
WebEventTypePaywallBusinessUserDetailsClosed: WebEventType
WebEventTypeDiscoverUpgradeToPro: WebEventType
WebEventTypeUserClickUpgradeToPro: WebEventType
WebEventTypeGoToPricingPage: WebEventType
WebEventTypeUpgradeToProRegionNotSupported: WebEventType
WebEventTypeUpgradeToProEncounteredError: WebEventType
WebEventTypeUpgradeToProSuccessful: WebEventType
WebEventTypeTriggerProPaywall: WebEventType
WebEventTypeTriggerProTierCap: WebEventType
WebEventTypeUserClickManageSubscription: WebEventType
WebEventTypeLearnMoreBusiness: WebEventType
WebEventTypeConnectWithAnExpert: WebEventType
DocActionSource_Unknown: DocActionSource
DocActionSource_HeaderBar: DocActionSource
DocActionSource_ContextMenu: DocActionSource
DocActionSource_ViewFilePage: DocActionSource
UserFieldType_unknown: UserFieldType
UserFieldType_firstName: UserFieldType
UserFieldType_lastName: UserFieldType
UserFieldType_companyName: UserFieldType
UserFieldType_displayName: UserFieldType
UserFieldType_profileStatus: UserFieldType
UserFieldType_bio: UserFieldType
UploadFileUnknown: ImportType
UploadFileButton: ImportType
UploadFileDnD: ImportType
UploadFileCopyPaste: ImportType
ViewOwnProfile: PublicProfileViewType
ViewOtherProfileAuthd: PublicProfileViewType
ViewOtherProfileUnauthd: PublicProfileViewType
DownloadMethod_Unknown: DownloadMethod
DownloadMethod_LP_Button: DownloadMethod
DownloadMethod_DragAndDrop: DownloadMethod
DownloadMethod_SaveAs: DownloadMethod
ViewFileSource_unknown: ViewFileSource
ViewFileSource_contextMenu: ViewFileSource
ViewFileSource_doubleClick: ViewFileSource
ViewFileSource_toolbar: ViewFileSource
ViewFileSource_URL: ViewFileSource
ViewFileSource_shared: ViewFileSource
SocialMediaTypeUnknown: SocialMediaType
SocialMediaTypeInstagram: SocialMediaType
SocialMediaTypeDiscord: SocialMediaType
SocialMediaTypeYoutube: SocialMediaType
SocialMediaLinkLocationUnknown: SocialMediaLinkLocation
SocialMediaLinkLocationTopNav: SocialMediaLinkLocation
SocialMediaLinkLocationPopup: SocialMediaLinkLocation
DownloadLocationUnknown: DownloadGSLocation
DownloadLocationSideBar: DownloadGSLocation
DownloadLocationDeepLink: DownloadGSLocation
DownloadLocationDeepLinkLaunch: DownloadGSLocation
DownloadLocationEnterprisePage: DownloadGSLocation
DownloadLocationEnterprisePageVersioned: DownloadGSLocation
DoNotShowAgainSource_Unknown: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamRenameFile: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamUploadFile: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamMoveFileByModal: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamMoveFileByDrag: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamNewRoom: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamRestoreFile: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamNewFolder: DoNotShowAgainSource
DoNotShowAgainSource_GuestTeamNewFolderCustomPath: DoNotShowAgainSource
AddTeamMemberLocation_Unknown: AddTeamMemberLocation
AddTeamMemberLocation_OrgMembersList: AddTeamMemberLocation
AddTeamMemberLocation_TeamMembersList: AddTeamMemberLocation
AddTeamMemberLocation_CreateTeamModal: AddTeamMemberLocation
RecentsType_Unknown: RecentsType
RecentsType_Files: RecentsType
RecentsType_Suggested: RecentsType
RecentsType_Recents: RecentsType
RecentsTimePeriod_Unknown: RecentsTimePeriod
RecentsTimePeriod_Today: RecentsTimePeriod
RecentsTimePeriod_ThisWeek: RecentsTimePeriod
RecentsTimePeriod_ThisMonth: RecentsTimePeriod
RecentsTimePeriod_ThisYear: RecentsTimePeriod
RecentsTimePeriod_Earlier: RecentsTimePeriod
SearchScope_Unknown: SearchScope
SearchScope_Full: SearchScope
SearchScope_Folder: SearchScope
FilterOption_Unknown: FilterOption
FilterOption_Sketches: FilterOption
FilterOption_ReferenceImages: FilterOption
FilterOption_ImportLibrary: FilterOption
FilterOption_Screenshots: FilterOption
FilterOption_Exports: FilterOption
FilterOption_CollabRooms: FilterOption
SortByOption_Unknown: SortByOption
SortByOption_Name: SortByOption
SortByOption_Created: SortByOption
SortByOption_Updated: SortByOption
SortByOption_Size: SortByOption
SortOrder_Unknown: SortOrder
SortOrder_Ascending: SortOrder
SortOrder_Descending: SortOrder
ViewMode_Unknown: ViewMode
ViewMode_Tiled: ViewMode
ViewMode_List: ViewMode
EmailLink_Unknown: EmailLink
EmailLink_Gmail: EmailLink
EmailLink_Outlook: EmailLink
Unknown: DocActionType
JoinRoom: DocActionType
ViewDoc: DocActionType
SetRoomPassword: DocActionType
ShareDoc: DocActionType
CopyInviteLink: DocActionType
MoveDoc: DocActionType
RenameDoc: DocActionType
DeleteDoc: DocActionType
EnterFolder: DocActionType
RemoveAccessToRoom: DocActionType
DownloadDoc: DocActionType
SendDoc: DocActionType
ExportDoc: DocActionType
Workspace_unknown: Workspace
Workspace_bonusPack: Workspace
Workspace_personalSpace: Workspace
Workspace_orgSpace: Workspace
NavbarNavigateOption_unknown: NavbarNavigateOption
NavbarNavigateOption_personalOrgSpace: NavbarNavigateOption
NavbarNavigateOption_sharedOrgSpace: NavbarNavigateOption
NavbarNavigateOption_teamSpace: NavbarNavigateOption
NavbarNavigateOption_manageOrg: NavbarNavigateOption
NavbarNavigateOption_manageMembers: NavbarNavigateOption
NavbarNavigateOption_manageTeams: NavbarNavigateOption
NavbarNavigateOption_cloudExports: NavbarNavigateOption
NavbarNavigateOption_recents: NavbarNavigateOption
NavbarNavigateOption_trashBin: NavbarNavigateOption

class WebEvent(_message.Message):
    __slots__ = ("eventType", "timestamp", "userId", "spaceId", "orgName", "docId", "sessionEventId", "deviceInfo", "sessionId", "docType", "recentsType", "recentsTimePeriod", "toggleAside", "uploadFile", "downloadFile", "downloadMultipleFiles", "trashFile", "viewFile", "createFolder", "renameFile", "openExternalSocialMedia", "moveFile", "sendFile", "receiveFile", "shareRoom", "directExportDownload", "downloadGS", "deeplinkLaunch", "acceptShareRoom", "requestInviteToAdmin", "approveRequestInviteToAdmin", "requestRoomAccess", "approveRoomAccessRequest", "updateProfileBio", "updateProfileStatus", "publicProfileView", "connectionInvitation", "toggleLayout", "toggleDoNotShowAgain", "changeRoomRole", "removeFromRoom", "search", "filter", "sortBy", "changeViewMode", "dragAndDropDocuments", "docActionTriggered", "exportViaPresetModal", "requestChangeEmail", "changeUserField", "toggleMFA", "toggleOrgLevelMFA", "inviteOrgMember", "changeOrgRole", "removeOrgUser", "makeOrgUserInactive", "renameTeam", "addTeamMembers", "changeTeamRole", "removeTeamMember", "removeAllTeamMembers", "openEmailLink", "sendLoginCode", "loginViaEmailCode", "click3DModelOnSignUp", "switchWorkspace", "navbarNavigate", "paywallTriggered", "discoverBusiness", "discoverUpgradeToPro", "userClicksUpgradeToPro", "goToPricingPage", "triggerProPaywall", "triggerProTierCap", "learnMoreBusiness", "connectWithAnExpert")
    EVENTTYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    ORGNAME_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    SESSIONEVENTID_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    RECENTSTYPE_FIELD_NUMBER: _ClassVar[int]
    RECENTSTIMEPERIOD_FIELD_NUMBER: _ClassVar[int]
    TOGGLEASIDE_FIELD_NUMBER: _ClassVar[int]
    UPLOADFILE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADFILE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADMULTIPLEFILES_FIELD_NUMBER: _ClassVar[int]
    TRASHFILE_FIELD_NUMBER: _ClassVar[int]
    VIEWFILE_FIELD_NUMBER: _ClassVar[int]
    CREATEFOLDER_FIELD_NUMBER: _ClassVar[int]
    RENAMEFILE_FIELD_NUMBER: _ClassVar[int]
    OPENEXTERNALSOCIALMEDIA_FIELD_NUMBER: _ClassVar[int]
    MOVEFILE_FIELD_NUMBER: _ClassVar[int]
    SENDFILE_FIELD_NUMBER: _ClassVar[int]
    RECEIVEFILE_FIELD_NUMBER: _ClassVar[int]
    SHAREROOM_FIELD_NUMBER: _ClassVar[int]
    DIRECTEXPORTDOWNLOAD_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADGS_FIELD_NUMBER: _ClassVar[int]
    DEEPLINKLAUNCH_FIELD_NUMBER: _ClassVar[int]
    ACCEPTSHAREROOM_FIELD_NUMBER: _ClassVar[int]
    REQUESTINVITETOADMIN_FIELD_NUMBER: _ClassVar[int]
    APPROVEREQUESTINVITETOADMIN_FIELD_NUMBER: _ClassVar[int]
    REQUESTROOMACCESS_FIELD_NUMBER: _ClassVar[int]
    APPROVEROOMACCESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEPROFILEBIO_FIELD_NUMBER: _ClassVar[int]
    UPDATEPROFILESTATUS_FIELD_NUMBER: _ClassVar[int]
    PUBLICPROFILEVIEW_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONINVITATION_FIELD_NUMBER: _ClassVar[int]
    TOGGLELAYOUT_FIELD_NUMBER: _ClassVar[int]
    TOGGLEDONOTSHOWAGAIN_FIELD_NUMBER: _ClassVar[int]
    CHANGEROOMROLE_FIELD_NUMBER: _ClassVar[int]
    REMOVEFROMROOM_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SORTBY_FIELD_NUMBER: _ClassVar[int]
    CHANGEVIEWMODE_FIELD_NUMBER: _ClassVar[int]
    DRAGANDDROPDOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    DOCACTIONTRIGGERED_FIELD_NUMBER: _ClassVar[int]
    EXPORTVIAPRESETMODAL_FIELD_NUMBER: _ClassVar[int]
    REQUESTCHANGEEMAIL_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERFIELD_FIELD_NUMBER: _ClassVar[int]
    TOGGLEMFA_FIELD_NUMBER: _ClassVar[int]
    TOGGLEORGLEVELMFA_FIELD_NUMBER: _ClassVar[int]
    INVITEORGMEMBER_FIELD_NUMBER: _ClassVar[int]
    CHANGEORGROLE_FIELD_NUMBER: _ClassVar[int]
    REMOVEORGUSER_FIELD_NUMBER: _ClassVar[int]
    MAKEORGUSERINACTIVE_FIELD_NUMBER: _ClassVar[int]
    RENAMETEAM_FIELD_NUMBER: _ClassVar[int]
    ADDTEAMMEMBERS_FIELD_NUMBER: _ClassVar[int]
    CHANGETEAMROLE_FIELD_NUMBER: _ClassVar[int]
    REMOVETEAMMEMBER_FIELD_NUMBER: _ClassVar[int]
    REMOVEALLTEAMMEMBERS_FIELD_NUMBER: _ClassVar[int]
    OPENEMAILLINK_FIELD_NUMBER: _ClassVar[int]
    SENDLOGINCODE_FIELD_NUMBER: _ClassVar[int]
    LOGINVIAEMAILCODE_FIELD_NUMBER: _ClassVar[int]
    CLICK3DMODELONSIGNUP_FIELD_NUMBER: _ClassVar[int]
    SWITCHWORKSPACE_FIELD_NUMBER: _ClassVar[int]
    NAVBARNAVIGATE_FIELD_NUMBER: _ClassVar[int]
    PAYWALLTRIGGERED_FIELD_NUMBER: _ClassVar[int]
    DISCOVERBUSINESS_FIELD_NUMBER: _ClassVar[int]
    DISCOVERUPGRADETOPRO_FIELD_NUMBER: _ClassVar[int]
    USERCLICKSUPGRADETOPRO_FIELD_NUMBER: _ClassVar[int]
    GOTOPRICINGPAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERPROPAYWALL_FIELD_NUMBER: _ClassVar[int]
    TRIGGERPROTIERCAP_FIELD_NUMBER: _ClassVar[int]
    LEARNMOREBUSINESS_FIELD_NUMBER: _ClassVar[int]
    CONNECTWITHANEXPERT_FIELD_NUMBER: _ClassVar[int]
    eventType: WebEventType
    timestamp: int
    userId: str
    spaceId: _gravi_model_pb2.SpaceId
    orgName: str
    docId: str
    sessionEventId: int
    deviceInfo: _gravi_model_pb2.DeviceInfo
    sessionId: str
    docType: _gravi_model_pb2.DocumentType
    recentsType: RecentsType
    recentsTimePeriod: RecentsTimePeriod
    toggleAside: WebEventToggleAside
    uploadFile: WebEventUploadFile
    downloadFile: WebEventDownloadFile
    downloadMultipleFiles: WebEventDownloadMultipleFiles
    trashFile: WebEventTrashFile
    viewFile: WebEventViewFile
    createFolder: WebEventCreateFolder
    renameFile: WebEventRenameFile
    openExternalSocialMedia: WebEventOpenExternalSocialMedia
    moveFile: WebEventMoveFile
    sendFile: WebEventSendFile
    receiveFile: WebEventReceiveFile
    shareRoom: WebEventShareRoom
    directExportDownload: WebEventDirectDownloadExport
    downloadGS: WebEventDownloadGS
    deeplinkLaunch: WebEventDeeplinkLaunch
    acceptShareRoom: WebEventAcceptShareRoom
    requestInviteToAdmin: WebEventRequestInviteToAdmin
    approveRequestInviteToAdmin: WebEventApproveRequestInviteToAdmin
    requestRoomAccess: WebEventRequestRoomAccess
    approveRoomAccessRequest: WebEventApproveRoomAccessRequest
    updateProfileBio: WebEventUpdateProfileBio
    updateProfileStatus: WebEventUpdateProfileStatus
    publicProfileView: WebEventPublicProfileView
    connectionInvitation: WebEventConnectionInvitation
    toggleLayout: WebEventToggleLayout
    toggleDoNotShowAgain: WebEventToggleDoNotShowAgain
    changeRoomRole: WebEventChangeRoomRole
    removeFromRoom: WebEventRemoveFromRoom
    search: WebEventSearch
    filter: WebEventFilter
    sortBy: WebEventSortBy
    changeViewMode: WebEventChangeViewMode
    dragAndDropDocuments: WebEventDragAndDropDocuments
    docActionTriggered: WebDocActionTriggered
    exportViaPresetModal: WebEventExportViaPresetModal
    requestChangeEmail: WebEventRequestChangeEmail
    changeUserField: WebEventChangeUserField
    toggleMFA: WebEventToggleMFA
    toggleOrgLevelMFA: WebEventToggleOrgLevelMFA
    inviteOrgMember: WebEventInviteOrgMember
    changeOrgRole: WebEventChangeOrgRole
    removeOrgUser: WebEventRemoveOrgUser
    makeOrgUserInactive: WebEventMakeOrgUserInactive
    renameTeam: WebEventRenameTeam
    addTeamMembers: WebEventAddTeamMembers
    changeTeamRole: WebEventChangeTeamRole
    removeTeamMember: WebEventRemoveTeamMember
    removeAllTeamMembers: WebEventRemoveAllTeamMembers
    openEmailLink: WebEventOpenEmailForMagicLogin
    sendLoginCode: WebEventSendLoginCode
    loginViaEmailCode: WebEventLoginViaEmailCode
    click3DModelOnSignUp: WebEventClick3DModelOnSignUp
    switchWorkspace: WebEventSwitchWorkspace
    navbarNavigate: WebEventNavbarNavigate
    paywallTriggered: WebEventPaywallTriggered
    discoverBusiness: WebEventDiscoverBusiness
    discoverUpgradeToPro: WebEventDiscoverUpgradeToPro
    userClicksUpgradeToPro: WebEventUserClickUpgradeToPro
    goToPricingPage: WebEventGoToPricingPage
    triggerProPaywall: WebEventTriggerProPaywall
    triggerProTierCap: WebEventTriggerProTierCap
    learnMoreBusiness: WebEventLearnMoreBusiness
    connectWithAnExpert: WebEventConnectWithAnExpert
    def __init__(self, eventType: _Optional[_Union[WebEventType, str]] = ..., timestamp: _Optional[int] = ..., userId: _Optional[str] = ..., spaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., orgName: _Optional[str] = ..., docId: _Optional[str] = ..., sessionEventId: _Optional[int] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., sessionId: _Optional[str] = ..., docType: _Optional[_Union[_gravi_model_pb2.DocumentType, str]] = ..., recentsType: _Optional[_Union[RecentsType, str]] = ..., recentsTimePeriod: _Optional[_Union[RecentsTimePeriod, str]] = ..., toggleAside: _Optional[_Union[WebEventToggleAside, _Mapping]] = ..., uploadFile: _Optional[_Union[WebEventUploadFile, _Mapping]] = ..., downloadFile: _Optional[_Union[WebEventDownloadFile, _Mapping]] = ..., downloadMultipleFiles: _Optional[_Union[WebEventDownloadMultipleFiles, _Mapping]] = ..., trashFile: _Optional[_Union[WebEventTrashFile, _Mapping]] = ..., viewFile: _Optional[_Union[WebEventViewFile, _Mapping]] = ..., createFolder: _Optional[_Union[WebEventCreateFolder, _Mapping]] = ..., renameFile: _Optional[_Union[WebEventRenameFile, _Mapping]] = ..., openExternalSocialMedia: _Optional[_Union[WebEventOpenExternalSocialMedia, _Mapping]] = ..., moveFile: _Optional[_Union[WebEventMoveFile, _Mapping]] = ..., sendFile: _Optional[_Union[WebEventSendFile, _Mapping]] = ..., receiveFile: _Optional[_Union[WebEventReceiveFile, _Mapping]] = ..., shareRoom: _Optional[_Union[WebEventShareRoom, _Mapping]] = ..., directExportDownload: _Optional[_Union[WebEventDirectDownloadExport, _Mapping]] = ..., downloadGS: _Optional[_Union[WebEventDownloadGS, _Mapping]] = ..., deeplinkLaunch: _Optional[_Union[WebEventDeeplinkLaunch, _Mapping]] = ..., acceptShareRoom: _Optional[_Union[WebEventAcceptShareRoom, _Mapping]] = ..., requestInviteToAdmin: _Optional[_Union[WebEventRequestInviteToAdmin, _Mapping]] = ..., approveRequestInviteToAdmin: _Optional[_Union[WebEventApproveRequestInviteToAdmin, _Mapping]] = ..., requestRoomAccess: _Optional[_Union[WebEventRequestRoomAccess, _Mapping]] = ..., approveRoomAccessRequest: _Optional[_Union[WebEventApproveRoomAccessRequest, _Mapping]] = ..., updateProfileBio: _Optional[_Union[WebEventUpdateProfileBio, _Mapping]] = ..., updateProfileStatus: _Optional[_Union[WebEventUpdateProfileStatus, _Mapping]] = ..., publicProfileView: _Optional[_Union[WebEventPublicProfileView, _Mapping]] = ..., connectionInvitation: _Optional[_Union[WebEventConnectionInvitation, _Mapping]] = ..., toggleLayout: _Optional[_Union[WebEventToggleLayout, _Mapping]] = ..., toggleDoNotShowAgain: _Optional[_Union[WebEventToggleDoNotShowAgain, _Mapping]] = ..., changeRoomRole: _Optional[_Union[WebEventChangeRoomRole, _Mapping]] = ..., removeFromRoom: _Optional[_Union[WebEventRemoveFromRoom, _Mapping]] = ..., search: _Optional[_Union[WebEventSearch, _Mapping]] = ..., filter: _Optional[_Union[WebEventFilter, _Mapping]] = ..., sortBy: _Optional[_Union[WebEventSortBy, _Mapping]] = ..., changeViewMode: _Optional[_Union[WebEventChangeViewMode, _Mapping]] = ..., dragAndDropDocuments: _Optional[_Union[WebEventDragAndDropDocuments, _Mapping]] = ..., docActionTriggered: _Optional[_Union[WebDocActionTriggered, _Mapping]] = ..., exportViaPresetModal: _Optional[_Union[WebEventExportViaPresetModal, _Mapping]] = ..., requestChangeEmail: _Optional[_Union[WebEventRequestChangeEmail, _Mapping]] = ..., changeUserField: _Optional[_Union[WebEventChangeUserField, _Mapping]] = ..., toggleMFA: _Optional[_Union[WebEventToggleMFA, _Mapping]] = ..., toggleOrgLevelMFA: _Optional[_Union[WebEventToggleOrgLevelMFA, _Mapping]] = ..., inviteOrgMember: _Optional[_Union[WebEventInviteOrgMember, _Mapping]] = ..., changeOrgRole: _Optional[_Union[WebEventChangeOrgRole, _Mapping]] = ..., removeOrgUser: _Optional[_Union[WebEventRemoveOrgUser, _Mapping]] = ..., makeOrgUserInactive: _Optional[_Union[WebEventMakeOrgUserInactive, _Mapping]] = ..., renameTeam: _Optional[_Union[WebEventRenameTeam, _Mapping]] = ..., addTeamMembers: _Optional[_Union[WebEventAddTeamMembers, _Mapping]] = ..., changeTeamRole: _Optional[_Union[WebEventChangeTeamRole, _Mapping]] = ..., removeTeamMember: _Optional[_Union[WebEventRemoveTeamMember, _Mapping]] = ..., removeAllTeamMembers: _Optional[_Union[WebEventRemoveAllTeamMembers, _Mapping]] = ..., openEmailLink: _Optional[_Union[WebEventOpenEmailForMagicLogin, _Mapping]] = ..., sendLoginCode: _Optional[_Union[WebEventSendLoginCode, _Mapping]] = ..., loginViaEmailCode: _Optional[_Union[WebEventLoginViaEmailCode, _Mapping]] = ..., click3DModelOnSignUp: _Optional[_Union[WebEventClick3DModelOnSignUp, _Mapping]] = ..., switchWorkspace: _Optional[_Union[WebEventSwitchWorkspace, _Mapping]] = ..., navbarNavigate: _Optional[_Union[WebEventNavbarNavigate, _Mapping]] = ..., paywallTriggered: _Optional[_Union[WebEventPaywallTriggered, _Mapping]] = ..., discoverBusiness: _Optional[_Union[WebEventDiscoverBusiness, _Mapping]] = ..., discoverUpgradeToPro: _Optional[_Union[WebEventDiscoverUpgradeToPro, _Mapping]] = ..., userClicksUpgradeToPro: _Optional[_Union[WebEventUserClickUpgradeToPro, _Mapping]] = ..., goToPricingPage: _Optional[_Union[WebEventGoToPricingPage, _Mapping]] = ..., triggerProPaywall: _Optional[_Union[WebEventTriggerProPaywall, _Mapping]] = ..., triggerProTierCap: _Optional[_Union[WebEventTriggerProTierCap, _Mapping]] = ..., learnMoreBusiness: _Optional[_Union[WebEventLearnMoreBusiness, _Mapping]] = ..., connectWithAnExpert: _Optional[_Union[WebEventConnectWithAnExpert, _Mapping]] = ...) -> None: ...

class WebEventUploadFile(_message.Message):
    __slots__ = ("docSize", "importType")
    DOCSIZE_FIELD_NUMBER: _ClassVar[int]
    IMPORTTYPE_FIELD_NUMBER: _ClassVar[int]
    docSize: int
    importType: ImportType
    def __init__(self, docSize: _Optional[int] = ..., importType: _Optional[_Union[ImportType, str]] = ...) -> None: ...

class WebEventDownloadFile(_message.Message):
    __slots__ = ("downloadMethod", "docSize")
    DOWNLOADMETHOD_FIELD_NUMBER: _ClassVar[int]
    DOCSIZE_FIELD_NUMBER: _ClassVar[int]
    downloadMethod: DownloadMethod
    docSize: int
    def __init__(self, downloadMethod: _Optional[_Union[DownloadMethod, str]] = ..., docSize: _Optional[int] = ...) -> None: ...

class WebEventDownloadMultipleFiles(_message.Message):
    __slots__ = ("downloadedDocsIds", "docTypes", "docSizes")
    DOWNLOADEDDOCSIDS_FIELD_NUMBER: _ClassVar[int]
    DOCTYPES_FIELD_NUMBER: _ClassVar[int]
    DOCSIZES_FIELD_NUMBER: _ClassVar[int]
    downloadedDocsIds: _containers.RepeatedScalarFieldContainer[str]
    docTypes: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.DocumentType]
    docSizes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, downloadedDocsIds: _Optional[_Iterable[str]] = ..., docTypes: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentType, str]]] = ..., docSizes: _Optional[_Iterable[int]] = ...) -> None: ...

class WebEventTrashFile(_message.Message):
    __slots__ = ("docSize",)
    DOCSIZE_FIELD_NUMBER: _ClassVar[int]
    docSize: int
    def __init__(self, docSize: _Optional[int] = ...) -> None: ...

class WebEventViewFile(_message.Message):
    __slots__ = ("docSize", "viewFileSource")
    DOCSIZE_FIELD_NUMBER: _ClassVar[int]
    VIEWFILESOURCE_FIELD_NUMBER: _ClassVar[int]
    docSize: int
    viewFileSource: ViewFileSource
    def __init__(self, docSize: _Optional[int] = ..., viewFileSource: _Optional[_Union[ViewFileSource, str]] = ...) -> None: ...

class WebEventCreateFolder(_message.Message):
    __slots__ = ("docFullPath",)
    DOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    docFullPath: str
    def __init__(self, docFullPath: _Optional[str] = ...) -> None: ...

class WebEventRenameFile(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WebEventDirectDownloadExport(_message.Message):
    __slots__ = ("docSize",)
    DOCSIZE_FIELD_NUMBER: _ClassVar[int]
    docSize: int
    def __init__(self, docSize: _Optional[int] = ...) -> None: ...

class WebEventOpenExternalSocialMedia(_message.Message):
    __slots__ = ("type", "linkLocation")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LINKLOCATION_FIELD_NUMBER: _ClassVar[int]
    type: SocialMediaType
    linkLocation: SocialMediaLinkLocation
    def __init__(self, type: _Optional[_Union[SocialMediaType, str]] = ..., linkLocation: _Optional[_Union[SocialMediaLinkLocation, str]] = ...) -> None: ...

class WebEventMoveFile(_message.Message):
    __slots__ = ("toSpaceId",)
    TOSPACEID_FIELD_NUMBER: _ClassVar[int]
    toSpaceId: _gravi_model_pb2.SpaceId
    def __init__(self, toSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ...) -> None: ...

class WebEventSendFile(_message.Message):
    __slots__ = ("sendId",)
    SENDID_FIELD_NUMBER: _ClassVar[int]
    sendId: str
    def __init__(self, sendId: _Optional[str] = ...) -> None: ...

class WebEventReceiveFile(_message.Message):
    __slots__ = ("sendId",)
    SENDID_FIELD_NUMBER: _ClassVar[int]
    sendId: str
    def __init__(self, sendId: _Optional[str] = ...) -> None: ...

class WebEventDownloadGS(_message.Message):
    __slots__ = ("downloadLocation", "version")
    DOWNLOADLOCATION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    downloadLocation: DownloadGSLocation
    version: str
    def __init__(self, downloadLocation: _Optional[_Union[DownloadGSLocation, str]] = ..., version: _Optional[str] = ...) -> None: ...

class WebEventDeeplinkLaunch(_message.Message):
    __slots__ = ("deepLinkLocation", "isRetry")
    DEEPLINKLOCATION_FIELD_NUMBER: _ClassVar[int]
    ISRETRY_FIELD_NUMBER: _ClassVar[int]
    deepLinkLocation: _gravi_model_pb2.GSDeepLinkLocation
    isRetry: bool
    def __init__(self, deepLinkLocation: _Optional[_Union[_gravi_model_pb2.GSDeepLinkLocation, str]] = ..., isRetry: bool = ...) -> None: ...

class WebEventBatch(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[WebEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[WebEvent, _Mapping]]] = ...) -> None: ...

class WebEventShareRoom(_message.Message):
    __slots__ = ("userId", "magicId", "role", "downLeveledRole", "externalInvite", "success")
    USERID_FIELD_NUMBER: _ClassVar[int]
    MAGICID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLEVELEDROLE_FIELD_NUMBER: _ClassVar[int]
    EXTERNALINVITE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    userId: str
    magicId: str
    role: _gravi_model_pb2.CollaborationRole
    downLeveledRole: _gravi_model_pb2.CollaborationRole
    externalInvite: bool
    success: bool
    def __init__(self, userId: _Optional[str] = ..., magicId: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., downLeveledRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., externalInvite: bool = ..., success: bool = ...) -> None: ...

class WebEventChangeRoomRole(_message.Message):
    __slots__ = ("userId", "fromRole", "toRole", "success")
    USERID_FIELD_NUMBER: _ClassVar[int]
    FROMROLE_FIELD_NUMBER: _ClassVar[int]
    TOROLE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    userId: str
    fromRole: _gravi_model_pb2.CollaborationRole
    toRole: _gravi_model_pb2.CollaborationRole
    success: bool
    def __init__(self, userId: _Optional[str] = ..., fromRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., toRole: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ..., success: bool = ...) -> None: ...

class WebEventRemoveFromRoom(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class WebEventRequestInviteToAdmin(_message.Message):
    __slots__ = ("userId", "role", "selfRequest")
    USERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SELFREQUEST_FIELD_NUMBER: _ClassVar[int]
    userId: str
    role: _gravi_model_pb2.OrgMemberRole
    selfRequest: bool
    def __init__(self, userId: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., selfRequest: bool = ...) -> None: ...

class WebEventApproveRequestInviteToAdmin(_message.Message):
    __slots__ = ("approved", "userId", "role", "status")
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    approved: bool
    userId: str
    role: _gravi_model_pb2.OrgMemberRole
    status: _gravi_model_pb2.OrgMemberStatus
    def __init__(self, approved: bool = ..., userId: _Optional[str] = ..., role: _Optional[_Union[_gravi_model_pb2.OrgMemberRole, str]] = ..., status: _Optional[_Union[_gravi_model_pb2.OrgMemberStatus, str]] = ...) -> None: ...

class WebEventRequestRoomAccess(_message.Message):
    __slots__ = ("isOrg",)
    ISORG_FIELD_NUMBER: _ClassVar[int]
    isOrg: bool
    def __init__(self, isOrg: bool = ...) -> None: ...

class WebEventApproveRoomAccessRequest(_message.Message):
    __slots__ = ("userId", "approved", "role")
    USERID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    userId: str
    approved: bool
    role: _gravi_model_pb2.CollaborationRole
    def __init__(self, userId: _Optional[str] = ..., approved: bool = ..., role: _Optional[_Union[_gravi_model_pb2.CollaborationRole, str]] = ...) -> None: ...

class WebEventAcceptShareRoom(_message.Message):
    __slots__ = ("userId", "magicId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    MAGICID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    magicId: str
    def __init__(self, userId: _Optional[str] = ..., magicId: _Optional[str] = ...) -> None: ...

class WebEventUpdateProfileBio(_message.Message):
    __slots__ = ("bio",)
    BIO_FIELD_NUMBER: _ClassVar[int]
    bio: str
    def __init__(self, bio: _Optional[str] = ...) -> None: ...

class WebEventUpdateProfileStatus(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _gravi_model_pb2.PublicProfileStatus
    def __init__(self, status: _Optional[_Union[_gravi_model_pb2.PublicProfileStatus, str]] = ...) -> None: ...

class WebEventPublicProfileView(_message.Message):
    __slots__ = ("profileId", "type")
    PROFILEID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    profileId: str
    type: PublicProfileViewType
    def __init__(self, profileId: _Optional[str] = ..., type: _Optional[_Union[PublicProfileViewType, str]] = ...) -> None: ...

class WebEventConnectionInvitation(_message.Message):
    __slots__ = ("invitationId", "senderId", "recipientId")
    INVITATIONID_FIELD_NUMBER: _ClassVar[int]
    SENDERID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTID_FIELD_NUMBER: _ClassVar[int]
    invitationId: str
    senderId: str
    recipientId: str
    def __init__(self, invitationId: _Optional[str] = ..., senderId: _Optional[str] = ..., recipientId: _Optional[str] = ...) -> None: ...

class WebEventToggleLayout(_message.Message):
    __slots__ = ("isOldLayout",)
    ISOLDLAYOUT_FIELD_NUMBER: _ClassVar[int]
    isOldLayout: bool
    def __init__(self, isOldLayout: bool = ...) -> None: ...

class WebEventToggleAside(_message.Message):
    __slots__ = ("isOpen",)
    ISOPEN_FIELD_NUMBER: _ClassVar[int]
    isOpen: bool
    def __init__(self, isOpen: bool = ...) -> None: ...

class WebEventToggleDoNotShowAgain(_message.Message):
    __slots__ = ("checked", "source")
    CHECKED_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    checked: bool
    source: DoNotShowAgainSource
    def __init__(self, checked: bool = ..., source: _Optional[_Union[DoNotShowAgainSource, str]] = ...) -> None: ...

class WebEventSearch(_message.Message):
    __slots__ = ("userStartedSearch", "userSubmittedSearch", "searchScope")
    USERSTARTEDSEARCH_FIELD_NUMBER: _ClassVar[int]
    USERSUBMITTEDSEARCH_FIELD_NUMBER: _ClassVar[int]
    SEARCHSCOPE_FIELD_NUMBER: _ClassVar[int]
    userStartedSearch: bool
    userSubmittedSearch: bool
    searchScope: SearchScope
    def __init__(self, userStartedSearch: bool = ..., userSubmittedSearch: bool = ..., searchScope: _Optional[_Union[SearchScope, str]] = ...) -> None: ...

class WebEventFilter(_message.Message):
    __slots__ = ("openedFilterMenu", "clickedClearAll", "selectedFilterOptions")
    OPENEDFILTERMENU_FIELD_NUMBER: _ClassVar[int]
    CLICKEDCLEARALL_FIELD_NUMBER: _ClassVar[int]
    SELECTEDFILTEROPTIONS_FIELD_NUMBER: _ClassVar[int]
    openedFilterMenu: bool
    clickedClearAll: bool
    selectedFilterOptions: _containers.RepeatedScalarFieldContainer[FilterOption]
    def __init__(self, openedFilterMenu: bool = ..., clickedClearAll: bool = ..., selectedFilterOptions: _Optional[_Iterable[_Union[FilterOption, str]]] = ...) -> None: ...

class WebEventSortBy(_message.Message):
    __slots__ = ("openedSortByMenu", "selectedSortByOption", "toggledSortOrder")
    OPENEDSORTBYMENU_FIELD_NUMBER: _ClassVar[int]
    SELECTEDSORTBYOPTION_FIELD_NUMBER: _ClassVar[int]
    TOGGLEDSORTORDER_FIELD_NUMBER: _ClassVar[int]
    openedSortByMenu: bool
    selectedSortByOption: SortByOption
    toggledSortOrder: SortOrder
    def __init__(self, openedSortByMenu: bool = ..., selectedSortByOption: _Optional[_Union[SortByOption, str]] = ..., toggledSortOrder: _Optional[_Union[SortOrder, str]] = ...) -> None: ...

class WebEventChangeViewMode(_message.Message):
    __slots__ = ("toggledToViewMode",)
    TOGGLEDTOVIEWMODE_FIELD_NUMBER: _ClassVar[int]
    toggledToViewMode: ViewMode
    def __init__(self, toggledToViewMode: _Optional[_Union[ViewMode, str]] = ...) -> None: ...

class WebEventDragAndDropDocuments(_message.Message):
    __slots__ = ("numDocsSelected",)
    NUMDOCSSELECTED_FIELD_NUMBER: _ClassVar[int]
    numDocsSelected: int
    def __init__(self, numDocsSelected: _Optional[int] = ...) -> None: ...

class WebEventRequestChangeEmail(_message.Message):
    __slots__ = ("paywallStatus",)
    PAYWALLSTATUS_FIELD_NUMBER: _ClassVar[int]
    paywallStatus: _gravi_model_pb2.PaywallStatus
    def __init__(self, paywallStatus: _Optional[_Union[_gravi_model_pb2.PaywallStatus, str]] = ...) -> None: ...

class WebEventChangeUserField(_message.Message):
    __slots__ = ("fieldChanged",)
    FIELDCHANGED_FIELD_NUMBER: _ClassVar[int]
    fieldChanged: UserFieldType
    def __init__(self, fieldChanged: _Optional[_Union[UserFieldType, str]] = ...) -> None: ...

class WebEventOpenEmailForMagicLogin(_message.Message):
    __slots__ = ("emailLink",)
    EMAILLINK_FIELD_NUMBER: _ClassVar[int]
    emailLink: EmailLink
    def __init__(self, emailLink: _Optional[_Union[EmailLink, str]] = ...) -> None: ...

class WebEventSendLoginCode(_message.Message):
    __slots__ = ("queryCode",)
    QUERYCODE_FIELD_NUMBER: _ClassVar[int]
    queryCode: str
    def __init__(self, queryCode: _Optional[str] = ...) -> None: ...

class WebEventLoginViaEmailCode(_message.Message):
    __slots__ = ("queryCode",)
    QUERYCODE_FIELD_NUMBER: _ClassVar[int]
    queryCode: str
    def __init__(self, queryCode: _Optional[str] = ...) -> None: ...

class WebEventClick3DModelOnSignUp(_message.Message):
    __slots__ = ("displayModel",)
    DISPLAYMODEL_FIELD_NUMBER: _ClassVar[int]
    displayModel: str
    def __init__(self, displayModel: _Optional[str] = ...) -> None: ...

class WebDocActionTriggered(_message.Message):
    __slots__ = ("actionType", "docActionSource", "listDocTypesSelected")
    ACTIONTYPE_FIELD_NUMBER: _ClassVar[int]
    DOCACTIONSOURCE_FIELD_NUMBER: _ClassVar[int]
    LISTDOCTYPESSELECTED_FIELD_NUMBER: _ClassVar[int]
    actionType: DocActionType
    docActionSource: DocActionSource
    listDocTypesSelected: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.DocumentType]
    def __init__(self, actionType: _Optional[_Union[DocActionType, str]] = ..., docActionSource: _Optional[_Union[DocActionSource, str]] = ..., listDocTypesSelected: _Optional[_Iterable[_Union[_gravi_model_pb2.DocumentType, str]]] = ...) -> None: ...

class WebEventToggleMFA(_message.Message):
    __slots__ = ("activated",)
    ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    activated: bool
    def __init__(self, activated: bool = ...) -> None: ...

class WebEventSwitchWorkspace(_message.Message):
    __slots__ = ("fromLocation", "toLocation")
    FROMLOCATION_FIELD_NUMBER: _ClassVar[int]
    TOLOCATION_FIELD_NUMBER: _ClassVar[int]
    fromLocation: Workspace
    toLocation: Workspace
    def __init__(self, fromLocation: _Optional[_Union[Workspace, str]] = ..., toLocation: _Optional[_Union[Workspace, str]] = ...) -> None: ...

class WebEventNavbarNavigate(_message.Message):
    __slots__ = ("to",)
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    to: NavbarNavigateOption
    def __init__(self, to: _Optional[_Union[NavbarNavigateOption, str]] = ..., **kwargs) -> None: ...

class WebEventToggleOrgLevelMFA(_message.Message):
    __slots__ = ("toggledOn",)
    TOGGLEDON_FIELD_NUMBER: _ClassVar[int]
    toggledOn: bool
    def __init__(self, toggledOn: bool = ...) -> None: ...

class WebEventInviteOrgMember(_message.Message):
    __slots__ = ("emails", "licenseType", "asPersonalAccount")
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    LICENSETYPE_FIELD_NUMBER: _ClassVar[int]
    ASPERSONALACCOUNT_FIELD_NUMBER: _ClassVar[int]
    emails: _containers.RepeatedScalarFieldContainer[str]
    licenseType: _gravi_model_pb2.OrgLicenseType
    asPersonalAccount: bool
    def __init__(self, emails: _Optional[_Iterable[str]] = ..., licenseType: _Optional[_Union[_gravi_model_pb2.OrgLicenseType, str]] = ..., asPersonalAccount: bool = ...) -> None: ...

class WebEventChangeOrgRole(_message.Message):
    __slots__ = ("fromRole", "toRole", "changedRoleUserId")
    FROMROLE_FIELD_NUMBER: _ClassVar[int]
    TOROLE_FIELD_NUMBER: _ClassVar[int]
    CHANGEDROLEUSERID_FIELD_NUMBER: _ClassVar[int]
    fromRole: _gravi_model_pb2.OrgRoleType
    toRole: _gravi_model_pb2.OrgRoleType
    changedRoleUserId: str
    def __init__(self, fromRole: _Optional[_Union[_gravi_model_pb2.OrgRoleType, str]] = ..., toRole: _Optional[_Union[_gravi_model_pb2.OrgRoleType, str]] = ..., changedRoleUserId: _Optional[str] = ...) -> None: ...

class WebEventRemoveOrgUser(_message.Message):
    __slots__ = ("removedOrgUserId",)
    REMOVEDORGUSERID_FIELD_NUMBER: _ClassVar[int]
    removedOrgUserId: str
    def __init__(self, removedOrgUserId: _Optional[str] = ...) -> None: ...

class WebEventMakeOrgUserInactive(_message.Message):
    __slots__ = ("deactivated", "inactivatedOrgUser")
    DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    INACTIVATEDORGUSER_FIELD_NUMBER: _ClassVar[int]
    deactivated: bool
    inactivatedOrgUser: str
    def __init__(self, deactivated: bool = ..., inactivatedOrgUser: _Optional[str] = ...) -> None: ...

class WebEventRenameTeam(_message.Message):
    __slots__ = ("teamId",)
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    teamId: str
    def __init__(self, teamId: _Optional[str] = ...) -> None: ...

class WebEventAddTeamMembers(_message.Message):
    __slots__ = ("addedUserIds", "asRole", "teamId", "location")
    ADDEDUSERIDS_FIELD_NUMBER: _ClassVar[int]
    ASROLE_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    addedUserIds: _containers.RepeatedScalarFieldContainer[str]
    asRole: _team_pb2.OrgTeamRole
    teamId: str
    location: AddTeamMemberLocation
    def __init__(self, addedUserIds: _Optional[_Iterable[str]] = ..., asRole: _Optional[_Union[_team_pb2.OrgTeamRole, str]] = ..., teamId: _Optional[str] = ..., location: _Optional[_Union[AddTeamMemberLocation, str]] = ...) -> None: ...

class WebEventChangeTeamRole(_message.Message):
    __slots__ = ("userId", "fromRole", "toRole", "teamId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    FROMROLE_FIELD_NUMBER: _ClassVar[int]
    TOROLE_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    fromRole: _team_pb2.OrgTeamRole
    toRole: _team_pb2.OrgTeamRole
    teamId: str
    def __init__(self, userId: _Optional[str] = ..., fromRole: _Optional[_Union[_team_pb2.OrgTeamRole, str]] = ..., toRole: _Optional[_Union[_team_pb2.OrgTeamRole, str]] = ..., teamId: _Optional[str] = ...) -> None: ...

class WebEventRemoveTeamMember(_message.Message):
    __slots__ = ("userId", "teamId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    teamId: str
    def __init__(self, userId: _Optional[str] = ..., teamId: _Optional[str] = ...) -> None: ...

class WebEventRemoveAllTeamMembers(_message.Message):
    __slots__ = ("numMembersRemoved", "teamId")
    NUMMEMBERSREMOVED_FIELD_NUMBER: _ClassVar[int]
    TEAMID_FIELD_NUMBER: _ClassVar[int]
    numMembersRemoved: int
    teamId: str
    def __init__(self, numMembersRemoved: _Optional[int] = ..., teamId: _Optional[str] = ...) -> None: ...

class WebEventPaywallTriggered(_message.Message):
    __slots__ = ("paywallType",)
    PAYWALLTYPE_FIELD_NUMBER: _ClassVar[int]
    paywallType: _gravi_model_pb2.PaywallType
    def __init__(self, paywallType: _Optional[_Union[_gravi_model_pb2.PaywallType, str]] = ...) -> None: ...

class WebEventDiscoverBusiness(_message.Message):
    __slots__ = ("paywallStatus",)
    PAYWALLSTATUS_FIELD_NUMBER: _ClassVar[int]
    paywallStatus: _gravi_model_pb2.PaywallStatus
    def __init__(self, paywallStatus: _Optional[_Union[_gravi_model_pb2.PaywallStatus, str]] = ...) -> None: ...

class WebEventDiscoverUpgradeToPro(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class WebEventUserClickUpgradeToPro(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class WebEventGoToPricingPage(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class WebEventLearnMoreBusiness(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class WebEventConnectWithAnExpert(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class WebEventTriggerProPaywall(_message.Message):
    __slots__ = ("paywallType",)
    PAYWALLTYPE_FIELD_NUMBER: _ClassVar[int]
    paywallType: _gravi_model_pb2.PaywallType
    def __init__(self, paywallType: _Optional[_Union[_gravi_model_pb2.PaywallType, str]] = ...) -> None: ...

class WebEventTriggerProTierCap(_message.Message):
    __slots__ = ("paywallType", "storageAllowance")
    PAYWALLTYPE_FIELD_NUMBER: _ClassVar[int]
    STORAGEALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    paywallType: _gravi_model_pb2.PaywallType
    storageAllowance: int
    def __init__(self, paywallType: _Optional[_Union[_gravi_model_pb2.PaywallType, str]] = ..., storageAllowance: _Optional[int] = ...) -> None: ...

class WebEventExportViaPresetModal(_message.Message):
    __slots__ = ("exportPreference",)
    EXPORTPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    exportPreference: _preferences_pb2.ExportPreferencesTO
    def __init__(self, exportPreference: _Optional[_Union[_preferences_pb2.ExportPreferencesTO, _Mapping]] = ...) -> None: ...
