import gs_options_pb2 as _gs_options_pb2
from gravi.common import gravi_common_pb2 as _gravi_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReleaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RELEASE_TYPE_UNSET: _ClassVar[ReleaseType]
    PROMOTED_ENTERPRISE: _ClassVar[ReleaseType]

class ReleaseBundleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED_BUNDLE: _ClassVar[ReleaseBundleType]
    NO_BUNDLE: _ClassVar[ReleaseBundleType]
    MSI_BUNDLE: _ClassVar[ReleaseBundleType]
RELEASE_TYPE_UNSET: ReleaseType
PROMOTED_ENTERPRISE: ReleaseType
UNDEFINED_BUNDLE: ReleaseBundleType
NO_BUNDLE: ReleaseBundleType
MSI_BUNDLE: ReleaseBundleType

class ReleaseVersion(_message.Message):
    __slots__ = ("relative_path", "version", "timestamp", "os", "arch", "release_type", "release_bundle_type")
    RELATIVE_PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    RELEASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_BUNDLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    relative_path: str
    version: str
    timestamp: int
    os: _gravi_common_pb2.Os
    arch: _gravi_common_pb2.Arch
    release_type: ReleaseType
    release_bundle_type: ReleaseBundleType
    def __init__(self, relative_path: _Optional[str] = ..., version: _Optional[str] = ..., timestamp: _Optional[int] = ..., os: _Optional[_Union[_gravi_common_pb2.Os, str]] = ..., arch: _Optional[_Union[_gravi_common_pb2.Arch, str]] = ..., release_type: _Optional[_Union[ReleaseType, str]] = ..., release_bundle_type: _Optional[_Union[ReleaseBundleType, str]] = ...) -> None: ...

class Releases(_message.Message):
    __slots__ = ("versions",)
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[ReleaseVersion]
    def __init__(self, versions: _Optional[_Iterable[_Union[ReleaseVersion, _Mapping]]] = ...) -> None: ...
