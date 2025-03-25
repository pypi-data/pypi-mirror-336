from gravi.common import gravi_common_pb2 as _gravi_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PriceTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unused: _ClassVar[PriceTier]
    EarlyAdopter: _ClassVar[PriceTier]
    Pro: _ClassVar[PriceTier]
    Studio: _ClassVar[PriceTier]
    Enterprise: _ClassVar[PriceTier]
    Freemium: _ClassVar[PriceTier]

class ConnectionInvitationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ConnectionInvitationStatusPending: _ClassVar[ConnectionInvitationStatus]
    ConnectionInvitationStatusAccepted: _ClassVar[ConnectionInvitationStatus]
    ConnectionInvitationStatusRejected: _ClassVar[ConnectionInvitationStatus]

class CoSketchRoomStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RoomStatusUnknown: _ClassVar[CoSketchRoomStatus]
    RoomStatusNotLive: _ClassVar[CoSketchRoomStatus]
    RoomStatusLoading: _ClassVar[CoSketchRoomStatus]
    RoomStatusReady: _ClassVar[CoSketchRoomStatus]
    RoomStatusShuttingDown: _ClassVar[CoSketchRoomStatus]

class IdType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UserId: _ClassVar[IdType]
    OrgTeamId: _ClassVar[IdType]
    OrgId: _ClassVar[IdType]
    Community: _ClassVar[IdType]

class EnvironmentColorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EnvironmentFlat: _ClassVar[EnvironmentColorType]
    EnvironmentGradient: _ClassVar[EnvironmentColorType]

class LightTransformSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LightTransformSpaceNone: _ClassVar[LightTransformSpace]
    LightTransformSpaceSketch: _ClassVar[LightTransformSpace]
    LightTransformSpaceWorld: _ClassVar[LightTransformSpace]

class EnvironmentPreset(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EnvironmentPresetUndefined: _ClassVar[EnvironmentPreset]
    EnvironmentPresetGreyRoom: _ClassVar[EnvironmentPreset]
    EnvironmentPresetBlackRoom: _ClassVar[EnvironmentPreset]
    EnvironmentPresetWarehouse: _ClassVar[EnvironmentPreset]
    EnvironmentPresetStudio: _ClassVar[EnvironmentPreset]
    EnvironmentPresetCustom: _ClassVar[EnvironmentPreset]
    DeprecatedEnvironmentPresetXREnvironment: _ClassVar[EnvironmentPreset]
    EnvironmentPresetEmptyScene: _ClassVar[EnvironmentPreset]
    EnvironmentPresetGumdrop: _ClassVar[EnvironmentPreset]
    EnvironmentPresetLobby: _ClassVar[EnvironmentPreset]

class EnvironmentScene(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Empty: _ClassVar[EnvironmentScene]
    InfinitePlane: _ClassVar[EnvironmentScene]
    BlackGrid: _ClassVar[EnvironmentScene]
    Warehouse: _ClassVar[EnvironmentScene]
    ReflectionSkybox: _ClassVar[EnvironmentScene]
    ConfigurableEnvironment: _ClassVar[EnvironmentScene]
    Gumdrop: _ClassVar[EnvironmentScene]
    Lobby: _ClassVar[EnvironmentScene]
    ProceduralSky: _ClassVar[EnvironmentScene]

class EnvironmentBackgroundSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FlatColorBackground: _ClassVar[EnvironmentBackgroundSetting]
    GradientColorBackground: _ClassVar[EnvironmentBackgroundSetting]
    HDRBackground: _ClassVar[EnvironmentBackgroundSetting]

class EnvironmentReflectionSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoReflections: _ClassVar[EnvironmentReflectionSetting]
    BackgroundReflections: _ClassVar[EnvironmentReflectionSetting]
    ColorReflections: _ClassVar[EnvironmentReflectionSetting]
    CustomHDRReflections: _ClassVar[EnvironmentReflectionSetting]
    ZebraReflections: _ClassVar[EnvironmentReflectionSetting]

class UserBadge(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UserBadgeUnknown: _ClassVar[UserBadge]
    UserBadgeEarlyAdopter: _ClassVar[UserBadge]
    UserBadgeStudentAmbassador: _ClassVar[UserBadge]
    UserBadgeTrainedInstructor: _ClassVar[UserBadge]

class PublicProfileStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PublicProfileStatus_Default: _ClassVar[PublicProfileStatus]
    PublicProfileStatus_Public: _ClassVar[PublicProfileStatus]
    PublicProfileStatus_Private: _ClassVar[PublicProfileStatus]

class OrgMemberRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgMemberRoleStandard: _ClassVar[OrgMemberRole]
    OrgMemberRoleAdmin: _ClassVar[OrgMemberRole]
    OrgMemberRoleCoordinator: _ClassVar[OrgMemberRole]
    OrgMemberRoleReviewer: _ClassVar[OrgMemberRole]
    OrgMemberRoleViewer: _ClassVar[OrgMemberRole]
    OrgMemberScreenCollabTrial: _ClassVar[OrgMemberRole]
    OrgMemberGSConsultant: _ClassVar[OrgMemberRole]
    OrgMemberRoleReviewerAdmin: _ClassVar[OrgMemberRole]
    OrgMemberRoleViewerAdmin: _ClassVar[OrgMemberRole]
    OrgMemberScreenCollabTrialAdmin: _ClassVar[OrgMemberRole]

class OrgLicenseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgLicenseType_Unknown: _ClassVar[OrgLicenseType]
    OrgLicenseType_Creation: _ClassVar[OrgLicenseType]
    OrgLicenseType_Trainer: _ClassVar[OrgLicenseType]
    OrgLicenseType_Coordination: _ClassVar[OrgLicenseType]
    OrgLicenseType_ScreenTrial: _ClassVar[OrgLicenseType]
    OrgLicenseType_Review: _ClassVar[OrgLicenseType]
    OrgLicenseType_View: _ClassVar[OrgLicenseType]

class OrgRoleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgRoleType_Unknown: _ClassVar[OrgRoleType]
    OrgRoleType_Member: _ClassVar[OrgRoleType]
    OrgRoleType_Admin: _ClassVar[OrgRoleType]

class OrgMemberStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgMemberStatusDeactivated: _ClassVar[OrgMemberStatus]
    OrgMemberStatusActivated: _ClassVar[OrgMemberStatus]
    OrgMemberStatusDeleted: _ClassVar[OrgMemberStatus]

class CommunityStudioRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CommunityStudioRoleUnset: _ClassVar[CommunityStudioRole]
    CommunityStudioRoleMember: _ClassVar[CommunityStudioRole]
    CommunityStudioRoleMaintainer: _ClassVar[CommunityStudioRole]

class DataLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Any: _ClassVar[DataLocation]
    EU: _ClassVar[DataLocation]
    US: _ClassVar[DataLocation]

class SubscriptionFeatureFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SubscriptionFeatureFlagUnused: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagShareRoomWithExternalUser: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagTrafficRecording: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagNoScreenshotWatermark: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagMiniTrafficRecording: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagTeamSpace: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCoSketchReplay: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCloudLogger: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagDebugFileLogger: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlag2dApp: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagDisableCloudStorage: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagVoiceToText: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagInternalDevTools: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagGrandUnification: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagInviteToCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagScripting: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagJoinerRequest: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagAprilFools2025: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagSocialConnections: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagTrashedAndExpiringDocsEmailDigest: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCollabHearbeat: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEduCertTutorials: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagShareRoomWithinOrg: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagDebugUserAccount: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagUseNon443GatewayPort: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagFBXRoundTrip: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEnablePaywall: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagJailbreakCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagIngressToCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagJailbreakScreenCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagJailbreakDownload: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCrossSectionTool: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagRefLibFolderNameAndStructureChanged: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagLayerGrouping: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagOnlineSketch: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagExternalTeams: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCollapseMyWorkspaceAndMyFiles: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEnableCollabTestConnDebug: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEnablePingTests: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagAssetLibUpdate2024Q2: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagPaidCloudDecimation: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagVideoSetAutoplayWithSound: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagVideoSetPublicContentSource: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCloudDecimation: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagRhinoDecimation: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEnableScreenCreation: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagWebSocketCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagWebBrowserCollab: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagScreenConsole: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagAppStream: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagStatelessVoiceChat: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagScreenAppReSkinV1Demo: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagStatelessClientSession: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagRoomCode: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagProTier: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagCollabSqlPersistence: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagProTierMessaging: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagRemoveMultiOrgs: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagNewServerConnectorStage1: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagEnableCollabExperimentsFakeDoor: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagNewServerConnectorStage2: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagInternalOnlyAllowMultiOrgs: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagUseGradioWhisper: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagUseHttpWhisper: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagTurntable: _ClassVar[SubscriptionFeatureFlag]
    SubscriptionFeatureFlagImageTo3D: _ClassVar[SubscriptionFeatureFlag]

class SSOProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoProvider: _ClassVar[SSOProvider]
    Microsoft: _ClassVar[SSOProvider]
    Netflix: _ClassVar[SSOProvider]
    PAndG: _ClassVar[SSOProvider]
    Google: _ClassVar[SSOProvider]
    Renault: _ClassVar[SSOProvider]
    Okta: _ClassVar[SSOProvider]

class OIDCResourceProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Instagram: _ClassVar[OIDCResourceProvider]
    LinkedIn: _ClassVar[OIDCResourceProvider]

class DocumentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[DocumentType]
    Grs: _ClassVar[DocumentType]
    Image: _ClassVar[DocumentType]
    Obj: _ClassVar[DocumentType]
    Sketch: _ClassVar[DocumentType]
    SketchZip: _ClassVar[DocumentType]
    exportedObj: _ClassVar[DocumentType]
    exportedScreenshot: _ClassVar[DocumentType]
    zipObj: _ClassVar[DocumentType]
    exportedIGES: _ClassVar[DocumentType]
    exportedFBX: _ClassVar[DocumentType]
    importedFBX: _ClassVar[DocumentType]
    importedBlend: _ClassVar[DocumentType]
    importedGLTF: _ClassVar[DocumentType]
    importedSTL: _ClassVar[DocumentType]
    importedCollada: _ClassVar[DocumentType]
    importedIGES: _ClassVar[DocumentType]
    exportedUSDZ: _ClassVar[DocumentType]
    exportedGLB: _ClassVar[DocumentType]
    exportedMP4: _ClassVar[DocumentType]
    importedHDR: _ClassVar[DocumentType]
    svg: _ClassVar[DocumentType]
    importedMP4: _ClassVar[DocumentType]
    importedUSDZ: _ClassVar[DocumentType]
    trueTypeFont: _ClassVar[DocumentType]
    openTypeFont: _ClassVar[DocumentType]
    OnlineSketch: _ClassVar[DocumentType]
    exportedGif: _ClassVar[DocumentType]
    exportedBlend: _ClassVar[DocumentType]
    cosketchRoom: _ClassVar[DocumentType]
    folder: _ClassVar[DocumentType]
    exportPreset: _ClassVar[DocumentType]

class SketchMetaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SketchMetaTypeUndefined: _ClassVar[SketchMetaType]
    SketchMetaTypeAutoSave: _ClassVar[SketchMetaType]
    SketchMetaTypeLocalSketch: _ClassVar[SketchMetaType]
    SketchMetaTypeLandingPadSketch: _ClassVar[SketchMetaType]
    SketchMetaTypeCoCreationRoom: _ClassVar[SketchMetaType]
    SketchMetaTypeOnlineSketch: _ClassVar[SketchMetaType]

class CollaborationPermission(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PermissionInValid: _ClassVar[CollaborationPermission]
    PermissionViewOnly: _ClassVar[CollaborationPermission]
    PermissionComments: _ClassVar[CollaborationPermission]
    PermissionSaveToLocal: _ClassVar[CollaborationPermission]
    PermissionWrite: _ClassVar[CollaborationPermission]
    PermissionAdmin: _ClassVar[CollaborationPermission]

class CollaborationRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CollaborationRoleInvalid: _ClassVar[CollaborationRole]
    CollaborationRoleOwner: _ClassVar[CollaborationRole]
    CollaborationRoleViewer: _ClassVar[CollaborationRole]
    CollaborationRoleReviewer: _ClassVar[CollaborationRole]
    CollaborationRoleCoCreator: _ClassVar[CollaborationRole]

class PreProcessedImportStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PreProcessedImportStatusInvalid: _ClassVar[PreProcessedImportStatus]
    NoPreProcessedImport: _ClassVar[PreProcessedImportStatus]
    GeneratingPreProcessedImport: _ClassVar[PreProcessedImportStatus]
    HasPreProcessedImport: _ClassVar[PreProcessedImportStatus]
    FailedPreProcessedImport: _ClassVar[PreProcessedImportStatus]

class CoSketchReplayStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CoSketchReplayUnknown: _ClassVar[CoSketchReplayStatus]
    CoSketchReplayNoReplay: _ClassVar[CoSketchReplayStatus]
    CoSketchReplayReplaying: _ClassVar[CoSketchReplayStatus]
    CoSketchReplayReplayFailed: _ClassVar[CoSketchReplayStatus]
    CoSketchReplayReplaySuccess: _ClassVar[CoSketchReplayStatus]
    CoSketchReplayTimeout: _ClassVar[CoSketchReplayStatus]

class GSDeepLinkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GSDeepLinkUnknown: _ClassVar[GSDeepLinkType]
    GSDeepLinkOpenLinkId: _ClassVar[GSDeepLinkType]
    GSDeepLinkEnterPublicRoom: _ClassVar[GSDeepLinkType]
    GSDeepLinkEnterRoomByRoomId: _ClassVar[GSDeepLinkType]
    GSDeepLinkOpenSketchFile: _ClassVar[GSDeepLinkType]
    GSDeepLinkOpenLocalSketchFile: _ClassVar[GSDeepLinkType]
    GSDeepLinkAdminNotification: _ClassVar[GSDeepLinkType]

class GSDeepLinkLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GSDeepLinkLocationUnknown: _ClassVar[GSDeepLinkLocation]
    GSDeepLinkLocation2d: _ClassVar[GSDeepLinkLocation]
    GSDeepLinkLocationVr: _ClassVar[GSDeepLinkLocation]
    GSDeepLinkLocationRemote: _ClassVar[GSDeepLinkLocation]

class GSDeepLinkTargetAppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GSDeepLinkTargetAppTypeScreen: _ClassVar[GSDeepLinkTargetAppType]
    GSDeepLinkTargetAppTypeVR: _ClassVar[GSDeepLinkTargetAppType]
    GSDeepLinkTargetAppTypeStream: _ClassVar[GSDeepLinkTargetAppType]

class SourceApp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SourceAppUnset: _ClassVar[SourceApp]
    SourceAppLPWeb: _ClassVar[SourceApp]
    SourceAppVR: _ClassVar[SourceApp]
    SourceApp2DScreen: _ClassVar[SourceApp]
    SourceAppBot: _ClassVar[SourceApp]
    SourceAppWebViewer: _ClassVar[SourceApp]
    SourceAppPadApp: _ClassVar[SourceApp]
    SourceAppCli: _ClassVar[SourceApp]
    SourceAppOpsPortal: _ClassVar[SourceApp]

class PaywallType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PaywallTypeUnset: _ClassVar[PaywallType]
    PaywallTypeMax2InvitedUsersPerRoom: _ClassVar[PaywallType]
    PaywallTypeMax2SharedRoomsPerUser: _ClassVar[PaywallType]
    PaywallTypeOwnerMustBePresentInRoom: _ClassVar[PaywallType]
    PaywallTypeMax1RoomPerUser: _ClassVar[PaywallType]
    PaywallTypeScreenCollabNotAllowed: _ClassVar[PaywallType]
    PaywallTypeMaxMonthlyDownloadLimitExceeded: _ClassVar[PaywallType]
    PaywallTypeMax3ConcurrentUsersInRoom: _ClassVar[PaywallType]
    PaywallTypeDiscoverBusiness: _ClassVar[PaywallType]
    PaywallTypeCollabRoomLimit: _ClassVar[PaywallType]
    PaywallTypeStorageCapFileUpload: _ClassVar[PaywallType]
    PaywallTypeStorageCapFileExport: _ClassVar[PaywallType]
    PaywallTypeCollabRoomLimitExceeded: _ClassVar[PaywallType]
    PaywallTypeWaitingTimesForExport: _ClassVar[PaywallType]

class PaywallStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PaywallStatusUnset: _ClassVar[PaywallStatus]
    PaywallStatusNotApplied: _ClassVar[PaywallStatus]
    PaywallStatusPaywallApplied: _ClassVar[PaywallStatus]
    PaywallStatusJailbreakApplied: _ClassVar[PaywallStatus]
    PaywallStatusGSFriend: _ClassVar[PaywallStatus]
Unused: PriceTier
EarlyAdopter: PriceTier
Pro: PriceTier
Studio: PriceTier
Enterprise: PriceTier
Freemium: PriceTier
ConnectionInvitationStatusPending: ConnectionInvitationStatus
ConnectionInvitationStatusAccepted: ConnectionInvitationStatus
ConnectionInvitationStatusRejected: ConnectionInvitationStatus
RoomStatusUnknown: CoSketchRoomStatus
RoomStatusNotLive: CoSketchRoomStatus
RoomStatusLoading: CoSketchRoomStatus
RoomStatusReady: CoSketchRoomStatus
RoomStatusShuttingDown: CoSketchRoomStatus
UserId: IdType
OrgTeamId: IdType
OrgId: IdType
Community: IdType
EnvironmentFlat: EnvironmentColorType
EnvironmentGradient: EnvironmentColorType
LightTransformSpaceNone: LightTransformSpace
LightTransformSpaceSketch: LightTransformSpace
LightTransformSpaceWorld: LightTransformSpace
EnvironmentPresetUndefined: EnvironmentPreset
EnvironmentPresetGreyRoom: EnvironmentPreset
EnvironmentPresetBlackRoom: EnvironmentPreset
EnvironmentPresetWarehouse: EnvironmentPreset
EnvironmentPresetStudio: EnvironmentPreset
EnvironmentPresetCustom: EnvironmentPreset
DeprecatedEnvironmentPresetXREnvironment: EnvironmentPreset
EnvironmentPresetEmptyScene: EnvironmentPreset
EnvironmentPresetGumdrop: EnvironmentPreset
EnvironmentPresetLobby: EnvironmentPreset
Empty: EnvironmentScene
InfinitePlane: EnvironmentScene
BlackGrid: EnvironmentScene
Warehouse: EnvironmentScene
ReflectionSkybox: EnvironmentScene
ConfigurableEnvironment: EnvironmentScene
Gumdrop: EnvironmentScene
Lobby: EnvironmentScene
ProceduralSky: EnvironmentScene
FlatColorBackground: EnvironmentBackgroundSetting
GradientColorBackground: EnvironmentBackgroundSetting
HDRBackground: EnvironmentBackgroundSetting
NoReflections: EnvironmentReflectionSetting
BackgroundReflections: EnvironmentReflectionSetting
ColorReflections: EnvironmentReflectionSetting
CustomHDRReflections: EnvironmentReflectionSetting
ZebraReflections: EnvironmentReflectionSetting
UserBadgeUnknown: UserBadge
UserBadgeEarlyAdopter: UserBadge
UserBadgeStudentAmbassador: UserBadge
UserBadgeTrainedInstructor: UserBadge
PublicProfileStatus_Default: PublicProfileStatus
PublicProfileStatus_Public: PublicProfileStatus
PublicProfileStatus_Private: PublicProfileStatus
OrgMemberRoleStandard: OrgMemberRole
OrgMemberRoleAdmin: OrgMemberRole
OrgMemberRoleCoordinator: OrgMemberRole
OrgMemberRoleReviewer: OrgMemberRole
OrgMemberRoleViewer: OrgMemberRole
OrgMemberScreenCollabTrial: OrgMemberRole
OrgMemberGSConsultant: OrgMemberRole
OrgMemberRoleReviewerAdmin: OrgMemberRole
OrgMemberRoleViewerAdmin: OrgMemberRole
OrgMemberScreenCollabTrialAdmin: OrgMemberRole
OrgLicenseType_Unknown: OrgLicenseType
OrgLicenseType_Creation: OrgLicenseType
OrgLicenseType_Trainer: OrgLicenseType
OrgLicenseType_Coordination: OrgLicenseType
OrgLicenseType_ScreenTrial: OrgLicenseType
OrgLicenseType_Review: OrgLicenseType
OrgLicenseType_View: OrgLicenseType
OrgRoleType_Unknown: OrgRoleType
OrgRoleType_Member: OrgRoleType
OrgRoleType_Admin: OrgRoleType
OrgMemberStatusDeactivated: OrgMemberStatus
OrgMemberStatusActivated: OrgMemberStatus
OrgMemberStatusDeleted: OrgMemberStatus
CommunityStudioRoleUnset: CommunityStudioRole
CommunityStudioRoleMember: CommunityStudioRole
CommunityStudioRoleMaintainer: CommunityStudioRole
Any: DataLocation
EU: DataLocation
US: DataLocation
SubscriptionFeatureFlagUnused: SubscriptionFeatureFlag
SubscriptionFeatureFlagShareRoomWithExternalUser: SubscriptionFeatureFlag
SubscriptionFeatureFlagTrafficRecording: SubscriptionFeatureFlag
SubscriptionFeatureFlagNoScreenshotWatermark: SubscriptionFeatureFlag
SubscriptionFeatureFlagMiniTrafficRecording: SubscriptionFeatureFlag
SubscriptionFeatureFlagTeamSpace: SubscriptionFeatureFlag
SubscriptionFeatureFlagCoSketchReplay: SubscriptionFeatureFlag
SubscriptionFeatureFlagCloudLogger: SubscriptionFeatureFlag
SubscriptionFeatureFlagDebugFileLogger: SubscriptionFeatureFlag
SubscriptionFeatureFlag2dApp: SubscriptionFeatureFlag
SubscriptionFeatureFlagDisableCloudStorage: SubscriptionFeatureFlag
SubscriptionFeatureFlagVoiceToText: SubscriptionFeatureFlag
SubscriptionFeatureFlagInternalDevTools: SubscriptionFeatureFlag
SubscriptionFeatureFlagGrandUnification: SubscriptionFeatureFlag
SubscriptionFeatureFlagInviteToCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagScripting: SubscriptionFeatureFlag
SubscriptionFeatureFlagJoinerRequest: SubscriptionFeatureFlag
SubscriptionFeatureFlagAprilFools2025: SubscriptionFeatureFlag
SubscriptionFeatureFlagSocialConnections: SubscriptionFeatureFlag
SubscriptionFeatureFlagTrashedAndExpiringDocsEmailDigest: SubscriptionFeatureFlag
SubscriptionFeatureFlagCollabHearbeat: SubscriptionFeatureFlag
SubscriptionFeatureFlagEduCertTutorials: SubscriptionFeatureFlag
SubscriptionFeatureFlagShareRoomWithinOrg: SubscriptionFeatureFlag
SubscriptionFeatureFlagDebugUserAccount: SubscriptionFeatureFlag
SubscriptionFeatureFlagUseNon443GatewayPort: SubscriptionFeatureFlag
SubscriptionFeatureFlagFBXRoundTrip: SubscriptionFeatureFlag
SubscriptionFeatureFlagEnablePaywall: SubscriptionFeatureFlag
SubscriptionFeatureFlagJailbreakCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagIngressToCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagJailbreakScreenCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagJailbreakDownload: SubscriptionFeatureFlag
SubscriptionFeatureFlagCrossSectionTool: SubscriptionFeatureFlag
SubscriptionFeatureFlagRefLibFolderNameAndStructureChanged: SubscriptionFeatureFlag
SubscriptionFeatureFlagLayerGrouping: SubscriptionFeatureFlag
SubscriptionFeatureFlagOnlineSketch: SubscriptionFeatureFlag
SubscriptionFeatureFlagExternalTeams: SubscriptionFeatureFlag
SubscriptionFeatureFlagCollapseMyWorkspaceAndMyFiles: SubscriptionFeatureFlag
SubscriptionFeatureFlagEnableCollabTestConnDebug: SubscriptionFeatureFlag
SubscriptionFeatureFlagEnablePingTests: SubscriptionFeatureFlag
SubscriptionFeatureFlagAssetLibUpdate2024Q2: SubscriptionFeatureFlag
SubscriptionFeatureFlagPaidCloudDecimation: SubscriptionFeatureFlag
SubscriptionFeatureFlagVideoSetAutoplayWithSound: SubscriptionFeatureFlag
SubscriptionFeatureFlagVideoSetPublicContentSource: SubscriptionFeatureFlag
SubscriptionFeatureFlagCloudDecimation: SubscriptionFeatureFlag
SubscriptionFeatureFlagRhinoDecimation: SubscriptionFeatureFlag
SubscriptionFeatureFlagEnableScreenCreation: SubscriptionFeatureFlag
SubscriptionFeatureFlagWebSocketCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagWebBrowserCollab: SubscriptionFeatureFlag
SubscriptionFeatureFlagScreenConsole: SubscriptionFeatureFlag
SubscriptionFeatureFlagAppStream: SubscriptionFeatureFlag
SubscriptionFeatureFlagStatelessVoiceChat: SubscriptionFeatureFlag
SubscriptionFeatureFlagScreenAppReSkinV1Demo: SubscriptionFeatureFlag
SubscriptionFeatureFlagStatelessClientSession: SubscriptionFeatureFlag
SubscriptionFeatureFlagRoomCode: SubscriptionFeatureFlag
SubscriptionFeatureFlagProTier: SubscriptionFeatureFlag
SubscriptionFeatureFlagCollabSqlPersistence: SubscriptionFeatureFlag
SubscriptionFeatureFlagProTierMessaging: SubscriptionFeatureFlag
SubscriptionFeatureFlagRemoveMultiOrgs: SubscriptionFeatureFlag
SubscriptionFeatureFlagNewServerConnectorStage1: SubscriptionFeatureFlag
SubscriptionFeatureFlagEnableCollabExperimentsFakeDoor: SubscriptionFeatureFlag
SubscriptionFeatureFlagNewServerConnectorStage2: SubscriptionFeatureFlag
SubscriptionFeatureFlagInternalOnlyAllowMultiOrgs: SubscriptionFeatureFlag
SubscriptionFeatureFlagUseGradioWhisper: SubscriptionFeatureFlag
SubscriptionFeatureFlagUseHttpWhisper: SubscriptionFeatureFlag
SubscriptionFeatureFlagTurntable: SubscriptionFeatureFlag
SubscriptionFeatureFlagImageTo3D: SubscriptionFeatureFlag
NoProvider: SSOProvider
Microsoft: SSOProvider
Netflix: SSOProvider
PAndG: SSOProvider
Google: SSOProvider
Renault: SSOProvider
Okta: SSOProvider
Instagram: OIDCResourceProvider
LinkedIn: OIDCResourceProvider
Unknown: DocumentType
Grs: DocumentType
Image: DocumentType
Obj: DocumentType
Sketch: DocumentType
SketchZip: DocumentType
exportedObj: DocumentType
exportedScreenshot: DocumentType
zipObj: DocumentType
exportedIGES: DocumentType
exportedFBX: DocumentType
importedFBX: DocumentType
importedBlend: DocumentType
importedGLTF: DocumentType
importedSTL: DocumentType
importedCollada: DocumentType
importedIGES: DocumentType
exportedUSDZ: DocumentType
exportedGLB: DocumentType
exportedMP4: DocumentType
importedHDR: DocumentType
svg: DocumentType
importedMP4: DocumentType
importedUSDZ: DocumentType
trueTypeFont: DocumentType
openTypeFont: DocumentType
OnlineSketch: DocumentType
exportedGif: DocumentType
exportedBlend: DocumentType
cosketchRoom: DocumentType
folder: DocumentType
exportPreset: DocumentType
SketchMetaTypeUndefined: SketchMetaType
SketchMetaTypeAutoSave: SketchMetaType
SketchMetaTypeLocalSketch: SketchMetaType
SketchMetaTypeLandingPadSketch: SketchMetaType
SketchMetaTypeCoCreationRoom: SketchMetaType
SketchMetaTypeOnlineSketch: SketchMetaType
PermissionInValid: CollaborationPermission
PermissionViewOnly: CollaborationPermission
PermissionComments: CollaborationPermission
PermissionSaveToLocal: CollaborationPermission
PermissionWrite: CollaborationPermission
PermissionAdmin: CollaborationPermission
CollaborationRoleInvalid: CollaborationRole
CollaborationRoleOwner: CollaborationRole
CollaborationRoleViewer: CollaborationRole
CollaborationRoleReviewer: CollaborationRole
CollaborationRoleCoCreator: CollaborationRole
PreProcessedImportStatusInvalid: PreProcessedImportStatus
NoPreProcessedImport: PreProcessedImportStatus
GeneratingPreProcessedImport: PreProcessedImportStatus
HasPreProcessedImport: PreProcessedImportStatus
FailedPreProcessedImport: PreProcessedImportStatus
CoSketchReplayUnknown: CoSketchReplayStatus
CoSketchReplayNoReplay: CoSketchReplayStatus
CoSketchReplayReplaying: CoSketchReplayStatus
CoSketchReplayReplayFailed: CoSketchReplayStatus
CoSketchReplayReplaySuccess: CoSketchReplayStatus
CoSketchReplayTimeout: CoSketchReplayStatus
GSDeepLinkUnknown: GSDeepLinkType
GSDeepLinkOpenLinkId: GSDeepLinkType
GSDeepLinkEnterPublicRoom: GSDeepLinkType
GSDeepLinkEnterRoomByRoomId: GSDeepLinkType
GSDeepLinkOpenSketchFile: GSDeepLinkType
GSDeepLinkOpenLocalSketchFile: GSDeepLinkType
GSDeepLinkAdminNotification: GSDeepLinkType
GSDeepLinkLocationUnknown: GSDeepLinkLocation
GSDeepLinkLocation2d: GSDeepLinkLocation
GSDeepLinkLocationVr: GSDeepLinkLocation
GSDeepLinkLocationRemote: GSDeepLinkLocation
GSDeepLinkTargetAppTypeScreen: GSDeepLinkTargetAppType
GSDeepLinkTargetAppTypeVR: GSDeepLinkTargetAppType
GSDeepLinkTargetAppTypeStream: GSDeepLinkTargetAppType
SourceAppUnset: SourceApp
SourceAppLPWeb: SourceApp
SourceAppVR: SourceApp
SourceApp2DScreen: SourceApp
SourceAppBot: SourceApp
SourceAppWebViewer: SourceApp
SourceAppPadApp: SourceApp
SourceAppCli: SourceApp
SourceAppOpsPortal: SourceApp
PaywallTypeUnset: PaywallType
PaywallTypeMax2InvitedUsersPerRoom: PaywallType
PaywallTypeMax2SharedRoomsPerUser: PaywallType
PaywallTypeOwnerMustBePresentInRoom: PaywallType
PaywallTypeMax1RoomPerUser: PaywallType
PaywallTypeScreenCollabNotAllowed: PaywallType
PaywallTypeMaxMonthlyDownloadLimitExceeded: PaywallType
PaywallTypeMax3ConcurrentUsersInRoom: PaywallType
PaywallTypeDiscoverBusiness: PaywallType
PaywallTypeCollabRoomLimit: PaywallType
PaywallTypeStorageCapFileUpload: PaywallType
PaywallTypeStorageCapFileExport: PaywallType
PaywallTypeCollabRoomLimitExceeded: PaywallType
PaywallTypeWaitingTimesForExport: PaywallType
PaywallStatusUnset: PaywallStatus
PaywallStatusNotApplied: PaywallStatus
PaywallStatusPaywallApplied: PaywallStatus
PaywallStatusJailbreakApplied: PaywallStatus
PaywallStatusGSFriend: PaywallStatus

class IDTicket(_message.Message):
    __slots__ = ("expiry", "stoken")
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    STOKEN_FIELD_NUMBER: _ClassVar[int]
    expiry: int
    stoken: str
    def __init__(self, expiry: _Optional[int] = ..., stoken: _Optional[str] = ...) -> None: ...

class AuthDetail(_message.Message):
    __slots__ = ("userId", "priceTier", "startTime", "renewCount", "licenseExpiryTime", "organizationId", "availableHosts", "loggedInViaDevicePairing")
    USERID_FIELD_NUMBER: _ClassVar[int]
    PRICETIER_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    RENEWCOUNT_FIELD_NUMBER: _ClassVar[int]
    LICENSEEXPIRYTIME_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEHOSTS_FIELD_NUMBER: _ClassVar[int]
    LOGGEDINVIADEVICEPAIRING_FIELD_NUMBER: _ClassVar[int]
    userId: str
    priceTier: PriceTier
    startTime: int
    renewCount: int
    licenseExpiryTime: int
    organizationId: str
    availableHosts: _containers.RepeatedCompositeFieldContainer[_gravi_common_pb2.HostTO]
    loggedInViaDevicePairing: bool
    def __init__(self, userId: _Optional[str] = ..., priceTier: _Optional[_Union[PriceTier, str]] = ..., startTime: _Optional[int] = ..., renewCount: _Optional[int] = ..., licenseExpiryTime: _Optional[int] = ..., organizationId: _Optional[str] = ..., availableHosts: _Optional[_Iterable[_Union[_gravi_common_pb2.HostTO, _Mapping]]] = ..., loggedInViaDevicePairing: bool = ...) -> None: ...

class CoSketchTicket(_message.Message):
    __slots__ = ("secretCode",)
    SECRETCODE_FIELD_NUMBER: _ClassVar[int]
    secretCode: str
    def __init__(self, secretCode: _Optional[str] = ...) -> None: ...

class DeviceInfo(_message.Message):
    __slots__ = ("macAddress", "username", "machineName", "deviceId", "os", "osVersion", "browser", "browserVersion")
    MACADDRESS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    MACHINENAME_FIELD_NUMBER: _ClassVar[int]
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    OSVERSION_FIELD_NUMBER: _ClassVar[int]
    BROWSER_FIELD_NUMBER: _ClassVar[int]
    BROWSERVERSION_FIELD_NUMBER: _ClassVar[int]
    macAddress: str
    username: str
    machineName: str
    deviceId: str
    os: str
    osVersion: str
    browser: str
    browserVersion: str
    def __init__(self, macAddress: _Optional[str] = ..., username: _Optional[str] = ..., machineName: _Optional[str] = ..., deviceId: _Optional[str] = ..., os: _Optional[str] = ..., osVersion: _Optional[str] = ..., browser: _Optional[str] = ..., browserVersion: _Optional[str] = ...) -> None: ...

class DocIdList(_message.Message):
    __slots__ = ("docId",)
    DOCID_FIELD_NUMBER: _ClassVar[int]
    docId: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, docId: _Optional[_Iterable[str]] = ...) -> None: ...

class MaintenanceFlags(_message.Message):
    __slots__ = ("fullMaintenance", "docServiceMaintenance", "cosketchMaintenance", "maintenanceMessage")
    FULLMAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    DOCSERVICEMAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    COSKETCHMAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCEMESSAGE_FIELD_NUMBER: _ClassVar[int]
    fullMaintenance: bool
    docServiceMaintenance: bool
    cosketchMaintenance: bool
    maintenanceMessage: str
    def __init__(self, fullMaintenance: bool = ..., docServiceMaintenance: bool = ..., cosketchMaintenance: bool = ..., maintenanceMessage: _Optional[str] = ...) -> None: ...

class ClientTO(_message.Message):
    __slots__ = ("userId", "username")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    userId: str
    username: str
    def __init__(self, userId: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class ConnectionInvitationTO(_message.Message):
    __slots__ = ("invitationId", "senderId", "senderPublicInfo", "recipientId", "recipientPublicInfo", "invitationStatus", "createdOn", "updatedOn")
    INVITATIONID_FIELD_NUMBER: _ClassVar[int]
    SENDERID_FIELD_NUMBER: _ClassVar[int]
    SENDERPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    INVITATIONSTATUS_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    UPDATEDON_FIELD_NUMBER: _ClassVar[int]
    invitationId: str
    senderId: str
    senderPublicInfo: UserPublicTO
    recipientId: str
    recipientPublicInfo: UserPublicTO
    invitationStatus: ConnectionInvitationStatus
    createdOn: int
    updatedOn: int
    def __init__(self, invitationId: _Optional[str] = ..., senderId: _Optional[str] = ..., senderPublicInfo: _Optional[_Union[UserPublicTO, _Mapping]] = ..., recipientId: _Optional[str] = ..., recipientPublicInfo: _Optional[_Union[UserPublicTO, _Mapping]] = ..., invitationStatus: _Optional[_Union[ConnectionInvitationStatus, str]] = ..., createdOn: _Optional[int] = ..., updatedOn: _Optional[int] = ...) -> None: ...

class CollabUserDisplayInfo(_message.Message):
    __slots__ = ("displayName",)
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    displayName: str
    def __init__(self, displayName: _Optional[str] = ...) -> None: ...

class EnvironmentSettingTO(_message.Message):
    __slots__ = ("name", "deprecatedHDR", "deprecatedBuiltInReflectionSource", "deprecatedReflectionSourceSetting", "environmentScene", "skyColorR", "skyColorG", "skyColorB", "deprecatedShadowSetting", "deprecatedFloorGridSetting", "deprecatedColorType", "lightAngleX", "lightAngleY", "lightAngleZ", "lightAngleW", "lightTransformSpace", "directionalLightIntensity", "environmentLightIntensity", "horizonColorR", "horizonColorG", "horizonColorB", "floorColorR", "floorColorG", "floorColorB", "deprecatedHdrGuid", "deprecatedHdrFilePath", "deprecatedHdrDisplayName", "deprecatedHdrFileHash", "deprecatedHdrFileSize", "backgroundHdrUseGumdrop", "backgroundHdrGumdropHeight", "backgroundHdrData", "reflectionHdrData", "backgroundSetting", "reflectionSetting", "directionalLightColorR", "directionalLightColorG", "directionalLightColorB", "floorShadows", "sketchShadows")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDR_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDBUILTINREFLECTIONSOURCE_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDREFLECTIONSOURCESETTING_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTSCENE_FIELD_NUMBER: _ClassVar[int]
    SKYCOLORR_FIELD_NUMBER: _ClassVar[int]
    SKYCOLORG_FIELD_NUMBER: _ClassVar[int]
    SKYCOLORB_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDSHADOWSETTING_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDFLOORGRIDSETTING_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDCOLORTYPE_FIELD_NUMBER: _ClassVar[int]
    LIGHTANGLEX_FIELD_NUMBER: _ClassVar[int]
    LIGHTANGLEY_FIELD_NUMBER: _ClassVar[int]
    LIGHTANGLEZ_FIELD_NUMBER: _ClassVar[int]
    LIGHTANGLEW_FIELD_NUMBER: _ClassVar[int]
    LIGHTTRANSFORMSPACE_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONALLIGHTINTENSITY_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTLIGHTINTENSITY_FIELD_NUMBER: _ClassVar[int]
    HORIZONCOLORR_FIELD_NUMBER: _ClassVar[int]
    HORIZONCOLORG_FIELD_NUMBER: _ClassVar[int]
    HORIZONCOLORB_FIELD_NUMBER: _ClassVar[int]
    FLOORCOLORR_FIELD_NUMBER: _ClassVar[int]
    FLOORCOLORG_FIELD_NUMBER: _ClassVar[int]
    FLOORCOLORB_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDRGUID_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDRFILEPATH_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDRDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDRFILEHASH_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDHDRFILESIZE_FIELD_NUMBER: _ClassVar[int]
    BACKGROUNDHDRUSEGUMDROP_FIELD_NUMBER: _ClassVar[int]
    BACKGROUNDHDRGUMDROPHEIGHT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUNDHDRDATA_FIELD_NUMBER: _ClassVar[int]
    REFLECTIONHDRDATA_FIELD_NUMBER: _ClassVar[int]
    BACKGROUNDSETTING_FIELD_NUMBER: _ClassVar[int]
    REFLECTIONSETTING_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONALLIGHTCOLORR_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONALLIGHTCOLORG_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONALLIGHTCOLORB_FIELD_NUMBER: _ClassVar[int]
    FLOORSHADOWS_FIELD_NUMBER: _ClassVar[int]
    SKETCHSHADOWS_FIELD_NUMBER: _ClassVar[int]
    name: str
    deprecatedHDR: int
    deprecatedBuiltInReflectionSource: int
    deprecatedReflectionSourceSetting: int
    environmentScene: EnvironmentScene
    skyColorR: int
    skyColorG: int
    skyColorB: int
    deprecatedShadowSetting: int
    deprecatedFloorGridSetting: int
    deprecatedColorType: EnvironmentColorType
    lightAngleX: float
    lightAngleY: float
    lightAngleZ: float
    lightAngleW: float
    lightTransformSpace: LightTransformSpace
    directionalLightIntensity: float
    environmentLightIntensity: float
    horizonColorR: int
    horizonColorG: int
    horizonColorB: int
    floorColorR: int
    floorColorG: int
    floorColorB: int
    deprecatedHdrGuid: str
    deprecatedHdrFilePath: str
    deprecatedHdrDisplayName: str
    deprecatedHdrFileHash: str
    deprecatedHdrFileSize: int
    backgroundHdrUseGumdrop: bool
    backgroundHdrGumdropHeight: float
    backgroundHdrData: HDRData
    reflectionHdrData: HDRData
    backgroundSetting: EnvironmentBackgroundSetting
    reflectionSetting: EnvironmentReflectionSetting
    directionalLightColorR: int
    directionalLightColorG: int
    directionalLightColorB: int
    floorShadows: bool
    sketchShadows: bool
    def __init__(self, name: _Optional[str] = ..., deprecatedHDR: _Optional[int] = ..., deprecatedBuiltInReflectionSource: _Optional[int] = ..., deprecatedReflectionSourceSetting: _Optional[int] = ..., environmentScene: _Optional[_Union[EnvironmentScene, str]] = ..., skyColorR: _Optional[int] = ..., skyColorG: _Optional[int] = ..., skyColorB: _Optional[int] = ..., deprecatedShadowSetting: _Optional[int] = ..., deprecatedFloorGridSetting: _Optional[int] = ..., deprecatedColorType: _Optional[_Union[EnvironmentColorType, str]] = ..., lightAngleX: _Optional[float] = ..., lightAngleY: _Optional[float] = ..., lightAngleZ: _Optional[float] = ..., lightAngleW: _Optional[float] = ..., lightTransformSpace: _Optional[_Union[LightTransformSpace, str]] = ..., directionalLightIntensity: _Optional[float] = ..., environmentLightIntensity: _Optional[float] = ..., horizonColorR: _Optional[int] = ..., horizonColorG: _Optional[int] = ..., horizonColorB: _Optional[int] = ..., floorColorR: _Optional[int] = ..., floorColorG: _Optional[int] = ..., floorColorB: _Optional[int] = ..., deprecatedHdrGuid: _Optional[str] = ..., deprecatedHdrFilePath: _Optional[str] = ..., deprecatedHdrDisplayName: _Optional[str] = ..., deprecatedHdrFileHash: _Optional[str] = ..., deprecatedHdrFileSize: _Optional[int] = ..., backgroundHdrUseGumdrop: bool = ..., backgroundHdrGumdropHeight: _Optional[float] = ..., backgroundHdrData: _Optional[_Union[HDRData, _Mapping]] = ..., reflectionHdrData: _Optional[_Union[HDRData, _Mapping]] = ..., backgroundSetting: _Optional[_Union[EnvironmentBackgroundSetting, str]] = ..., reflectionSetting: _Optional[_Union[EnvironmentReflectionSetting, str]] = ..., directionalLightColorR: _Optional[int] = ..., directionalLightColorG: _Optional[int] = ..., directionalLightColorB: _Optional[int] = ..., floorShadows: bool = ..., sketchShadows: bool = ...) -> None: ...

class EnvironmentSettingFile(_message.Message):
    __slots__ = ("environments",)
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.RepeatedCompositeFieldContainer[EnvironmentSettingTO]
    def __init__(self, environments: _Optional[_Iterable[_Union[EnvironmentSettingTO, _Mapping]]] = ...) -> None: ...

class EnvironmentTO(_message.Message):
    __slots__ = ("deprecatedEnvironmentPreset", "environmentSetting", "environmentGuid")
    DEPRECATEDENVIRONMENTPRESET_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTSETTING_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTGUID_FIELD_NUMBER: _ClassVar[int]
    deprecatedEnvironmentPreset: EnvironmentPreset
    environmentSetting: EnvironmentSettingTO
    environmentGuid: str
    def __init__(self, deprecatedEnvironmentPreset: _Optional[_Union[EnvironmentPreset, str]] = ..., environmentSetting: _Optional[_Union[EnvironmentSettingTO, _Mapping]] = ..., environmentGuid: _Optional[str] = ...) -> None: ...

class HDRData(_message.Message):
    __slots__ = ("hdrGuid", "hdrFilePath", "hdrDisplayName", "hdrFileHash", "hdrFileSize", "hdrRotationX", "hdrRotationY", "hdrRotationZ", "hdrRotationW", "hdrBlur")
    HDRGUID_FIELD_NUMBER: _ClassVar[int]
    HDRFILEPATH_FIELD_NUMBER: _ClassVar[int]
    HDRDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    HDRFILEHASH_FIELD_NUMBER: _ClassVar[int]
    HDRFILESIZE_FIELD_NUMBER: _ClassVar[int]
    HDRROTATIONX_FIELD_NUMBER: _ClassVar[int]
    HDRROTATIONY_FIELD_NUMBER: _ClassVar[int]
    HDRROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    HDRROTATIONW_FIELD_NUMBER: _ClassVar[int]
    HDRBLUR_FIELD_NUMBER: _ClassVar[int]
    hdrGuid: str
    hdrFilePath: str
    hdrDisplayName: str
    hdrFileHash: str
    hdrFileSize: int
    hdrRotationX: float
    hdrRotationY: float
    hdrRotationZ: float
    hdrRotationW: float
    hdrBlur: float
    def __init__(self, hdrGuid: _Optional[str] = ..., hdrFilePath: _Optional[str] = ..., hdrDisplayName: _Optional[str] = ..., hdrFileHash: _Optional[str] = ..., hdrFileSize: _Optional[int] = ..., hdrRotationX: _Optional[float] = ..., hdrRotationY: _Optional[float] = ..., hdrRotationZ: _Optional[float] = ..., hdrRotationW: _Optional[float] = ..., hdrBlur: _Optional[float] = ...) -> None: ...

class UserTO(_message.Message):
    __slots__ = ("userId", "email", "displayName", "earlyAdopter", "firstName", "lastName", "companyName", "surveyCompleted", "mfaEnabled", "orgMemberships", "ssoProvider", "isOrgAccount", "enabledFeatures", "sharedOrganizations", "badges", "studioMemberships", "passwordSet")
    USERID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    EARLYADOPTER_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    COMPANYNAME_FIELD_NUMBER: _ClassVar[int]
    SURVEYCOMPLETED_FIELD_NUMBER: _ClassVar[int]
    MFAENABLED_FIELD_NUMBER: _ClassVar[int]
    ORGMEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    SSOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    ISORGACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ENABLEDFEATURES_FIELD_NUMBER: _ClassVar[int]
    SHAREDORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    STUDIOMEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    PASSWORDSET_FIELD_NUMBER: _ClassVar[int]
    userId: str
    email: str
    displayName: str
    earlyAdopter: bool
    firstName: str
    lastName: str
    companyName: str
    surveyCompleted: bool
    mfaEnabled: bool
    orgMemberships: _containers.RepeatedCompositeFieldContainer[OrgMembership]
    ssoProvider: SSOProvider
    isOrgAccount: bool
    enabledFeatures: _containers.RepeatedScalarFieldContainer[SubscriptionFeatureFlag]
    sharedOrganizations: _containers.RepeatedCompositeFieldContainer[SharedOrganization]
    badges: _containers.RepeatedScalarFieldContainer[UserBadge]
    studioMemberships: _containers.RepeatedCompositeFieldContainer[CommunityStudioMembership]
    passwordSet: bool
    def __init__(self, userId: _Optional[str] = ..., email: _Optional[str] = ..., displayName: _Optional[str] = ..., earlyAdopter: bool = ..., firstName: _Optional[str] = ..., lastName: _Optional[str] = ..., companyName: _Optional[str] = ..., surveyCompleted: bool = ..., mfaEnabled: bool = ..., orgMemberships: _Optional[_Iterable[_Union[OrgMembership, _Mapping]]] = ..., ssoProvider: _Optional[_Union[SSOProvider, str]] = ..., isOrgAccount: bool = ..., enabledFeatures: _Optional[_Iterable[_Union[SubscriptionFeatureFlag, str]]] = ..., sharedOrganizations: _Optional[_Iterable[_Union[SharedOrganization, _Mapping]]] = ..., badges: _Optional[_Iterable[_Union[UserBadge, str]]] = ..., studioMemberships: _Optional[_Iterable[_Union[CommunityStudioMembership, _Mapping]]] = ..., passwordSet: bool = ...) -> None: ...

class UserStatsTO(_message.Message):
    __slots__ = ("totalSketchMS", "splineCounts", "lifeHourDistributions", "currentMonthFirstUsage", "monthHourDistributions", "weekTimeDistributions")
    class SplineCountsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class LifeHourDistributionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class MonthHourDistributionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class WeekTimeDistributionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTALSKETCHMS_FIELD_NUMBER: _ClassVar[int]
    SPLINECOUNTS_FIELD_NUMBER: _ClassVar[int]
    LIFEHOURDISTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
    CURRENTMONTHFIRSTUSAGE_FIELD_NUMBER: _ClassVar[int]
    MONTHHOURDISTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
    WEEKTIMEDISTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
    totalSketchMS: int
    splineCounts: _containers.ScalarMap[str, int]
    lifeHourDistributions: _containers.ScalarMap[str, int]
    currentMonthFirstUsage: int
    monthHourDistributions: _containers.ScalarMap[str, int]
    weekTimeDistributions: _containers.ScalarMap[str, int]
    def __init__(self, totalSketchMS: _Optional[int] = ..., splineCounts: _Optional[_Mapping[str, int]] = ..., lifeHourDistributions: _Optional[_Mapping[str, int]] = ..., currentMonthFirstUsage: _Optional[int] = ..., monthHourDistributions: _Optional[_Mapping[str, int]] = ..., weekTimeDistributions: _Optional[_Mapping[str, int]] = ...) -> None: ...

class UserPublicSocialInfo(_message.Message):
    __slots__ = ("provider", "userName", "displayName", "profilePictureUrl", "linkToPublicPage")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILEPICTUREURL_FIELD_NUMBER: _ClassVar[int]
    LINKTOPUBLICPAGE_FIELD_NUMBER: _ClassVar[int]
    provider: OIDCResourceProvider
    userName: str
    displayName: str
    profilePictureUrl: str
    linkToPublicPage: str
    def __init__(self, provider: _Optional[_Union[OIDCResourceProvider, str]] = ..., userName: _Optional[str] = ..., displayName: _Optional[str] = ..., profilePictureUrl: _Optional[str] = ..., linkToPublicPage: _Optional[str] = ...) -> None: ...

class UserPublicTO(_message.Message):
    __slots__ = ("displayName", "socialInfo", "bio", "status", "id", "isDeleted")
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    SOCIALINFO_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ISDELETED_FIELD_NUMBER: _ClassVar[int]
    displayName: str
    socialInfo: _containers.RepeatedCompositeFieldContainer[UserPublicSocialInfo]
    bio: str
    status: PublicProfileStatus
    id: str
    isDeleted: bool
    def __init__(self, displayName: _Optional[str] = ..., socialInfo: _Optional[_Iterable[_Union[UserPublicSocialInfo, _Mapping]]] = ..., bio: _Optional[str] = ..., status: _Optional[_Union[PublicProfileStatus, str]] = ..., id: _Optional[str] = ..., isDeleted: bool = ...) -> None: ...

class OrgMembership(_message.Message):
    __slots__ = ("orgId", "userId", "role", "status", "orgName", "orgEnabledFeatures", "orgLicenseType", "orgRoleType")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORGNAME_FIELD_NUMBER: _ClassVar[int]
    ORGENABLEDFEATURES_FIELD_NUMBER: _ClassVar[int]
    ORGLICENSETYPE_FIELD_NUMBER: _ClassVar[int]
    ORGROLETYPE_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    userId: str
    role: OrgMemberRole
    status: OrgMemberStatus
    orgName: str
    orgEnabledFeatures: _containers.RepeatedScalarFieldContainer[SubscriptionFeatureFlag]
    orgLicenseType: OrgLicenseType
    orgRoleType: OrgRoleType
    def __init__(self, orgId: _Optional[str] = ..., userId: _Optional[str] = ..., role: _Optional[_Union[OrgMemberRole, str]] = ..., status: _Optional[_Union[OrgMemberStatus, str]] = ..., orgName: _Optional[str] = ..., orgEnabledFeatures: _Optional[_Iterable[_Union[SubscriptionFeatureFlag, str]]] = ..., orgLicenseType: _Optional[_Union[OrgLicenseType, str]] = ..., orgRoleType: _Optional[_Union[OrgRoleType, str]] = ...) -> None: ...

class SharedOrganization(_message.Message):
    __slots__ = ("orgId", "orgName", "sharedSpaceIds", "sharedSpaceNames")
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ORGNAME_FIELD_NUMBER: _ClassVar[int]
    SHAREDSPACEIDS_FIELD_NUMBER: _ClassVar[int]
    SHAREDSPACENAMES_FIELD_NUMBER: _ClassVar[int]
    orgId: str
    orgName: str
    sharedSpaceIds: _containers.RepeatedCompositeFieldContainer[SpaceId]
    sharedSpaceNames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, orgId: _Optional[str] = ..., orgName: _Optional[str] = ..., sharedSpaceIds: _Optional[_Iterable[_Union[SpaceId, _Mapping]]] = ..., sharedSpaceNames: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityStudioMembership(_message.Message):
    __slots__ = ("studioId", "studioName", "userId", "role")
    STUDIOID_FIELD_NUMBER: _ClassVar[int]
    STUDIONAME_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    studioId: str
    studioName: str
    userId: str
    role: CommunityStudioRole
    def __init__(self, studioId: _Optional[str] = ..., studioName: _Optional[str] = ..., userId: _Optional[str] = ..., role: _Optional[_Union[CommunityStudioRole, str]] = ...) -> None: ...

class SharableUserInfo(_message.Message):
    __slots__ = ("userId", "userEmail", "userName")
    USERID_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    userId: str
    userEmail: str
    userName: str
    def __init__(self, userId: _Optional[str] = ..., userEmail: _Optional[str] = ..., userName: _Optional[str] = ...) -> None: ...

class DocumentTO(_message.Message):
    __slots__ = ("documentId", "docType", "ownerId", "docFullPath", "lastModifiedBy", "fileSize", "createdOn", "updatedOn", "revisionId", "trashed", "trashedOn", "spaceId", "requirePassword", "docName", "docParentFolder", "ccMetadata", "ccLiveInstance", "downloadCount", "hasThumbnail", "thumbnailUrl", "publicAccessible", "hasNoContent", "thumbnailTTL", "joinerRequestEnabled", "createdBy", "revisions", "passwordSetBy", "lastAccessedOnByUser", "explicitRole", "isIncrementallySaved", "preProcessedImportStatus", "turntableThumbnail", "creatorInfo")
    DOCUMENTID_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    DOCFULLPATH_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIEDBY_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    UPDATEDON_FIELD_NUMBER: _ClassVar[int]
    REVISIONID_FIELD_NUMBER: _ClassVar[int]
    TRASHED_FIELD_NUMBER: _ClassVar[int]
    TRASHEDON_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    REQUIREPASSWORD_FIELD_NUMBER: _ClassVar[int]
    DOCNAME_FIELD_NUMBER: _ClassVar[int]
    DOCPARENTFOLDER_FIELD_NUMBER: _ClassVar[int]
    CCMETADATA_FIELD_NUMBER: _ClassVar[int]
    CCLIVEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADCOUNT_FIELD_NUMBER: _ClassVar[int]
    HASTHUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILURL_FIELD_NUMBER: _ClassVar[int]
    PUBLICACCESSIBLE_FIELD_NUMBER: _ClassVar[int]
    HASNOCONTENT_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILTTL_FIELD_NUMBER: _ClassVar[int]
    JOINERREQUESTENABLED_FIELD_NUMBER: _ClassVar[int]
    CREATEDBY_FIELD_NUMBER: _ClassVar[int]
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    PASSWORDSETBY_FIELD_NUMBER: _ClassVar[int]
    LASTACCESSEDONBYUSER_FIELD_NUMBER: _ClassVar[int]
    EXPLICITROLE_FIELD_NUMBER: _ClassVar[int]
    ISINCREMENTALLYSAVED_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSEDIMPORTSTATUS_FIELD_NUMBER: _ClassVar[int]
    TURNTABLETHUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    CREATORINFO_FIELD_NUMBER: _ClassVar[int]
    documentId: str
    docType: DocumentType
    ownerId: str
    docFullPath: str
    lastModifiedBy: str
    fileSize: int
    createdOn: int
    updatedOn: int
    revisionId: str
    trashed: bool
    trashedOn: int
    spaceId: SpaceId
    requirePassword: bool
    docName: str
    docParentFolder: str
    ccMetadata: CoCreationMetadata
    ccLiveInstance: CoCreationLiveInstance
    downloadCount: int
    hasThumbnail: bool
    thumbnailUrl: str
    publicAccessible: bool
    hasNoContent: bool
    thumbnailTTL: int
    joinerRequestEnabled: bool
    createdBy: str
    revisions: _containers.RepeatedCompositeFieldContainer[DocRevision]
    passwordSetBy: str
    lastAccessedOnByUser: int
    explicitRole: CollaborationRole
    isIncrementallySaved: bool
    preProcessedImportStatus: PreProcessedImportStatus
    turntableThumbnail: str
    creatorInfo: SharableUserInfo
    def __init__(self, documentId: _Optional[str] = ..., docType: _Optional[_Union[DocumentType, str]] = ..., ownerId: _Optional[str] = ..., docFullPath: _Optional[str] = ..., lastModifiedBy: _Optional[str] = ..., fileSize: _Optional[int] = ..., createdOn: _Optional[int] = ..., updatedOn: _Optional[int] = ..., revisionId: _Optional[str] = ..., trashed: bool = ..., trashedOn: _Optional[int] = ..., spaceId: _Optional[_Union[SpaceId, _Mapping]] = ..., requirePassword: bool = ..., docName: _Optional[str] = ..., docParentFolder: _Optional[str] = ..., ccMetadata: _Optional[_Union[CoCreationMetadata, _Mapping]] = ..., ccLiveInstance: _Optional[_Union[CoCreationLiveInstance, _Mapping]] = ..., downloadCount: _Optional[int] = ..., hasThumbnail: bool = ..., thumbnailUrl: _Optional[str] = ..., publicAccessible: bool = ..., hasNoContent: bool = ..., thumbnailTTL: _Optional[int] = ..., joinerRequestEnabled: bool = ..., createdBy: _Optional[str] = ..., revisions: _Optional[_Iterable[_Union[DocRevision, _Mapping]]] = ..., passwordSetBy: _Optional[str] = ..., lastAccessedOnByUser: _Optional[int] = ..., explicitRole: _Optional[_Union[CollaborationRole, str]] = ..., isIncrementallySaved: bool = ..., preProcessedImportStatus: _Optional[_Union[PreProcessedImportStatus, str]] = ..., turntableThumbnail: _Optional[str] = ..., creatorInfo: _Optional[_Union[SharableUserInfo, _Mapping]] = ...) -> None: ...

class CoCreationMetadata(_message.Message):
    __slots__ = ("lockedByUserForLoading", "miniClientVersion", "availableFrom", "availableUntil")
    LOCKEDBYUSERFORLOADING_FIELD_NUMBER: _ClassVar[int]
    MINICLIENTVERSION_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEFROM_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEUNTIL_FIELD_NUMBER: _ClassVar[int]
    lockedByUserForLoading: str
    miniClientVersion: str
    availableFrom: int
    availableUntil: int
    def __init__(self, lockedByUserForLoading: _Optional[str] = ..., miniClientVersion: _Optional[str] = ..., availableFrom: _Optional[int] = ..., availableUntil: _Optional[int] = ...) -> None: ...

class CoCreationLiveInstance(_message.Message):
    __slots__ = ("status", "connectedUserCount", "maxUserCount", "ownerPresent", "connectedUsers")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONNECTEDUSERCOUNT_FIELD_NUMBER: _ClassVar[int]
    MAXUSERCOUNT_FIELD_NUMBER: _ClassVar[int]
    OWNERPRESENT_FIELD_NUMBER: _ClassVar[int]
    CONNECTEDUSERS_FIELD_NUMBER: _ClassVar[int]
    status: CoSketchRoomStatus
    connectedUserCount: int
    maxUserCount: int
    ownerPresent: bool
    connectedUsers: _containers.RepeatedCompositeFieldContainer[CollabUserDisplayInfo]
    def __init__(self, status: _Optional[_Union[CoSketchRoomStatus, str]] = ..., connectedUserCount: _Optional[int] = ..., maxUserCount: _Optional[int] = ..., ownerPresent: bool = ..., connectedUsers: _Optional[_Iterable[_Union[CollabUserDisplayInfo, _Mapping]]] = ...) -> None: ...

class DocRevision(_message.Message):
    __slots__ = ("createdOn", "hash", "size", "isCurrent")
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    ISCURRENT_FIELD_NUMBER: _ClassVar[int]
    createdOn: int
    hash: str
    size: int
    isCurrent: bool
    def __init__(self, createdOn: _Optional[int] = ..., hash: _Optional[str] = ..., size: _Optional[int] = ..., isCurrent: bool = ...) -> None: ...

class SpaceId(_message.Message):
    __slots__ = ("ownerIdType", "ownerId", "partitionIdType", "partitionId")
    OWNERIDTYPE_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    PARTITIONIDTYPE_FIELD_NUMBER: _ClassVar[int]
    PARTITIONID_FIELD_NUMBER: _ClassVar[int]
    ownerIdType: IdType
    ownerId: str
    partitionIdType: IdType
    partitionId: str
    def __init__(self, ownerIdType: _Optional[_Union[IdType, str]] = ..., ownerId: _Optional[str] = ..., partitionIdType: _Optional[_Union[IdType, str]] = ..., partitionId: _Optional[str] = ...) -> None: ...

class RecentSketchMetaData(_message.Message):
    __slots__ = ("sketchMetaType", "timeOfLastOpenOrSave", "filename", "document")
    SKETCHMETATYPE_FIELD_NUMBER: _ClassVar[int]
    TIMEOFLASTOPENORSAVE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    sketchMetaType: SketchMetaType
    timeOfLastOpenOrSave: int
    filename: str
    document: DocumentTO
    def __init__(self, sketchMetaType: _Optional[_Union[SketchMetaType, str]] = ..., timeOfLastOpenOrSave: _Optional[int] = ..., filename: _Optional[str] = ..., document: _Optional[_Union[DocumentTO, _Mapping]] = ...) -> None: ...

class SubscriptionPackTO(_message.Message):
    __slots__ = ("ownerId", "priceTier", "roomPolicyId", "licenseExpiryOn", "numOfRooms", "spaceAllowance", "enabledFeatures", "daysToAutoBinFiles", "daysToPermanentlyDeleteBinnedFiles", "monthlyDownloadAllowanceGranted", "availableDownloadAllowance", "availableDownloadAllowanceVersion", "downloadAllowanceRefreshAt")
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    PRICETIER_FIELD_NUMBER: _ClassVar[int]
    ROOMPOLICYID_FIELD_NUMBER: _ClassVar[int]
    LICENSEEXPIRYON_FIELD_NUMBER: _ClassVar[int]
    NUMOFROOMS_FIELD_NUMBER: _ClassVar[int]
    SPACEALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    ENABLEDFEATURES_FIELD_NUMBER: _ClassVar[int]
    DAYSTOAUTOBINFILES_FIELD_NUMBER: _ClassVar[int]
    DAYSTOPERMANENTLYDELETEBINNEDFILES_FIELD_NUMBER: _ClassVar[int]
    MONTHLYDOWNLOADALLOWANCEGRANTED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEDOWNLOADALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEDOWNLOADALLOWANCEVERSION_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADALLOWANCEREFRESHAT_FIELD_NUMBER: _ClassVar[int]
    ownerId: str
    priceTier: PriceTier
    roomPolicyId: str
    licenseExpiryOn: int
    numOfRooms: int
    spaceAllowance: int
    enabledFeatures: _containers.RepeatedScalarFieldContainer[SubscriptionFeatureFlag]
    daysToAutoBinFiles: int
    daysToPermanentlyDeleteBinnedFiles: int
    monthlyDownloadAllowanceGranted: int
    availableDownloadAllowance: int
    availableDownloadAllowanceVersion: str
    downloadAllowanceRefreshAt: int
    def __init__(self, ownerId: _Optional[str] = ..., priceTier: _Optional[_Union[PriceTier, str]] = ..., roomPolicyId: _Optional[str] = ..., licenseExpiryOn: _Optional[int] = ..., numOfRooms: _Optional[int] = ..., spaceAllowance: _Optional[int] = ..., enabledFeatures: _Optional[_Iterable[_Union[SubscriptionFeatureFlag, str]]] = ..., daysToAutoBinFiles: _Optional[int] = ..., daysToPermanentlyDeleteBinnedFiles: _Optional[int] = ..., monthlyDownloadAllowanceGranted: _Optional[int] = ..., availableDownloadAllowance: _Optional[int] = ..., availableDownloadAllowanceVersion: _Optional[str] = ..., downloadAllowanceRefreshAt: _Optional[int] = ...) -> None: ...

class UserBehaviourSync(_message.Message):
    __slots__ = ("inSketchIncrementalTimeMS", "createdSplineTypes", "splineCounts")
    INSKETCHINCREMENTALTIMEMS_FIELD_NUMBER: _ClassVar[int]
    CREATEDSPLINETYPES_FIELD_NUMBER: _ClassVar[int]
    SPLINECOUNTS_FIELD_NUMBER: _ClassVar[int]
    inSketchIncrementalTimeMS: int
    createdSplineTypes: _containers.RepeatedScalarFieldContainer[int]
    splineCounts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, inSketchIncrementalTimeMS: _Optional[int] = ..., createdSplineTypes: _Optional[_Iterable[int]] = ..., splineCounts: _Optional[_Iterable[int]] = ...) -> None: ...

class SignUpCacheTicket(_message.Message):
    __slots__ = ("userDisplayName", "signupExpiry", "signupQueryToken")
    USERDISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    SIGNUPEXPIRY_FIELD_NUMBER: _ClassVar[int]
    SIGNUPQUERYTOKEN_FIELD_NUMBER: _ClassVar[int]
    userDisplayName: str
    signupExpiry: int
    signupQueryToken: str
    def __init__(self, userDisplayName: _Optional[str] = ..., signupExpiry: _Optional[int] = ..., signupQueryToken: _Optional[str] = ...) -> None: ...

class CachedAuth(_message.Message):
    __slots__ = ("expiry", "stoken", "lastUsedPriceTier", "earlyAdopter")
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    STOKEN_FIELD_NUMBER: _ClassVar[int]
    LASTUSEDPRICETIER_FIELD_NUMBER: _ClassVar[int]
    EARLYADOPTER_FIELD_NUMBER: _ClassVar[int]
    expiry: int
    stoken: str
    lastUsedPriceTier: PriceTier
    earlyAdopter: bool
    def __init__(self, expiry: _Optional[int] = ..., stoken: _Optional[str] = ..., lastUsedPriceTier: _Optional[_Union[PriceTier, str]] = ..., earlyAdopter: bool = ...) -> None: ...

class CachedInstallationData(_message.Message):
    __slots__ = ("installationTime", "installId")
    INSTALLATIONTIME_FIELD_NUMBER: _ClassVar[int]
    INSTALLID_FIELD_NUMBER: _ClassVar[int]
    installationTime: int
    installId: str
    def __init__(self, installationTime: _Optional[int] = ..., installId: _Optional[str] = ...) -> None: ...

class CloudDocumentMetaLocalCache(_message.Message):
    __slots__ = ("document", "editedLocally", "deletedLocally", "renamedLocally")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    EDITEDLOCALLY_FIELD_NUMBER: _ClassVar[int]
    DELETEDLOCALLY_FIELD_NUMBER: _ClassVar[int]
    RENAMEDLOCALLY_FIELD_NUMBER: _ClassVar[int]
    document: DocumentTO
    editedLocally: bool
    deletedLocally: bool
    renamedLocally: bool
    def __init__(self, document: _Optional[_Union[DocumentTO, _Mapping]] = ..., editedLocally: bool = ..., deletedLocally: bool = ..., renamedLocally: bool = ...) -> None: ...

class CloudDocumentIDOrdering(_message.Message):
    __slots__ = ("idOrdering",)
    IDORDERING_FIELD_NUMBER: _ClassVar[int]
    idOrdering: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, idOrdering: _Optional[_Iterable[str]] = ...) -> None: ...

class CachedCloudDocumentProperties(_message.Message):
    __slots__ = ("cachedCloudDocumentPropertyList",)
    CACHEDCLOUDDOCUMENTPROPERTYLIST_FIELD_NUMBER: _ClassVar[int]
    cachedCloudDocumentPropertyList: _containers.RepeatedCompositeFieldContainer[CachedCloudDocumentProperty]
    def __init__(self, cachedCloudDocumentPropertyList: _Optional[_Iterable[_Union[CachedCloudDocumentProperty, _Mapping]]] = ...) -> None: ...

class CachedCloudDocumentProperty(_message.Message):
    __slots__ = ("documentId", "lastOpenTime", "fullPath")
    DOCUMENTID_FIELD_NUMBER: _ClassVar[int]
    LASTOPENTIME_FIELD_NUMBER: _ClassVar[int]
    FULLPATH_FIELD_NUMBER: _ClassVar[int]
    documentId: str
    lastOpenTime: int
    fullPath: str
    def __init__(self, documentId: _Optional[str] = ..., lastOpenTime: _Optional[int] = ..., fullPath: _Optional[str] = ...) -> None: ...

class CoSketchCachedAssetInfo(_message.Message):
    __slots__ = ("cachedAssetTOs",)
    CACHEDASSETTOS_FIELD_NUMBER: _ClassVar[int]
    cachedAssetTOs: _containers.RepeatedCompositeFieldContainer[CoSketchCachedAssetTO]
    def __init__(self, cachedAssetTOs: _Optional[_Iterable[_Union[CoSketchCachedAssetTO, _Mapping]]] = ...) -> None: ...

class CoSketchCachedAssetTO(_message.Message):
    __slots__ = ("roomId", "size")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    size: int
    def __init__(self, roomId: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class BatchedBytesData(_message.Message):
    __slots__ = ("responseData",)
    RESPONSEDATA_FIELD_NUMBER: _ClassVar[int]
    responseData: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, responseData: _Optional[_Iterable[bytes]] = ...) -> None: ...

class CoSketchRecordingTO(_message.Message):
    __slots__ = ("recordingId", "roomId", "ownerId", "queryIdType", "startRecordingTime", "endRecordingTime", "expiryTimeSecs", "replayStatus", "replayLastFlushTime", "replayFinalCounter")
    RECORDINGID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNERID_FIELD_NUMBER: _ClassVar[int]
    QUERYIDTYPE_FIELD_NUMBER: _ClassVar[int]
    STARTRECORDINGTIME_FIELD_NUMBER: _ClassVar[int]
    ENDRECORDINGTIME_FIELD_NUMBER: _ClassVar[int]
    EXPIRYTIMESECS_FIELD_NUMBER: _ClassVar[int]
    REPLAYSTATUS_FIELD_NUMBER: _ClassVar[int]
    REPLAYLASTFLUSHTIME_FIELD_NUMBER: _ClassVar[int]
    REPLAYFINALCOUNTER_FIELD_NUMBER: _ClassVar[int]
    recordingId: str
    roomId: str
    ownerId: str
    queryIdType: IdType
    startRecordingTime: int
    endRecordingTime: int
    expiryTimeSecs: int
    replayStatus: CoSketchReplayStatus
    replayLastFlushTime: int
    replayFinalCounter: int
    def __init__(self, recordingId: _Optional[str] = ..., roomId: _Optional[str] = ..., ownerId: _Optional[str] = ..., queryIdType: _Optional[_Union[IdType, str]] = ..., startRecordingTime: _Optional[int] = ..., endRecordingTime: _Optional[int] = ..., expiryTimeSecs: _Optional[int] = ..., replayStatus: _Optional[_Union[CoSketchReplayStatus, str]] = ..., replayLastFlushTime: _Optional[int] = ..., replayFinalCounter: _Optional[int] = ...) -> None: ...

class GSDeepLinkTO(_message.Message):
    __slots__ = ("linkType", "deepLinkId", "oneTimeToken", "targetAppType", "enableScreenConsole")
    LINKTYPE_FIELD_NUMBER: _ClassVar[int]
    DEEPLINKID_FIELD_NUMBER: _ClassVar[int]
    ONETIMETOKEN_FIELD_NUMBER: _ClassVar[int]
    TARGETAPPTYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLESCREENCONSOLE_FIELD_NUMBER: _ClassVar[int]
    linkType: GSDeepLinkType
    deepLinkId: str
    oneTimeToken: str
    targetAppType: GSDeepLinkTargetAppType
    enableScreenConsole: bool
    def __init__(self, linkType: _Optional[_Union[GSDeepLinkType, str]] = ..., deepLinkId: _Optional[str] = ..., oneTimeToken: _Optional[str] = ..., targetAppType: _Optional[_Union[GSDeepLinkTargetAppType, str]] = ..., enableScreenConsole: bool = ...) -> None: ...

class CommunityStudio(_message.Message):
    __slots__ = ("id", "displayName", "createdOn", "spaceId", "description", "memberships")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    id: str
    displayName: str
    createdOn: int
    spaceId: SpaceId
    description: str
    memberships: _containers.RepeatedCompositeFieldContainer[CommunityStudioMembership]
    def __init__(self, id: _Optional[str] = ..., displayName: _Optional[str] = ..., createdOn: _Optional[int] = ..., spaceId: _Optional[_Union[SpaceId, _Mapping]] = ..., description: _Optional[str] = ..., memberships: _Optional[_Iterable[_Union[CommunityStudioMembership, _Mapping]]] = ...) -> None: ...

class GSVideoAsset(_message.Message):
    __slots__ = ("title", "downloadUrl", "docTO", "isPublicContent")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    DOCTO_FIELD_NUMBER: _ClassVar[int]
    ISPUBLICCONTENT_FIELD_NUMBER: _ClassVar[int]
    title: str
    downloadUrl: str
    docTO: DocumentTO
    isPublicContent: bool
    def __init__(self, title: _Optional[str] = ..., downloadUrl: _Optional[str] = ..., docTO: _Optional[_Union[DocumentTO, _Mapping]] = ..., isPublicContent: bool = ...) -> None: ...

class GSVideoAssetList(_message.Message):
    __slots__ = ("videoAssetList",)
    VIDEOASSETLIST_FIELD_NUMBER: _ClassVar[int]
    videoAssetList: _containers.RepeatedCompositeFieldContainer[GSVideoAsset]
    def __init__(self, videoAssetList: _Optional[_Iterable[_Union[GSVideoAsset, _Mapping]]] = ...) -> None: ...

class CoSketchConfig(_message.Message):
    __slots__ = ("NetPrefab", "SingleplayerPrefab", "ReliableRpcTimeoutFrameCount", "ReliableRpcTimeoutMS", "ReliableRpcLatencyWarningMS", "ReliableRpcCheckInterval", "ListRoomRefreshIntervalMS", "PollStrokesIntervalMS", "MinimumOutboundFPS", "ReliableRpcLatencyWarningFrameCount", "HeartBeatIntervalMS", "InitHeartBeatCompensationMS", "CollabMaxReadIdle", "LatencyStatsPrintIntervalMS", "ReliableRpcMaxQueueSize")
    NETPREFAB_FIELD_NUMBER: _ClassVar[int]
    SINGLEPLAYERPREFAB_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCTIMEOUTFRAMECOUNT_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCTIMEOUTMS_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCLATENCYWARNINGMS_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCCHECKINTERVAL_FIELD_NUMBER: _ClassVar[int]
    LISTROOMREFRESHINTERVALMS_FIELD_NUMBER: _ClassVar[int]
    POLLSTROKESINTERVALMS_FIELD_NUMBER: _ClassVar[int]
    MINIMUMOUTBOUNDFPS_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCLATENCYWARNINGFRAMECOUNT_FIELD_NUMBER: _ClassVar[int]
    HEARTBEATINTERVALMS_FIELD_NUMBER: _ClassVar[int]
    INITHEARTBEATCOMPENSATIONMS_FIELD_NUMBER: _ClassVar[int]
    COLLABMAXREADIDLE_FIELD_NUMBER: _ClassVar[int]
    LATENCYSTATSPRINTINTERVALMS_FIELD_NUMBER: _ClassVar[int]
    RELIABLERPCMAXQUEUESIZE_FIELD_NUMBER: _ClassVar[int]
    NetPrefab: str
    SingleplayerPrefab: str
    ReliableRpcTimeoutFrameCount: int
    ReliableRpcTimeoutMS: int
    ReliableRpcLatencyWarningMS: int
    ReliableRpcCheckInterval: int
    ListRoomRefreshIntervalMS: int
    PollStrokesIntervalMS: int
    MinimumOutboundFPS: int
    ReliableRpcLatencyWarningFrameCount: int
    HeartBeatIntervalMS: int
    InitHeartBeatCompensationMS: int
    CollabMaxReadIdle: int
    LatencyStatsPrintIntervalMS: int
    ReliableRpcMaxQueueSize: int
    def __init__(self, NetPrefab: _Optional[str] = ..., SingleplayerPrefab: _Optional[str] = ..., ReliableRpcTimeoutFrameCount: _Optional[int] = ..., ReliableRpcTimeoutMS: _Optional[int] = ..., ReliableRpcLatencyWarningMS: _Optional[int] = ..., ReliableRpcCheckInterval: _Optional[int] = ..., ListRoomRefreshIntervalMS: _Optional[int] = ..., PollStrokesIntervalMS: _Optional[int] = ..., MinimumOutboundFPS: _Optional[int] = ..., ReliableRpcLatencyWarningFrameCount: _Optional[int] = ..., HeartBeatIntervalMS: _Optional[int] = ..., InitHeartBeatCompensationMS: _Optional[int] = ..., CollabMaxReadIdle: _Optional[int] = ..., LatencyStatsPrintIntervalMS: _Optional[int] = ..., ReliableRpcMaxQueueSize: _Optional[int] = ...) -> None: ...

class GlobalClientConfig(_message.Message):
    __slots__ = ("CloudLoggerConfig", "AnalyticsConfig", "webSocketProbingConfig")
    CLOUDLOGGERCONFIG_FIELD_NUMBER: _ClassVar[int]
    ANALYTICSCONFIG_FIELD_NUMBER: _ClassVar[int]
    WEBSOCKETPROBINGCONFIG_FIELD_NUMBER: _ClassVar[int]
    CloudLoggerConfig: CloudLoggerConfig
    AnalyticsConfig: AnalyticsConfig
    webSocketProbingConfig: WebSocketProbingConfig
    def __init__(self, CloudLoggerConfig: _Optional[_Union[CloudLoggerConfig, _Mapping]] = ..., AnalyticsConfig: _Optional[_Union[AnalyticsConfig, _Mapping]] = ..., webSocketProbingConfig: _Optional[_Union[WebSocketProbingConfig, _Mapping]] = ...) -> None: ...

class CloudLoggerConfig(_message.Message):
    __slots__ = ("EnableCloudLogger", "EndPoint", "DataDiscardThreshold", "NormalRetryInternalMS", "LazyRetryInternalMS", "MaxNormalRetry")
    ENABLECLOUDLOGGER_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    DATADISCARDTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    NORMALRETRYINTERNALMS_FIELD_NUMBER: _ClassVar[int]
    LAZYRETRYINTERNALMS_FIELD_NUMBER: _ClassVar[int]
    MAXNORMALRETRY_FIELD_NUMBER: _ClassVar[int]
    EnableCloudLogger: bool
    EndPoint: str
    DataDiscardThreshold: int
    NormalRetryInternalMS: int
    LazyRetryInternalMS: int
    MaxNormalRetry: int
    def __init__(self, EnableCloudLogger: bool = ..., EndPoint: _Optional[str] = ..., DataDiscardThreshold: _Optional[int] = ..., NormalRetryInternalMS: _Optional[int] = ..., LazyRetryInternalMS: _Optional[int] = ..., MaxNormalRetry: _Optional[int] = ...) -> None: ...

class AnalyticsConfig(_message.Message):
    __slots__ = ("Enabled", "EndPoint", "DataDiscardThreshold", "NormalRetryInternalMS", "LazyRetryInternalMS", "MaxNormalRetry")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    DATADISCARDTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    NORMALRETRYINTERNALMS_FIELD_NUMBER: _ClassVar[int]
    LAZYRETRYINTERNALMS_FIELD_NUMBER: _ClassVar[int]
    MAXNORMALRETRY_FIELD_NUMBER: _ClassVar[int]
    Enabled: bool
    EndPoint: str
    DataDiscardThreshold: int
    NormalRetryInternalMS: int
    LazyRetryInternalMS: int
    MaxNormalRetry: int
    def __init__(self, Enabled: bool = ..., EndPoint: _Optional[str] = ..., DataDiscardThreshold: _Optional[int] = ..., NormalRetryInternalMS: _Optional[int] = ..., LazyRetryInternalMS: _Optional[int] = ..., MaxNormalRetry: _Optional[int] = ...) -> None: ...

class WebSocketProbingConfig(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class ServerControlledConfig(_message.Message):
    __slots__ = ("CoSketchConfig", "GlobalConfig")
    COSKETCHCONFIG_FIELD_NUMBER: _ClassVar[int]
    GLOBALCONFIG_FIELD_NUMBER: _ClassVar[int]
    CoSketchConfig: CoSketchConfig
    GlobalConfig: GlobalClientConfig
    def __init__(self, CoSketchConfig: _Optional[_Union[CoSketchConfig, _Mapping]] = ..., GlobalConfig: _Optional[_Union[GlobalClientConfig, _Mapping]] = ...) -> None: ...
