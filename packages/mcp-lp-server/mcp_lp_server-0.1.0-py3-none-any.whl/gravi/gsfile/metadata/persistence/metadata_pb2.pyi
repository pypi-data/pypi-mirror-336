import gs_options_pb2 as _gs_options_pb2
from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SketchMetadataModel(_message.Message):
    __slots__ = ("version", "activeLayerGuid", "lastUsedOrientation", "userChoseThumbnailOrientation", "environment", "spatialAnchorInformation", "repairVersion", "sectionViewData")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ACTIVELAYERGUID_FIELD_NUMBER: _ClassVar[int]
    LASTUSEDORIENTATION_FIELD_NUMBER: _ClassVar[int]
    USERCHOSETHUMBNAILORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SPATIALANCHORINFORMATION_FIELD_NUMBER: _ClassVar[int]
    REPAIRVERSION_FIELD_NUMBER: _ClassVar[int]
    SECTIONVIEWDATA_FIELD_NUMBER: _ClassVar[int]
    version: int
    activeLayerGuid: str
    lastUsedOrientation: _gravi_unity_pb2.TransformTO
    userChoseThumbnailOrientation: _gravi_unity_pb2.ThumbnailCameraTO
    environment: _gravi_model_pb2.EnvironmentTO
    spatialAnchorInformation: _sketch_common_pb2.PersistentSpatialAnchorInformation
    repairVersion: int
    sectionViewData: _sketch_common_pb2.SectionViewData
    def __init__(self, version: _Optional[int] = ..., activeLayerGuid: _Optional[str] = ..., lastUsedOrientation: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., userChoseThumbnailOrientation: _Optional[_Union[_gravi_unity_pb2.ThumbnailCameraTO, _Mapping]] = ..., environment: _Optional[_Union[_gravi_model_pb2.EnvironmentTO, _Mapping]] = ..., spatialAnchorInformation: _Optional[_Union[_sketch_common_pb2.PersistentSpatialAnchorInformation, _Mapping]] = ..., repairVersion: _Optional[int] = ..., sectionViewData: _Optional[_Union[_sketch_common_pb2.SectionViewData, _Mapping]] = ...) -> None: ...
