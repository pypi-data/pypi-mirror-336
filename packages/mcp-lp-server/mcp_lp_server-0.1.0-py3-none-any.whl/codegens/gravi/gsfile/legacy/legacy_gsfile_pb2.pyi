from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model.common import sketch_interactions_pb2 as _sketch_interactions_pb2
import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.models import preferences_pb2 as _preferences_pb2
from gravi.gsfile.layergroup.persistence import layer_group_pb2 as _layer_group_pb2
from gravi.gsfile.metadata.persistence import metadata_pb2 as _metadata_pb2
from gravi.gsfile.asset.persistence import asset_pb2 as _asset_pb2
from gravi.gsfile import sketch_gsfile_pb2 as _sketch_gsfile_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GSFile(_message.Message):
    __slots__ = ("Version", "Layers", "RepairVersion", "groups", "layerGrouping", "materials", "activeLayerGuid", "lastUsedOrientation", "userChoseThumbnailOrientation", "environment", "deprecatedViewPoints", "spatialAnchorInformation", "layerGroups", "metadata", "assets")
    class LayerGroupingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    REPAIRVERSION_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPING_FIELD_NUMBER: _ClassVar[int]
    MATERIALS_FIELD_NUMBER: _ClassVar[int]
    ACTIVELAYERGUID_FIELD_NUMBER: _ClassVar[int]
    LASTUSEDORIENTATION_FIELD_NUMBER: _ClassVar[int]
    USERCHOSETHUMBNAILORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDVIEWPOINTS_FIELD_NUMBER: _ClassVar[int]
    SPATIALANCHORINFORMATION_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUPS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    Version: int
    Layers: _containers.RepeatedCompositeFieldContainer[_sketch_gsfile_pb2.Layer]
    RepairVersion: int
    groups: _containers.RepeatedCompositeFieldContainer[_sketch_gsfile_pb2.NestedGroupRelationship]
    layerGrouping: _containers.ScalarMap[str, str]
    materials: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DrawMaterial]
    activeLayerGuid: str
    lastUsedOrientation: _gravi_unity_pb2.TransformTO
    userChoseThumbnailOrientation: _gravi_unity_pb2.ThumbnailCameraTO
    environment: _gravi_model_pb2.EnvironmentTO
    deprecatedViewPoints: _containers.RepeatedCompositeFieldContainer[_sketch_common_pb2.DeprecatedViewPointModelTO]
    spatialAnchorInformation: _sketch_common_pb2.PersistentSpatialAnchorInformation
    layerGroups: _containers.RepeatedCompositeFieldContainer[_layer_group_pb2.LayerGroupModel]
    metadata: _metadata_pb2.SketchMetadataModel
    assets: _containers.RepeatedCompositeFieldContainer[_asset_pb2.AssetModel]
    def __init__(self, Version: _Optional[int] = ..., Layers: _Optional[_Iterable[_Union[_sketch_gsfile_pb2.Layer, _Mapping]]] = ..., RepairVersion: _Optional[int] = ..., groups: _Optional[_Iterable[_Union[_sketch_gsfile_pb2.NestedGroupRelationship, _Mapping]]] = ..., layerGrouping: _Optional[_Mapping[str, str]] = ..., materials: _Optional[_Iterable[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]]] = ..., activeLayerGuid: _Optional[str] = ..., lastUsedOrientation: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ..., userChoseThumbnailOrientation: _Optional[_Union[_gravi_unity_pb2.ThumbnailCameraTO, _Mapping]] = ..., environment: _Optional[_Union[_gravi_model_pb2.EnvironmentTO, _Mapping]] = ..., deprecatedViewPoints: _Optional[_Iterable[_Union[_sketch_common_pb2.DeprecatedViewPointModelTO, _Mapping]]] = ..., spatialAnchorInformation: _Optional[_Union[_sketch_common_pb2.PersistentSpatialAnchorInformation, _Mapping]] = ..., layerGroups: _Optional[_Iterable[_Union[_layer_group_pb2.LayerGroupModel, _Mapping]]] = ..., metadata: _Optional[_Union[_metadata_pb2.SketchMetadataModel, _Mapping]] = ..., assets: _Optional[_Iterable[_Union[_asset_pb2.AssetModel, _Mapping]]] = ...) -> None: ...
