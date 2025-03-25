import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckForClientAppUpdateResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CheckForClientAppUpdateResponseCode_Unknown: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_ClientAlreadyUpToDate: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_UrgentUpdateAvailable: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_DelayableUpdateAvailable: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_UpdateOnClientOSUnsupported: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_FailedToParseVersionNumber: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_UpdateProcessForBuildProfileUnsupported: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_ServerFailedToGetUpdateVersion: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_ServerFailedToParseUpdateVersion: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_ServerFailedToGenerateUpdateDownloadURL: _ClassVar[CheckForClientAppUpdateResponseCode]
    CheckForClientAppUpdateResponseCode_ServerFailedWithCustomResponse: _ClassVar[CheckForClientAppUpdateResponseCode]
CheckForClientAppUpdateResponseCode_Unknown: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_ClientAlreadyUpToDate: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_UrgentUpdateAvailable: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_DelayableUpdateAvailable: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_UpdateOnClientOSUnsupported: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_FailedToParseVersionNumber: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_UpdateProcessForBuildProfileUnsupported: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_ServerFailedToGetUpdateVersion: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_ServerFailedToParseUpdateVersion: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_ServerFailedToGenerateUpdateDownloadURL: CheckForClientAppUpdateResponseCode
CheckForClientAppUpdateResponseCode_ServerFailedWithCustomResponse: CheckForClientAppUpdateResponseCode

class CheckForClientAppUpdateRequest(_message.Message):
    __slots__ = ("clientAppFullVersionString", "clientAppVersionNumber", "clientAppBuildProfile", "clientSystemOs", "clientPlatform", "clientAppInstallationPath", "clientInstallPathRequiresAdmin")
    CLIENTAPPFULLVERSIONSTRING_FIELD_NUMBER: _ClassVar[int]
    CLIENTAPPVERSIONNUMBER_FIELD_NUMBER: _ClassVar[int]
    CLIENTAPPBUILDPROFILE_FIELD_NUMBER: _ClassVar[int]
    CLIENTSYSTEMOS_FIELD_NUMBER: _ClassVar[int]
    CLIENTPLATFORM_FIELD_NUMBER: _ClassVar[int]
    CLIENTAPPINSTALLATIONPATH_FIELD_NUMBER: _ClassVar[int]
    CLIENTINSTALLPATHREQUIRESADMIN_FIELD_NUMBER: _ClassVar[int]
    clientAppFullVersionString: str
    clientAppVersionNumber: str
    clientAppBuildProfile: str
    clientSystemOs: str
    clientPlatform: str
    clientAppInstallationPath: str
    clientInstallPathRequiresAdmin: bool
    def __init__(self, clientAppFullVersionString: _Optional[str] = ..., clientAppVersionNumber: _Optional[str] = ..., clientAppBuildProfile: _Optional[str] = ..., clientSystemOs: _Optional[str] = ..., clientPlatform: _Optional[str] = ..., clientAppInstallationPath: _Optional[str] = ..., clientInstallPathRequiresAdmin: bool = ...) -> None: ...

class CheckForClientAppUpdateResponse(_message.Message):
    __slots__ = ("responseCode", "availableClientAppUpdateVersionNumber", "clientAppUpdateMSIDownloadURL", "delayTimeInHoursTillNextUpdateReminder", "customResponseMessage")
    RESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLECLIENTAPPUPDATEVERSIONNUMBER_FIELD_NUMBER: _ClassVar[int]
    CLIENTAPPUPDATEMSIDOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    DELAYTIMEINHOURSTILLNEXTUPDATEREMINDER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMRESPONSEMESSAGE_FIELD_NUMBER: _ClassVar[int]
    responseCode: CheckForClientAppUpdateResponseCode
    availableClientAppUpdateVersionNumber: str
    clientAppUpdateMSIDownloadURL: str
    delayTimeInHoursTillNextUpdateReminder: int
    customResponseMessage: str
    def __init__(self, responseCode: _Optional[_Union[CheckForClientAppUpdateResponseCode, str]] = ..., availableClientAppUpdateVersionNumber: _Optional[str] = ..., clientAppUpdateMSIDownloadURL: _Optional[str] = ..., delayTimeInHoursTillNextUpdateReminder: _Optional[int] = ..., customResponseMessage: _Optional[str] = ...) -> None: ...
