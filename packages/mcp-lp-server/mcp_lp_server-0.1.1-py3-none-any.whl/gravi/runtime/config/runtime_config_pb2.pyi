from gravi.common import gravi_common_pb2 as _gravi_common_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LLTrace: _ClassVar[LogLevel]
    LLDebug: _ClassVar[LogLevel]
    LLInfo: _ClassVar[LogLevel]
    LLWarn: _ClassVar[LogLevel]
    LLError: _ClassVar[LogLevel]
    LLAll: _ClassVar[LogLevel]

class ShadowQuality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SQDisable: _ClassVar[ShadowQuality]
    SQHardOnly: _ClassVar[ShadowQuality]
    SQAll: _ClassVar[ShadowQuality]

class ShadowResolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SRLow: _ClassVar[ShadowResolution]
    SRMedium: _ClassVar[ShadowResolution]
    SRHigh: _ClassVar[ShadowResolution]
    SRVeryHigh: _ClassVar[ShadowResolution]

class LicenseValidatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LVCloudAuth: _ClassVar[LicenseValidatorType]
    LVSteam: _ClassVar[LicenseValidatorType]
    LVFixed: _ClassVar[LicenseValidatorType]
    LVDummy: _ClassVar[LicenseValidatorType]
LLTrace: LogLevel
LLDebug: LogLevel
LLInfo: LogLevel
LLWarn: LogLevel
LLError: LogLevel
LLAll: LogLevel
SQDisable: ShadowQuality
SQHardOnly: ShadowQuality
SQAll: ShadowQuality
SRLow: ShadowResolution
SRMedium: ShadowResolution
SRHigh: ShadowResolution
SRVeryHigh: ShadowResolution
LVCloudAuth: LicenseValidatorType
LVSteam: LicenseValidatorType
LVFixed: LicenseValidatorType
LVDummy: LicenseValidatorType

class RuntimeConfig(_message.Message):
    __slots__ = ("configName", "logLevel", "ReferenceImagePresets", "EnvironmentScenes", "SlackWebhookURL", "RiggedPrefabs", "StockContentPrefabs", "ServerConfig", "LicenseConfig", "AutoSaveConfig", "BuiltInMaterialConfig", "FeatureFlags", "AlertConfig", "QualityConfig", "DebugConfig", "useProdPatches", "VRController", "ServerControlledConfig", "signature")
    CONFIGNAME_FIELD_NUMBER: _ClassVar[int]
    LOGLEVEL_FIELD_NUMBER: _ClassVar[int]
    REFERENCEIMAGEPRESETS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTSCENES_FIELD_NUMBER: _ClassVar[int]
    SLACKWEBHOOKURL_FIELD_NUMBER: _ClassVar[int]
    RIGGEDPREFABS_FIELD_NUMBER: _ClassVar[int]
    STOCKCONTENTPREFABS_FIELD_NUMBER: _ClassVar[int]
    SERVERCONFIG_FIELD_NUMBER: _ClassVar[int]
    LICENSECONFIG_FIELD_NUMBER: _ClassVar[int]
    AUTOSAVECONFIG_FIELD_NUMBER: _ClassVar[int]
    BUILTINMATERIALCONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATUREFLAGS_FIELD_NUMBER: _ClassVar[int]
    ALERTCONFIG_FIELD_NUMBER: _ClassVar[int]
    QUALITYCONFIG_FIELD_NUMBER: _ClassVar[int]
    DEBUGCONFIG_FIELD_NUMBER: _ClassVar[int]
    USEPRODPATCHES_FIELD_NUMBER: _ClassVar[int]
    VRCONTROLLER_FIELD_NUMBER: _ClassVar[int]
    SERVERCONTROLLEDCONFIG_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    configName: str
    logLevel: LogLevel
    ReferenceImagePresets: _containers.RepeatedScalarFieldContainer[str]
    EnvironmentScenes: _containers.RepeatedScalarFieldContainer[str]
    SlackWebhookURL: str
    RiggedPrefabs: RiggedPrefabs
    StockContentPrefabs: StockContentPrefabs
    ServerConfig: ServerConfig
    LicenseConfig: LicenseConfig
    AutoSaveConfig: AutoSaveConfig
    BuiltInMaterialConfig: BuiltInMaterialConfig
    FeatureFlags: FeatureFlags
    AlertConfig: AlertConfig
    QualityConfig: QualityConfiguration
    DebugConfig: DebugConfiguration
    useProdPatches: bool
    VRController: str
    ServerControlledConfig: _gravi_model_pb2.ServerControlledConfig
    signature: bytes
    def __init__(self, configName: _Optional[str] = ..., logLevel: _Optional[_Union[LogLevel, str]] = ..., ReferenceImagePresets: _Optional[_Iterable[str]] = ..., EnvironmentScenes: _Optional[_Iterable[str]] = ..., SlackWebhookURL: _Optional[str] = ..., RiggedPrefabs: _Optional[_Union[RiggedPrefabs, _Mapping]] = ..., StockContentPrefabs: _Optional[_Union[StockContentPrefabs, _Mapping]] = ..., ServerConfig: _Optional[_Union[ServerConfig, _Mapping]] = ..., LicenseConfig: _Optional[_Union[LicenseConfig, _Mapping]] = ..., AutoSaveConfig: _Optional[_Union[AutoSaveConfig, _Mapping]] = ..., BuiltInMaterialConfig: _Optional[_Union[BuiltInMaterialConfig, _Mapping]] = ..., FeatureFlags: _Optional[_Union[FeatureFlags, _Mapping]] = ..., AlertConfig: _Optional[_Union[AlertConfig, _Mapping]] = ..., QualityConfig: _Optional[_Union[QualityConfiguration, _Mapping]] = ..., DebugConfig: _Optional[_Union[DebugConfiguration, _Mapping]] = ..., useProdPatches: bool = ..., VRController: _Optional[str] = ..., ServerControlledConfig: _Optional[_Union[_gravi_model_pb2.ServerControlledConfig, _Mapping]] = ..., signature: _Optional[bytes] = ...) -> None: ...

class RiggedPrefabs(_message.Message):
    __slots__ = ("RiggedCarPrefab", "FemaleRiggedMannequinPrefab", "MaleRiggedMannequinPrefab")
    RIGGEDCARPREFAB_FIELD_NUMBER: _ClassVar[int]
    FEMALERIGGEDMANNEQUINPREFAB_FIELD_NUMBER: _ClassVar[int]
    MALERIGGEDMANNEQUINPREFAB_FIELD_NUMBER: _ClassVar[int]
    RiggedCarPrefab: str
    FemaleRiggedMannequinPrefab: str
    MaleRiggedMannequinPrefab: str
    def __init__(self, RiggedCarPrefab: _Optional[str] = ..., FemaleRiggedMannequinPrefab: _Optional[str] = ..., MaleRiggedMannequinPrefab: _Optional[str] = ...) -> None: ...

class StockContentPrefabs(_message.Message):
    __slots__ = ("MannequinPrefab", "HeadPrefab")
    MANNEQUINPREFAB_FIELD_NUMBER: _ClassVar[int]
    HEADPREFAB_FIELD_NUMBER: _ClassVar[int]
    MannequinPrefab: str
    HeadPrefab: str
    def __init__(self, MannequinPrefab: _Optional[str] = ..., HeadPrefab: _Optional[str] = ...) -> None: ...

class AutoSaveConfig(_message.Message):
    __slots__ = ("MaxCacheSizeMB", "MaxFiles")
    MAXCACHESIZEMB_FIELD_NUMBER: _ClassVar[int]
    MAXFILES_FIELD_NUMBER: _ClassVar[int]
    MaxCacheSizeMB: int
    MaxFiles: int
    def __init__(self, MaxCacheSizeMB: _Optional[int] = ..., MaxFiles: _Optional[int] = ...) -> None: ...

class BuiltInMaterialConfig(_message.Message):
    __slots__ = ("DefaultMaterial", "BaseMaterials")
    DEFAULTMATERIAL_FIELD_NUMBER: _ClassVar[int]
    BASEMATERIALS_FIELD_NUMBER: _ClassVar[int]
    DefaultMaterial: str
    BaseMaterials: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, DefaultMaterial: _Optional[str] = ..., BaseMaterials: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureFlags(_message.Message):
    __slots__ = ("onlineEnabled", "metricsEnabled", "isDemo", "csvUsageStats", "supportMultiLanguages", "viewerBetaFeaturesEnabled", "gsAnalyticsEnabled", "vrConsole")
    ONLINEENABLED_FIELD_NUMBER: _ClassVar[int]
    METRICSENABLED_FIELD_NUMBER: _ClassVar[int]
    ISDEMO_FIELD_NUMBER: _ClassVar[int]
    CSVUSAGESTATS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTMULTILANGUAGES_FIELD_NUMBER: _ClassVar[int]
    VIEWERBETAFEATURESENABLED_FIELD_NUMBER: _ClassVar[int]
    GSANALYTICSENABLED_FIELD_NUMBER: _ClassVar[int]
    VRCONSOLE_FIELD_NUMBER: _ClassVar[int]
    onlineEnabled: bool
    metricsEnabled: bool
    isDemo: bool
    csvUsageStats: bool
    supportMultiLanguages: bool
    viewerBetaFeaturesEnabled: bool
    gsAnalyticsEnabled: bool
    vrConsole: bool
    def __init__(self, onlineEnabled: bool = ..., metricsEnabled: bool = ..., isDemo: bool = ..., csvUsageStats: bool = ..., supportMultiLanguages: bool = ..., viewerBetaFeaturesEnabled: bool = ..., gsAnalyticsEnabled: bool = ..., vrConsole: bool = ...) -> None: ...

class AlertConfig(_message.Message):
    __slots__ = ("latencyAlertThreshold", "latencyAlertIntervalMS")
    LATENCYALERTTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    LATENCYALERTINTERVALMS_FIELD_NUMBER: _ClassVar[int]
    latencyAlertThreshold: int
    latencyAlertIntervalMS: int
    def __init__(self, latencyAlertThreshold: _Optional[int] = ..., latencyAlertIntervalMS: _Optional[int] = ...) -> None: ...

class QualityConfiguration(_message.Message):
    __slots__ = ("doLevelOfDetailRendering", "urpQualityLevel")
    DOLEVELOFDETAILRENDERING_FIELD_NUMBER: _ClassVar[int]
    URPQUALITYLEVEL_FIELD_NUMBER: _ClassVar[int]
    doLevelOfDetailRendering: bool
    urpQualityLevel: int
    def __init__(self, doLevelOfDetailRendering: bool = ..., urpQualityLevel: _Optional[int] = ...) -> None: ...

class DebugConfiguration(_message.Message):
    __slots__ = ("displayCommitHash",)
    DISPLAYCOMMITHASH_FIELD_NUMBER: _ClassVar[int]
    displayCommitHash: bool
    def __init__(self, displayCommitHash: bool = ...) -> None: ...

class ServerConfig(_message.Message):
    __slots__ = ("serverHost", "protocol", "certificateValidation")
    SERVERHOST_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATEVALIDATION_FIELD_NUMBER: _ClassVar[int]
    serverHost: _containers.RepeatedCompositeFieldContainer[_gravi_common_pb2.HostTO]
    protocol: str
    certificateValidation: bool
    def __init__(self, serverHost: _Optional[_Iterable[_Union[_gravi_common_pb2.HostTO, _Mapping]]] = ..., protocol: _Optional[str] = ..., certificateValidation: bool = ...) -> None: ...

class LicenseConfig(_message.Message):
    __slots__ = ("CurrentPriceTier", "IsTrial", "RenewIntervalSecs", "NumOfRetries", "SecondsBeforeQuitDuringSketch", "ValidatorType", "HardExpiryDate")
    CURRENTPRICETIER_FIELD_NUMBER: _ClassVar[int]
    ISTRIAL_FIELD_NUMBER: _ClassVar[int]
    RENEWINTERVALSECS_FIELD_NUMBER: _ClassVar[int]
    NUMOFRETRIES_FIELD_NUMBER: _ClassVar[int]
    SECONDSBEFOREQUITDURINGSKETCH_FIELD_NUMBER: _ClassVar[int]
    VALIDATORTYPE_FIELD_NUMBER: _ClassVar[int]
    HARDEXPIRYDATE_FIELD_NUMBER: _ClassVar[int]
    CurrentPriceTier: _gravi_model_pb2.PriceTier
    IsTrial: bool
    RenewIntervalSecs: int
    NumOfRetries: int
    SecondsBeforeQuitDuringSketch: int
    ValidatorType: LicenseValidatorType
    HardExpiryDate: str
    def __init__(self, CurrentPriceTier: _Optional[_Union[_gravi_model_pb2.PriceTier, str]] = ..., IsTrial: bool = ..., RenewIntervalSecs: _Optional[int] = ..., NumOfRetries: _Optional[int] = ..., SecondsBeforeQuitDuringSketch: _Optional[int] = ..., ValidatorType: _Optional[_Union[LicenseValidatorType, str]] = ..., HardExpiryDate: _Optional[str] = ...) -> None: ...
