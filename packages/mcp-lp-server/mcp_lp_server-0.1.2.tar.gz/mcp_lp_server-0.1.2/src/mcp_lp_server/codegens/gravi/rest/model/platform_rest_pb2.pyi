from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.models import notifications_pb2 as _notifications_pb2
from gravi.rest.doc import doc_rest_pb2 as _doc_rest_pb2
from gravi.rest.doc import export_pb2 as _export_pb2
from gravi.rest.doc import room_pb2 as _room_pb2
from gravi.rest.doc import comment_pb2 as _comment_pb2
from gravi.rest.auth import auth_pb2 as _auth_pb2
from gravi.rest.user import profile_pb2 as _profile_pb2
from gravi.rest.user import connections_pb2 as _connections_pb2
from gravi.rest.user import update_check_pb2 as _update_check_pb2
from gravi.rest.org import management_pb2 as _management_pb2
from gravi.rest.org import invitation_pb2 as _invitation_pb2
from gravi.rest.org import team_pb2 as _team_pb2
from gravi.rest.org import team_member_pb2 as _team_member_pb2
from gravi.localization import localization_pb2 as _localization_pb2
from gravi.rest.model import signup_pb2 as _signup_pb2
from gravi.rest.model import achievement_pb2 as _achievement_pb2
from gravi.rest.model import organisation_pb2 as _organisation_pb2
from gravi.rest.voicechat import transcribe_pb2 as _transcribe_pb2
from gravi.rest.model import collab_pb2 as _collab_pb2
from gravi.rest.user import account_pb2 as _account_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.rest.model import activate_code_pb2 as _activate_code_pb2
from gravi.rest.model import login_pb2 as _login_pb2
from gravi.rest.model import pair_device_pb2 as _pair_device_pb2
from gravi.rest.model import online_sketch_pb2 as _online_sketch_pb2
from gravi.rest.ai import ask_pb2 as _ask_pb2
from gravi.rest.ai import image_pb2 as _image_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlatformRestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[PlatformRestType]
    Login: _ClassVar[PlatformRestType]
    RenewTicket: _ClassVar[PlatformRestType]
    Logout: _ClassVar[PlatformRestType]
    MagicLinkLogin: _ClassVar[PlatformRestType]
    SignUp: _ClassVar[PlatformRestType]
    SteamLogin: _ClassVar[PlatformRestType]
    OculusLogin: _ClassVar[PlatformRestType]
    SteamSignUp: _ClassVar[PlatformRestType]
    OculusSignUp: _ClassVar[PlatformRestType]
    SteamEmailAccountLink: _ClassVar[PlatformRestType]
    OculusEmailAccountLink: _ClassVar[PlatformRestType]
    DetachDevice: _ClassVar[PlatformRestType]
    AppleLogin: _ClassVar[PlatformRestType]
    AppleSignUp: _ClassVar[PlatformRestType]
    AppleGrsAccountLink: _ClassVar[PlatformRestType]
    DeleteAccount: _ClassVar[PlatformRestType]
    EarlyAdopterCheck: _ClassVar[PlatformRestType]
    SignUpByEmailPass: _ClassVar[PlatformRestType]
    LoginBySavedTicket: _ClassVar[PlatformRestType]
    ListSSOProvidersEmail: _ClassVar[PlatformRestType]
    InitiateOidcSSOLogin: _ClassVar[PlatformRestType]
    CompleteOidcSSOLogin: _ClassVar[PlatformRestType]
    GetSSOProviderForSignup: _ClassVar[PlatformRestType]
    SendBetaSignupEmail: _ClassVar[PlatformRestType]
    SignUpWithSSO: _ClassVar[PlatformRestType]
    ResendEmailVerification: _ClassVar[PlatformRestType]
    LoginByOneTimeAuthToken: _ClassVar[PlatformRestType]
    GetPublicKey: _ClassVar[PlatformRestType]
    AttachEmail: _ClassVar[PlatformRestType]
    GetCMSURL: _ClassVar[PlatformRestType]
    ResendStoreSignupEmail: _ClassVar[PlatformRestType]
    InvalidateSignupLink: _ClassVar[PlatformRestType]
    InitiateSignUp: _ClassVar[PlatformRestType]
    EnableMfa: _ClassVar[PlatformRestType]
    SendUserFeedback: _ClassVar[PlatformRestType]
    EnableTwoFactorAuth: _ClassVar[PlatformRestType]
    CompleteSignUpByCode: _ClassVar[PlatformRestType]
    ActivateCode: _ClassVar[PlatformRestType]
    ActivateMagicLinkLoginCode: _ClassVar[PlatformRestType]
    LoginByEmail: _ClassVar[PlatformRestType]
    GetLoggedInUser: _ClassVar[PlatformRestType]
    GetLoggedInUserV2: _ClassVar[PlatformRestType]
    UpdateUserInfo: _ClassVar[PlatformRestType]
    SendPasswordResetEmail: _ClassVar[PlatformRestType]
    ResetPassword: _ClassVar[PlatformRestType]
    ChangePassword: _ClassVar[PlatformRestType]
    ChangeEmail: _ClassVar[PlatformRestType]
    GenerateSecretKey: _ClassVar[PlatformRestType]
    DeleteTwoFactorKey: _ClassVar[PlatformRestType]
    GetLoggedInUserOrgInfo: _ClassVar[PlatformRestType]
    GetSubscriptionPack: _ClassVar[PlatformRestType]
    ConsumeNotification: _ClassVar[PlatformRestType]
    ChangeUserPassword: _ClassVar[PlatformRestType]
    GetLoggedUserSummary: _ClassVar[PlatformRestType]
    GetNotificationsForLoggedInUser: _ClassVar[PlatformRestType]
    CreateUserSurvey: _ClassVar[PlatformRestType]
    GetOrg: _ClassVar[PlatformRestType]
    ListUserLoginAudits: _ClassVar[PlatformRestType]
    ListOrgUserActionAudits: _ClassVar[PlatformRestType]
    CreateVoiceToTextUrl: _ClassVar[PlatformRestType]
    ConvertDoc: _ClassVar[PlatformRestType]
    ListDocs: _ClassVar[PlatformRestType]
    ListRecentDocs: _ClassVar[PlatformRestType]
    DeprecatedGetDocuments: _ClassVar[PlatformRestType]
    GetUsedSpaceSize: _ClassVar[PlatformRestType]
    SendDocument: _ClassVar[PlatformRestType]
    CreateFolder: _ClassVar[PlatformRestType]
    MoveDocument: _ClassVar[PlatformRestType]
    InitiateFileUpload: _ClassVar[PlatformRestType]
    DownloadDoc: _ClassVar[PlatformRestType]
    CreateDoc: _ClassVar[PlatformRestType]
    UpdateDoc: _ClassVar[PlatformRestType]
    TrashDoc: _ClassVar[PlatformRestType]
    RestoreDoc: _ClassVar[PlatformRestType]
    ListDocsInBin: _ClassVar[PlatformRestType]
    deleteDocsInBin: _ClassVar[PlatformRestType]
    ExportDoc: _ClassVar[PlatformRestType]
    ListDocExports: _ClassVar[PlatformRestType]
    DownloadDocExport: _ClassVar[PlatformRestType]
    GetDocExport: _ClassVar[PlatformRestType]
    SearchDocs: _ClassVar[PlatformRestType]
    UploadDocExport: _ClassVar[PlatformRestType]
    CreateDocAsset: _ClassVar[PlatformRestType]
    DownloadDocAssets: _ClassVar[PlatformRestType]
    CreateDocExportEntry: _ClassVar[PlatformRestType]
    GetSketchRoomUpdates: _ClassVar[PlatformRestType]
    UploadDocThumbnail: _ClassVar[PlatformRestType]
    CopyDoc: _ClassVar[PlatformRestType]
    SearchPublicContentDocByPath: _ClassVar[PlatformRestType]
    GetDocumentById: _ClassVar[PlatformRestType]
    GetDocumentByPath: _ClassVar[PlatformRestType]
    GetDocumentSpaceName: _ClassVar[PlatformRestType]
    CreateDocComment: _ClassVar[PlatformRestType]
    ListDocComments: _ClassVar[PlatformRestType]
    UpdateDocComment: _ClassVar[PlatformRestType]
    ListNewDocComments: _ClassVar[PlatformRestType]
    GeneratePairDeviceCode: _ClassVar[PlatformRestType]
    PairDevice: _ClassVar[PlatformRestType]
    GetPairedDevice: _ClassVar[PlatformRestType]
    RevokeDevicePairing: _ClassVar[PlatformRestType]
    GetUserFromPairedDeviceId: _ClassVar[PlatformRestType]
    LaunchRoom: _ClassVar[PlatformRestType]
    EnterRoom: _ClassVar[PlatformRestType]
    ShutdownRoom: _ClassVar[PlatformRestType]
    ReleaseRoomInitLock: _ClassVar[PlatformRestType]
    InviteUsersToCollab: _ClassVar[PlatformRestType]
    ListInvitableUsers: _ClassVar[PlatformRestType]
    EnterRoomWithDeepLink: _ClassVar[PlatformRestType]
    ChangeUserCollaborationRole: _ClassVar[PlatformRestType]
    ListSharedDocs: _ClassVar[PlatformRestType]
    ReportAbusiveBehaviour: _ClassVar[PlatformRestType]
    ListRoomRecordings: _ClassVar[PlatformRestType]
    ReplayRoomRecording: _ClassVar[PlatformRestType]
    GetRoomRecording: _ClassVar[PlatformRestType]
    GetRoomRecordingReplayData: _ClassVar[PlatformRestType]
    GetRoomRecordingReplayAssets: _ClassVar[PlatformRestType]
    ShareRoomWithUser: _ClassVar[PlatformRestType]
    ListRoomAccesses: _ClassVar[PlatformRestType]
    RemoveAccessFromRoom: _ClassVar[PlatformRestType]
    SetCoSketchRoomPass: _ClassVar[PlatformRestType]
    GenerateDeepAccessLink: _ClassVar[PlatformRestType]
    EnterPublicRoom: _ClassVar[PlatformRestType]
    BookmarkPublicDoc: _ClassVar[PlatformRestType]
    ListPublicRoom: _ClassVar[PlatformRestType]
    SetPublicDoc: _ClassVar[PlatformRestType]
    StopRoomSharing: _ClassVar[PlatformRestType]
    CreateEnterRoomNotification: _ClassVar[PlatformRestType]
    EnterRoomOneStep: _ClassVar[PlatformRestType]
    EnterRoomNonLPUser: _ClassVar[PlatformRestType]
    ListRoomAccessRequests: _ClassVar[PlatformRestType]
    ApproveRoomAccess: _ClassVar[PlatformRestType]
    ListAllUsersWithAccessToDoc: _ClassVar[PlatformRestType]
    LaunchStreamingAgentForRoom: _ClassVar[PlatformRestType]
    EnterRoomViaAdminNotificationDeeplink: _ClassVar[PlatformRestType]
    CheckForClientAppUpdate: _ClassVar[PlatformRestType]
    GetRoomIdByShortCode: _ClassVar[PlatformRestType]
    GetShortCodeByRoomId: _ClassVar[PlatformRestType]
    OfflineUserAppLaunched: _ClassVar[PlatformRestType]
    OfflineUserSync: _ClassVar[PlatformRestType]
    SyncAchievement: _ClassVar[PlatformRestType]
    GetAchievements: _ClassVar[PlatformRestType]
    UpdateOrg: _ClassVar[PlatformRestType]
    MarkTeamAsFavorite: _ClassVar[PlatformRestType]
    RemoveExternalMembersFromTeam: _ClassVar[PlatformRestType]
    ListAllTeamsForUser: _ClassVar[PlatformRestType]
    ListOrgTeamMembers: _ClassVar[PlatformRestType]
    ListUserOrgTeamMemberships: _ClassVar[PlatformRestType]
    CreateOrgTeam: _ClassVar[PlatformRestType]
    DeleteOrgTeam: _ClassVar[PlatformRestType]
    ListOrgTeams: _ClassVar[PlatformRestType]
    GetOrgTeam: _ClassVar[PlatformRestType]
    UpdateOrgTeam: _ClassVar[PlatformRestType]
    CreateOrgTeamMember: _ClassVar[PlatformRestType]
    DeleteOrgTeamMember: _ClassVar[PlatformRestType]
    UpdateOrgTeamMember: _ClassVar[PlatformRestType]
    GetTeam: _ClassVar[PlatformRestType]
    GetAllOrgTeams: _ClassVar[PlatformRestType]
    InviteMembers: _ClassVar[PlatformRestType]
    EditMemberActiveStatus: _ClassVar[PlatformRestType]
    SwitchUserOrg: _ClassVar[PlatformRestType]
    EditMemberRole: _ClassVar[PlatformRestType]
    GetOrgDownloadVersions: _ClassVar[PlatformRestType]
    RequestUserInviteToOrgAdmin: _ClassVar[PlatformRestType]
    UserInviteApproval: _ClassVar[PlatformRestType]
    ListOrgJoinRequests: _ClassVar[PlatformRestType]
    RequestRoomAccess: _ClassVar[PlatformRestType]
    RemoveMemberFromOrg: _ClassVar[PlatformRestType]
    GetUsersInOrg: _ClassVar[PlatformRestType]
    ListOrgMembershipInvitations: _ClassVar[PlatformRestType]
    DeleteOrgMembershipInvitation: _ClassVar[PlatformRestType]
    CreateOrgAccountsByOrgAdmin: _ClassVar[PlatformRestType]
    CreateConnectionInvitation: _ClassVar[PlatformRestType]
    ListConnectionInvitations: _ClassVar[PlatformRestType]
    UpdateConnectionInvitation: _ClassVar[PlatformRestType]
    ListConnections: _ClassVar[PlatformRestType]
    InitiateOidcAuthorisation: _ClassVar[PlatformRestType]
    CompleteOidcAuthorisation: _ClassVar[PlatformRestType]
    RevokeOidcAuthorisation: _ClassVar[PlatformRestType]
    SearchPublicUser: _ClassVar[PlatformRestType]
    CreateCommunityStudio: _ClassVar[PlatformRestType]
    UpdateCommunityStudio: _ClassVar[PlatformRestType]
    GetCommunityStudio: _ClassVar[PlatformRestType]
    ListCommunityStudios: _ClassVar[PlatformRestType]
    SendSupportEmail: _ClassVar[PlatformRestType]
    RequestCertificate: _ClassVar[PlatformRestType]
    UpdateSketchObjects: _ClassVar[PlatformRestType]
    HandraiseToPaywall: _ClassVar[PlatformRestType]
    ConsumeDownloadAllowance: _ClassVar[PlatformRestType]
    CreateSubscription: _ClassVar[PlatformRestType]
    GetSubscriptionPrice: _ClassVar[PlatformRestType]
    GetStripeCustomerPortalLink: _ClassVar[PlatformRestType]
    PostImageToDiscord: _ClassVar[PlatformRestType]
    GetPublicUserProfile: _ClassVar[PlatformRestType]
    MaintenanceCheck: _ClassVar[PlatformRestType]
    ListPublicSpaceDocs: _ClassVar[PlatformRestType]
    DownloadPublicSpaceDoc: _ClassVar[PlatformRestType]
    DownloadOverrideConfig: _ClassVar[PlatformRestType]
    Transcribe: _ClassVar[PlatformRestType]
    AskShrek: _ClassVar[PlatformRestType]
    GenerateImages: _ClassVar[PlatformRestType]
    Generate3DModel: _ClassVar[PlatformRestType]

class PlatformRestError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownErrorType: _ClassVar[PlatformRestError]
    Ok: _ClassVar[PlatformRestError]
    ClientCancelled: _ClassVar[PlatformRestError]
    BadClientRequest: _ClassVar[PlatformRestError]
    DeadlineExceeded: _ClassVar[PlatformRestError]
    PermissionDenied: _ClassVar[PlatformRestError]
    Unauthenticated: _ClassVar[PlatformRestError]
    NotFound: _ClassVar[PlatformRestError]
    ServerAborted: _ClassVar[PlatformRestError]
    ServerError: _ClassVar[PlatformRestError]
    ServerUnavailable: _ClassVar[PlatformRestError]
    ConnectionError: _ClassVar[PlatformRestError]
    InValidClientVersion: _ClassVar[PlatformRestError]
    ConnectionTimeout: _ClassVar[PlatformRestError]
    OrgRequiredVersionViolation: _ClassVar[PlatformRestError]
    InvalidLicense: _ClassVar[PlatformRestError]
    NotAllowedRequest: _ClassVar[PlatformRestError]
    ExceedLicenseCount: _ClassVar[PlatformRestError]
    InvalidTicket: _ClassVar[PlatformRestError]

class SourceAppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SourceAppTypeUnset: _ClassVar[SourceAppType]
    SourceAppCommunity: _ClassVar[SourceAppType]
    SourceAppEnterprise: _ClassVar[SourceAppType]

class AnalyticsHint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AnalyticsHintUnset: _ClassVar[AnalyticsHint]
    AnalyticsHintPaywallTriggered: _ClassVar[AnalyticsHint]

class ChangeUserPasswordResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ChangeUserPasswordResponseCode_Success: _ClassVar[ChangeUserPasswordResponseCode]
    ChangeUserPasswordResponseCode_SameOldNewPassword: _ClassVar[ChangeUserPasswordResponseCode]
    ChangeUserPasswordResponseCode_InvalidPassword: _ClassVar[ChangeUserPasswordResponseCode]
    ChangeUserPasswordResponseCode_IncorrectPassword: _ClassVar[ChangeUserPasswordResponseCode]

class AccountDeletionFeedbackType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AccountDeletionFeedbackType_Unset: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_Others: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_NeverStarted: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_StoppedUsing: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_DontUseLandingPad: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_HaveAnotherAccount: _ClassVar[AccountDeletionFeedbackType]
    AccountDeletionFeedbackType_DataPrivacy: _ClassVar[AccountDeletionFeedbackType]

class DeleteAccountResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeleteAccountResponseCode_Success: _ClassVar[DeleteAccountResponseCode]
    DeleteAccountResponseCode_IncorrectPassword: _ClassVar[DeleteAccountResponseCode]

class MagicLinkLoginResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MagicLinkLoginSuccess: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginSignupRequired: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginWaitingForLinkConfirm: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginFailed: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginInvalidEmail: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginInvalidLoginType: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginLinkNotFoundOrExpired: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginInvalidReCaptcha: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginSSOSignUpRequired: _ClassVar[MagicLinkLoginResultCode]
    MagicLinkLoginSSOLoginRequired: _ClassVar[MagicLinkLoginResultCode]

class MagicLinkLoginType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MagicLinkLoginType_LPAuthentication: _ClassVar[MagicLinkLoginType]
    MagicLinkLoginType_EmailAuthentication: _ClassVar[MagicLinkLoginType]

class OculusAppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InvalidDevice: _ClassVar[OculusAppType]
    OculusRift: _ClassVar[OculusAppType]
    OculusQuest: _ClassVar[OculusAppType]

class SignUpResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SignUpResponseCodeSuccess: _ClassVar[SignUpResponseCode]
    SignUpResponseCodeEmailAlreadyInUse: _ClassVar[SignUpResponseCode]
    SignUpResponseCodePasswordTooSimple: _ClassVar[SignUpResponseCode]

class EmailAccountLinkResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EmailAccountLinkUnknown: _ClassVar[EmailAccountLinkResult]
    EmailAccountLinkSuccess: _ClassVar[EmailAccountLinkResult]
    EmailAccountLinkedToOtherDevice: _ClassVar[EmailAccountLinkResult]

class AttachEmailResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AttachEmailSuccess: _ClassVar[AttachEmailResult]
    AttachEmailEmailUsed: _ClassVar[AttachEmailResult]
    AttachEmailInvalidEmail: _ClassVar[AttachEmailResult]
    AttachEmailNetIssue: _ClassVar[AttachEmailResult]

class LaunchRoomResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LaunchRoomResponseCodeUnknown: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeSuccess: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeRoomNotFound: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeServerError: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeNoReadyInstance: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeMaxLaunchedRoomExceeded: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeInitLockExists: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeNoPermission: _ClassVar[LaunchRoomResponseCode]
    LaunchRoomResponseCodeRoomShuttingDown: _ClassVar[LaunchRoomResponseCode]

class EnterRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EnterRoomUnknown: _ClassVar[EnterRoomResult]
    EnterRoomSuccess: _ClassVar[EnterRoomResult]
    EnterRoomOutOfDateClientVersion: _ClassVar[EnterRoomResult]
    EnterRoomRoomNotFound: _ClassVar[EnterRoomResult]
    EnterRoomServerFailure: _ClassVar[EnterRoomResult]
    EnterRoomMaxUserCapExceeded: _ClassVar[EnterRoomResult]
    EnterRoomRoomNotLaunchedOrReady: _ClassVar[EnterRoomResult]
    EnterRoomNoPermission: _ClassVar[EnterRoomResult]
    EnterRoomServerOutOfDate: _ClassVar[EnterRoomResult]
    EnterRoomInitLockExists: _ClassVar[EnterRoomResult]
    EnterRoomMaxLaunchedRoomExceeded: _ClassVar[EnterRoomResult]
    EnterRoomResultScreenAppDisallowed: _ClassVar[EnterRoomResult]
    EnterRoomResultWaitingForHostToLaunch: _ClassVar[EnterRoomResult]
    EnterRoomResultWaitingForHostToGrantEntry: _ClassVar[EnterRoomResult]
    EnterRoomResultPasswordFailed: _ClassVar[EnterRoomResult]
    EnterRoomResultRoomOwnerIsNotPresent: _ClassVar[EnterRoomResult]
    EnterRoomResultDeepLinkNotFound: _ClassVar[EnterRoomResult]
    EnterRoomResultViaOneTimeAdminTokenNotInGSOrg: _ClassVar[EnterRoomResult]

class ShutdownRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ShutdownRoomUnknown: _ClassVar[ShutdownRoomResult]
    ShutdownRoomSuccess: _ClassVar[ShutdownRoomResult]
    ShutdownRoomHasConnectedUsers: _ClassVar[ShutdownRoomResult]
    ShutdownRoomNotReadyStatus: _ClassVar[ShutdownRoomResult]
    ShutdownRoomServerError: _ClassVar[ShutdownRoomResult]

class InviteUsersToCollabResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InviteUsersToCollabResponseCodeSuccess: _ClassVar[InviteUsersToCollabResponseCode]
    InviteUsersToCollabResponseCodeDocNotFound: _ClassVar[InviteUsersToCollabResponseCode]
    InviteUsersToCollabResponseCodeInvalidDocType: _ClassVar[InviteUsersToCollabResponseCode]
    InviteUsersToCollabResponseCodeInvalidInvitedRole: _ClassVar[InviteUsersToCollabResponseCode]
    InviteUsersToCollabResponseCodeOculusIdsOnlyApplicableToFreeCollab: _ClassVar[InviteUsersToCollabResponseCode]

class DeletePersistedRoomResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeletePersistedRoomUnknown: _ClassVar[DeletePersistedRoomResult]
    DeletePersistedRoomSuccess: _ClassVar[DeletePersistedRoomResult]
    DeletePersistedRoomHasConnectedUsers: _ClassVar[DeletePersistedRoomResult]
    DeletePersistedRoomServerError: _ClassVar[DeletePersistedRoomResult]

class BetaEmailType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    noEmail: _ClassVar[BetaEmailType]
    subD: _ClassVar[BetaEmailType]
    toolBelt: _ClassVar[BetaEmailType]

class ResendStoreSignupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ResendStoreSignupType_Unknown: _ClassVar[ResendStoreSignupType]
    ResendStoreSignupType_Steam: _ClassVar[ResendStoreSignupType]
    ResendStoreSignupType_Oculus: _ClassVar[ResendStoreSignupType]
    ResendStoreSignupType_GSStore: _ClassVar[ResendStoreSignupType]

class ResendStoreSignupEmailResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ResendStoreSignupEmailResultUnknownError: _ClassVar[ResendStoreSignupEmailResult]
    ResendStoreSignupEmailResultSuccess: _ClassVar[ResendStoreSignupEmailResult]
    ResendStoreSignupEmailResultLinkMissing: _ClassVar[ResendStoreSignupEmailResult]

class ReplayRecordingResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ReplayRecordingUnknown: _ClassVar[ReplayRecordingResult]
    ReplayRecordingSuccess: _ClassVar[ReplayRecordingResult]
    ReplayRecordingFinished: _ClassVar[ReplayRecordingResult]
    ReplayRecordingNotFound: _ClassVar[ReplayRecordingResult]
    ReplayRecordingOnGoing: _ClassVar[ReplayRecordingResult]
    ReplayRecordingFailed: _ClassVar[ReplayRecordingResult]
    ReplayRecordingNoPermission: _ClassVar[ReplayRecordingResult]

class GetPublicUserProfileResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetPublicUserProfileResult_Success: _ClassVar[GetPublicUserProfileResult]
    GetPublicUserProfileResult_PrivateProfile: _ClassVar[GetPublicUserProfileResult]

class GetOrgResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetOrgResponseCodeSuccess: _ClassVar[GetOrgResponseCode]
    GetOrgResponseCodeOrgNotFound: _ClassVar[GetOrgResponseCode]

class PostImageToDiscordResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UndefinedPostToDiscordResponseCode: _ClassVar[PostImageToDiscordResponseCode]
    PostImageToDiscordSuccess: _ClassVar[PostImageToDiscordResponseCode]
    InvalidDiscordChannel: _ClassVar[PostImageToDiscordResponseCode]
    InvalidOrMissingImageData: _ClassVar[PostImageToDiscordResponseCode]
    DiscordServerSendError: _ClassVar[PostImageToDiscordResponseCode]
    DiscordServerInitialiseError: _ClassVar[PostImageToDiscordResponseCode]

class DiscordChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UnknownDiscordChannel: _ClassVar[DiscordChannelType]
    GSDiscordServerInkGameAprilFools: _ClassVar[DiscordChannelType]

class CreateVoiceToTextUrlResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateVoiceToTextUrlUnknown: _ClassVar[CreateVoiceToTextUrlResult]
    CreateVoiceToTextUrlSuccess: _ClassVar[CreateVoiceToTextUrlResult]
    CreateVoiceToTextUrlNoPermission: _ClassVar[CreateVoiceToTextUrlResult]

class UpdateCommunityStudioResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateCommunityStudioResponseCodeSuccess: _ClassVar[UpdateCommunityStudioResponseCode]
    UpdateCommunityStudioResponseCodeStudioNotFound: _ClassVar[UpdateCommunityStudioResponseCode]

class RequestCertificateResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RequestCertificateResponseCodeUnknown: _ClassVar[RequestCertificateResponseCode]
    RequestCertificateResponseCodeSuccess: _ClassVar[RequestCertificateResponseCode]

class HandraiseToPaywallRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    None: _ClassVar[HandraiseToPaywallRequestType]
    ForBusiness: _ClassVar[HandraiseToPaywallRequestType]
    ForIndividual: _ClassVar[HandraiseToPaywallRequestType]
    ForTeamsPlan: _ClassVar[HandraiseToPaywallRequestType]
    ForEnterprisePlan: _ClassVar[HandraiseToPaywallRequestType]

class ConsumeDownloadAllowanceResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ConsumeDownloadAllowanceResponseCodeSuccess: _ClassVar[ConsumeDownloadAllowanceResponseCode]
    ConsumeDownloadAllowanceResponseCodeInsufficientCredit: _ClassVar[ConsumeDownloadAllowanceResponseCode]
    ConsumeDownloadAllowanceResponseCodeVersionOutOfDate: _ClassVar[ConsumeDownloadAllowanceResponseCode]
Unknown: PlatformRestType
Login: PlatformRestType
RenewTicket: PlatformRestType
Logout: PlatformRestType
MagicLinkLogin: PlatformRestType
SignUp: PlatformRestType
SteamLogin: PlatformRestType
OculusLogin: PlatformRestType
SteamSignUp: PlatformRestType
OculusSignUp: PlatformRestType
SteamEmailAccountLink: PlatformRestType
OculusEmailAccountLink: PlatformRestType
DetachDevice: PlatformRestType
AppleLogin: PlatformRestType
AppleSignUp: PlatformRestType
AppleGrsAccountLink: PlatformRestType
DeleteAccount: PlatformRestType
EarlyAdopterCheck: PlatformRestType
SignUpByEmailPass: PlatformRestType
LoginBySavedTicket: PlatformRestType
ListSSOProvidersEmail: PlatformRestType
InitiateOidcSSOLogin: PlatformRestType
CompleteOidcSSOLogin: PlatformRestType
GetSSOProviderForSignup: PlatformRestType
SendBetaSignupEmail: PlatformRestType
SignUpWithSSO: PlatformRestType
ResendEmailVerification: PlatformRestType
LoginByOneTimeAuthToken: PlatformRestType
GetPublicKey: PlatformRestType
AttachEmail: PlatformRestType
GetCMSURL: PlatformRestType
ResendStoreSignupEmail: PlatformRestType
InvalidateSignupLink: PlatformRestType
InitiateSignUp: PlatformRestType
EnableMfa: PlatformRestType
SendUserFeedback: PlatformRestType
EnableTwoFactorAuth: PlatformRestType
CompleteSignUpByCode: PlatformRestType
ActivateCode: PlatformRestType
ActivateMagicLinkLoginCode: PlatformRestType
LoginByEmail: PlatformRestType
GetLoggedInUser: PlatformRestType
GetLoggedInUserV2: PlatformRestType
UpdateUserInfo: PlatformRestType
SendPasswordResetEmail: PlatformRestType
ResetPassword: PlatformRestType
ChangePassword: PlatformRestType
ChangeEmail: PlatformRestType
GenerateSecretKey: PlatformRestType
DeleteTwoFactorKey: PlatformRestType
GetLoggedInUserOrgInfo: PlatformRestType
GetSubscriptionPack: PlatformRestType
ConsumeNotification: PlatformRestType
ChangeUserPassword: PlatformRestType
GetLoggedUserSummary: PlatformRestType
GetNotificationsForLoggedInUser: PlatformRestType
CreateUserSurvey: PlatformRestType
GetOrg: PlatformRestType
ListUserLoginAudits: PlatformRestType
ListOrgUserActionAudits: PlatformRestType
CreateVoiceToTextUrl: PlatformRestType
ConvertDoc: PlatformRestType
ListDocs: PlatformRestType
ListRecentDocs: PlatformRestType
DeprecatedGetDocuments: PlatformRestType
GetUsedSpaceSize: PlatformRestType
SendDocument: PlatformRestType
CreateFolder: PlatformRestType
MoveDocument: PlatformRestType
InitiateFileUpload: PlatformRestType
DownloadDoc: PlatformRestType
CreateDoc: PlatformRestType
UpdateDoc: PlatformRestType
TrashDoc: PlatformRestType
RestoreDoc: PlatformRestType
ListDocsInBin: PlatformRestType
deleteDocsInBin: PlatformRestType
ExportDoc: PlatformRestType
ListDocExports: PlatformRestType
DownloadDocExport: PlatformRestType
GetDocExport: PlatformRestType
SearchDocs: PlatformRestType
UploadDocExport: PlatformRestType
CreateDocAsset: PlatformRestType
DownloadDocAssets: PlatformRestType
CreateDocExportEntry: PlatformRestType
GetSketchRoomUpdates: PlatformRestType
UploadDocThumbnail: PlatformRestType
CopyDoc: PlatformRestType
SearchPublicContentDocByPath: PlatformRestType
GetDocumentById: PlatformRestType
GetDocumentByPath: PlatformRestType
GetDocumentSpaceName: PlatformRestType
CreateDocComment: PlatformRestType
ListDocComments: PlatformRestType
UpdateDocComment: PlatformRestType
ListNewDocComments: PlatformRestType
GeneratePairDeviceCode: PlatformRestType
PairDevice: PlatformRestType
GetPairedDevice: PlatformRestType
RevokeDevicePairing: PlatformRestType
GetUserFromPairedDeviceId: PlatformRestType
LaunchRoom: PlatformRestType
EnterRoom: PlatformRestType
ShutdownRoom: PlatformRestType
ReleaseRoomInitLock: PlatformRestType
InviteUsersToCollab: PlatformRestType
ListInvitableUsers: PlatformRestType
EnterRoomWithDeepLink: PlatformRestType
ChangeUserCollaborationRole: PlatformRestType
ListSharedDocs: PlatformRestType
ReportAbusiveBehaviour: PlatformRestType
ListRoomRecordings: PlatformRestType
ReplayRoomRecording: PlatformRestType
GetRoomRecording: PlatformRestType
GetRoomRecordingReplayData: PlatformRestType
GetRoomRecordingReplayAssets: PlatformRestType
ShareRoomWithUser: PlatformRestType
ListRoomAccesses: PlatformRestType
RemoveAccessFromRoom: PlatformRestType
SetCoSketchRoomPass: PlatformRestType
GenerateDeepAccessLink: PlatformRestType
EnterPublicRoom: PlatformRestType
BookmarkPublicDoc: PlatformRestType
ListPublicRoom: PlatformRestType
SetPublicDoc: PlatformRestType
StopRoomSharing: PlatformRestType
CreateEnterRoomNotification: PlatformRestType
EnterRoomOneStep: PlatformRestType
EnterRoomNonLPUser: PlatformRestType
ListRoomAccessRequests: PlatformRestType
ApproveRoomAccess: PlatformRestType
ListAllUsersWithAccessToDoc: PlatformRestType
LaunchStreamingAgentForRoom: PlatformRestType
EnterRoomViaAdminNotificationDeeplink: PlatformRestType
CheckForClientAppUpdate: PlatformRestType
GetRoomIdByShortCode: PlatformRestType
GetShortCodeByRoomId: PlatformRestType
OfflineUserAppLaunched: PlatformRestType
OfflineUserSync: PlatformRestType
SyncAchievement: PlatformRestType
GetAchievements: PlatformRestType
UpdateOrg: PlatformRestType
MarkTeamAsFavorite: PlatformRestType
RemoveExternalMembersFromTeam: PlatformRestType
ListAllTeamsForUser: PlatformRestType
ListOrgTeamMembers: PlatformRestType
ListUserOrgTeamMemberships: PlatformRestType
CreateOrgTeam: PlatformRestType
DeleteOrgTeam: PlatformRestType
ListOrgTeams: PlatformRestType
GetOrgTeam: PlatformRestType
UpdateOrgTeam: PlatformRestType
CreateOrgTeamMember: PlatformRestType
DeleteOrgTeamMember: PlatformRestType
UpdateOrgTeamMember: PlatformRestType
GetTeam: PlatformRestType
GetAllOrgTeams: PlatformRestType
InviteMembers: PlatformRestType
EditMemberActiveStatus: PlatformRestType
SwitchUserOrg: PlatformRestType
EditMemberRole: PlatformRestType
GetOrgDownloadVersions: PlatformRestType
RequestUserInviteToOrgAdmin: PlatformRestType
UserInviteApproval: PlatformRestType
ListOrgJoinRequests: PlatformRestType
RequestRoomAccess: PlatformRestType
RemoveMemberFromOrg: PlatformRestType
GetUsersInOrg: PlatformRestType
ListOrgMembershipInvitations: PlatformRestType
DeleteOrgMembershipInvitation: PlatformRestType
CreateOrgAccountsByOrgAdmin: PlatformRestType
CreateConnectionInvitation: PlatformRestType
ListConnectionInvitations: PlatformRestType
UpdateConnectionInvitation: PlatformRestType
ListConnections: PlatformRestType
InitiateOidcAuthorisation: PlatformRestType
CompleteOidcAuthorisation: PlatformRestType
RevokeOidcAuthorisation: PlatformRestType
SearchPublicUser: PlatformRestType
CreateCommunityStudio: PlatformRestType
UpdateCommunityStudio: PlatformRestType
GetCommunityStudio: PlatformRestType
ListCommunityStudios: PlatformRestType
SendSupportEmail: PlatformRestType
RequestCertificate: PlatformRestType
UpdateSketchObjects: PlatformRestType
HandraiseToPaywall: PlatformRestType
ConsumeDownloadAllowance: PlatformRestType
CreateSubscription: PlatformRestType
GetSubscriptionPrice: PlatformRestType
GetStripeCustomerPortalLink: PlatformRestType
PostImageToDiscord: PlatformRestType
GetPublicUserProfile: PlatformRestType
MaintenanceCheck: PlatformRestType
ListPublicSpaceDocs: PlatformRestType
DownloadPublicSpaceDoc: PlatformRestType
DownloadOverrideConfig: PlatformRestType
Transcribe: PlatformRestType
AskShrek: PlatformRestType
GenerateImages: PlatformRestType
Generate3DModel: PlatformRestType
UnknownErrorType: PlatformRestError
Ok: PlatformRestError
ClientCancelled: PlatformRestError
BadClientRequest: PlatformRestError
DeadlineExceeded: PlatformRestError
PermissionDenied: PlatformRestError
Unauthenticated: PlatformRestError
NotFound: PlatformRestError
ServerAborted: PlatformRestError
ServerError: PlatformRestError
ServerUnavailable: PlatformRestError
ConnectionError: PlatformRestError
InValidClientVersion: PlatformRestError
ConnectionTimeout: PlatformRestError
OrgRequiredVersionViolation: PlatformRestError
InvalidLicense: PlatformRestError
NotAllowedRequest: PlatformRestError
ExceedLicenseCount: PlatformRestError
InvalidTicket: PlatformRestError
SourceAppTypeUnset: SourceAppType
SourceAppCommunity: SourceAppType
SourceAppEnterprise: SourceAppType
AnalyticsHintUnset: AnalyticsHint
AnalyticsHintPaywallTriggered: AnalyticsHint
ChangeUserPasswordResponseCode_Success: ChangeUserPasswordResponseCode
ChangeUserPasswordResponseCode_SameOldNewPassword: ChangeUserPasswordResponseCode
ChangeUserPasswordResponseCode_InvalidPassword: ChangeUserPasswordResponseCode
ChangeUserPasswordResponseCode_IncorrectPassword: ChangeUserPasswordResponseCode
AccountDeletionFeedbackType_Unset: AccountDeletionFeedbackType
AccountDeletionFeedbackType_Others: AccountDeletionFeedbackType
AccountDeletionFeedbackType_NeverStarted: AccountDeletionFeedbackType
AccountDeletionFeedbackType_StoppedUsing: AccountDeletionFeedbackType
AccountDeletionFeedbackType_DontUseLandingPad: AccountDeletionFeedbackType
AccountDeletionFeedbackType_HaveAnotherAccount: AccountDeletionFeedbackType
AccountDeletionFeedbackType_DataPrivacy: AccountDeletionFeedbackType
DeleteAccountResponseCode_Success: DeleteAccountResponseCode
DeleteAccountResponseCode_IncorrectPassword: DeleteAccountResponseCode
MagicLinkLoginSuccess: MagicLinkLoginResultCode
MagicLinkLoginSignupRequired: MagicLinkLoginResultCode
MagicLinkLoginWaitingForLinkConfirm: MagicLinkLoginResultCode
MagicLinkLoginFailed: MagicLinkLoginResultCode
MagicLinkLoginInvalidEmail: MagicLinkLoginResultCode
MagicLinkLoginInvalidLoginType: MagicLinkLoginResultCode
MagicLinkLoginLinkNotFoundOrExpired: MagicLinkLoginResultCode
MagicLinkLoginInvalidReCaptcha: MagicLinkLoginResultCode
MagicLinkLoginSSOSignUpRequired: MagicLinkLoginResultCode
MagicLinkLoginSSOLoginRequired: MagicLinkLoginResultCode
MagicLinkLoginType_LPAuthentication: MagicLinkLoginType
MagicLinkLoginType_EmailAuthentication: MagicLinkLoginType
InvalidDevice: OculusAppType
OculusRift: OculusAppType
OculusQuest: OculusAppType
SignUpResponseCodeSuccess: SignUpResponseCode
SignUpResponseCodeEmailAlreadyInUse: SignUpResponseCode
SignUpResponseCodePasswordTooSimple: SignUpResponseCode
EmailAccountLinkUnknown: EmailAccountLinkResult
EmailAccountLinkSuccess: EmailAccountLinkResult
EmailAccountLinkedToOtherDevice: EmailAccountLinkResult
AttachEmailSuccess: AttachEmailResult
AttachEmailEmailUsed: AttachEmailResult
AttachEmailInvalidEmail: AttachEmailResult
AttachEmailNetIssue: AttachEmailResult
LaunchRoomResponseCodeUnknown: LaunchRoomResponseCode
LaunchRoomResponseCodeSuccess: LaunchRoomResponseCode
LaunchRoomResponseCodeRoomNotFound: LaunchRoomResponseCode
LaunchRoomResponseCodeServerError: LaunchRoomResponseCode
LaunchRoomResponseCodeNoReadyInstance: LaunchRoomResponseCode
LaunchRoomResponseCodeMaxLaunchedRoomExceeded: LaunchRoomResponseCode
LaunchRoomResponseCodeInitLockExists: LaunchRoomResponseCode
LaunchRoomResponseCodeNoPermission: LaunchRoomResponseCode
LaunchRoomResponseCodeRoomShuttingDown: LaunchRoomResponseCode
EnterRoomUnknown: EnterRoomResult
EnterRoomSuccess: EnterRoomResult
EnterRoomOutOfDateClientVersion: EnterRoomResult
EnterRoomRoomNotFound: EnterRoomResult
EnterRoomServerFailure: EnterRoomResult
EnterRoomMaxUserCapExceeded: EnterRoomResult
EnterRoomRoomNotLaunchedOrReady: EnterRoomResult
EnterRoomNoPermission: EnterRoomResult
EnterRoomServerOutOfDate: EnterRoomResult
EnterRoomInitLockExists: EnterRoomResult
EnterRoomMaxLaunchedRoomExceeded: EnterRoomResult
EnterRoomResultScreenAppDisallowed: EnterRoomResult
EnterRoomResultWaitingForHostToLaunch: EnterRoomResult
EnterRoomResultWaitingForHostToGrantEntry: EnterRoomResult
EnterRoomResultPasswordFailed: EnterRoomResult
EnterRoomResultRoomOwnerIsNotPresent: EnterRoomResult
EnterRoomResultDeepLinkNotFound: EnterRoomResult
EnterRoomResultViaOneTimeAdminTokenNotInGSOrg: EnterRoomResult
ShutdownRoomUnknown: ShutdownRoomResult
ShutdownRoomSuccess: ShutdownRoomResult
ShutdownRoomHasConnectedUsers: ShutdownRoomResult
ShutdownRoomNotReadyStatus: ShutdownRoomResult
ShutdownRoomServerError: ShutdownRoomResult
InviteUsersToCollabResponseCodeSuccess: InviteUsersToCollabResponseCode
InviteUsersToCollabResponseCodeDocNotFound: InviteUsersToCollabResponseCode
InviteUsersToCollabResponseCodeInvalidDocType: InviteUsersToCollabResponseCode
InviteUsersToCollabResponseCodeInvalidInvitedRole: InviteUsersToCollabResponseCode
InviteUsersToCollabResponseCodeOculusIdsOnlyApplicableToFreeCollab: InviteUsersToCollabResponseCode
DeletePersistedRoomUnknown: DeletePersistedRoomResult
DeletePersistedRoomSuccess: DeletePersistedRoomResult
DeletePersistedRoomHasConnectedUsers: DeletePersistedRoomResult
DeletePersistedRoomServerError: DeletePersistedRoomResult
noEmail: BetaEmailType
subD: BetaEmailType
toolBelt: BetaEmailType
ResendStoreSignupType_Unknown: ResendStoreSignupType
ResendStoreSignupType_Steam: ResendStoreSignupType
ResendStoreSignupType_Oculus: ResendStoreSignupType
ResendStoreSignupType_GSStore: ResendStoreSignupType
ResendStoreSignupEmailResultUnknownError: ResendStoreSignupEmailResult
ResendStoreSignupEmailResultSuccess: ResendStoreSignupEmailResult
ResendStoreSignupEmailResultLinkMissing: ResendStoreSignupEmailResult
ReplayRecordingUnknown: ReplayRecordingResult
ReplayRecordingSuccess: ReplayRecordingResult
ReplayRecordingFinished: ReplayRecordingResult
ReplayRecordingNotFound: ReplayRecordingResult
ReplayRecordingOnGoing: ReplayRecordingResult
ReplayRecordingFailed: ReplayRecordingResult
ReplayRecordingNoPermission: ReplayRecordingResult
GetPublicUserProfileResult_Success: GetPublicUserProfileResult
GetPublicUserProfileResult_PrivateProfile: GetPublicUserProfileResult
GetOrgResponseCodeSuccess: GetOrgResponseCode
GetOrgResponseCodeOrgNotFound: GetOrgResponseCode
UndefinedPostToDiscordResponseCode: PostImageToDiscordResponseCode
PostImageToDiscordSuccess: PostImageToDiscordResponseCode
InvalidDiscordChannel: PostImageToDiscordResponseCode
InvalidOrMissingImageData: PostImageToDiscordResponseCode
DiscordServerSendError: PostImageToDiscordResponseCode
DiscordServerInitialiseError: PostImageToDiscordResponseCode
UnknownDiscordChannel: DiscordChannelType
GSDiscordServerInkGameAprilFools: DiscordChannelType
CreateVoiceToTextUrlUnknown: CreateVoiceToTextUrlResult
CreateVoiceToTextUrlSuccess: CreateVoiceToTextUrlResult
CreateVoiceToTextUrlNoPermission: CreateVoiceToTextUrlResult
UpdateCommunityStudioResponseCodeSuccess: UpdateCommunityStudioResponseCode
UpdateCommunityStudioResponseCodeStudioNotFound: UpdateCommunityStudioResponseCode
RequestCertificateResponseCodeUnknown: RequestCertificateResponseCode
RequestCertificateResponseCodeSuccess: RequestCertificateResponseCode
None: HandraiseToPaywallRequestType
ForBusiness: HandraiseToPaywallRequestType
ForIndividual: HandraiseToPaywallRequestType
ForTeamsPlan: HandraiseToPaywallRequestType
ForEnterprisePlan: HandraiseToPaywallRequestType
ConsumeDownloadAllowanceResponseCodeSuccess: ConsumeDownloadAllowanceResponseCode
ConsumeDownloadAllowanceResponseCodeInsufficientCredit: ConsumeDownloadAllowanceResponseCode
ConsumeDownloadAllowanceResponseCodeVersionOutOfDate: ConsumeDownloadAllowanceResponseCode

class PardotMetadata(_message.Message):
    __slots__ = ("visitorId",)
    VISITORID_FIELD_NUMBER: _ClassVar[int]
    visitorId: int
    def __init__(self, visitorId: _Optional[int] = ...) -> None: ...

class PlatformRestRequest(_message.Message):
    __slots__ = ("restType", "clientVersion", "ticket", "reqId", "cmsVersion", "lang", "unityUserId", "sessionId", "userBehaviourSync", "signUpRequest", "loginRequest", "logoutRequest", "loginByOneTimeAuthTokenRequest", "magicLinkLoginRequest", "steamLoginRequest", "oculusLoginRequest", "steamSignUpRequest", "oculusSignUpRequest", "steamEmailAccountLinkRequest", "oculusEmailAccountLinkRequest", "signUpByEmailPassRequest", "detachDeviceRequest", "appleLoginRequest", "appleSignUpRequest", "sendBetaSignupEmailRequest", "appleGrsAccountLinkRequest", "deleteAccountRequest", "earlyAdopterCheckRequest", "resendEmailVerificationRequest", "listSSOProvidersForEmailRequest", "initiateOidcSSOLoginRequest", "completeOidcSSOLoginRequest", "getSSOProviderForSignupRequest", "signUpWithSSORequest", "attachEmailRequest", "resendStoreSignupEmailRequest", "invalidateSignupLinkRequest", "initiateSignUpRequest", "enableMfaRequest", "sendUserFeedbackRequest", "enableTwoFactorAuthRequest", "completeSignUpByCodeRequest", "activateCodeRequest", "loginByEmailRequest", "getLoggedInUserRequest", "getLoggedInUserRequestV2", "updateUserInfoRequest", "sendPasswordResetEmailRequest", "resetPasswordRequest", "changePasswordRequest", "changeEmailRequest", "generateSecretKeyRequest", "getLoggedInUserOrgInfoRequest", "getSubscriptionPackRequest", "consumeNotificationRequest", "changeUserPasswordRequest", "getNotificationsForLoggedInUserRequest", "createUserSurveyRequest", "getOrgRequest", "listUserLoginAuditsRequest", "listOrgUserActionAuditsRequest", "createVoiceToTextUrlRequest", "convertDocRequest", "listDocsRequest", "listRecentDocsRequest", "deprecatedGetDocumentsRequest", "getUsedSpaceSizeRequest", "sendDocumentRequest", "createFolderRequest", "moveDocumentRequest", "initiateFileUploadRequest", "downloadDocRequest", "createDocRequest", "updateDocRequest", "trashDocRequest", "restoreDocRequest", "listDocsInBinRequest", "deleteDocsInBinRequest", "exportDocRequest", "listDocExportsRequest", "downloadDocExportRequest", "getDocExportRequest", "searchDocsRequest", "uploadDocExportRequest", "createDocAssetRequest", "downloadDocAssetsRequest", "createDocExportEntryRequest", "getSketchRoomUpdatesRequest", "uploadDocThumbnailRequest", "copyDocRequest", "searchPublicContentDocByPathRequest", "getDocumentByIdRequest", "getDocumentByPathRequest", "getDocumentSpaceNameRequest", "createDocCommentRequest", "listDocCommentsRequest", "updateDocCommentRequest", "listNewDocCommentsRequest", "generatePairDeviceCodeRequest", "pairDeviceRequest", "getPairedDeviceRequest", "revokeDevicePairingRequest", "getUserFromPairedDeviceIdRequest", "LaunchRoomRequest", "enterRoomRequest", "shutdownRoomRequest", "releaseRoomInitLockRequest", "inviteUsersToCollabRequest", "listInvitableUsersRequest", "enterRoomWithDeepLinkRequest", "changeUserCollaborationRoleRequest", "listSharedDocsRequest", "reportAbusiveBehaviourRequest", "listRoomRecordingsRequest", "replayRoomRecordingRequest", "getRoomRecordingRequest", "getRoomRecordingReplayDataRequest", "getRoomRecordingReplayAssetsRequest", "shareRoomWithUserRequest", "listRoomAccessesRequest", "removeAccessFromRoomRequest", "setCoSketchRoomPassRequest", "generateDeepAccessLinkRequest", "enterPublicRoomRequest", "bookmarkPublicDocRequest", "listPublicRoomRequest", "setPublicDocRequest", "stopRoomSharingRequest", "createEnterRoomNotificationRequest", "listRoomAccessRequestsRequest", "approveRoomAccessRequest", "listAllUsersWithAccessToDocRequest", "launchStreamingAgentForRoomRequest", "enterRoomViaAdminNotificationDeeplinkRequest", "checkForClientAppUpdateRequest", "getRoomIdByShortCodeRequest", "getShortCodeByRoomIdRequest", "offlineUserTrace", "syncAchievementRequest", "updateOrgRequest", "markTeamAsFavoriteRequest", "removeExternalMembersFromTeamRequest", "listAllTeamsForUserRequest", "listOrgTeamMembersRequest", "listUserOrgTeamMembershipsRequest", "createOrgTeamRequest", "deleteOrgTeamRequest", "listOrgTeamsRequest", "getOrgTeamRequest", "updateOrgTeamRequest", "createOrgTeamMemberRequest", "deleteOrgTeamMemberRequest", "updateOrgTeamMemberRequest", "getTeamRequest", "getAllOrgTeamsRequest", "inviteMembersRequest", "editMemberActiveStatusRequest", "switchUserOrgRequest", "editMemberRoleRequest", "getOrgDownloadVersionsRequest", "requestUserInviteToOrgAdminRequest", "userInviteApprovalRequest", "listOrgJoinRequestsRequest", "requestRoomAccessRequest", "removeMemberFromOrgRequest", "getUsersInOrgRequest", "listOrgMembershipInvitationsRequest", "deleteOrgMembershipInvitationRequest", "createOrgAccountsByOrgAdminRequest", "createConnectionInvitationRequest", "listConnectionInvitationRequest", "updateConnectionInvitationRequest", "listConnectionsRequest", "initiateOidcAuthorisationRequest", "completeOidcAuthorisationRequest", "revokeOidcAuthorisationRequest", "searchPublicUserRequest", "createCommunityStudioRequest", "updateCommunityStudioRequest", "getCommunityStudioRequest", "listCommunityStudiosRequest", "sendSupportEmailRequest", "requestCertificateRequest", "updateSketchObjectsRequest", "handraiseToPaywallRequest", "consumeDownloadAllowanceRequest", "createSubscriptionRequest", "getSubscriptionPriceRequest", "getStripeCustomerPortalLinkRequest", "deviceInfo", "source", "appType", "analyticsHints", "pardotMetadata", "postImageToDiscordRequest", "getPublicUserProfileRequest", "maintenanceCheckRequest", "listPublicSpaceDocsRequest", "downloadPublicSpaceDocRequest", "transcribeRequest", "askShrekRequest", "generateImagesRequest", "generate3DModelRequest", "lastNotificationQueryTime")
    RESTTYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    REQID_FIELD_NUMBER: _ClassVar[int]
    CMSVERSION_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    UNITYUSERID_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    USERBEHAVIOURSYNC_FIELD_NUMBER: _ClassVar[int]
    SIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    LOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    LOGOUTREQUEST_FIELD_NUMBER: _ClassVar[int]
    LOGINBYONETIMEAUTHTOKENREQUEST_FIELD_NUMBER: _ClassVar[int]
    MAGICLINKLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    STEAMLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    OCULUSLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    STEAMSIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    OCULUSSIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    STEAMEMAILACCOUNTLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    OCULUSEMAILACCOUNTLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGNUPBYEMAILPASSREQUEST_FIELD_NUMBER: _ClassVar[int]
    DETACHDEVICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    APPLELOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    APPLESIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    SENDBETASIGNUPEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    APPLEGRSACCOUNTLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEACCOUNTREQUEST_FIELD_NUMBER: _ClassVar[int]
    EARLYADOPTERCHECKREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESENDEMAILVERIFICATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTSSOPROVIDERSFOREMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    INITIATEOIDCSSOLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    COMPLETEOIDCSSOLOGINREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSSOPROVIDERFORSIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGNUPWITHSSOREQUEST_FIELD_NUMBER: _ClassVar[int]
    ATTACHEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESENDSTORESIGNUPEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    INVALIDATESIGNUPLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    INITIATESIGNUPREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENABLEMFAREQUEST_FIELD_NUMBER: _ClassVar[int]
    SENDUSERFEEDBACKREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENABLETWOFACTORAUTHREQUEST_FIELD_NUMBER: _ClassVar[int]
    COMPLETESIGNUPBYCODEREQUEST_FIELD_NUMBER: _ClassVar[int]
    ACTIVATECODEREQUEST_FIELD_NUMBER: _ClassVar[int]
    LOGINBYEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERREQUESTV2_FIELD_NUMBER: _ClassVar[int]
    UPDATEUSERINFOREQUEST_FIELD_NUMBER: _ClassVar[int]
    SENDPASSWORDRESETEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESETPASSWORDREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGEPASSWORDREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGEEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    GENERATESECRETKEYREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERORGINFOREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSUBSCRIPTIONPACKREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONSUMENOTIFICATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERPASSWORDREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETNOTIFICATIONSFORLOGGEDINUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEUSERSURVEYREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETORGREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTUSERLOGINAUDITSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTORGUSERACTIONAUDITSREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEVOICETOTEXTURLREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONVERTDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTDOCSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTRECENTDOCSREQUEST_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDGETDOCUMENTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETUSEDSPACESIZEREQUEST_FIELD_NUMBER: _ClassVar[int]
    SENDDOCUMENTREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEFOLDERREQUEST_FIELD_NUMBER: _ClassVar[int]
    MOVEDOCUMENTREQUEST_FIELD_NUMBER: _ClassVar[int]
    INITIATEFILEUPLOADREQUEST_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    TRASHDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESTOREDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTDOCSINBINREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEDOCSINBINREQUEST_FIELD_NUMBER: _ClassVar[int]
    EXPORTDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTDOCEXPORTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCEXPORTREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETDOCEXPORTREQUEST_FIELD_NUMBER: _ClassVar[int]
    SEARCHDOCSREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPLOADDOCEXPORTREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCASSETREQUEST_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCASSETSREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCEXPORTENTRYREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSKETCHROOMUPDATESREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPLOADDOCTHUMBNAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    COPYDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    SEARCHPUBLICCONTENTDOCBYPATHREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTBYIDREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTBYPATHREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTSPACENAMEREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCCOMMENTREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTDOCCOMMENTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEDOCCOMMENTREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTNEWDOCCOMMENTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GENERATEPAIRDEVICECODEREQUEST_FIELD_NUMBER: _ClassVar[int]
    PAIRDEVICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETPAIREDDEVICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    REVOKEDEVICEPAIRINGREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETUSERFROMPAIREDDEVICEIDREQUEST_FIELD_NUMBER: _ClassVar[int]
    LAUNCHROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENTERROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWNROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    RELEASEROOMINITLOCKREQUEST_FIELD_NUMBER: _ClassVar[int]
    INVITEUSERSTOCOLLABREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTINVITABLEUSERSREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENTERROOMWITHDEEPLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERCOLLABORATIONROLEREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTSHAREDDOCSREQUEST_FIELD_NUMBER: _ClassVar[int]
    REPORTABUSIVEBEHAVIOURREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTROOMRECORDINGSREQUEST_FIELD_NUMBER: _ClassVar[int]
    REPLAYROOMRECORDINGREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGREPLAYDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGREPLAYASSETSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SHAREROOMWITHUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTROOMACCESSESREQUEST_FIELD_NUMBER: _ClassVar[int]
    REMOVEACCESSFROMROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETCOSKETCHROOMPASSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GENERATEDEEPACCESSLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENTERPUBLICROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    BOOKMARKPUBLICDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTPUBLICROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETPUBLICDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    STOPROOMSHARINGREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEENTERROOMNOTIFICATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTROOMACCESSREQUESTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    APPROVEROOMACCESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTALLUSERSWITHACCESSTODOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    LAUNCHSTREAMINGAGENTFORROOMREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENTERROOMVIAADMINNOTIFICATIONDEEPLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    CHECKFORCLIENTAPPUPDATEREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETROOMIDBYSHORTCODEREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSHORTCODEBYROOMIDREQUEST_FIELD_NUMBER: _ClassVar[int]
    OFFLINEUSERTRACE_FIELD_NUMBER: _ClassVar[int]
    SYNCACHIEVEMENTREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGREQUEST_FIELD_NUMBER: _ClassVar[int]
    MARKTEAMASFAVORITEREQUEST_FIELD_NUMBER: _ClassVar[int]
    REMOVEEXTERNALMEMBERSFROMTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTALLTEAMSFORUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTORGTEAMMEMBERSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTUSERORGTEAMMEMBERSHIPSREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEORGTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEORGTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTORGTEAMSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETORGTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEORGTEAMMEMBERREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEORGTEAMMEMBERREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGTEAMMEMBERREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETTEAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETALLORGTEAMSREQUEST_FIELD_NUMBER: _ClassVar[int]
    INVITEMEMBERSREQUEST_FIELD_NUMBER: _ClassVar[int]
    EDITMEMBERACTIVESTATUSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SWITCHUSERORGREQUEST_FIELD_NUMBER: _ClassVar[int]
    EDITMEMBERROLEREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETORGDOWNLOADVERSIONSREQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUESTUSERINVITETOORGADMINREQUEST_FIELD_NUMBER: _ClassVar[int]
    USERINVITEAPPROVALREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTORGJOINREQUESTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUESTROOMACCESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    REMOVEMEMBERFROMORGREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETUSERSINORGREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTORGMEMBERSHIPINVITATIONSREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEORGMEMBERSHIPINVITATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEORGACCOUNTSBYORGADMINREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATECONNECTIONINVITATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTCONNECTIONINVITATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATECONNECTIONINVITATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTCONNECTIONSREQUEST_FIELD_NUMBER: _ClassVar[int]
    INITIATEOIDCAUTHORISATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    COMPLETEOIDCAUTHORISATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    REVOKEOIDCAUTHORISATIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    SEARCHPUBLICUSERREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATECOMMUNITYSTUDIOREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATECOMMUNITYSTUDIOREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETCOMMUNITYSTUDIOREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTCOMMUNITYSTUDIOSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SENDSUPPORTEMAILREQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUESTCERTIFICATEREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATESKETCHOBJECTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    HANDRAISETOPAYWALLREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONSUMEDOWNLOADALLOWANCEREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATESUBSCRIPTIONREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSUBSCRIPTIONPRICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSTRIPECUSTOMERPORTALLINKREQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    APPTYPE_FIELD_NUMBER: _ClassVar[int]
    ANALYTICSHINTS_FIELD_NUMBER: _ClassVar[int]
    PARDOTMETADATA_FIELD_NUMBER: _ClassVar[int]
    POSTIMAGETODISCORDREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETPUBLICUSERPROFILEREQUEST_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCECHECKREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTPUBLICSPACEDOCSREQUEST_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADPUBLICSPACEDOCREQUEST_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIBEREQUEST_FIELD_NUMBER: _ClassVar[int]
    ASKSHREKREQUEST_FIELD_NUMBER: _ClassVar[int]
    GENERATEIMAGESREQUEST_FIELD_NUMBER: _ClassVar[int]
    GENERATE3DMODELREQUEST_FIELD_NUMBER: _ClassVar[int]
    LASTNOTIFICATIONQUERYTIME_FIELD_NUMBER: _ClassVar[int]
    restType: PlatformRestType
    clientVersion: str
    ticket: _gravi_model_pb2.IDTicket
    reqId: str
    cmsVersion: str
    lang: _localization_pb2.LocalLang
    unityUserId: str
    sessionId: int
    userBehaviourSync: _gravi_model_pb2.UserBehaviourSync
    signUpRequest: SignUpRequest
    loginRequest: _login_pb2.LoginRequest
    logoutRequest: LogoutRequest
    loginByOneTimeAuthTokenRequest: LoginByOneTimeAuthTokenRequest
    magicLinkLoginRequest: MagicLinkLoginRequest
    steamLoginRequest: SteamLoginRequest
    oculusLoginRequest: OculusLoginRequest
    steamSignUpRequest: SteamSignUpRequest
    oculusSignUpRequest: OculusSignUpRequest
    steamEmailAccountLinkRequest: SteamEmailAccountLinkRequest
    oculusEmailAccountLinkRequest: OculusEmailAccountLinkRequest
    signUpByEmailPassRequest: _signup_pb2.SignUpByEmailPassRequest
    detachDeviceRequest: DetachDeviceRequest
    appleLoginRequest: AppleLoginRequest
    appleSignUpRequest: AppleSignUpRequest
    sendBetaSignupEmailRequest: SendBetaSignupEmailRequest
    appleGrsAccountLinkRequest: AppleGrsAccountLinkRequest
    deleteAccountRequest: DeleteAccountRequest
    earlyAdopterCheckRequest: EarlyAdopterCheckRequest
    resendEmailVerificationRequest: _signup_pb2.ResendEmailVerificationRequest
    listSSOProvidersForEmailRequest: _auth_pb2.ListSSOProvidersForEmailRequest
    initiateOidcSSOLoginRequest: _auth_pb2.InitiateOidcSSOLoginRequest
    completeOidcSSOLoginRequest: _auth_pb2.CompleteOidcSSOLoginRequest
    getSSOProviderForSignupRequest: _auth_pb2.GetSSOProviderForSignupRequest
    signUpWithSSORequest: _auth_pb2.SignUpWithSSORequest
    attachEmailRequest: AttachEmailRequest
    resendStoreSignupEmailRequest: ResendStoreSignupEmailRequest
    invalidateSignupLinkRequest: InvalidateSignupLinkRequest
    initiateSignUpRequest: _signup_pb2.InitiateSignUpRequest
    enableMfaRequest: _auth_pb2.EnableMfaRequest
    sendUserFeedbackRequest: _signup_pb2.SendUserFeedbackRequest
    enableTwoFactorAuthRequest: _auth_pb2.EnableTwoFactorAuthRequest
    completeSignUpByCodeRequest: _auth_pb2.CompleteSignUpByCodeRequest
    activateCodeRequest: _activate_code_pb2.ActivateCodeRequest
    loginByEmailRequest: _auth_pb2.LoginByEmailRequest
    getLoggedInUserRequest: GetLoggedInUserRequest
    getLoggedInUserRequestV2: _account_pb2.GetLoggedInUserRequestV2
    updateUserInfoRequest: _profile_pb2.UpdateUserInfoRequest
    sendPasswordResetEmailRequest: _auth_pb2.SendPasswordResetEmailRequest
    resetPasswordRequest: _auth_pb2.ResetPasswordRequest
    changePasswordRequest: _auth_pb2.ChangePasswordRequest
    changeEmailRequest: _auth_pb2.ChangeEmailRequest
    generateSecretKeyRequest: _auth_pb2.GenerateSecretKeyRequest
    getLoggedInUserOrgInfoRequest: GetLoggedInUserOrgInfoRequest
    getSubscriptionPackRequest: GetSubscriptionPackRequest
    consumeNotificationRequest: ConsumeNotificationRequest
    changeUserPasswordRequest: ChangeUserPasswordRequest
    getNotificationsForLoggedInUserRequest: GetNotificationsForLoggedInUserRequest
    createUserSurveyRequest: _profile_pb2.CreateUserSurveyRequest
    getOrgRequest: GetOrgRequest
    listUserLoginAuditsRequest: _auth_pb2.ListUserLoginAuditsRequest
    listOrgUserActionAuditsRequest: _organisation_pb2.ListOrgUserActionAuditsRequest
    createVoiceToTextUrlRequest: CreateVoiceToTextUrlRequest
    convertDocRequest: _doc_rest_pb2.ConvertDocRequest
    listDocsRequest: _doc_rest_pb2.ListDocsRequest
    listRecentDocsRequest: _doc_rest_pb2.ListRecentDocsRequest
    deprecatedGetDocumentsRequest: _doc_rest_pb2.DeprecatedGetDocumentsRequest
    getUsedSpaceSizeRequest: _doc_rest_pb2.GetUsedSpaceSizeRequest
    sendDocumentRequest: _doc_rest_pb2.SendDocumentRequest
    createFolderRequest: _doc_rest_pb2.CreateFolderRequest
    moveDocumentRequest: _doc_rest_pb2.MoveDocumentRequest
    initiateFileUploadRequest: _doc_rest_pb2.InitiateFileUploadRequest
    downloadDocRequest: _doc_rest_pb2.DownloadDocRequest
    createDocRequest: _doc_rest_pb2.CreateDocRequest
    updateDocRequest: _doc_rest_pb2.UpdateDocRequest
    trashDocRequest: _doc_rest_pb2.TrashDocRequest
    restoreDocRequest: _doc_rest_pb2.RestoreDocRequest
    listDocsInBinRequest: _doc_rest_pb2.ListDocsInBinRequest
    deleteDocsInBinRequest: _doc_rest_pb2.DeleteDocsInBinRequest
    exportDocRequest: _export_pb2.ExportDocRequest
    listDocExportsRequest: _export_pb2.ListDocExportsRequest
    downloadDocExportRequest: _export_pb2.DownloadDocExportRequest
    getDocExportRequest: _export_pb2.GetDocExportRequest
    searchDocsRequest: _doc_rest_pb2.SearchDocsRequest
    uploadDocExportRequest: _export_pb2.UploadDocExportRequest
    createDocAssetRequest: _doc_rest_pb2.CreateDocAssetRequest
    downloadDocAssetsRequest: _doc_rest_pb2.DownloadDocAssetsRequest
    createDocExportEntryRequest: _export_pb2.CreateDocExportEntryRequest
    getSketchRoomUpdatesRequest: _room_pb2.GetSketchRoomUpdatesRequest
    uploadDocThumbnailRequest: _doc_rest_pb2.UploadDocThumbnailRequest
    copyDocRequest: _doc_rest_pb2.CopyDocRequest
    searchPublicContentDocByPathRequest: _doc_rest_pb2.SearchPublicContentDocByPathRequest
    getDocumentByIdRequest: _doc_rest_pb2.GetDocumentByIdRequest
    getDocumentByPathRequest: _doc_rest_pb2.GetDocumentByPathRequest
    getDocumentSpaceNameRequest: _doc_rest_pb2.GetDocumentSpaceNameRequest
    createDocCommentRequest: _comment_pb2.CreateDocCommentRequest
    listDocCommentsRequest: _comment_pb2.ListDocCommentsRequest
    updateDocCommentRequest: _comment_pb2.UpdateDocCommentRequest
    listNewDocCommentsRequest: _comment_pb2.ListNewDocCommentsRequest
    generatePairDeviceCodeRequest: _pair_device_pb2.GeneratePairDeviceCodeRequest
    pairDeviceRequest: _pair_device_pb2.PairDeviceRequest
    getPairedDeviceRequest: _pair_device_pb2.GetPairedDeviceRequest
    revokeDevicePairingRequest: _pair_device_pb2.RevokeDevicePairingRequest
    getUserFromPairedDeviceIdRequest: _pair_device_pb2.GetUserFromPairedDeviceIdRequest
    LaunchRoomRequest: LaunchRoomRequest
    enterRoomRequest: EnterRoomRequest
    shutdownRoomRequest: ShutdownRoomRequest
    releaseRoomInitLockRequest: ReleaseRoomInitLockRequest
    inviteUsersToCollabRequest: InviteUsersToCollabRequest
    listInvitableUsersRequest: ListInvitableUsersRequest
    enterRoomWithDeepLinkRequest: EnterRoomWithDeepLinkRequest
    changeUserCollaborationRoleRequest: _collab_pb2.ChangeUserCollaborationRoleRequest
    listSharedDocsRequest: _doc_rest_pb2.ListSharedDocsRequest
    reportAbusiveBehaviourRequest: _collab_pb2.ReportAbusiveBehaviourRequest
    listRoomRecordingsRequest: ListRoomRecordingsRequest
    replayRoomRecordingRequest: ReplayRoomRecordingRequest
    getRoomRecordingRequest: GetRoomRecordingRequest
    getRoomRecordingReplayDataRequest: GetRoomRecordingReplayDataRequest
    getRoomRecordingReplayAssetsRequest: GetRoomRecordingReplayAssetsRequest
    shareRoomWithUserRequest: _room_pb2.ShareRoomWithUserRequest
    listRoomAccessesRequest: _room_pb2.ListRoomAccessesRequest
    removeAccessFromRoomRequest: _room_pb2.RemoveAccessFromRoomRequest
    setCoSketchRoomPassRequest: _room_pb2.SetCoSketchRoomPassRequest
    generateDeepAccessLinkRequest: _room_pb2.GenerateDeepAccessLinkRequest
    enterPublicRoomRequest: EnterRoomRequest
    bookmarkPublicDocRequest: _room_pb2.BookmarkPublicDocRequest
    listPublicRoomRequest: _room_pb2.ListPublicRoomRequest
    setPublicDocRequest: _room_pb2.SetPublicDocRequest
    stopRoomSharingRequest: _room_pb2.StopRoomSharingRequest
    createEnterRoomNotificationRequest: _doc_rest_pb2.CreateEnterRoomNotificationRequest
    listRoomAccessRequestsRequest: _room_pb2.ListRoomAccessRequestsRequest
    approveRoomAccessRequest: _room_pb2.ApproveRoomAccessRequest
    listAllUsersWithAccessToDocRequest: _doc_rest_pb2.ListAllUsersWithAccessToDocRequest
    launchStreamingAgentForRoomRequest: _room_pb2.LaunchStreamingAgentForRoomRequest
    enterRoomViaAdminNotificationDeeplinkRequest: _room_pb2.EnterRoomViaAdminNotificationDeeplinkRequest
    checkForClientAppUpdateRequest: _update_check_pb2.CheckForClientAppUpdateRequest
    getRoomIdByShortCodeRequest: _room_pb2.GetRoomIdByShortCodeRequest
    getShortCodeByRoomIdRequest: _room_pb2.GetShortCodeByRoomIdRequest
    offlineUserTrace: OfflineUserTrace
    syncAchievementRequest: SyncAchievementRequest
    updateOrgRequest: _management_pb2.UpdateOrgRequest
    markTeamAsFavoriteRequest: _team_pb2.MarkTeamAsFavoriteRequest
    removeExternalMembersFromTeamRequest: _team_pb2.RemoveExternalMembersFromTeamRequest
    listAllTeamsForUserRequest: _team_pb2.ListAllTeamsForUserRequest
    listOrgTeamMembersRequest: _team_member_pb2.ListOrgTeamMembersRequest
    listUserOrgTeamMembershipsRequest: _team_pb2.ListUserOrgTeamMembershipsRequest
    createOrgTeamRequest: _team_pb2.CreateOrgTeamRequest
    deleteOrgTeamRequest: _team_pb2.DeleteOrgTeamRequest
    listOrgTeamsRequest: _team_pb2.ListOrgTeamsRequest
    getOrgTeamRequest: _team_pb2.GetOrgTeamRequest
    updateOrgTeamRequest: _team_pb2.UpdateOrgTeamRequest
    createOrgTeamMemberRequest: _team_member_pb2.CreateOrgTeamMemberRequest
    deleteOrgTeamMemberRequest: _team_member_pb2.DeleteOrgTeamMemberRequest
    updateOrgTeamMemberRequest: _team_member_pb2.UpdateOrgTeamMemberRequest
    getTeamRequest: _team_pb2.GetTeamRequest
    getAllOrgTeamsRequest: _team_pb2.GetAllOrgTeamsRequest
    inviteMembersRequest: _team_pb2.InviteMembersRequest
    editMemberActiveStatusRequest: _team_pb2.EditMemberActiveStatusRequest
    switchUserOrgRequest: _team_pb2.SwitchUserOrgRequest
    editMemberRoleRequest: _team_pb2.EditMemberRoleRequest
    getOrgDownloadVersionsRequest: _management_pb2.GetOrgDownloadVersionsRequest
    requestUserInviteToOrgAdminRequest: _team_pb2.RequestUserInviteToOrgAdminRequest
    userInviteApprovalRequest: _team_pb2.UserInviteApprovalRequest
    listOrgJoinRequestsRequest: _team_pb2.ListOrgJoinRequestsRequest
    requestRoomAccessRequest: _room_pb2.RequestRoomAccessRequest
    removeMemberFromOrgRequest: _team_pb2.RemoveMemberFromOrgRequest
    getUsersInOrgRequest: _team_pb2.GetUsersInOrgRequest
    listOrgMembershipInvitationsRequest: _invitation_pb2.ListOrgMembershipInvitationsRequest
    deleteOrgMembershipInvitationRequest: _invitation_pb2.DeleteOrgMembershipInvitationRequest
    createOrgAccountsByOrgAdminRequest: _invitation_pb2.CreateOrgAccountsByOrgAdminRequest
    createConnectionInvitationRequest: _connections_pb2.CreateConnectionInvitationRequest
    listConnectionInvitationRequest: _connections_pb2.ListConnectionInvitationsRequest
    updateConnectionInvitationRequest: _connections_pb2.UpdateConnectionInvitationRequest
    listConnectionsRequest: _connections_pb2.ListConnectionsRequest
    initiateOidcAuthorisationRequest: _connections_pb2.InitiateOidcAuthorisationRequest
    completeOidcAuthorisationRequest: _connections_pb2.CompleteOidcAuthorisationRequest
    revokeOidcAuthorisationRequest: _connections_pb2.RevokeOidcAuthorisationRequest
    searchPublicUserRequest: _connections_pb2.SearchPublicUserRequest
    createCommunityStudioRequest: CreateCommunityStudioRequest
    updateCommunityStudioRequest: UpdateCommunityStudioRequest
    getCommunityStudioRequest: GetCommunityStudioRequest
    listCommunityStudiosRequest: ListCommunityStudiosRequest
    sendSupportEmailRequest: SendSupportEmailRequest
    requestCertificateRequest: RequestCertificateRequest
    updateSketchObjectsRequest: _online_sketch_pb2.UpdateSketchObjectsRequest
    handraiseToPaywallRequest: HandraiseToPaywallRequest
    consumeDownloadAllowanceRequest: ConsumeDownloadAllowanceRequest
    createSubscriptionRequest: _profile_pb2.CreateSubscriptionRequest
    getSubscriptionPriceRequest: _profile_pb2.GetSubscriptionPriceRequest
    getStripeCustomerPortalLinkRequest: _profile_pb2.GetStripeCustomerPortalLinkRequest
    deviceInfo: _gravi_model_pb2.DeviceInfo
    source: _gravi_model_pb2.SourceApp
    appType: SourceAppType
    analyticsHints: _containers.RepeatedScalarFieldContainer[AnalyticsHint]
    pardotMetadata: PardotMetadata
    postImageToDiscordRequest: PostImageToDiscordRequest
    getPublicUserProfileRequest: GetPublicUserProfileRequest
    maintenanceCheckRequest: MaintenanceCheckRequest
    listPublicSpaceDocsRequest: _doc_rest_pb2.ListPublicSpaceDocsRequest
    downloadPublicSpaceDocRequest: _doc_rest_pb2.DownloadPublicSpaceDocRequest
    transcribeRequest: _transcribe_pb2.TranscribeRequest
    askShrekRequest: _ask_pb2.AskShrekRequest
    generateImagesRequest: _image_pb2.GenerateImagesRequest
    generate3DModelRequest: _image_pb2.Generate3DModelRequest
    lastNotificationQueryTime: int
    def __init__(self, restType: _Optional[_Union[PlatformRestType, str]] = ..., clientVersion: _Optional[str] = ..., ticket: _Optional[_Union[_gravi_model_pb2.IDTicket, _Mapping]] = ..., reqId: _Optional[str] = ..., cmsVersion: _Optional[str] = ..., lang: _Optional[_Union[_localization_pb2.LocalLang, str]] = ..., unityUserId: _Optional[str] = ..., sessionId: _Optional[int] = ..., userBehaviourSync: _Optional[_Union[_gravi_model_pb2.UserBehaviourSync, _Mapping]] = ..., signUpRequest: _Optional[_Union[SignUpRequest, _Mapping]] = ..., loginRequest: _Optional[_Union[_login_pb2.LoginRequest, _Mapping]] = ..., logoutRequest: _Optional[_Union[LogoutRequest, _Mapping]] = ..., loginByOneTimeAuthTokenRequest: _Optional[_Union[LoginByOneTimeAuthTokenRequest, _Mapping]] = ..., magicLinkLoginRequest: _Optional[_Union[MagicLinkLoginRequest, _Mapping]] = ..., steamLoginRequest: _Optional[_Union[SteamLoginRequest, _Mapping]] = ..., oculusLoginRequest: _Optional[_Union[OculusLoginRequest, _Mapping]] = ..., steamSignUpRequest: _Optional[_Union[SteamSignUpRequest, _Mapping]] = ..., oculusSignUpRequest: _Optional[_Union[OculusSignUpRequest, _Mapping]] = ..., steamEmailAccountLinkRequest: _Optional[_Union[SteamEmailAccountLinkRequest, _Mapping]] = ..., oculusEmailAccountLinkRequest: _Optional[_Union[OculusEmailAccountLinkRequest, _Mapping]] = ..., signUpByEmailPassRequest: _Optional[_Union[_signup_pb2.SignUpByEmailPassRequest, _Mapping]] = ..., detachDeviceRequest: _Optional[_Union[DetachDeviceRequest, _Mapping]] = ..., appleLoginRequest: _Optional[_Union[AppleLoginRequest, _Mapping]] = ..., appleSignUpRequest: _Optional[_Union[AppleSignUpRequest, _Mapping]] = ..., sendBetaSignupEmailRequest: _Optional[_Union[SendBetaSignupEmailRequest, _Mapping]] = ..., appleGrsAccountLinkRequest: _Optional[_Union[AppleGrsAccountLinkRequest, _Mapping]] = ..., deleteAccountRequest: _Optional[_Union[DeleteAccountRequest, _Mapping]] = ..., earlyAdopterCheckRequest: _Optional[_Union[EarlyAdopterCheckRequest, _Mapping]] = ..., resendEmailVerificationRequest: _Optional[_Union[_signup_pb2.ResendEmailVerificationRequest, _Mapping]] = ..., listSSOProvidersForEmailRequest: _Optional[_Union[_auth_pb2.ListSSOProvidersForEmailRequest, _Mapping]] = ..., initiateOidcSSOLoginRequest: _Optional[_Union[_auth_pb2.InitiateOidcSSOLoginRequest, _Mapping]] = ..., completeOidcSSOLoginRequest: _Optional[_Union[_auth_pb2.CompleteOidcSSOLoginRequest, _Mapping]] = ..., getSSOProviderForSignupRequest: _Optional[_Union[_auth_pb2.GetSSOProviderForSignupRequest, _Mapping]] = ..., signUpWithSSORequest: _Optional[_Union[_auth_pb2.SignUpWithSSORequest, _Mapping]] = ..., attachEmailRequest: _Optional[_Union[AttachEmailRequest, _Mapping]] = ..., resendStoreSignupEmailRequest: _Optional[_Union[ResendStoreSignupEmailRequest, _Mapping]] = ..., invalidateSignupLinkRequest: _Optional[_Union[InvalidateSignupLinkRequest, _Mapping]] = ..., initiateSignUpRequest: _Optional[_Union[_signup_pb2.InitiateSignUpRequest, _Mapping]] = ..., enableMfaRequest: _Optional[_Union[_auth_pb2.EnableMfaRequest, _Mapping]] = ..., sendUserFeedbackRequest: _Optional[_Union[_signup_pb2.SendUserFeedbackRequest, _Mapping]] = ..., enableTwoFactorAuthRequest: _Optional[_Union[_auth_pb2.EnableTwoFactorAuthRequest, _Mapping]] = ..., completeSignUpByCodeRequest: _Optional[_Union[_auth_pb2.CompleteSignUpByCodeRequest, _Mapping]] = ..., activateCodeRequest: _Optional[_Union[_activate_code_pb2.ActivateCodeRequest, _Mapping]] = ..., loginByEmailRequest: _Optional[_Union[_auth_pb2.LoginByEmailRequest, _Mapping]] = ..., getLoggedInUserRequest: _Optional[_Union[GetLoggedInUserRequest, _Mapping]] = ..., getLoggedInUserRequestV2: _Optional[_Union[_account_pb2.GetLoggedInUserRequestV2, _Mapping]] = ..., updateUserInfoRequest: _Optional[_Union[_profile_pb2.UpdateUserInfoRequest, _Mapping]] = ..., sendPasswordResetEmailRequest: _Optional[_Union[_auth_pb2.SendPasswordResetEmailRequest, _Mapping]] = ..., resetPasswordRequest: _Optional[_Union[_auth_pb2.ResetPasswordRequest, _Mapping]] = ..., changePasswordRequest: _Optional[_Union[_auth_pb2.ChangePasswordRequest, _Mapping]] = ..., changeEmailRequest: _Optional[_Union[_auth_pb2.ChangeEmailRequest, _Mapping]] = ..., generateSecretKeyRequest: _Optional[_Union[_auth_pb2.GenerateSecretKeyRequest, _Mapping]] = ..., getLoggedInUserOrgInfoRequest: _Optional[_Union[GetLoggedInUserOrgInfoRequest, _Mapping]] = ..., getSubscriptionPackRequest: _Optional[_Union[GetSubscriptionPackRequest, _Mapping]] = ..., consumeNotificationRequest: _Optional[_Union[ConsumeNotificationRequest, _Mapping]] = ..., changeUserPasswordRequest: _Optional[_Union[ChangeUserPasswordRequest, _Mapping]] = ..., getNotificationsForLoggedInUserRequest: _Optional[_Union[GetNotificationsForLoggedInUserRequest, _Mapping]] = ..., createUserSurveyRequest: _Optional[_Union[_profile_pb2.CreateUserSurveyRequest, _Mapping]] = ..., getOrgRequest: _Optional[_Union[GetOrgRequest, _Mapping]] = ..., listUserLoginAuditsRequest: _Optional[_Union[_auth_pb2.ListUserLoginAuditsRequest, _Mapping]] = ..., listOrgUserActionAuditsRequest: _Optional[_Union[_organisation_pb2.ListOrgUserActionAuditsRequest, _Mapping]] = ..., createVoiceToTextUrlRequest: _Optional[_Union[CreateVoiceToTextUrlRequest, _Mapping]] = ..., convertDocRequest: _Optional[_Union[_doc_rest_pb2.ConvertDocRequest, _Mapping]] = ..., listDocsRequest: _Optional[_Union[_doc_rest_pb2.ListDocsRequest, _Mapping]] = ..., listRecentDocsRequest: _Optional[_Union[_doc_rest_pb2.ListRecentDocsRequest, _Mapping]] = ..., deprecatedGetDocumentsRequest: _Optional[_Union[_doc_rest_pb2.DeprecatedGetDocumentsRequest, _Mapping]] = ..., getUsedSpaceSizeRequest: _Optional[_Union[_doc_rest_pb2.GetUsedSpaceSizeRequest, _Mapping]] = ..., sendDocumentRequest: _Optional[_Union[_doc_rest_pb2.SendDocumentRequest, _Mapping]] = ..., createFolderRequest: _Optional[_Union[_doc_rest_pb2.CreateFolderRequest, _Mapping]] = ..., moveDocumentRequest: _Optional[_Union[_doc_rest_pb2.MoveDocumentRequest, _Mapping]] = ..., initiateFileUploadRequest: _Optional[_Union[_doc_rest_pb2.InitiateFileUploadRequest, _Mapping]] = ..., downloadDocRequest: _Optional[_Union[_doc_rest_pb2.DownloadDocRequest, _Mapping]] = ..., createDocRequest: _Optional[_Union[_doc_rest_pb2.CreateDocRequest, _Mapping]] = ..., updateDocRequest: _Optional[_Union[_doc_rest_pb2.UpdateDocRequest, _Mapping]] = ..., trashDocRequest: _Optional[_Union[_doc_rest_pb2.TrashDocRequest, _Mapping]] = ..., restoreDocRequest: _Optional[_Union[_doc_rest_pb2.RestoreDocRequest, _Mapping]] = ..., listDocsInBinRequest: _Optional[_Union[_doc_rest_pb2.ListDocsInBinRequest, _Mapping]] = ..., deleteDocsInBinRequest: _Optional[_Union[_doc_rest_pb2.DeleteDocsInBinRequest, _Mapping]] = ..., exportDocRequest: _Optional[_Union[_export_pb2.ExportDocRequest, _Mapping]] = ..., listDocExportsRequest: _Optional[_Union[_export_pb2.ListDocExportsRequest, _Mapping]] = ..., downloadDocExportRequest: _Optional[_Union[_export_pb2.DownloadDocExportRequest, _Mapping]] = ..., getDocExportRequest: _Optional[_Union[_export_pb2.GetDocExportRequest, _Mapping]] = ..., searchDocsRequest: _Optional[_Union[_doc_rest_pb2.SearchDocsRequest, _Mapping]] = ..., uploadDocExportRequest: _Optional[_Union[_export_pb2.UploadDocExportRequest, _Mapping]] = ..., createDocAssetRequest: _Optional[_Union[_doc_rest_pb2.CreateDocAssetRequest, _Mapping]] = ..., downloadDocAssetsRequest: _Optional[_Union[_doc_rest_pb2.DownloadDocAssetsRequest, _Mapping]] = ..., createDocExportEntryRequest: _Optional[_Union[_export_pb2.CreateDocExportEntryRequest, _Mapping]] = ..., getSketchRoomUpdatesRequest: _Optional[_Union[_room_pb2.GetSketchRoomUpdatesRequest, _Mapping]] = ..., uploadDocThumbnailRequest: _Optional[_Union[_doc_rest_pb2.UploadDocThumbnailRequest, _Mapping]] = ..., copyDocRequest: _Optional[_Union[_doc_rest_pb2.CopyDocRequest, _Mapping]] = ..., searchPublicContentDocByPathRequest: _Optional[_Union[_doc_rest_pb2.SearchPublicContentDocByPathRequest, _Mapping]] = ..., getDocumentByIdRequest: _Optional[_Union[_doc_rest_pb2.GetDocumentByIdRequest, _Mapping]] = ..., getDocumentByPathRequest: _Optional[_Union[_doc_rest_pb2.GetDocumentByPathRequest, _Mapping]] = ..., getDocumentSpaceNameRequest: _Optional[_Union[_doc_rest_pb2.GetDocumentSpaceNameRequest, _Mapping]] = ..., createDocCommentRequest: _Optional[_Union[_comment_pb2.CreateDocCommentRequest, _Mapping]] = ..., listDocCommentsRequest: _Optional[_Union[_comment_pb2.ListDocCommentsRequest, _Mapping]] = ..., updateDocCommentRequest: _Optional[_Union[_comment_pb2.UpdateDocCommentRequest, _Mapping]] = ..., listNewDocCommentsRequest: _Optional[_Union[_comment_pb2.ListNewDocCommentsRequest, _Mapping]] = ..., generatePairDeviceCodeRequest: _Optional[_Union[_pair_device_pb2.GeneratePairDeviceCodeRequest, _Mapping]] = ..., pairDeviceRequest: _Optional[_Union[_pair_device_pb2.PairDeviceRequest, _Mapping]] = ..., getPairedDeviceRequest: _Optional[_Union[_pair_device_pb2.GetPairedDeviceRequest, _Mapping]] = ..., revokeDevicePairingRequest: _Optional[_Union[_pair_device_pb2.RevokeDevicePairingRequest, _Mapping]] = ..., getUserFromPairedDeviceIdRequest: _Optional[_Union[_pair_device_pb2.GetUserFromPairedDeviceIdRequest, _Mapping]] = ..., LaunchRoomRequest: _Optional[_Union[LaunchRoomRequest, _Mapping]] = ..., enterRoomRequest: _Optional[_Union[EnterRoomRequest, _Mapping]] = ..., shutdownRoomRequest: _Optional[_Union[ShutdownRoomRequest, _Mapping]] = ..., releaseRoomInitLockRequest: _Optional[_Union[ReleaseRoomInitLockRequest, _Mapping]] = ..., inviteUsersToCollabRequest: _Optional[_Union[InviteUsersToCollabRequest, _Mapping]] = ..., listInvitableUsersRequest: _Optional[_Union[ListInvitableUsersRequest, _Mapping]] = ..., enterRoomWithDeepLinkRequest: _Optional[_Union[EnterRoomWithDeepLinkRequest, _Mapping]] = ..., changeUserCollaborationRoleRequest: _Optional[_Union[_collab_pb2.ChangeUserCollaborationRoleRequest, _Mapping]] = ..., listSharedDocsRequest: _Optional[_Union[_doc_rest_pb2.ListSharedDocsRequest, _Mapping]] = ..., reportAbusiveBehaviourRequest: _Optional[_Union[_collab_pb2.ReportAbusiveBehaviourRequest, _Mapping]] = ..., listRoomRecordingsRequest: _Optional[_Union[ListRoomRecordingsRequest, _Mapping]] = ..., replayRoomRecordingRequest: _Optional[_Union[ReplayRoomRecordingRequest, _Mapping]] = ..., getRoomRecordingRequest: _Optional[_Union[GetRoomRecordingRequest, _Mapping]] = ..., getRoomRecordingReplayDataRequest: _Optional[_Union[GetRoomRecordingReplayDataRequest, _Mapping]] = ..., getRoomRecordingReplayAssetsRequest: _Optional[_Union[GetRoomRecordingReplayAssetsRequest, _Mapping]] = ..., shareRoomWithUserRequest: _Optional[_Union[_room_pb2.ShareRoomWithUserRequest, _Mapping]] = ..., listRoomAccessesRequest: _Optional[_Union[_room_pb2.ListRoomAccessesRequest, _Mapping]] = ..., removeAccessFromRoomRequest: _Optional[_Union[_room_pb2.RemoveAccessFromRoomRequest, _Mapping]] = ..., setCoSketchRoomPassRequest: _Optional[_Union[_room_pb2.SetCoSketchRoomPassRequest, _Mapping]] = ..., generateDeepAccessLinkRequest: _Optional[_Union[_room_pb2.GenerateDeepAccessLinkRequest, _Mapping]] = ..., enterPublicRoomRequest: _Optional[_Union[EnterRoomRequest, _Mapping]] = ..., bookmarkPublicDocRequest: _Optional[_Union[_room_pb2.BookmarkPublicDocRequest, _Mapping]] = ..., listPublicRoomRequest: _Optional[_Union[_room_pb2.ListPublicRoomRequest, _Mapping]] = ..., setPublicDocRequest: _Optional[_Union[_room_pb2.SetPublicDocRequest, _Mapping]] = ..., stopRoomSharingRequest: _Optional[_Union[_room_pb2.StopRoomSharingRequest, _Mapping]] = ..., createEnterRoomNotificationRequest: _Optional[_Union[_doc_rest_pb2.CreateEnterRoomNotificationRequest, _Mapping]] = ..., listRoomAccessRequestsRequest: _Optional[_Union[_room_pb2.ListRoomAccessRequestsRequest, _Mapping]] = ..., approveRoomAccessRequest: _Optional[_Union[_room_pb2.ApproveRoomAccessRequest, _Mapping]] = ..., listAllUsersWithAccessToDocRequest: _Optional[_Union[_doc_rest_pb2.ListAllUsersWithAccessToDocRequest, _Mapping]] = ..., launchStreamingAgentForRoomRequest: _Optional[_Union[_room_pb2.LaunchStreamingAgentForRoomRequest, _Mapping]] = ..., enterRoomViaAdminNotificationDeeplinkRequest: _Optional[_Union[_room_pb2.EnterRoomViaAdminNotificationDeeplinkRequest, _Mapping]] = ..., checkForClientAppUpdateRequest: _Optional[_Union[_update_check_pb2.CheckForClientAppUpdateRequest, _Mapping]] = ..., getRoomIdByShortCodeRequest: _Optional[_Union[_room_pb2.GetRoomIdByShortCodeRequest, _Mapping]] = ..., getShortCodeByRoomIdRequest: _Optional[_Union[_room_pb2.GetShortCodeByRoomIdRequest, _Mapping]] = ..., offlineUserTrace: _Optional[_Union[OfflineUserTrace, _Mapping]] = ..., syncAchievementRequest: _Optional[_Union[SyncAchievementRequest, _Mapping]] = ..., updateOrgRequest: _Optional[_Union[_management_pb2.UpdateOrgRequest, _Mapping]] = ..., markTeamAsFavoriteRequest: _Optional[_Union[_team_pb2.MarkTeamAsFavoriteRequest, _Mapping]] = ..., removeExternalMembersFromTeamRequest: _Optional[_Union[_team_pb2.RemoveExternalMembersFromTeamRequest, _Mapping]] = ..., listAllTeamsForUserRequest: _Optional[_Union[_team_pb2.ListAllTeamsForUserRequest, _Mapping]] = ..., listOrgTeamMembersRequest: _Optional[_Union[_team_member_pb2.ListOrgTeamMembersRequest, _Mapping]] = ..., listUserOrgTeamMembershipsRequest: _Optional[_Union[_team_pb2.ListUserOrgTeamMembershipsRequest, _Mapping]] = ..., createOrgTeamRequest: _Optional[_Union[_team_pb2.CreateOrgTeamRequest, _Mapping]] = ..., deleteOrgTeamRequest: _Optional[_Union[_team_pb2.DeleteOrgTeamRequest, _Mapping]] = ..., listOrgTeamsRequest: _Optional[_Union[_team_pb2.ListOrgTeamsRequest, _Mapping]] = ..., getOrgTeamRequest: _Optional[_Union[_team_pb2.GetOrgTeamRequest, _Mapping]] = ..., updateOrgTeamRequest: _Optional[_Union[_team_pb2.UpdateOrgTeamRequest, _Mapping]] = ..., createOrgTeamMemberRequest: _Optional[_Union[_team_member_pb2.CreateOrgTeamMemberRequest, _Mapping]] = ..., deleteOrgTeamMemberRequest: _Optional[_Union[_team_member_pb2.DeleteOrgTeamMemberRequest, _Mapping]] = ..., updateOrgTeamMemberRequest: _Optional[_Union[_team_member_pb2.UpdateOrgTeamMemberRequest, _Mapping]] = ..., getTeamRequest: _Optional[_Union[_team_pb2.GetTeamRequest, _Mapping]] = ..., getAllOrgTeamsRequest: _Optional[_Union[_team_pb2.GetAllOrgTeamsRequest, _Mapping]] = ..., inviteMembersRequest: _Optional[_Union[_team_pb2.InviteMembersRequest, _Mapping]] = ..., editMemberActiveStatusRequest: _Optional[_Union[_team_pb2.EditMemberActiveStatusRequest, _Mapping]] = ..., switchUserOrgRequest: _Optional[_Union[_team_pb2.SwitchUserOrgRequest, _Mapping]] = ..., editMemberRoleRequest: _Optional[_Union[_team_pb2.EditMemberRoleRequest, _Mapping]] = ..., getOrgDownloadVersionsRequest: _Optional[_Union[_management_pb2.GetOrgDownloadVersionsRequest, _Mapping]] = ..., requestUserInviteToOrgAdminRequest: _Optional[_Union[_team_pb2.RequestUserInviteToOrgAdminRequest, _Mapping]] = ..., userInviteApprovalRequest: _Optional[_Union[_team_pb2.UserInviteApprovalRequest, _Mapping]] = ..., listOrgJoinRequestsRequest: _Optional[_Union[_team_pb2.ListOrgJoinRequestsRequest, _Mapping]] = ..., requestRoomAccessRequest: _Optional[_Union[_room_pb2.RequestRoomAccessRequest, _Mapping]] = ..., removeMemberFromOrgRequest: _Optional[_Union[_team_pb2.RemoveMemberFromOrgRequest, _Mapping]] = ..., getUsersInOrgRequest: _Optional[_Union[_team_pb2.GetUsersInOrgRequest, _Mapping]] = ..., listOrgMembershipInvitationsRequest: _Optional[_Union[_invitation_pb2.ListOrgMembershipInvitationsRequest, _Mapping]] = ..., deleteOrgMembershipInvitationRequest: _Optional[_Union[_invitation_pb2.DeleteOrgMembershipInvitationRequest, _Mapping]] = ..., createOrgAccountsByOrgAdminRequest: _Optional[_Union[_invitation_pb2.CreateOrgAccountsByOrgAdminRequest, _Mapping]] = ..., createConnectionInvitationRequest: _Optional[_Union[_connections_pb2.CreateConnectionInvitationRequest, _Mapping]] = ..., listConnectionInvitationRequest: _Optional[_Union[_connections_pb2.ListConnectionInvitationsRequest, _Mapping]] = ..., updateConnectionInvitationRequest: _Optional[_Union[_connections_pb2.UpdateConnectionInvitationRequest, _Mapping]] = ..., listConnectionsRequest: _Optional[_Union[_connections_pb2.ListConnectionsRequest, _Mapping]] = ..., initiateOidcAuthorisationRequest: _Optional[_Union[_connections_pb2.InitiateOidcAuthorisationRequest, _Mapping]] = ..., completeOidcAuthorisationRequest: _Optional[_Union[_connections_pb2.CompleteOidcAuthorisationRequest, _Mapping]] = ..., revokeOidcAuthorisationRequest: _Optional[_Union[_connections_pb2.RevokeOidcAuthorisationRequest, _Mapping]] = ..., searchPublicUserRequest: _Optional[_Union[_connections_pb2.SearchPublicUserRequest, _Mapping]] = ..., createCommunityStudioRequest: _Optional[_Union[CreateCommunityStudioRequest, _Mapping]] = ..., updateCommunityStudioRequest: _Optional[_Union[UpdateCommunityStudioRequest, _Mapping]] = ..., getCommunityStudioRequest: _Optional[_Union[GetCommunityStudioRequest, _Mapping]] = ..., listCommunityStudiosRequest: _Optional[_Union[ListCommunityStudiosRequest, _Mapping]] = ..., sendSupportEmailRequest: _Optional[_Union[SendSupportEmailRequest, _Mapping]] = ..., requestCertificateRequest: _Optional[_Union[RequestCertificateRequest, _Mapping]] = ..., updateSketchObjectsRequest: _Optional[_Union[_online_sketch_pb2.UpdateSketchObjectsRequest, _Mapping]] = ..., handraiseToPaywallRequest: _Optional[_Union[HandraiseToPaywallRequest, _Mapping]] = ..., consumeDownloadAllowanceRequest: _Optional[_Union[ConsumeDownloadAllowanceRequest, _Mapping]] = ..., createSubscriptionRequest: _Optional[_Union[_profile_pb2.CreateSubscriptionRequest, _Mapping]] = ..., getSubscriptionPriceRequest: _Optional[_Union[_profile_pb2.GetSubscriptionPriceRequest, _Mapping]] = ..., getStripeCustomerPortalLinkRequest: _Optional[_Union[_profile_pb2.GetStripeCustomerPortalLinkRequest, _Mapping]] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., source: _Optional[_Union[_gravi_model_pb2.SourceApp, str]] = ..., appType: _Optional[_Union[SourceAppType, str]] = ..., analyticsHints: _Optional[_Iterable[_Union[AnalyticsHint, str]]] = ..., pardotMetadata: _Optional[_Union[PardotMetadata, _Mapping]] = ..., postImageToDiscordRequest: _Optional[_Union[PostImageToDiscordRequest, _Mapping]] = ..., getPublicUserProfileRequest: _Optional[_Union[GetPublicUserProfileRequest, _Mapping]] = ..., maintenanceCheckRequest: _Optional[_Union[MaintenanceCheckRequest, _Mapping]] = ..., listPublicSpaceDocsRequest: _Optional[_Union[_doc_rest_pb2.ListPublicSpaceDocsRequest, _Mapping]] = ..., downloadPublicSpaceDocRequest: _Optional[_Union[_doc_rest_pb2.DownloadPublicSpaceDocRequest, _Mapping]] = ..., transcribeRequest: _Optional[_Union[_transcribe_pb2.TranscribeRequest, _Mapping]] = ..., askShrekRequest: _Optional[_Union[_ask_pb2.AskShrekRequest, _Mapping]] = ..., generateImagesRequest: _Optional[_Union[_image_pb2.GenerateImagesRequest, _Mapping]] = ..., generate3DModelRequest: _Optional[_Union[_image_pb2.Generate3DModelRequest, _Mapping]] = ..., lastNotificationQueryTime: _Optional[int] = ...) -> None: ...

class PlatformRestResponse(_message.Message):
    __slots__ = ("restType", "errorCode", "upgradeToClientVersion", "cmsUpdateUrlBucket", "cmsUpdateVersion", "cmsUpdateUrlFolder", "maintenanceFlags", "notifications", "requestId", "publicContentSpaceId", "loginResponse", "magicLinkLoginResponse", "storeSignUpResponse", "emailAccountLinkResponse", "signUpByEmailPassResponse", "detachDeviceResponse", "sendBetaSignupEmailResponse", "deleteAccountResponse", "earlyAdopterCheckResponse", "resendEmailVerificationResponse", "listSSOProvidersForEmailResponse", "initiateOidcSSOLoginResponse", "getSSOProviderForSignupResponse", "signUpWithSSOResponse", "getPublicKeyResponse", "attachEmailResponse", "getCMSURLResponse", "resendStoreSignupEmailResponse", "initiateSignUpResponse", "sendUserFeedbackResponse", "enableTwoFactorAuthResponse", "completeSignUpByCodeResponse", "activateCodeResponse", "getLoggedInUserResponse", "getLoggedInUserResponseV2", "updateUserInfoResponse", "changePasswordResponse", "changeEmailResponse", "generateSecretKeyResponse", "getLoggedInUserOrgInfoResponse", "getSubscriptionPackResponse", "consumeNotificationResponse", "changeUserPasswordResponse", "getNotificationsForLoggedInUserResponse", "createUserSurveyResponse", "getOrgResponse", "listUserLoginAuditsResponse", "listOrgUserActionAuditsResponse", "createVoiceToTextUrlResponse", "convertDocResponse", "listDocsResponse", "listRecentDocsResponse", "deprecatedGetDocumentsResponse", "getUsedSpaceSizeResponse", "sendDocumentResponse", "createFolderResponse", "moveDocumentResponse", "InitiateFileUploadResponse", "DownloadDocResponse", "createDocResponse", "updateDocResponse", "trashDocResponse", "restoreDocResponse", "listDocsInBinResponse", "deleteDocsInBinResponse", "exportDocResponse", "listDocExportsResponse", "downloadDocExportResponse", "getDocExportResponse", "searchDocsResponse", "uploadDocExportResponse", "createDocAssetResponse", "downloadDocAssetsResponse", "createDocExportEntryResponse", "getSketchRoomUpdatesResponse", "uploadDocThumbnailResponse", "copyDocResponse", "searchPublicContentDocByPathResponse", "getDocumentByIdResponse", "getDocumentByPathResponse", "getDocumentSpaceNameResponse", "createDocCommentResponse", "listDocCommentsResponse", "updateDocCommentResponse", "generatePairDeviceCodeResponse", "getPairedDeviceResponse", "revokeDevicePairingResponse", "getUserFromPairedDeviceIdResponse", "LaunchRoomResponse", "enterRoomResponse", "shutdownRoomResponse", "inviteUsersToCollabResponse", "listInvitableUsersResponse", "changeUserCollaborationRoleResponse", "listSharedDocsResponse", "reportAbusiveBehaviourResponse", "listRoomRecordingsResponse", "replayRoomRecordingResponse", "getRoomRecordingResponse", "getRoomRecordingReplayDataResponse", "getRoomRecordingReplayAssetsResponse", "shareRoomWithUserResponse", "listRoomAccessesResponse", "removeAccessFromRoomResponse", "setCoSketchRoomPassResponse", "generateDeepAccessLinkResponse", "bookmarkPublicDocResponse", "setPublicDocResponse", "stopRoomSharingResponse", "createEnterRoomNotificationResponse", "listRoomAccessRequestsResponse", "approveRoomAccessResponse", "listAllUsersWithAccessToDocResponse", "launchStreamingAgentForRoomResponse", "checkForClientAppUpdateResponse", "getRoomIdByShortCodeResponse", "getShortCodeByRoomIdResponse", "offlineUserTraceResponse", "getAchievementsResponse", "updateOrgResponse", "markTeamAsFavoriteResponse", "removeExternalMembersFromTeamResponse", "listAllTeamsForUserResponse", "listOrgTeamMembersResponse", "listUserOrgTeamMembershipsResponse", "createOrgTeamResponse", "deleteOrgTeamResponse", "listOrgTeamsResponse", "getOrgTeamResponse", "updateOrgTeamResponse", "createOrgTeamMemberResponse", "deleteOrgTeamMemberResponse", "updateOrgTeamMemberResponse", "getTeamResponse", "getAllOrgTeamsResponse", "inviteMembersResponse", "editMemberActiveStatusResponse", "switchUserOrgResponse", "editMemberRoleResponse", "getOrgDownloadVersionsResponse", "requestUserInviteToOrgAdminResponse", "userInviteApprovalResponse", "listOrgJoinRequestsResponse", "requestRoomAccessResponse", "removeMemberFromOrgResponse", "getUsersInOrgResponse", "listOrgMembershipInvitationsResponse", "deleteOrgMembershipInvitationResponse", "createOrgAccountsByOrgAdminResponse", "createConnectionInvitationResponse", "listConnectionInvitationsResponse", "updateConnectionInvitationResponse", "listConnectionsResponse", "initiateOidcAuthorisationResponse", "completeOidcAuthorisationResponse", "revokeOidcAuthorisationResponse", "searchPublicUserResponse", "createCommunityStudioResponse", "updateCommunityStudioResponse", "getCommunityStudioResponse", "listCommunityStudiosResponse", "sendSupportEmailResponse", "requestCertificateResponse", "updateSketchObjectsResponse", "handraiseToPaywallResponse", "consumeDownloadAllowanceResponse", "createSubscriptionResponse", "getSubscriptionPriceResponse", "getStripeCustomerPortalLinkResponse", "postImageToDiscordResponse", "getPublicUserProfileResponse", "maintenanceCheckResponse", "publicCollabsSpaceId", "listPublicSpaceDocsResponse", "downloadPublicSpaceDocResponse", "downloadOverrideConfigResponse", "transcribeResponse", "askShrekResponse", "generateImagesResponse", "generate3DModelResponse", "orgRequiredVersions", "restErrorMessage")
    RESTTYPE_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    UPGRADETOCLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    CMSUPDATEURLBUCKET_FIELD_NUMBER: _ClassVar[int]
    CMSUPDATEVERSION_FIELD_NUMBER: _ClassVar[int]
    CMSUPDATEURLFOLDER_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCEFLAGS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    PUBLICCONTENTSPACEID_FIELD_NUMBER: _ClassVar[int]
    LOGINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MAGICLINKLOGINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    STORESIGNUPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    EMAILACCOUNTLINKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGNUPBYEMAILPASSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DETACHDEVICERESPONSE_FIELD_NUMBER: _ClassVar[int]
    SENDBETASIGNUPEMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEACCOUNTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    EARLYADOPTERCHECKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESENDEMAILVERIFICATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTSSOPROVIDERSFOREMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INITIATEOIDCSSOLOGINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSSOPROVIDERFORSIGNUPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGNUPWITHSSORESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETPUBLICKEYRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ATTACHEMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETCMSURLRESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESENDSTORESIGNUPEMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INITIATESIGNUPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SENDUSERFEEDBACKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ENABLETWOFACTORAUTHRESPONSE_FIELD_NUMBER: _ClassVar[int]
    COMPLETESIGNUPBYCODERESPONSE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATECODERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERRESPONSEV2_FIELD_NUMBER: _ClassVar[int]
    UPDATEUSERINFORESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANGEPASSWORDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANGEEMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GENERATESECRETKEYRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETLOGGEDINUSERORGINFORESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSUBSCRIPTIONPACKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONSUMENOTIFICATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERPASSWORDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETNOTIFICATIONSFORLOGGEDINUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEUSERSURVEYRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETORGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTUSERLOGINAUDITSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTORGUSERACTIONAUDITSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEVOICETOTEXTURLRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONVERTDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTDOCSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTRECENTDOCSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDGETDOCUMENTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETUSEDSPACESIZERESPONSE_FIELD_NUMBER: _ClassVar[int]
    SENDDOCUMENTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEFOLDERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MOVEDOCUMENTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INITIATEFILEUPLOADRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATEDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    TRASHDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESTOREDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTDOCSINBINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEDOCSINBINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    EXPORTDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTDOCEXPORTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCEXPORTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETDOCEXPORTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SEARCHDOCSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPLOADDOCEXPORTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCASSETRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADDOCASSETSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCEXPORTENTRYRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSKETCHROOMUPDATESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPLOADDOCTHUMBNAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    COPYDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SEARCHPUBLICCONTENTDOCBYPATHRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTBYIDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTBYPATHRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETDOCUMENTSPACENAMERESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEDOCCOMMENTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTDOCCOMMENTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATEDOCCOMMENTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GENERATEPAIRDEVICECODERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETPAIREDDEVICERESPONSE_FIELD_NUMBER: _ClassVar[int]
    REVOKEDEVICEPAIRINGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETUSERFROMPAIREDDEVICEIDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LAUNCHROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ENTERROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWNROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INVITEUSERSTOCOLLABRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTINVITABLEUSERSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERCOLLABORATIONROLERESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTSHAREDDOCSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REPORTABUSIVEBEHAVIOURRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTROOMRECORDINGSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REPLAYROOMRECORDINGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGREPLAYDATARESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETROOMRECORDINGREPLAYASSETSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SHAREROOMWITHUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTROOMACCESSESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REMOVEACCESSFROMROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SETCOSKETCHROOMPASSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GENERATEDEEPACCESSLINKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    BOOKMARKPUBLICDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SETPUBLICDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    STOPROOMSHARINGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEENTERROOMNOTIFICATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTROOMACCESSREQUESTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    APPROVEROOMACCESSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTALLUSERSWITHACCESSTODOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LAUNCHSTREAMINGAGENTFORROOMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHECKFORCLIENTAPPUPDATERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETROOMIDBYSHORTCODERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSHORTCODEBYROOMIDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    OFFLINEUSERTRACERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETACHIEVEMENTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MARKTEAMASFAVORITERESPONSE_FIELD_NUMBER: _ClassVar[int]
    REMOVEEXTERNALMEMBERSFROMTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTALLTEAMSFORUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTORGTEAMMEMBERSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTUSERORGTEAMMEMBERSHIPSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEORGTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEORGTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTORGTEAMSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETORGTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEORGTEAMMEMBERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEORGTEAMMEMBERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATEORGTEAMMEMBERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETTEAMRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETALLORGTEAMSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INVITEMEMBERSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    EDITMEMBERACTIVESTATUSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SWITCHUSERORGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    EDITMEMBERROLERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETORGDOWNLOADVERSIONSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REQUESTUSERINVITETOORGADMINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    USERINVITEAPPROVALRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTORGJOINREQUESTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REQUESTROOMACCESSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REMOVEMEMBERFROMORGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETUSERSINORGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTORGMEMBERSHIPINVITATIONSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEORGMEMBERSHIPINVITATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEORGACCOUNTSBYORGADMINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATECONNECTIONINVITATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTCONNECTIONINVITATIONSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATECONNECTIONINVITATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTCONNECTIONSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    INITIATEOIDCAUTHORISATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    COMPLETEOIDCAUTHORISATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REVOKEOIDCAUTHORISATIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SEARCHPUBLICUSERRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATECOMMUNITYSTUDIORESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATECOMMUNITYSTUDIORESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETCOMMUNITYSTUDIORESPONSE_FIELD_NUMBER: _ClassVar[int]
    LISTCOMMUNITYSTUDIOSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SENDSUPPORTEMAILRESPONSE_FIELD_NUMBER: _ClassVar[int]
    REQUESTCERTIFICATERESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATESKETCHOBJECTSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    HANDRAISETOPAYWALLRESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONSUMEDOWNLOADALLOWANCERESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATESUBSCRIPTIONRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSUBSCRIPTIONPRICERESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETSTRIPECUSTOMERPORTALLINKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    POSTIMAGETODISCORDRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETPUBLICUSERPROFILERESPONSE_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCECHECKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    PUBLICCOLLABSSPACEID_FIELD_NUMBER: _ClassVar[int]
    LISTPUBLICSPACEDOCSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADPUBLICSPACEDOCRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADOVERRIDECONFIGRESPONSE_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIBERESPONSE_FIELD_NUMBER: _ClassVar[int]
    ASKSHREKRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GENERATEIMAGESRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GENERATE3DMODELRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ORGREQUIREDVERSIONS_FIELD_NUMBER: _ClassVar[int]
    RESTERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    restType: PlatformRestType
    errorCode: PlatformRestError
    upgradeToClientVersion: str
    cmsUpdateUrlBucket: str
    cmsUpdateVersion: str
    cmsUpdateUrlFolder: str
    maintenanceFlags: _gravi_model_pb2.MaintenanceFlags
    notifications: _containers.RepeatedCompositeFieldContainer[_notifications_pb2.NotificationTO]
    requestId: str
    publicContentSpaceId: _gravi_model_pb2.SpaceId
    loginResponse: _login_pb2.LoginResponse
    magicLinkLoginResponse: MagicLinkLoginResponse
    storeSignUpResponse: StoreSignUpResponse
    emailAccountLinkResponse: EmailAccountLinkResponse
    signUpByEmailPassResponse: _signup_pb2.SignUpByEmailPassResponse
    detachDeviceResponse: DetachDeviceResponse
    sendBetaSignupEmailResponse: SendBetaSignupEmailResponse
    deleteAccountResponse: DeleteAccountResponse
    earlyAdopterCheckResponse: EarlyAdopterCheckResponse
    resendEmailVerificationResponse: _signup_pb2.ResendEmailVerificationResponse
    listSSOProvidersForEmailResponse: _auth_pb2.ListSSOProvidersForEmailResponse
    initiateOidcSSOLoginResponse: _auth_pb2.InitiateOidcSSOLoginResponse
    getSSOProviderForSignupResponse: _auth_pb2.GetSSOProviderForSignupResponse
    signUpWithSSOResponse: _auth_pb2.SignUpWithSSOResponse
    getPublicKeyResponse: GetPublicKeyResponse
    attachEmailResponse: AttachEmailResponse
    getCMSURLResponse: GetCMSURLResponse
    resendStoreSignupEmailResponse: ResendStoreSignupEmailResponse
    initiateSignUpResponse: _signup_pb2.InitiateSignUpResponse
    sendUserFeedbackResponse: _signup_pb2.SendUserFeedbackResponse
    enableTwoFactorAuthResponse: _auth_pb2.EnableTwoFactorAuthResponse
    completeSignUpByCodeResponse: _auth_pb2.CompleteSignUpByCodeResponse
    activateCodeResponse: _activate_code_pb2.ActivateCodeResponse
    getLoggedInUserResponse: GetLoggedInUserResponse
    getLoggedInUserResponseV2: _account_pb2.GetLoggedInUserResponseV2
    updateUserInfoResponse: _profile_pb2.UpdateUserInfoResponse
    changePasswordResponse: _auth_pb2.ChangePasswordResponse
    changeEmailResponse: _auth_pb2.ChangeEmailResponse
    generateSecretKeyResponse: _auth_pb2.GenerateSecretKeyResponse
    getLoggedInUserOrgInfoResponse: GetLoggedInUserOrgInfoResponse
    getSubscriptionPackResponse: GetSubscriptionPackResponse
    consumeNotificationResponse: ConsumeNotificationResponse
    changeUserPasswordResponse: ChangeUserPasswordResponse
    getNotificationsForLoggedInUserResponse: GetNotificationsForLoggedInUserResponse
    createUserSurveyResponse: _profile_pb2.CreateUserSurveyResponse
    getOrgResponse: GetOrgResponse
    listUserLoginAuditsResponse: _auth_pb2.ListUserLoginAuditsResponse
    listOrgUserActionAuditsResponse: _organisation_pb2.ListOrgUserActionAuditsResponse
    createVoiceToTextUrlResponse: CreateVoiceToTextUrlResponse
    convertDocResponse: _doc_rest_pb2.ConvertDocResponse
    listDocsResponse: _doc_rest_pb2.ListDocsResponse
    listRecentDocsResponse: _doc_rest_pb2.ListRecentDocsResponse
    deprecatedGetDocumentsResponse: _doc_rest_pb2.DeprecatedGetDocumentsResponse
    getUsedSpaceSizeResponse: _doc_rest_pb2.GetUsedSpaceSizeResponse
    sendDocumentResponse: _doc_rest_pb2.SendDocumentResponse
    createFolderResponse: _doc_rest_pb2.CreateFolderResponse
    moveDocumentResponse: _doc_rest_pb2.MoveDocumentResponse
    InitiateFileUploadResponse: _doc_rest_pb2.InitiateFileUploadResponse
    DownloadDocResponse: _doc_rest_pb2.DownloadDocResponse
    createDocResponse: _doc_rest_pb2.CreateDocResponse
    updateDocResponse: _doc_rest_pb2.UpdateDocResponse
    trashDocResponse: _doc_rest_pb2.TrashDocResponse
    restoreDocResponse: _doc_rest_pb2.RestoreDocResponse
    listDocsInBinResponse: _doc_rest_pb2.ListDocsInBinResponse
    deleteDocsInBinResponse: _doc_rest_pb2.DeleteDocsInBinResponse
    exportDocResponse: _export_pb2.ExportDocResponse
    listDocExportsResponse: _export_pb2.ListDocExportsResponse
    downloadDocExportResponse: _export_pb2.DownloadDocExportResponse
    getDocExportResponse: _export_pb2.GetDocExportResponse
    searchDocsResponse: _doc_rest_pb2.SearchDocsResponse
    uploadDocExportResponse: _export_pb2.UploadDocExportResponse
    createDocAssetResponse: _doc_rest_pb2.CreateDocAssetResponse
    downloadDocAssetsResponse: _doc_rest_pb2.DownloadDocAssetsResponse
    createDocExportEntryResponse: _export_pb2.CreateDocExportEntryResponse
    getSketchRoomUpdatesResponse: _room_pb2.GetSketchRoomUpdatesResponse
    uploadDocThumbnailResponse: _doc_rest_pb2.UploadDocThumbnailResponse
    copyDocResponse: _doc_rest_pb2.CopyDocResponse
    searchPublicContentDocByPathResponse: _doc_rest_pb2.SearchPublicContentDocByPathResponse
    getDocumentByIdResponse: _doc_rest_pb2.GetDocumentResponse
    getDocumentByPathResponse: _doc_rest_pb2.GetDocumentResponse
    getDocumentSpaceNameResponse: _doc_rest_pb2.GetDocumentSpaceNameResponse
    createDocCommentResponse: _comment_pb2.CreateDocCommentResponse
    listDocCommentsResponse: _comment_pb2.ListDocCommentsResponse
    updateDocCommentResponse: _comment_pb2.UpdateDocCommentResponse
    generatePairDeviceCodeResponse: _pair_device_pb2.GeneratePairDeviceCodeResponse
    getPairedDeviceResponse: _pair_device_pb2.GetPairedDeviceResponse
    revokeDevicePairingResponse: _pair_device_pb2.RevokeDevicePairingResponse
    getUserFromPairedDeviceIdResponse: _pair_device_pb2.GetUserFromPairedDeviceIdResponse
    LaunchRoomResponse: LaunchRoomResponse
    enterRoomResponse: EnterRoomResponse
    shutdownRoomResponse: ShutdownRoomResponse
    inviteUsersToCollabResponse: InviteUsersToCollabResponse
    listInvitableUsersResponse: ListInvitableUsersResponse
    changeUserCollaborationRoleResponse: _collab_pb2.ChangeUserCollaborationRoleResponse
    listSharedDocsResponse: _doc_rest_pb2.ListSharedDocsResponse
    reportAbusiveBehaviourResponse: _collab_pb2.ReportAbusiveBehaviourResponse
    listRoomRecordingsResponse: ListRoomRecordingsResponse
    replayRoomRecordingResponse: ReplayRoomRecordingResponse
    getRoomRecordingResponse: GetRoomRecordingResponse
    getRoomRecordingReplayDataResponse: GetRoomRecordingReplayDataResponse
    getRoomRecordingReplayAssetsResponse: GetRoomRecordingReplayAssetsResponse
    shareRoomWithUserResponse: _room_pb2.ShareRoomWithUserResponse
    listRoomAccessesResponse: _room_pb2.ListRoomAccessesResponse
    removeAccessFromRoomResponse: _room_pb2.RemoveAccessFromRoomResponse
    setCoSketchRoomPassResponse: _room_pb2.SetCoSketchRoomPassResponse
    generateDeepAccessLinkResponse: _room_pb2.GenerateDeepAccessLinkResponse
    bookmarkPublicDocResponse: _room_pb2.BookmarkPublicDocResponse
    setPublicDocResponse: _room_pb2.SetPublicDocResponse
    stopRoomSharingResponse: _room_pb2.StopRoomSharingResponse
    createEnterRoomNotificationResponse: _doc_rest_pb2.CreateEnterRoomNotificationResponse
    listRoomAccessRequestsResponse: _room_pb2.ListRoomAccessRequestsResponse
    approveRoomAccessResponse: _room_pb2.ApproveRoomAccessResponse
    listAllUsersWithAccessToDocResponse: _doc_rest_pb2.ListAllUsersWithAccessToDocResponse
    launchStreamingAgentForRoomResponse: _room_pb2.LaunchStreamingAgentForRoomResponse
    checkForClientAppUpdateResponse: _update_check_pb2.CheckForClientAppUpdateResponse
    getRoomIdByShortCodeResponse: _room_pb2.GetRoomIdByShortCodeResponse
    getShortCodeByRoomIdResponse: _room_pb2.GetShortCodeByRoomIdResponse
    offlineUserTraceResponse: OfflineUserTraceResponse
    getAchievementsResponse: GetAchievementsResponse
    updateOrgResponse: _management_pb2.UpdateOrgResponse
    markTeamAsFavoriteResponse: _team_pb2.MarkTeamAsFavoriteResponse
    removeExternalMembersFromTeamResponse: _team_pb2.RemoveExternalMembersFromTeamResponse
    listAllTeamsForUserResponse: _team_pb2.ListAllTeamsForUserResponse
    listOrgTeamMembersResponse: _team_member_pb2.ListOrgTeamMembersResponse
    listUserOrgTeamMembershipsResponse: _team_pb2.ListUserOrgTeamMembershipsResponse
    createOrgTeamResponse: _team_pb2.CreateOrgTeamResponse
    deleteOrgTeamResponse: _team_pb2.DeleteOrgTeamResponse
    listOrgTeamsResponse: _team_pb2.ListOrgTeamsResponse
    getOrgTeamResponse: _team_pb2.GetOrgTeamResponse
    updateOrgTeamResponse: _team_pb2.UpdateOrgTeamResponse
    createOrgTeamMemberResponse: _team_member_pb2.CreateOrgTeamMemberResponse
    deleteOrgTeamMemberResponse: _team_member_pb2.DeleteOrgTeamMemberResponse
    updateOrgTeamMemberResponse: _team_member_pb2.UpdateOrgTeamMemberResponse
    getTeamResponse: _team_pb2.GetTeamResponse
    getAllOrgTeamsResponse: _team_pb2.GetAllOrgTeamsResponse
    inviteMembersResponse: _team_pb2.InviteMembersResponse
    editMemberActiveStatusResponse: _team_pb2.EditMemberActiveStatusResponse
    switchUserOrgResponse: _team_pb2.SwitchUserOrgResponse
    editMemberRoleResponse: _team_pb2.EditMemberRoleResponse
    getOrgDownloadVersionsResponse: _management_pb2.GetOrgDownloadVersionsResponse
    requestUserInviteToOrgAdminResponse: _team_pb2.RequestUserInviteToOrgAdminResponse
    userInviteApprovalResponse: _team_pb2.UserInviteApprovalResponse
    listOrgJoinRequestsResponse: _team_pb2.ListOrgJoinRequestsResponse
    requestRoomAccessResponse: _room_pb2.RequestRoomAccessResponse
    removeMemberFromOrgResponse: _team_pb2.RemoveMemberFromOrgResponse
    getUsersInOrgResponse: _team_pb2.GetUsersInOrgResponse
    listOrgMembershipInvitationsResponse: _invitation_pb2.ListOrgMembershipInvitationsResponse
    deleteOrgMembershipInvitationResponse: _invitation_pb2.DeleteOrgMembershipInvitationResponse
    createOrgAccountsByOrgAdminResponse: _invitation_pb2.CreateOrgAccountsByOrgAdminResponse
    createConnectionInvitationResponse: _connections_pb2.CreateConnectionInvitationResponse
    listConnectionInvitationsResponse: _connections_pb2.ListConnectionInvitationsResponse
    updateConnectionInvitationResponse: _connections_pb2.UpdateConnectionInvitationResponse
    listConnectionsResponse: _connections_pb2.ListConnectionsResponse
    initiateOidcAuthorisationResponse: _connections_pb2.InitiateOidcAuthorisationResponse
    completeOidcAuthorisationResponse: _connections_pb2.CompleteOidcAuthorisationResponse
    revokeOidcAuthorisationResponse: _connections_pb2.RevokeOidcAuthorisationResponse
    searchPublicUserResponse: _connections_pb2.SearchPublicUserResponse
    createCommunityStudioResponse: CreateCommunityStudioResponse
    updateCommunityStudioResponse: UpdateCommunityStudioResponse
    getCommunityStudioResponse: GetCommunityStudioResponse
    listCommunityStudiosResponse: ListCommunityStudiosResponse
    sendSupportEmailResponse: SendSupportEmailResponse
    requestCertificateResponse: RequestCertificateResponse
    updateSketchObjectsResponse: _online_sketch_pb2.UpdateSketchObjectsResponse
    handraiseToPaywallResponse: HandraiseToPaywallResponse
    consumeDownloadAllowanceResponse: ConsumeDownloadAllowanceResponse
    createSubscriptionResponse: _profile_pb2.CreateSubscriptionResponse
    getSubscriptionPriceResponse: _profile_pb2.GetSubscriptionPriceResponse
    getStripeCustomerPortalLinkResponse: _profile_pb2.GetStripeCustomerPortalLinkResponse
    postImageToDiscordResponse: PostImageToDiscordResponse
    getPublicUserProfileResponse: GetPublicUserProfileResponse
    maintenanceCheckResponse: MaintenanceCheckResponse
    publicCollabsSpaceId: _gravi_model_pb2.SpaceId
    listPublicSpaceDocsResponse: _doc_rest_pb2.ListPublicSpaceDocsResponse
    downloadPublicSpaceDocResponse: _doc_rest_pb2.DownloadPublicSpaceDocResponse
    downloadOverrideConfigResponse: DownloadOverrideConfigResponse
    transcribeResponse: _transcribe_pb2.TranscribeResponse
    askShrekResponse: _ask_pb2.AskShrekResponse
    generateImagesResponse: _image_pb2.GenerateImagesResponse
    generate3DModelResponse: _image_pb2.Generate3DModelResponse
    orgRequiredVersions: _containers.RepeatedScalarFieldContainer[str]
    restErrorMessage: str
    def __init__(self, restType: _Optional[_Union[PlatformRestType, str]] = ..., errorCode: _Optional[_Union[PlatformRestError, str]] = ..., upgradeToClientVersion: _Optional[str] = ..., cmsUpdateUrlBucket: _Optional[str] = ..., cmsUpdateVersion: _Optional[str] = ..., cmsUpdateUrlFolder: _Optional[str] = ..., maintenanceFlags: _Optional[_Union[_gravi_model_pb2.MaintenanceFlags, _Mapping]] = ..., notifications: _Optional[_Iterable[_Union[_notifications_pb2.NotificationTO, _Mapping]]] = ..., requestId: _Optional[str] = ..., publicContentSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., loginResponse: _Optional[_Union[_login_pb2.LoginResponse, _Mapping]] = ..., magicLinkLoginResponse: _Optional[_Union[MagicLinkLoginResponse, _Mapping]] = ..., storeSignUpResponse: _Optional[_Union[StoreSignUpResponse, _Mapping]] = ..., emailAccountLinkResponse: _Optional[_Union[EmailAccountLinkResponse, _Mapping]] = ..., signUpByEmailPassResponse: _Optional[_Union[_signup_pb2.SignUpByEmailPassResponse, _Mapping]] = ..., detachDeviceResponse: _Optional[_Union[DetachDeviceResponse, _Mapping]] = ..., sendBetaSignupEmailResponse: _Optional[_Union[SendBetaSignupEmailResponse, _Mapping]] = ..., deleteAccountResponse: _Optional[_Union[DeleteAccountResponse, _Mapping]] = ..., earlyAdopterCheckResponse: _Optional[_Union[EarlyAdopterCheckResponse, _Mapping]] = ..., resendEmailVerificationResponse: _Optional[_Union[_signup_pb2.ResendEmailVerificationResponse, _Mapping]] = ..., listSSOProvidersForEmailResponse: _Optional[_Union[_auth_pb2.ListSSOProvidersForEmailResponse, _Mapping]] = ..., initiateOidcSSOLoginResponse: _Optional[_Union[_auth_pb2.InitiateOidcSSOLoginResponse, _Mapping]] = ..., getSSOProviderForSignupResponse: _Optional[_Union[_auth_pb2.GetSSOProviderForSignupResponse, _Mapping]] = ..., signUpWithSSOResponse: _Optional[_Union[_auth_pb2.SignUpWithSSOResponse, _Mapping]] = ..., getPublicKeyResponse: _Optional[_Union[GetPublicKeyResponse, _Mapping]] = ..., attachEmailResponse: _Optional[_Union[AttachEmailResponse, _Mapping]] = ..., getCMSURLResponse: _Optional[_Union[GetCMSURLResponse, _Mapping]] = ..., resendStoreSignupEmailResponse: _Optional[_Union[ResendStoreSignupEmailResponse, _Mapping]] = ..., initiateSignUpResponse: _Optional[_Union[_signup_pb2.InitiateSignUpResponse, _Mapping]] = ..., sendUserFeedbackResponse: _Optional[_Union[_signup_pb2.SendUserFeedbackResponse, _Mapping]] = ..., enableTwoFactorAuthResponse: _Optional[_Union[_auth_pb2.EnableTwoFactorAuthResponse, _Mapping]] = ..., completeSignUpByCodeResponse: _Optional[_Union[_auth_pb2.CompleteSignUpByCodeResponse, _Mapping]] = ..., activateCodeResponse: _Optional[_Union[_activate_code_pb2.ActivateCodeResponse, _Mapping]] = ..., getLoggedInUserResponse: _Optional[_Union[GetLoggedInUserResponse, _Mapping]] = ..., getLoggedInUserResponseV2: _Optional[_Union[_account_pb2.GetLoggedInUserResponseV2, _Mapping]] = ..., updateUserInfoResponse: _Optional[_Union[_profile_pb2.UpdateUserInfoResponse, _Mapping]] = ..., changePasswordResponse: _Optional[_Union[_auth_pb2.ChangePasswordResponse, _Mapping]] = ..., changeEmailResponse: _Optional[_Union[_auth_pb2.ChangeEmailResponse, _Mapping]] = ..., generateSecretKeyResponse: _Optional[_Union[_auth_pb2.GenerateSecretKeyResponse, _Mapping]] = ..., getLoggedInUserOrgInfoResponse: _Optional[_Union[GetLoggedInUserOrgInfoResponse, _Mapping]] = ..., getSubscriptionPackResponse: _Optional[_Union[GetSubscriptionPackResponse, _Mapping]] = ..., consumeNotificationResponse: _Optional[_Union[ConsumeNotificationResponse, _Mapping]] = ..., changeUserPasswordResponse: _Optional[_Union[ChangeUserPasswordResponse, _Mapping]] = ..., getNotificationsForLoggedInUserResponse: _Optional[_Union[GetNotificationsForLoggedInUserResponse, _Mapping]] = ..., createUserSurveyResponse: _Optional[_Union[_profile_pb2.CreateUserSurveyResponse, _Mapping]] = ..., getOrgResponse: _Optional[_Union[GetOrgResponse, _Mapping]] = ..., listUserLoginAuditsResponse: _Optional[_Union[_auth_pb2.ListUserLoginAuditsResponse, _Mapping]] = ..., listOrgUserActionAuditsResponse: _Optional[_Union[_organisation_pb2.ListOrgUserActionAuditsResponse, _Mapping]] = ..., createVoiceToTextUrlResponse: _Optional[_Union[CreateVoiceToTextUrlResponse, _Mapping]] = ..., convertDocResponse: _Optional[_Union[_doc_rest_pb2.ConvertDocResponse, _Mapping]] = ..., listDocsResponse: _Optional[_Union[_doc_rest_pb2.ListDocsResponse, _Mapping]] = ..., listRecentDocsResponse: _Optional[_Union[_doc_rest_pb2.ListRecentDocsResponse, _Mapping]] = ..., deprecatedGetDocumentsResponse: _Optional[_Union[_doc_rest_pb2.DeprecatedGetDocumentsResponse, _Mapping]] = ..., getUsedSpaceSizeResponse: _Optional[_Union[_doc_rest_pb2.GetUsedSpaceSizeResponse, _Mapping]] = ..., sendDocumentResponse: _Optional[_Union[_doc_rest_pb2.SendDocumentResponse, _Mapping]] = ..., createFolderResponse: _Optional[_Union[_doc_rest_pb2.CreateFolderResponse, _Mapping]] = ..., moveDocumentResponse: _Optional[_Union[_doc_rest_pb2.MoveDocumentResponse, _Mapping]] = ..., InitiateFileUploadResponse: _Optional[_Union[_doc_rest_pb2.InitiateFileUploadResponse, _Mapping]] = ..., DownloadDocResponse: _Optional[_Union[_doc_rest_pb2.DownloadDocResponse, _Mapping]] = ..., createDocResponse: _Optional[_Union[_doc_rest_pb2.CreateDocResponse, _Mapping]] = ..., updateDocResponse: _Optional[_Union[_doc_rest_pb2.UpdateDocResponse, _Mapping]] = ..., trashDocResponse: _Optional[_Union[_doc_rest_pb2.TrashDocResponse, _Mapping]] = ..., restoreDocResponse: _Optional[_Union[_doc_rest_pb2.RestoreDocResponse, _Mapping]] = ..., listDocsInBinResponse: _Optional[_Union[_doc_rest_pb2.ListDocsInBinResponse, _Mapping]] = ..., deleteDocsInBinResponse: _Optional[_Union[_doc_rest_pb2.DeleteDocsInBinResponse, _Mapping]] = ..., exportDocResponse: _Optional[_Union[_export_pb2.ExportDocResponse, _Mapping]] = ..., listDocExportsResponse: _Optional[_Union[_export_pb2.ListDocExportsResponse, _Mapping]] = ..., downloadDocExportResponse: _Optional[_Union[_export_pb2.DownloadDocExportResponse, _Mapping]] = ..., getDocExportResponse: _Optional[_Union[_export_pb2.GetDocExportResponse, _Mapping]] = ..., searchDocsResponse: _Optional[_Union[_doc_rest_pb2.SearchDocsResponse, _Mapping]] = ..., uploadDocExportResponse: _Optional[_Union[_export_pb2.UploadDocExportResponse, _Mapping]] = ..., createDocAssetResponse: _Optional[_Union[_doc_rest_pb2.CreateDocAssetResponse, _Mapping]] = ..., downloadDocAssetsResponse: _Optional[_Union[_doc_rest_pb2.DownloadDocAssetsResponse, _Mapping]] = ..., createDocExportEntryResponse: _Optional[_Union[_export_pb2.CreateDocExportEntryResponse, _Mapping]] = ..., getSketchRoomUpdatesResponse: _Optional[_Union[_room_pb2.GetSketchRoomUpdatesResponse, _Mapping]] = ..., uploadDocThumbnailResponse: _Optional[_Union[_doc_rest_pb2.UploadDocThumbnailResponse, _Mapping]] = ..., copyDocResponse: _Optional[_Union[_doc_rest_pb2.CopyDocResponse, _Mapping]] = ..., searchPublicContentDocByPathResponse: _Optional[_Union[_doc_rest_pb2.SearchPublicContentDocByPathResponse, _Mapping]] = ..., getDocumentByIdResponse: _Optional[_Union[_doc_rest_pb2.GetDocumentResponse, _Mapping]] = ..., getDocumentByPathResponse: _Optional[_Union[_doc_rest_pb2.GetDocumentResponse, _Mapping]] = ..., getDocumentSpaceNameResponse: _Optional[_Union[_doc_rest_pb2.GetDocumentSpaceNameResponse, _Mapping]] = ..., createDocCommentResponse: _Optional[_Union[_comment_pb2.CreateDocCommentResponse, _Mapping]] = ..., listDocCommentsResponse: _Optional[_Union[_comment_pb2.ListDocCommentsResponse, _Mapping]] = ..., updateDocCommentResponse: _Optional[_Union[_comment_pb2.UpdateDocCommentResponse, _Mapping]] = ..., generatePairDeviceCodeResponse: _Optional[_Union[_pair_device_pb2.GeneratePairDeviceCodeResponse, _Mapping]] = ..., getPairedDeviceResponse: _Optional[_Union[_pair_device_pb2.GetPairedDeviceResponse, _Mapping]] = ..., revokeDevicePairingResponse: _Optional[_Union[_pair_device_pb2.RevokeDevicePairingResponse, _Mapping]] = ..., getUserFromPairedDeviceIdResponse: _Optional[_Union[_pair_device_pb2.GetUserFromPairedDeviceIdResponse, _Mapping]] = ..., LaunchRoomResponse: _Optional[_Union[LaunchRoomResponse, _Mapping]] = ..., enterRoomResponse: _Optional[_Union[EnterRoomResponse, _Mapping]] = ..., shutdownRoomResponse: _Optional[_Union[ShutdownRoomResponse, _Mapping]] = ..., inviteUsersToCollabResponse: _Optional[_Union[InviteUsersToCollabResponse, _Mapping]] = ..., listInvitableUsersResponse: _Optional[_Union[ListInvitableUsersResponse, _Mapping]] = ..., changeUserCollaborationRoleResponse: _Optional[_Union[_collab_pb2.ChangeUserCollaborationRoleResponse, _Mapping]] = ..., listSharedDocsResponse: _Optional[_Union[_doc_rest_pb2.ListSharedDocsResponse, _Mapping]] = ..., reportAbusiveBehaviourResponse: _Optional[_Union[_collab_pb2.ReportAbusiveBehaviourResponse, _Mapping]] = ..., listRoomRecordingsResponse: _Optional[_Union[ListRoomRecordingsResponse, _Mapping]] = ..., replayRoomRecordingResponse: _Optional[_Union[ReplayRoomRecordingResponse, _Mapping]] = ..., getRoomRecordingResponse: _Optional[_Union[GetRoomRecordingResponse, _Mapping]] = ..., getRoomRecordingReplayDataResponse: _Optional[_Union[GetRoomRecordingReplayDataResponse, _Mapping]] = ..., getRoomRecordingReplayAssetsResponse: _Optional[_Union[GetRoomRecordingReplayAssetsResponse, _Mapping]] = ..., shareRoomWithUserResponse: _Optional[_Union[_room_pb2.ShareRoomWithUserResponse, _Mapping]] = ..., listRoomAccessesResponse: _Optional[_Union[_room_pb2.ListRoomAccessesResponse, _Mapping]] = ..., removeAccessFromRoomResponse: _Optional[_Union[_room_pb2.RemoveAccessFromRoomResponse, _Mapping]] = ..., setCoSketchRoomPassResponse: _Optional[_Union[_room_pb2.SetCoSketchRoomPassResponse, _Mapping]] = ..., generateDeepAccessLinkResponse: _Optional[_Union[_room_pb2.GenerateDeepAccessLinkResponse, _Mapping]] = ..., bookmarkPublicDocResponse: _Optional[_Union[_room_pb2.BookmarkPublicDocResponse, _Mapping]] = ..., setPublicDocResponse: _Optional[_Union[_room_pb2.SetPublicDocResponse, _Mapping]] = ..., stopRoomSharingResponse: _Optional[_Union[_room_pb2.StopRoomSharingResponse, _Mapping]] = ..., createEnterRoomNotificationResponse: _Optional[_Union[_doc_rest_pb2.CreateEnterRoomNotificationResponse, _Mapping]] = ..., listRoomAccessRequestsResponse: _Optional[_Union[_room_pb2.ListRoomAccessRequestsResponse, _Mapping]] = ..., approveRoomAccessResponse: _Optional[_Union[_room_pb2.ApproveRoomAccessResponse, _Mapping]] = ..., listAllUsersWithAccessToDocResponse: _Optional[_Union[_doc_rest_pb2.ListAllUsersWithAccessToDocResponse, _Mapping]] = ..., launchStreamingAgentForRoomResponse: _Optional[_Union[_room_pb2.LaunchStreamingAgentForRoomResponse, _Mapping]] = ..., checkForClientAppUpdateResponse: _Optional[_Union[_update_check_pb2.CheckForClientAppUpdateResponse, _Mapping]] = ..., getRoomIdByShortCodeResponse: _Optional[_Union[_room_pb2.GetRoomIdByShortCodeResponse, _Mapping]] = ..., getShortCodeByRoomIdResponse: _Optional[_Union[_room_pb2.GetShortCodeByRoomIdResponse, _Mapping]] = ..., offlineUserTraceResponse: _Optional[_Union[OfflineUserTraceResponse, _Mapping]] = ..., getAchievementsResponse: _Optional[_Union[GetAchievementsResponse, _Mapping]] = ..., updateOrgResponse: _Optional[_Union[_management_pb2.UpdateOrgResponse, _Mapping]] = ..., markTeamAsFavoriteResponse: _Optional[_Union[_team_pb2.MarkTeamAsFavoriteResponse, _Mapping]] = ..., removeExternalMembersFromTeamResponse: _Optional[_Union[_team_pb2.RemoveExternalMembersFromTeamResponse, _Mapping]] = ..., listAllTeamsForUserResponse: _Optional[_Union[_team_pb2.ListAllTeamsForUserResponse, _Mapping]] = ..., listOrgTeamMembersResponse: _Optional[_Union[_team_member_pb2.ListOrgTeamMembersResponse, _Mapping]] = ..., listUserOrgTeamMembershipsResponse: _Optional[_Union[_team_pb2.ListUserOrgTeamMembershipsResponse, _Mapping]] = ..., createOrgTeamResponse: _Optional[_Union[_team_pb2.CreateOrgTeamResponse, _Mapping]] = ..., deleteOrgTeamResponse: _Optional[_Union[_team_pb2.DeleteOrgTeamResponse, _Mapping]] = ..., listOrgTeamsResponse: _Optional[_Union[_team_pb2.ListOrgTeamsResponse, _Mapping]] = ..., getOrgTeamResponse: _Optional[_Union[_team_pb2.GetOrgTeamResponse, _Mapping]] = ..., updateOrgTeamResponse: _Optional[_Union[_team_pb2.UpdateOrgTeamResponse, _Mapping]] = ..., createOrgTeamMemberResponse: _Optional[_Union[_team_member_pb2.CreateOrgTeamMemberResponse, _Mapping]] = ..., deleteOrgTeamMemberResponse: _Optional[_Union[_team_member_pb2.DeleteOrgTeamMemberResponse, _Mapping]] = ..., updateOrgTeamMemberResponse: _Optional[_Union[_team_member_pb2.UpdateOrgTeamMemberResponse, _Mapping]] = ..., getTeamResponse: _Optional[_Union[_team_pb2.GetTeamResponse, _Mapping]] = ..., getAllOrgTeamsResponse: _Optional[_Union[_team_pb2.GetAllOrgTeamsResponse, _Mapping]] = ..., inviteMembersResponse: _Optional[_Union[_team_pb2.InviteMembersResponse, _Mapping]] = ..., editMemberActiveStatusResponse: _Optional[_Union[_team_pb2.EditMemberActiveStatusResponse, _Mapping]] = ..., switchUserOrgResponse: _Optional[_Union[_team_pb2.SwitchUserOrgResponse, _Mapping]] = ..., editMemberRoleResponse: _Optional[_Union[_team_pb2.EditMemberRoleResponse, _Mapping]] = ..., getOrgDownloadVersionsResponse: _Optional[_Union[_management_pb2.GetOrgDownloadVersionsResponse, _Mapping]] = ..., requestUserInviteToOrgAdminResponse: _Optional[_Union[_team_pb2.RequestUserInviteToOrgAdminResponse, _Mapping]] = ..., userInviteApprovalResponse: _Optional[_Union[_team_pb2.UserInviteApprovalResponse, _Mapping]] = ..., listOrgJoinRequestsResponse: _Optional[_Union[_team_pb2.ListOrgJoinRequestsResponse, _Mapping]] = ..., requestRoomAccessResponse: _Optional[_Union[_room_pb2.RequestRoomAccessResponse, _Mapping]] = ..., removeMemberFromOrgResponse: _Optional[_Union[_team_pb2.RemoveMemberFromOrgResponse, _Mapping]] = ..., getUsersInOrgResponse: _Optional[_Union[_team_pb2.GetUsersInOrgResponse, _Mapping]] = ..., listOrgMembershipInvitationsResponse: _Optional[_Union[_invitation_pb2.ListOrgMembershipInvitationsResponse, _Mapping]] = ..., deleteOrgMembershipInvitationResponse: _Optional[_Union[_invitation_pb2.DeleteOrgMembershipInvitationResponse, _Mapping]] = ..., createOrgAccountsByOrgAdminResponse: _Optional[_Union[_invitation_pb2.CreateOrgAccountsByOrgAdminResponse, _Mapping]] = ..., createConnectionInvitationResponse: _Optional[_Union[_connections_pb2.CreateConnectionInvitationResponse, _Mapping]] = ..., listConnectionInvitationsResponse: _Optional[_Union[_connections_pb2.ListConnectionInvitationsResponse, _Mapping]] = ..., updateConnectionInvitationResponse: _Optional[_Union[_connections_pb2.UpdateConnectionInvitationResponse, _Mapping]] = ..., listConnectionsResponse: _Optional[_Union[_connections_pb2.ListConnectionsResponse, _Mapping]] = ..., initiateOidcAuthorisationResponse: _Optional[_Union[_connections_pb2.InitiateOidcAuthorisationResponse, _Mapping]] = ..., completeOidcAuthorisationResponse: _Optional[_Union[_connections_pb2.CompleteOidcAuthorisationResponse, _Mapping]] = ..., revokeOidcAuthorisationResponse: _Optional[_Union[_connections_pb2.RevokeOidcAuthorisationResponse, _Mapping]] = ..., searchPublicUserResponse: _Optional[_Union[_connections_pb2.SearchPublicUserResponse, _Mapping]] = ..., createCommunityStudioResponse: _Optional[_Union[CreateCommunityStudioResponse, _Mapping]] = ..., updateCommunityStudioResponse: _Optional[_Union[UpdateCommunityStudioResponse, _Mapping]] = ..., getCommunityStudioResponse: _Optional[_Union[GetCommunityStudioResponse, _Mapping]] = ..., listCommunityStudiosResponse: _Optional[_Union[ListCommunityStudiosResponse, _Mapping]] = ..., sendSupportEmailResponse: _Optional[_Union[SendSupportEmailResponse, _Mapping]] = ..., requestCertificateResponse: _Optional[_Union[RequestCertificateResponse, _Mapping]] = ..., updateSketchObjectsResponse: _Optional[_Union[_online_sketch_pb2.UpdateSketchObjectsResponse, _Mapping]] = ..., handraiseToPaywallResponse: _Optional[_Union[HandraiseToPaywallResponse, _Mapping]] = ..., consumeDownloadAllowanceResponse: _Optional[_Union[ConsumeDownloadAllowanceResponse, _Mapping]] = ..., createSubscriptionResponse: _Optional[_Union[_profile_pb2.CreateSubscriptionResponse, _Mapping]] = ..., getSubscriptionPriceResponse: _Optional[_Union[_profile_pb2.GetSubscriptionPriceResponse, _Mapping]] = ..., getStripeCustomerPortalLinkResponse: _Optional[_Union[_profile_pb2.GetStripeCustomerPortalLinkResponse, _Mapping]] = ..., postImageToDiscordResponse: _Optional[_Union[PostImageToDiscordResponse, _Mapping]] = ..., getPublicUserProfileResponse: _Optional[_Union[GetPublicUserProfileResponse, _Mapping]] = ..., maintenanceCheckResponse: _Optional[_Union[MaintenanceCheckResponse, _Mapping]] = ..., publicCollabsSpaceId: _Optional[_Union[_gravi_model_pb2.SpaceId, _Mapping]] = ..., listPublicSpaceDocsResponse: _Optional[_Union[_doc_rest_pb2.ListPublicSpaceDocsResponse, _Mapping]] = ..., downloadPublicSpaceDocResponse: _Optional[_Union[_doc_rest_pb2.DownloadPublicSpaceDocResponse, _Mapping]] = ..., downloadOverrideConfigResponse: _Optional[_Union[DownloadOverrideConfigResponse, _Mapping]] = ..., transcribeResponse: _Optional[_Union[_transcribe_pb2.TranscribeResponse, _Mapping]] = ..., askShrekResponse: _Optional[_Union[_ask_pb2.AskShrekResponse, _Mapping]] = ..., generateImagesResponse: _Optional[_Union[_image_pb2.GenerateImagesResponse, _Mapping]] = ..., generate3DModelResponse: _Optional[_Union[_image_pb2.Generate3DModelResponse, _Mapping]] = ..., orgRequiredVersions: _Optional[_Iterable[str]] = ..., restErrorMessage: _Optional[str] = ...) -> None: ...

class ChangeUserPasswordRequest(_message.Message):
    __slots__ = ("userId", "oldPwd", "newPwd")
    USERID_FIELD_NUMBER: _ClassVar[int]
    OLDPWD_FIELD_NUMBER: _ClassVar[int]
    NEWPWD_FIELD_NUMBER: _ClassVar[int]
    userId: str
    oldPwd: bytes
    newPwd: bytes
    def __init__(self, userId: _Optional[str] = ..., oldPwd: _Optional[bytes] = ..., newPwd: _Optional[bytes] = ...) -> None: ...

class ChangeUserPasswordResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ChangeUserPasswordResponseCode
    def __init__(self, code: _Optional[_Union[ChangeUserPasswordResponseCode, str]] = ...) -> None: ...

class EarlyAdopterCheckRequest(_message.Message):
    __slots__ = ("oculusId", "oculusNonce", "oculusType", "steamTicket", "unityId")
    OCULUSID_FIELD_NUMBER: _ClassVar[int]
    OCULUSNONCE_FIELD_NUMBER: _ClassVar[int]
    OCULUSTYPE_FIELD_NUMBER: _ClassVar[int]
    STEAMTICKET_FIELD_NUMBER: _ClassVar[int]
    UNITYID_FIELD_NUMBER: _ClassVar[int]
    oculusId: int
    oculusNonce: str
    oculusType: OculusAppType
    steamTicket: str
    unityId: str
    def __init__(self, oculusId: _Optional[int] = ..., oculusNonce: _Optional[str] = ..., oculusType: _Optional[_Union[OculusAppType, str]] = ..., steamTicket: _Optional[str] = ..., unityId: _Optional[str] = ...) -> None: ...

class EarlyAdopterCheckResponse(_message.Message):
    __slots__ = ("isEarlyAdopter",)
    ISEARLYADOPTER_FIELD_NUMBER: _ClassVar[int]
    isEarlyAdopter: bool
    def __init__(self, isEarlyAdopter: bool = ...) -> None: ...

class DeleteAccountRequest(_message.Message):
    __slots__ = ("encryptedPassword", "feedbackType", "verbalFeedback")
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    FEEDBACKTYPE_FIELD_NUMBER: _ClassVar[int]
    VERBALFEEDBACK_FIELD_NUMBER: _ClassVar[int]
    encryptedPassword: bytes
    feedbackType: AccountDeletionFeedbackType
    verbalFeedback: str
    def __init__(self, encryptedPassword: _Optional[bytes] = ..., feedbackType: _Optional[_Union[AccountDeletionFeedbackType, str]] = ..., verbalFeedback: _Optional[str] = ...) -> None: ...

class DeleteAccountResponse(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: DeleteAccountResponseCode
    def __init__(self, code: _Optional[_Union[DeleteAccountResponseCode, str]] = ...) -> None: ...

class SignUpRequest(_message.Message):
    __slots__ = ("deviceInfo", "authType", "email", "userName", "encryptedPassword")
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    AUTHTYPE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    deviceInfo: _gravi_model_pb2.DeviceInfo
    authType: _login_pb2.AuthType
    email: str
    userName: str
    encryptedPassword: bytes
    def __init__(self, deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., authType: _Optional[_Union[_login_pb2.AuthType, str]] = ..., email: _Optional[str] = ..., userName: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ...) -> None: ...

class MagicLinkLoginRequest(_message.Message):
    __slots__ = ("queryCode", "email", "loginType", "reCaptchaToken", "rememberMe")
    QUERYCODE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    LOGINTYPE_FIELD_NUMBER: _ClassVar[int]
    RECAPTCHATOKEN_FIELD_NUMBER: _ClassVar[int]
    REMEMBERME_FIELD_NUMBER: _ClassVar[int]
    queryCode: str
    email: str
    loginType: MagicLinkLoginType
    reCaptchaToken: str
    rememberMe: bool
    def __init__(self, queryCode: _Optional[str] = ..., email: _Optional[str] = ..., loginType: _Optional[_Union[MagicLinkLoginType, str]] = ..., reCaptchaToken: _Optional[str] = ..., rememberMe: bool = ...) -> None: ...

class MagicLinkLoginResponse(_message.Message):
    __slots__ = ("queryCode", "resultCode", "expiryTime", "loginResponse", "newUserCreated")
    QUERYCODE_FIELD_NUMBER: _ClassVar[int]
    RESULTCODE_FIELD_NUMBER: _ClassVar[int]
    EXPIRYTIME_FIELD_NUMBER: _ClassVar[int]
    LOGINRESPONSE_FIELD_NUMBER: _ClassVar[int]
    NEWUSERCREATED_FIELD_NUMBER: _ClassVar[int]
    queryCode: str
    resultCode: MagicLinkLoginResultCode
    expiryTime: int
    loginResponse: _login_pb2.LoginResponse
    newUserCreated: bool
    def __init__(self, queryCode: _Optional[str] = ..., resultCode: _Optional[_Union[MagicLinkLoginResultCode, str]] = ..., expiryTime: _Optional[int] = ..., loginResponse: _Optional[_Union[_login_pb2.LoginResponse, _Mapping]] = ..., newUserCreated: bool = ...) -> None: ...

class SteamLoginRequest(_message.Message):
    __slots__ = ("steamTicket", "steamUserId", "deviceInfo")
    STEAMTICKET_FIELD_NUMBER: _ClassVar[int]
    STEAMUSERID_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    steamTicket: str
    steamUserId: int
    deviceInfo: _gravi_model_pb2.DeviceInfo
    def __init__(self, steamTicket: _Optional[str] = ..., steamUserId: _Optional[int] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ...) -> None: ...

class AppleLoginRequest(_message.Message):
    __slots__ = ("identityToken",)
    IDENTITYTOKEN_FIELD_NUMBER: _ClassVar[int]
    identityToken: str
    def __init__(self, identityToken: _Optional[str] = ...) -> None: ...

class AppleSignUpRequest(_message.Message):
    __slots__ = ("identityToken", "email", "encryptedPassword")
    IDENTITYTOKEN_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    identityToken: str
    email: str
    encryptedPassword: bytes
    def __init__(self, identityToken: _Optional[str] = ..., email: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ...) -> None: ...

class AppleGrsAccountLinkRequest(_message.Message):
    __slots__ = ("identityToken", "email", "encryptedPassword")
    IDENTITYTOKEN_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    identityToken: str
    email: str
    encryptedPassword: bytes
    def __init__(self, identityToken: _Optional[str] = ..., email: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ...) -> None: ...

class OculusLoginRequest(_message.Message):
    __slots__ = ("oculusUserId", "nonce", "appType", "deviceInfo")
    OCULUSUSERID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    APPTYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    oculusUserId: int
    nonce: str
    appType: OculusAppType
    deviceInfo: _gravi_model_pb2.DeviceInfo
    def __init__(self, oculusUserId: _Optional[int] = ..., nonce: _Optional[str] = ..., appType: _Optional[_Union[OculusAppType, str]] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ...) -> None: ...

class SteamSignUpRequest(_message.Message):
    __slots__ = ("steamTicket", "steamUserId", "email")
    STEAMTICKET_FIELD_NUMBER: _ClassVar[int]
    STEAMUSERID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    steamTicket: str
    steamUserId: int
    email: str
    def __init__(self, steamTicket: _Optional[str] = ..., steamUserId: _Optional[int] = ..., email: _Optional[str] = ...) -> None: ...

class OculusSignUpRequest(_message.Message):
    __slots__ = ("oculusUserId", "nonce", "appType", "email")
    OCULUSUSERID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    APPTYPE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    oculusUserId: int
    nonce: str
    appType: OculusAppType
    email: str
    def __init__(self, oculusUserId: _Optional[int] = ..., nonce: _Optional[str] = ..., appType: _Optional[_Union[OculusAppType, str]] = ..., email: _Optional[str] = ...) -> None: ...

class StoreSignUpResponse(_message.Message):
    __slots__ = ("queryToken", "orgLicensePass", "expiryTime", "code")
    QUERYTOKEN_FIELD_NUMBER: _ClassVar[int]
    ORGLICENSEPASS_FIELD_NUMBER: _ClassVar[int]
    EXPIRYTIME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    queryToken: str
    orgLicensePass: bytes
    expiryTime: int
    code: SignUpResponseCode
    def __init__(self, queryToken: _Optional[str] = ..., orgLicensePass: _Optional[bytes] = ..., expiryTime: _Optional[int] = ..., code: _Optional[_Union[SignUpResponseCode, str]] = ...) -> None: ...

class SteamEmailAccountLinkRequest(_message.Message):
    __slots__ = ("steamTicket", "steamUserId", "deviceInfo", "email", "encryptedPassword", "forceUnlink")
    STEAMTICKET_FIELD_NUMBER: _ClassVar[int]
    STEAMUSERID_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    FORCEUNLINK_FIELD_NUMBER: _ClassVar[int]
    steamTicket: str
    steamUserId: int
    deviceInfo: _gravi_model_pb2.DeviceInfo
    email: str
    encryptedPassword: bytes
    forceUnlink: bool
    def __init__(self, steamTicket: _Optional[str] = ..., steamUserId: _Optional[int] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., email: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ..., forceUnlink: bool = ...) -> None: ...

class OculusEmailAccountLinkRequest(_message.Message):
    __slots__ = ("oculusUserId", "nonce", "appType", "deviceInfo", "email", "encryptedPassword", "forceUnlink")
    OCULUSUSERID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    APPTYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICEINFO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASSWORD_FIELD_NUMBER: _ClassVar[int]
    FORCEUNLINK_FIELD_NUMBER: _ClassVar[int]
    oculusUserId: int
    nonce: str
    appType: OculusAppType
    deviceInfo: _gravi_model_pb2.DeviceInfo
    email: str
    encryptedPassword: bytes
    forceUnlink: bool
    def __init__(self, oculusUserId: _Optional[int] = ..., nonce: _Optional[str] = ..., appType: _Optional[_Union[OculusAppType, str]] = ..., deviceInfo: _Optional[_Union[_gravi_model_pb2.DeviceInfo, _Mapping]] = ..., email: _Optional[str] = ..., encryptedPassword: _Optional[bytes] = ..., forceUnlink: bool = ...) -> None: ...

class EmailAccountLinkResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EmailAccountLinkResult
    def __init__(self, result: _Optional[_Union[EmailAccountLinkResult, str]] = ...) -> None: ...

class LoginByOneTimeAuthTokenRequest(_message.Message):
    __slots__ = ("oneTimeToken",)
    ONETIMETOKEN_FIELD_NUMBER: _ClassVar[int]
    oneTimeToken: str
    def __init__(self, oneTimeToken: _Optional[str] = ...) -> None: ...

class GetPublicKeyResponse(_message.Message):
    __slots__ = ("modulusBase64", "exponentBase64")
    MODULUSBASE64_FIELD_NUMBER: _ClassVar[int]
    EXPONENTBASE64_FIELD_NUMBER: _ClassVar[int]
    modulusBase64: str
    exponentBase64: str
    def __init__(self, modulusBase64: _Optional[str] = ..., exponentBase64: _Optional[str] = ...) -> None: ...

class GetCMSURLResponse(_message.Message):
    __slots__ = ("cmsUrl",)
    CMSURL_FIELD_NUMBER: _ClassVar[int]
    cmsUrl: str
    def __init__(self, cmsUrl: _Optional[str] = ...) -> None: ...

class AttachEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class AttachEmailResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: AttachEmailResult
    def __init__(self, result: _Optional[_Union[AttachEmailResult, str]] = ...) -> None: ...

class LaunchRoomRequest(_message.Message):
    __slots__ = ("roomId", "isSharedRoom", "expectedGrsVersion")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    EXPECTEDGRSVERSION_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    isSharedRoom: bool
    expectedGrsVersion: int
    def __init__(self, roomId: _Optional[str] = ..., isSharedRoom: bool = ..., expectedGrsVersion: _Optional[int] = ...) -> None: ...

class LaunchRoomResponse(_message.Message):
    __slots__ = ("code", "whereByRoomLink")
    CODE_FIELD_NUMBER: _ClassVar[int]
    WHEREBYROOMLINK_FIELD_NUMBER: _ClassVar[int]
    code: LaunchRoomResponseCode
    whereByRoomLink: str
    def __init__(self, code: _Optional[_Union[LaunchRoomResponseCode, str]] = ..., whereByRoomLink: _Optional[str] = ...) -> None: ...

class EnterRoomRequest(_message.Message):
    __slots__ = ("roomId", "grsVersion", "isSharedRoom", "password")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    GRSVERSION_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    grsVersion: int
    isSharedRoom: bool
    password: str
    def __init__(self, roomId: _Optional[str] = ..., grsVersion: _Optional[int] = ..., isSharedRoom: bool = ..., password: _Optional[str] = ...) -> None: ...

class EnterRoomResponse(_message.Message):
    __slots__ = ("roomId", "roomName", "minimumClientVersion", "ticket", "permissions", "coSketchProtocol", "failIfCertificateInvalid", "clientId", "instanceAddress", "instanceTcpPort", "instanceWebSocketPort", "result", "entityId", "roomSessionId", "instanceVoiceRelayTcpPort", "doc", "gatewayAddress", "gatewayPort", "heartBeatEnabled")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMNAME_FIELD_NUMBER: _ClassVar[int]
    MINIMUMCLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    COSKETCHPROTOCOL_FIELD_NUMBER: _ClassVar[int]
    FAILIFCERTIFICATEINVALID_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    INSTANCEADDRESS_FIELD_NUMBER: _ClassVar[int]
    INSTANCETCPPORT_FIELD_NUMBER: _ClassVar[int]
    INSTANCEWEBSOCKETPORT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ENTITYID_FIELD_NUMBER: _ClassVar[int]
    ROOMSESSIONID_FIELD_NUMBER: _ClassVar[int]
    INSTANCEVOICERELAYTCPPORT_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    GATEWAYADDRESS_FIELD_NUMBER: _ClassVar[int]
    GATEWAYPORT_FIELD_NUMBER: _ClassVar[int]
    HEARTBEATENABLED_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    roomName: str
    minimumClientVersion: str
    ticket: _gravi_model_pb2.CoSketchTicket
    permissions: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.CollaborationPermission]
    coSketchProtocol: str
    failIfCertificateInvalid: bool
    clientId: int
    instanceAddress: str
    instanceTcpPort: int
    instanceWebSocketPort: int
    result: EnterRoomResult
    entityId: int
    roomSessionId: str
    instanceVoiceRelayTcpPort: int
    doc: _gravi_model_pb2.DocumentTO
    gatewayAddress: str
    gatewayPort: int
    heartBeatEnabled: bool
    def __init__(self, roomId: _Optional[str] = ..., roomName: _Optional[str] = ..., minimumClientVersion: _Optional[str] = ..., ticket: _Optional[_Union[_gravi_model_pb2.CoSketchTicket, _Mapping]] = ..., permissions: _Optional[_Iterable[_Union[_gravi_model_pb2.CollaborationPermission, str]]] = ..., coSketchProtocol: _Optional[str] = ..., failIfCertificateInvalid: bool = ..., clientId: _Optional[int] = ..., instanceAddress: _Optional[str] = ..., instanceTcpPort: _Optional[int] = ..., instanceWebSocketPort: _Optional[int] = ..., result: _Optional[_Union[EnterRoomResult, str]] = ..., entityId: _Optional[int] = ..., roomSessionId: _Optional[str] = ..., instanceVoiceRelayTcpPort: _Optional[int] = ..., doc: _Optional[_Union[_gravi_model_pb2.DocumentTO, _Mapping]] = ..., gatewayAddress: _Optional[str] = ..., gatewayPort: _Optional[int] = ..., heartBeatEnabled: bool = ...) -> None: ...

class ShutdownRoomRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class ShutdownRoomResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ShutdownRoomResult
    def __init__(self, result: _Optional[_Union[ShutdownRoomResult, str]] = ...) -> None: ...

class ReleaseRoomInitLockRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class InviteUsersToCollabRequest(_message.Message):
    __slots__ = ("docId", "userIds", "oculusIds", "rolesToInviteAs")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    USERIDS_FIELD_NUMBER: _ClassVar[int]
    OCULUSIDS_FIELD_NUMBER: _ClassVar[int]
    ROLESTOINVITEAS_FIELD_NUMBER: _ClassVar[int]
    docId: str
    userIds: _containers.RepeatedScalarFieldContainer[str]
    oculusIds: _containers.RepeatedScalarFieldContainer[int]
    rolesToInviteAs: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.CollaborationRole]
    def __init__(self, docId: _Optional[str] = ..., userIds: _Optional[_Iterable[str]] = ..., oculusIds: _Optional[_Iterable[int]] = ..., rolesToInviteAs: _Optional[_Iterable[_Union[_gravi_model_pb2.CollaborationRole, str]]] = ...) -> None: ...

class InviteUsersToCollabResponse(_message.Message):
    __slots__ = ("code", "oculusIdsWithoutAccounts")
    CODE_FIELD_NUMBER: _ClassVar[int]
    OCULUSIDSWITHOUTACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    code: InviteUsersToCollabResponseCode
    oculusIdsWithoutAccounts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, code: _Optional[_Union[InviteUsersToCollabResponseCode, str]] = ..., oculusIdsWithoutAccounts: _Optional[_Iterable[int]] = ...) -> None: ...

class ListInvitableUsersRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class ListInvitableUsersResponse(_message.Message):
    __slots__ = ("invitableUsers",)
    INVITABLEUSERS_FIELD_NUMBER: _ClassVar[int]
    invitableUsers: _containers.RepeatedCompositeFieldContainer[InvitableUserInfo]
    def __init__(self, invitableUsers: _Optional[_Iterable[_Union[InvitableUserInfo, _Mapping]]] = ...) -> None: ...

class EnterRoomWithDeepLinkRequest(_message.Message):
    __slots__ = ("deepLink", "grsVersion", "password")
    DEEPLINK_FIELD_NUMBER: _ClassVar[int]
    GRSVERSION_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    deepLink: str
    grsVersion: int
    password: str
    def __init__(self, deepLink: _Optional[str] = ..., grsVersion: _Optional[int] = ..., password: _Optional[str] = ...) -> None: ...

class InvitableUserInfo(_message.Message):
    __slots__ = ("userId", "username")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    userId: str
    username: str
    def __init__(self, userId: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class DeletePersistedRoomRequest(_message.Message):
    __slots__ = ("roomId",)
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    def __init__(self, roomId: _Optional[str] = ...) -> None: ...

class DeletePersistedRoomResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: DeletePersistedRoomResult
    def __init__(self, result: _Optional[_Union[DeletePersistedRoomResult, str]] = ...) -> None: ...

class GetLoggedInUserRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class GetLoggedInUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _gravi_model_pb2.UserTO
    def __init__(self, user: _Optional[_Union[_gravi_model_pb2.UserTO, _Mapping]] = ...) -> None: ...

class GetLoggedInUserOrgInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLoggedInUserOrgInfoResponse(_message.Message):
    __slots__ = ("currentOrgId", "belongToOrgs")
    CURRENTORGID_FIELD_NUMBER: _ClassVar[int]
    BELONGTOORGS_FIELD_NUMBER: _ClassVar[int]
    currentOrgId: str
    belongToOrgs: _containers.RepeatedCompositeFieldContainer[_management_pb2.OrganizationTO]
    def __init__(self, currentOrgId: _Optional[str] = ..., belongToOrgs: _Optional[_Iterable[_Union[_management_pb2.OrganizationTO, _Mapping]]] = ...) -> None: ...

class GetSubscriptionPackRequest(_message.Message):
    __slots__ = ("currentOrgId",)
    CURRENTORGID_FIELD_NUMBER: _ClassVar[int]
    currentOrgId: str
    def __init__(self, currentOrgId: _Optional[str] = ...) -> None: ...

class GetSubscriptionPackResponse(_message.Message):
    __slots__ = ("subscriptionPack",)
    SUBSCRIPTIONPACK_FIELD_NUMBER: _ClassVar[int]
    subscriptionPack: _gravi_model_pb2.SubscriptionPackTO
    def __init__(self, subscriptionPack: _Optional[_Union[_gravi_model_pb2.SubscriptionPackTO, _Mapping]] = ...) -> None: ...

class ConsumeNotificationRequest(_message.Message):
    __slots__ = ("notificationId",)
    NOTIFICATIONID_FIELD_NUMBER: _ClassVar[int]
    notificationId: str
    def __init__(self, notificationId: _Optional[str] = ...) -> None: ...

class ConsumeNotificationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNotificationsForLoggedInUserRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNotificationsForLoggedInUserResponse(_message.Message):
    __slots__ = ("notifications",)
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    notifications: _containers.RepeatedCompositeFieldContainer[_notifications_pb2.NotificationTO]
    def __init__(self, notifications: _Optional[_Iterable[_Union[_notifications_pb2.NotificationTO, _Mapping]]] = ...) -> None: ...

class SendBetaSignupEmailRequest(_message.Message):
    __slots__ = ("betaEmailType",)
    BETAEMAILTYPE_FIELD_NUMBER: _ClassVar[int]
    betaEmailType: BetaEmailType
    def __init__(self, betaEmailType: _Optional[_Union[BetaEmailType, str]] = ...) -> None: ...

class SendBetaSignupEmailResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DetachDeviceRequest(_message.Message):
    __slots__ = ("detachDeviceType",)
    DETACHDEVICETYPE_FIELD_NUMBER: _ClassVar[int]
    detachDeviceType: _auth_pb2.DetachDeviceType
    def __init__(self, detachDeviceType: _Optional[_Union[_auth_pb2.DetachDeviceType, str]] = ...) -> None: ...

class DetachDeviceResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ResendStoreSignupEmailRequest(_message.Message):
    __slots__ = ("queryToken", "type")
    QUERYTOKEN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    queryToken: str
    type: ResendStoreSignupType
    def __init__(self, queryToken: _Optional[str] = ..., type: _Optional[_Union[ResendStoreSignupType, str]] = ...) -> None: ...

class ResendStoreSignupEmailResponse(_message.Message):
    __slots__ = ("result", "expiryTime")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EXPIRYTIME_FIELD_NUMBER: _ClassVar[int]
    result: ResendStoreSignupEmailResult
    expiryTime: int
    def __init__(self, result: _Optional[_Union[ResendStoreSignupEmailResult, str]] = ..., expiryTime: _Optional[int] = ...) -> None: ...

class InvalidateSignupLinkRequest(_message.Message):
    __slots__ = ("queryToken",)
    QUERYTOKEN_FIELD_NUMBER: _ClassVar[int]
    queryToken: str
    def __init__(self, queryToken: _Optional[str] = ...) -> None: ...

class OfflineUserTrace(_message.Message):
    __slots__ = ("traceId", "oculusQuestUserId", "oculusRiftUserId", "steamTicket", "steamUserId", "unityId")
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    OCULUSQUESTUSERID_FIELD_NUMBER: _ClassVar[int]
    OCULUSRIFTUSERID_FIELD_NUMBER: _ClassVar[int]
    STEAMTICKET_FIELD_NUMBER: _ClassVar[int]
    STEAMUSERID_FIELD_NUMBER: _ClassVar[int]
    UNITYID_FIELD_NUMBER: _ClassVar[int]
    traceId: str
    oculusQuestUserId: int
    oculusRiftUserId: int
    steamTicket: str
    steamUserId: int
    unityId: str
    def __init__(self, traceId: _Optional[str] = ..., oculusQuestUserId: _Optional[int] = ..., oculusRiftUserId: _Optional[int] = ..., steamTicket: _Optional[str] = ..., steamUserId: _Optional[int] = ..., unityId: _Optional[str] = ...) -> None: ...

class OfflineUserTraceResponse(_message.Message):
    __slots__ = ("traceId",)
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    traceId: str
    def __init__(self, traceId: _Optional[str] = ...) -> None: ...

class SyncAchievementRequest(_message.Message):
    __slots__ = ("achievement",)
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    achievement: _achievement_pb2.AchievementRecord
    def __init__(self, achievement: _Optional[_Union[_achievement_pb2.AchievementRecord, _Mapping]] = ...) -> None: ...

class GetAchievementsResponse(_message.Message):
    __slots__ = ("achievement",)
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    achievement: _containers.RepeatedCompositeFieldContainer[_achievement_pb2.AchievementRecord]
    def __init__(self, achievement: _Optional[_Iterable[_Union[_achievement_pb2.AchievementRecord, _Mapping]]] = ...) -> None: ...

class LogoutRequest(_message.Message):
    __slots__ = ("releaseTicketOnly",)
    RELEASETICKETONLY_FIELD_NUMBER: _ClassVar[int]
    releaseTicketOnly: bool
    def __init__(self, releaseTicketOnly: bool = ...) -> None: ...

class ListRoomRecordingsRequest(_message.Message):
    __slots__ = ("roomId", "lastRecordingId", "isSharedRoom")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    LASTRECORDINGID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    lastRecordingId: str
    isSharedRoom: bool
    def __init__(self, roomId: _Optional[str] = ..., lastRecordingId: _Optional[str] = ..., isSharedRoom: bool = ...) -> None: ...

class ListRoomRecordingsResponse(_message.Message):
    __slots__ = ("recordings", "lastRecordingId")
    RECORDINGS_FIELD_NUMBER: _ClassVar[int]
    LASTRECORDINGID_FIELD_NUMBER: _ClassVar[int]
    recordings: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.CoSketchRecordingTO]
    lastRecordingId: str
    def __init__(self, recordings: _Optional[_Iterable[_Union[_gravi_model_pb2.CoSketchRecordingTO, _Mapping]]] = ..., lastRecordingId: _Optional[str] = ...) -> None: ...

class ReplayRoomRecordingRequest(_message.Message):
    __slots__ = ("ownerId", "recordingId", "isSharedRoom")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    RECORDINGID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    recordingId: str
    isSharedRoom: bool
    def __init__(self, ownerId: _Optional[str] = ..., recordingId: _Optional[str] = ..., isSharedRoom: bool = ...) -> None: ...

class ReplayRoomRecordingResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ReplayRecordingResult
    def __init__(self, result: _Optional[_Union[ReplayRecordingResult, str]] = ...) -> None: ...

class GetRoomRecordingRequest(_message.Message):
    __slots__ = ("ownerId", "recordingId", "isSharedRoom")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    RECORDINGID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    recordingId: str
    isSharedRoom: bool
    def __init__(self, ownerId: _Optional[str] = ..., recordingId: _Optional[str] = ..., isSharedRoom: bool = ...) -> None: ...

class GetRoomRecordingResponse(_message.Message):
    __slots__ = ("recording",)
    RECORDING_FIELD_NUMBER: _ClassVar[int]
    recording: _gravi_model_pb2.CoSketchRecordingTO
    def __init__(self, recording: _Optional[_Union[_gravi_model_pb2.CoSketchRecordingTO, _Mapping]] = ...) -> None: ...

class GetRoomRecordingReplayDataRequest(_message.Message):
    __slots__ = ("ownerId", "recordingId", "replayNum", "isSharedRoom")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    RECORDINGID_FIELD_NUMBER: _ClassVar[int]
    REPLAYNUM_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    recordingId: str
    replayNum: int
    isSharedRoom: bool
    def __init__(self, ownerId: _Optional[str] = ..., recordingId: _Optional[str] = ..., replayNum: _Optional[int] = ..., isSharedRoom: bool = ...) -> None: ...

class GetRoomRecordingReplayDataResponse(_message.Message):
    __slots__ = ("downloadUrl",)
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    downloadUrl: str
    def __init__(self, downloadUrl: _Optional[str] = ...) -> None: ...

class GetRoomRecordingReplayAssetsRequest(_message.Message):
    __slots__ = ("ownerId", "recordingId", "isSharedRoom")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    RECORDINGID_FIELD_NUMBER: _ClassVar[int]
    ISSHAREDROOM_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    recordingId: str
    isSharedRoom: bool
    def __init__(self, ownerId: _Optional[str] = ..., recordingId: _Optional[str] = ..., isSharedRoom: bool = ...) -> None: ...

class GetRoomRecordingReplayAssetsResponse(_message.Message):
    __slots__ = ("downloadUrls",)
    DOWNLOADURLS_FIELD_NUMBER: _ClassVar[int]
    downloadUrls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, downloadUrls: _Optional[_Iterable[str]] = ...) -> None: ...

class GetPublicUserProfileRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class GetPublicUserProfileResponse(_message.Message):
    __slots__ = ("userDisplayName", "userStats", "badges", "userInfo", "result")
    USERDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    USERSTATS_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    userDisplayName: str
    userStats: _gravi_model_pb2.UserStatsTO
    badges: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.UserBadge]
    userInfo: _gravi_model_pb2.UserPublicTO
    result: GetPublicUserProfileResult
    def __init__(self, userDisplayName: _Optional[str] = ..., userStats: _Optional[_Union[_gravi_model_pb2.UserStatsTO, _Mapping]] = ..., badges: _Optional[_Iterable[_Union[_gravi_model_pb2.UserBadge, str]]] = ..., userInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ..., result: _Optional[_Union[GetPublicUserProfileResult, str]] = ...) -> None: ...

class GetOrgRequest(_message.Message):
    __slots__ = ("orgId",)
    ORGID_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    def __init__(self, orgId: _Optional[str] = ...) -> None: ...

class GetOrgResponse(_message.Message):
    __slots__ = ("name", "seats", "priceTier", "licenseExpiryOn", "openToEmailDns", "emailWhitelist", "seatsUsed", "secPolicyMfaEnforcement", "org", "code")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEATS_FIELD_NUMBER: _ClassVar[int]
    PRICETIER_FIELD_NUMBER: _ClassVar[int]
    LICENSEEXPIRYON_FIELD_NUMBER: _ClassVar[int]
    OPENTOEMAILDNS_FIELD_NUMBER: _ClassVar[int]
    EMAILWHITELIST_FIELD_NUMBER: _ClassVar[int]
    SEATSUSED_FIELD_NUMBER: _ClassVar[int]
    SECPOLICYMFAENFORCEMENT_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    name: str
    seats: int
    priceTier: _gravi_model_pb2.PriceTier
    licenseExpiryOn: int
    openToEmailDns: bool
    emailWhitelist: _containers.RepeatedScalarFieldContainer[str]
    seatsUsed: int
    secPolicyMfaEnforcement: bool
    org: _management_pb2.OrganizationTO
    code: GetOrgResponseCode
    def __init__(self, name: _Optional[str] = ..., seats: _Optional[int] = ..., priceTier: _Optional[_Union[_gravi_model_pb2.PriceTier, str]] = ..., licenseExpiryOn: _Optional[int] = ..., openToEmailDns: bool = ..., emailWhitelist: _Optional[_Iterable[str]] = ..., seatsUsed: _Optional[int] = ..., secPolicyMfaEnforcement: bool = ..., org: _Optional[_Union[_management_pb2.OrganizationTO, _Mapping]] = ..., code: _Optional[_Union[GetOrgResponseCode, str]] = ...) -> None: ...

class PostImageToDiscordRequest(_message.Message):
    __slots__ = ("discordPostMessage", "discordPostImageData", "discordChannel")
    DISCORDPOSTMESSAGE_FIELD_NUMBER: _ClassVar[int]
    DISCORDPOSTIMAGEDATA_FIELD_NUMBER: _ClassVar[int]
    DISCORDCHANNEL_FIELD_NUMBER: _ClassVar[int]
    discordPostMessage: str
    discordPostImageData: bytes
    discordChannel: DiscordChannelType
    def __init__(self, discordPostMessage: _Optional[str] = ..., discordPostImageData: _Optional[bytes] = ..., discordChannel: _Optional[_Union[DiscordChannelType, str]] = ...) -> None: ...

class PostImageToDiscordResponse(_message.Message):
    __slots__ = ("responseCode",)
    RESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    responseCode: PostImageToDiscordResponseCode
    def __init__(self, responseCode: _Optional[_Union[PostImageToDiscordResponseCode, str]] = ...) -> None: ...

class CreateVoiceToTextUrlRequest(_message.Message):
    __slots__ = ("audioFileType", "audioBitRate")
    AUDIOFILETYPE_FIELD_NUMBER: _ClassVar[int]
    AUDIOBITRATE_FIELD_NUMBER: _ClassVar[int]
    audioFileType: str
    audioBitRate: str
    def __init__(self, audioFileType: _Optional[str] = ..., audioBitRate: _Optional[str] = ...) -> None: ...

class CreateVoiceToTextUrlResponse(_message.Message):
    __slots__ = ("url", "result")
    URL_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    url: str
    result: CreateVoiceToTextUrlResult
    def __init__(self, url: _Optional[str] = ..., result: _Optional[_Union[CreateVoiceToTextUrlResult, str]] = ...) -> None: ...

class MaintenanceCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MaintenanceCheckResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateCommunityStudioRequest(_message.Message):
    __slots__ = ("displayName", "description")
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    displayName: str
    description: str
    def __init__(self, displayName: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateCommunityStudioResponse(_message.Message):
    __slots__ = ("studio",)
    STUDIO_FIELD_NUMBER: _ClassVar[int]
    studio: _gravi_model_pb2.CommunityStudio
    def __init__(self, studio: _Optional[_Union[_gravi_model_pb2.CommunityStudio, _Mapping]] = ...) -> None: ...

class UpdateCommunityStudioRequest(_message.Message):
    __slots__ = ("studioId", "emailsToAdd", "rolesToAdd", "userIdsToRemove")
    STUDIOID_FIELD_NUMBER: _ClassVar[int]
    EMAILSTOADD_FIELD_NUMBER: _ClassVar[int]
    ROLESTOADD_FIELD_NUMBER: _ClassVar[int]
    USERIDSTOREMOVE_FIELD_NUMBER: _ClassVar[int]
    studioId: str
    emailsToAdd: _containers.RepeatedScalarFieldContainer[str]
    rolesToAdd: _containers.RepeatedScalarFieldContainer[_gravi_model_pb2.CommunityStudioRole]
    userIdsToRemove: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, studioId: _Optional[str] = ..., emailsToAdd: _Optional[_Iterable[str]] = ..., rolesToAdd: _Optional[_Iterable[_Union[_gravi_model_pb2.CommunityStudioRole, str]]] = ..., userIdsToRemove: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateCommunityStudioResponse(_message.Message):
    __slots__ = ("studio", "code")
    STUDIO_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    studio: _gravi_model_pb2.CommunityStudio
    code: UpdateCommunityStudioResponseCode
    def __init__(self, studio: _Optional[_Union[_gravi_model_pb2.CommunityStudio, _Mapping]] = ..., code: _Optional[_Union[UpdateCommunityStudioResponseCode, str]] = ...) -> None: ...

class GetCommunityStudioRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCommunityStudioResponse(_message.Message):
    __slots__ = ("studio",)
    STUDIO_FIELD_NUMBER: _ClassVar[int]
    studio: _gravi_model_pb2.CommunityStudio
    def __init__(self, studio: _Optional[_Union[_gravi_model_pb2.CommunityStudio, _Mapping]] = ...) -> None: ...

class ListCommunityStudiosRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCommunityStudiosResponse(_message.Message):
    __slots__ = ("studios",)
    STUDIOS_FIELD_NUMBER: _ClassVar[int]
    studios: _containers.RepeatedCompositeFieldContainer[_gravi_model_pb2.CommunityStudio]
    def __init__(self, studios: _Optional[_Iterable[_Union[_gravi_model_pb2.CommunityStudio, _Mapping]]] = ...) -> None: ...

class SendSupportEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class SendSupportEmailResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RequestCertificateRequest(_message.Message):
    __slots__ = ("courseName",)
    COURSENAME_FIELD_NUMBER: _ClassVar[int]
    courseName: str
    def __init__(self, courseName: _Optional[str] = ...) -> None: ...

class RequestCertificateResponse(_message.Message):
    __slots__ = ("requestCertificateResponseCode",)
    REQUESTCERTIFICATERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    requestCertificateResponseCode: RequestCertificateResponseCode
    def __init__(self, requestCertificateResponseCode: _Optional[_Union[RequestCertificateResponseCode, str]] = ...) -> None: ...

class HandraiseToPaywallRequest(_message.Message):
    __slots__ = ("paywall", "type")
    PAYWALL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    paywall: _gravi_model_pb2.PaywallType
    type: HandraiseToPaywallRequestType
    def __init__(self, paywall: _Optional[_Union[_gravi_model_pb2.PaywallType, str]] = ..., type: _Optional[_Union[HandraiseToPaywallRequestType, str]] = ...) -> None: ...

class HandraiseToPaywallResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ConsumeDownloadAllowanceRequest(_message.Message):
    __slots__ = ("allowanceToConsume", "versionToLock")
    ALLOWANCETOCONSUME_FIELD_NUMBER: _ClassVar[int]
    VERSIONTOLOCK_FIELD_NUMBER: _ClassVar[int]
    allowanceToConsume: int
    versionToLock: str
    def __init__(self, allowanceToConsume: _Optional[int] = ..., versionToLock: _Optional[str] = ...) -> None: ...

class ConsumeDownloadAllowanceResponse(_message.Message):
    __slots__ = ("code", "currentAllowance", "currentAllowanceVersion")
    CODE_FIELD_NUMBER: _ClassVar[int]
    CURRENTALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENTALLOWANCEVERSION_FIELD_NUMBER: _ClassVar[int]
    code: ConsumeDownloadAllowanceResponseCode
    currentAllowance: int
    currentAllowanceVersion: str
    def __init__(self, code: _Optional[_Union[ConsumeDownloadAllowanceResponseCode, str]] = ..., currentAllowance: _Optional[int] = ..., currentAllowanceVersion: _Optional[str] = ...) -> None: ...

class DownloadOverrideConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _gravi_model_pb2.ServerControlledConfig
    def __init__(self, config: _Optional[_Union[_gravi_model_pb2.ServerControlledConfig, _Mapping]] = ...) -> None: ...
