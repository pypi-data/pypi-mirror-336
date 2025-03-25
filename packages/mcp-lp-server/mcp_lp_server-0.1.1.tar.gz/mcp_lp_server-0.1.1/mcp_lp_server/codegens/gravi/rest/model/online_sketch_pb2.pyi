from gravi.unity import gravi_unity_pb2 as _gravi_unity_pb2
from gravi.rpc import cosketch_rpc_pb2 as _cosketch_rpc_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.gsfile import sketch_gsfile_pb2 as _sketch_gsfile_pb2
from gravi.gsfile.strokelayer.persistence import layer_pb2 as _layer_pb2
from gravi.gsfile.layergroup.persistence import layer_group_pb2 as _layer_group_pb2
from gravi.gsfile.metadata.persistence import metadata_pb2 as _metadata_pb2
from gravi.gsfile.asset.persistence import asset_pb2 as _asset_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateSketchObjectsResponseResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateSketchObjectsResponseResult_Unknown: _ClassVar[UpdateSketchObjectsResponseResult]
    UpdateSketchObjectsResponseResult_Success: _ClassVar[UpdateSketchObjectsResponseResult]
    UpdateSketchObjectsResponseResult_DocumentNotFound: _ClassVar[UpdateSketchObjectsResponseResult]
    UpdateSketchObjectsResponseResult_UpdateOutdated: _ClassVar[UpdateSketchObjectsResponseResult]
    UpdateSketchObjectsResponseResult_StorageLimitExceeded: _ClassVar[UpdateSketchObjectsResponseResult]
UpdateSketchObjectsResponseResult_Unknown: UpdateSketchObjectsResponseResult
UpdateSketchObjectsResponseResult_Success: UpdateSketchObjectsResponseResult
UpdateSketchObjectsResponseResult_DocumentNotFound: UpdateSketchObjectsResponseResult
UpdateSketchObjectsResponseResult_UpdateOutdated: UpdateSketchObjectsResponseResult
UpdateSketchObjectsResponseResult_StorageLimitExceeded: UpdateSketchObjectsResponseResult

class UpdateSketchObjectsRequest(_message.Message):
    __slots__ = ("documentId", "expectedSketchVersion", "sketchStateUpdate")
    DOCUMENTID_FIELD_NUMBER: _ClassVar[int]
    EXPECTEDSKETCHVERSION_FIELD_NUMBER: _ClassVar[int]
    SKETCHSTATEUPDATE_FIELD_NUMBER: _ClassVar[int]
    documentId: str
    expectedSketchVersion: str
    sketchStateUpdate: SketchStateUpdate
    def __init__(self, documentId: _Optional[str] = ..., expectedSketchVersion: _Optional[str] = ..., sketchStateUpdate: _Optional[_Union[SketchStateUpdate, _Mapping]] = ...) -> None: ...

class UpdateSketchObjectsResponse(_message.Message):
    __slots__ = ("result", "currentSketchVersion")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CURRENTSKETCHVERSION_FIELD_NUMBER: _ClassVar[int]
    result: UpdateSketchObjectsResponseResult
    currentSketchVersion: str
    def __init__(self, result: _Optional[_Union[UpdateSketchObjectsResponseResult, str]] = ..., currentSketchVersion: _Optional[str] = ...) -> None: ...

class DeleteMaterialEvent(_message.Message):
    __slots__ = ("materialId",)
    MATERIALID_FIELD_NUMBER: _ClassVar[int]
    materialId: str
    def __init__(self, materialId: _Optional[str] = ...) -> None: ...

class ChangeVersionEvent(_message.Message):
    __slots__ = ("version", "repairVersion")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REPAIRVERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    repairVersion: int
    def __init__(self, version: _Optional[int] = ..., repairVersion: _Optional[int] = ...) -> None: ...

class ChangeActiveLayerEvent(_message.Message):
    __slots__ = ("activeLayerGuid",)
    ACTIVELAYERGUID_FIELD_NUMBER: _ClassVar[int]
    activeLayerGuid: str
    def __init__(self, activeLayerGuid: _Optional[str] = ...) -> None: ...

class ChangeLastUsedOrientationEvent(_message.Message):
    __slots__ = ("lastUsedOrientation",)
    LASTUSEDORIENTATION_FIELD_NUMBER: _ClassVar[int]
    lastUsedOrientation: _gravi_unity_pb2.TransformTO
    def __init__(self, lastUsedOrientation: _Optional[_Union[_gravi_unity_pb2.TransformTO, _Mapping]] = ...) -> None: ...

class ChangeUserChoseThumbnailOrientationEvent(_message.Message):
    __slots__ = ("userChoseThumbnailOrientation",)
    USERCHOSETHUMBNAILORIENTATION_FIELD_NUMBER: _ClassVar[int]
    userChoseThumbnailOrientation: _gravi_unity_pb2.ThumbnailCameraTO
    def __init__(self, userChoseThumbnailOrientation: _Optional[_Union[_gravi_unity_pb2.ThumbnailCameraTO, _Mapping]] = ...) -> None: ...

class ChangeEnvironmentEvent(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: _gravi_model_pb2.EnvironmentTO
    def __init__(self, environment: _Optional[_Union[_gravi_model_pb2.EnvironmentTO, _Mapping]] = ...) -> None: ...

class ChangeSpatialAnchorInformationEvent(_message.Message):
    __slots__ = ("spatialAnchorInformation",)
    SPATIALANCHORINFORMATION_FIELD_NUMBER: _ClassVar[int]
    spatialAnchorInformation: _sketch_common_pb2.PersistentSpatialAnchorInformation
    def __init__(self, spatialAnchorInformation: _Optional[_Union[_sketch_common_pb2.PersistentSpatialAnchorInformation, _Mapping]] = ...) -> None: ...

class ChangeSectionViewDataEvent(_message.Message):
    __slots__ = ("sectionViewData",)
    SECTIONVIEWDATA_FIELD_NUMBER: _ClassVar[int]
    sectionViewData: _sketch_common_pb2.SectionViewData
    def __init__(self, sectionViewData: _Optional[_Union[_sketch_common_pb2.SectionViewData, _Mapping]] = ...) -> None: ...

class CreateAssetEvent(_message.Message):
    __slots__ = ("asset",)
    ASSET_FIELD_NUMBER: _ClassVar[int]
    asset: _asset_pb2.AssetModel
    def __init__(self, asset: _Optional[_Union[_asset_pb2.AssetModel, _Mapping]] = ...) -> None: ...

class DeleteAssetEvent(_message.Message):
    __slots__ = ("asset",)
    ASSET_FIELD_NUMBER: _ClassVar[int]
    asset: _asset_pb2.AssetModel
    def __init__(self, asset: _Optional[_Union[_asset_pb2.AssetModel, _Mapping]] = ...) -> None: ...

class SketchStateChangeEvent(_message.Message):
    __slots__ = ("sketchActionEvent", "updateMaterialEvent", "deleteMaterialEvent", "changeLayerEvent", "addLayerEvent", "modifyLayerEvent", "deleteLayerEvent", "groupObjectsEvent", "ungroupObjectsEvent", "convertToSubDEvent", "mergeSubDObjectsEvent", "revertSubDConversionEvent", "addImportedGroupEvent", "modifyLayerGroupEvent", "changeVersionEvent", "changeActiveLayerEvent", "changeLastUsedOrientationEvent", "changeUserChoseThumbnailOrientationEvent", "changeEnvironmentEvent", "changeSpatialAnchorInformationEvent", "changeSectionViewDataEvent", "createAssetEvent", "deleteAssetEvent")
    SKETCHACTIONEVENT_FIELD_NUMBER: _ClassVar[int]
    UPDATEMATERIALEVENT_FIELD_NUMBER: _ClassVar[int]
    DELETEMATERIALEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGELAYEREVENT_FIELD_NUMBER: _ClassVar[int]
    ADDLAYEREVENT_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYEREVENT_FIELD_NUMBER: _ClassVar[int]
    DELETELAYEREVENT_FIELD_NUMBER: _ClassVar[int]
    GROUPOBJECTSEVENT_FIELD_NUMBER: _ClassVar[int]
    UNGROUPOBJECTSEVENT_FIELD_NUMBER: _ClassVar[int]
    CONVERTTOSUBDEVENT_FIELD_NUMBER: _ClassVar[int]
    MERGESUBDOBJECTSEVENT_FIELD_NUMBER: _ClassVar[int]
    REVERTSUBDCONVERSIONEVENT_FIELD_NUMBER: _ClassVar[int]
    ADDIMPORTEDGROUPEVENT_FIELD_NUMBER: _ClassVar[int]
    MODIFYLAYERGROUPEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGEVERSIONEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGEACTIVELAYEREVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGELASTUSEDORIENTATIONEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGEUSERCHOSETHUMBNAILORIENTATIONEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGEENVIRONMENTEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGESPATIALANCHORINFORMATIONEVENT_FIELD_NUMBER: _ClassVar[int]
    CHANGESECTIONVIEWDATAEVENT_FIELD_NUMBER: _ClassVar[int]
    CREATEASSETEVENT_FIELD_NUMBER: _ClassVar[int]
    DELETEASSETEVENT_FIELD_NUMBER: _ClassVar[int]
    sketchActionEvent: _cosketch_rpc_pb2.SketchActionRequest
    updateMaterialEvent: _cosketch_rpc_pb2.UpdateMaterialRequest
    deleteMaterialEvent: DeleteMaterialEvent
    changeLayerEvent: _cosketch_rpc_pb2.ChangeLayerRequest
    addLayerEvent: _cosketch_rpc_pb2.AddLayerRequest
    modifyLayerEvent: _cosketch_rpc_pb2.ModifyLayerRequest
    deleteLayerEvent: _cosketch_rpc_pb2.DeleteLayerRequest
    groupObjectsEvent: _cosketch_rpc_pb2.GroupingObjectsRequest
    ungroupObjectsEvent: _cosketch_rpc_pb2.UnGroupObjectsRequest
    convertToSubDEvent: _cosketch_rpc_pb2.ConvertToSubDRequest
    mergeSubDObjectsEvent: _cosketch_rpc_pb2.MergeSubDObjectsRequest
    revertSubDConversionEvent: _cosketch_rpc_pb2.ReverseSubDConversionRequest
    addImportedGroupEvent: _cosketch_rpc_pb2.AddImportedGroupRequest
    modifyLayerGroupEvent: _cosketch_rpc_pb2.ModifyLayerGroupRequest
    changeVersionEvent: ChangeVersionEvent
    changeActiveLayerEvent: ChangeActiveLayerEvent
    changeLastUsedOrientationEvent: ChangeLastUsedOrientationEvent
    changeUserChoseThumbnailOrientationEvent: ChangeUserChoseThumbnailOrientationEvent
    changeEnvironmentEvent: ChangeEnvironmentEvent
    changeSpatialAnchorInformationEvent: ChangeSpatialAnchorInformationEvent
    changeSectionViewDataEvent: ChangeSectionViewDataEvent
    createAssetEvent: CreateAssetEvent
    deleteAssetEvent: DeleteAssetEvent
    def __init__(self, sketchActionEvent: _Optional[_Union[_cosketch_rpc_pb2.SketchActionRequest, _Mapping]] = ..., updateMaterialEvent: _Optional[_Union[_cosketch_rpc_pb2.UpdateMaterialRequest, _Mapping]] = ..., deleteMaterialEvent: _Optional[_Union[DeleteMaterialEvent, _Mapping]] = ..., changeLayerEvent: _Optional[_Union[_cosketch_rpc_pb2.ChangeLayerRequest, _Mapping]] = ..., addLayerEvent: _Optional[_Union[_cosketch_rpc_pb2.AddLayerRequest, _Mapping]] = ..., modifyLayerEvent: _Optional[_Union[_cosketch_rpc_pb2.ModifyLayerRequest, _Mapping]] = ..., deleteLayerEvent: _Optional[_Union[_cosketch_rpc_pb2.DeleteLayerRequest, _Mapping]] = ..., groupObjectsEvent: _Optional[_Union[_cosketch_rpc_pb2.GroupingObjectsRequest, _Mapping]] = ..., ungroupObjectsEvent: _Optional[_Union[_cosketch_rpc_pb2.UnGroupObjectsRequest, _Mapping]] = ..., convertToSubDEvent: _Optional[_Union[_cosketch_rpc_pb2.ConvertToSubDRequest, _Mapping]] = ..., mergeSubDObjectsEvent: _Optional[_Union[_cosketch_rpc_pb2.MergeSubDObjectsRequest, _Mapping]] = ..., revertSubDConversionEvent: _Optional[_Union[_cosketch_rpc_pb2.ReverseSubDConversionRequest, _Mapping]] = ..., addImportedGroupEvent: _Optional[_Union[_cosketch_rpc_pb2.AddImportedGroupRequest, _Mapping]] = ..., modifyLayerGroupEvent: _Optional[_Union[_cosketch_rpc_pb2.ModifyLayerGroupRequest, _Mapping]] = ..., changeVersionEvent: _Optional[_Union[ChangeVersionEvent, _Mapping]] = ..., changeActiveLayerEvent: _Optional[_Union[ChangeActiveLayerEvent, _Mapping]] = ..., changeLastUsedOrientationEvent: _Optional[_Union[ChangeLastUsedOrientationEvent, _Mapping]] = ..., changeUserChoseThumbnailOrientationEvent: _Optional[_Union[ChangeUserChoseThumbnailOrientationEvent, _Mapping]] = ..., changeEnvironmentEvent: _Optional[_Union[ChangeEnvironmentEvent, _Mapping]] = ..., changeSpatialAnchorInformationEvent: _Optional[_Union[ChangeSpatialAnchorInformationEvent, _Mapping]] = ..., changeSectionViewDataEvent: _Optional[_Union[ChangeSectionViewDataEvent, _Mapping]] = ..., createAssetEvent: _Optional[_Union[CreateAssetEvent, _Mapping]] = ..., deleteAssetEvent: _Optional[_Union[DeleteAssetEvent, _Mapping]] = ...) -> None: ...

class SketchStateUpdate(_message.Message):
    __slots__ = ("updates",)
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[SketchObjectUpdate]
    def __init__(self, updates: _Optional[_Iterable[_Union[SketchObjectUpdate, _Mapping]]] = ...) -> None: ...

class SketchObjectUpdate(_message.Message):
    __slots__ = ("dataId", "stringId", "isDeleted", "overwritePayload", "deltaEncodedPayload")
    DATAID_FIELD_NUMBER: _ClassVar[int]
    STRINGID_FIELD_NUMBER: _ClassVar[int]
    ISDELETED_FIELD_NUMBER: _ClassVar[int]
    OVERWRITEPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    DELTAENCODEDPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    dataId: _sketch_common_pb2.GSDataID
    stringId: str
    isDeleted: bool
    overwritePayload: SketchObjectOverwritePayload
    deltaEncodedPayload: SketchObjectDeltaEncodedPayload
    def __init__(self, dataId: _Optional[_Union[_sketch_common_pb2.GSDataID, _Mapping]] = ..., stringId: _Optional[str] = ..., isDeleted: bool = ..., overwritePayload: _Optional[_Union[SketchObjectOverwritePayload, _Mapping]] = ..., deltaEncodedPayload: _Optional[_Union[SketchObjectDeltaEncodedPayload, _Mapping]] = ...) -> None: ...

class SketchObjectOverwritePayload(_message.Message):
    __slots__ = ("stroke", "layer", "material", "nestedGroup", "metadata", "asset", "strokeLayer", "layerGroup", "strokeGroup")
    STROKE_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    NESTEDGROUP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ASSET_FIELD_NUMBER: _ClassVar[int]
    STROKELAYER_FIELD_NUMBER: _ClassVar[int]
    LAYERGROUP_FIELD_NUMBER: _ClassVar[int]
    STROKEGROUP_FIELD_NUMBER: _ClassVar[int]
    stroke: _sketch_model_pb2.StrokeDataSnapshot
    layer: _layer_pb2.LayerModel
    material: _sketch_common_pb2.DrawMaterial
    nestedGroup: _sketch_gsfile_pb2.NestedGroupRelationship
    metadata: _metadata_pb2.SketchMetadataModel
    asset: _asset_pb2.AssetModel
    strokeLayer: _sketch_model_pb2.StrokeLayerRelationship
    layerGroup: _sketch_common_pb2.NestedLayerRelationship
    strokeGroup: _sketch_model_pb2.StrokeGroupRelationship
    def __init__(self, stroke: _Optional[_Union[_sketch_model_pb2.StrokeDataSnapshot, _Mapping]] = ..., layer: _Optional[_Union[_layer_pb2.LayerModel, _Mapping]] = ..., material: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ..., nestedGroup: _Optional[_Union[_sketch_gsfile_pb2.NestedGroupRelationship, _Mapping]] = ..., metadata: _Optional[_Union[_metadata_pb2.SketchMetadataModel, _Mapping]] = ..., asset: _Optional[_Union[_asset_pb2.AssetModel, _Mapping]] = ..., strokeLayer: _Optional[_Union[_sketch_model_pb2.StrokeLayerRelationship, _Mapping]] = ..., layerGroup: _Optional[_Union[_sketch_common_pb2.NestedLayerRelationship, _Mapping]] = ..., strokeGroup: _Optional[_Union[_sketch_model_pb2.StrokeGroupRelationship, _Mapping]] = ...) -> None: ...

class SketchObjectDeltaEncodedPayload(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
