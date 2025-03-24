from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateObjectResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateObjectResponseUnknown: _ClassVar[CreateObjectResponseCode]
    CreateObjectResponseSuccess: _ClassVar[CreateObjectResponseCode]
    CreateObjectResponseFailure: _ClassVar[CreateObjectResponseCode]

class ModifyObjectResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ModifyObjectResponseUnknown: _ClassVar[ModifyObjectResponseCode]
    ModifyObjectResponseSuccess: _ClassVar[ModifyObjectResponseCode]
    ModifyObjectResponseFailure: _ClassVar[ModifyObjectResponseCode]

class DeleteObjectResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeleteObjectResponseUnknown: _ClassVar[DeleteObjectResponseCode]
    DeleteObjectResponseSuccess: _ClassVar[DeleteObjectResponseCode]
    DeleteObjectResponseFailure: _ClassVar[DeleteObjectResponseCode]
CreateObjectResponseUnknown: CreateObjectResponseCode
CreateObjectResponseSuccess: CreateObjectResponseCode
CreateObjectResponseFailure: CreateObjectResponseCode
ModifyObjectResponseUnknown: ModifyObjectResponseCode
ModifyObjectResponseSuccess: ModifyObjectResponseCode
ModifyObjectResponseFailure: ModifyObjectResponseCode
DeleteObjectResponseUnknown: DeleteObjectResponseCode
DeleteObjectResponseSuccess: DeleteObjectResponseCode
DeleteObjectResponseFailure: DeleteObjectResponseCode

class CommandRequest(_message.Message):
    __slots__ = ("getSceneInfoRequest", "createObjectRequest", "modifyObjectRequest", "deleteObjectRequest", "setMaterialRequest")
    GETSCENEINFOREQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATEOBJECTREQUEST_FIELD_NUMBER: _ClassVar[int]
    MODIFYOBJECTREQUEST_FIELD_NUMBER: _ClassVar[int]
    DELETEOBJECTREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETMATERIALREQUEST_FIELD_NUMBER: _ClassVar[int]
    getSceneInfoRequest: GetSceneInfoRequest
    createObjectRequest: CreateObjectRequest
    modifyObjectRequest: ModifyObjectRequest
    deleteObjectRequest: DeleteObjectRequest
    setMaterialRequest: SetMaterialRequest
    def __init__(self, getSceneInfoRequest: _Optional[_Union[GetSceneInfoRequest, _Mapping]] = ..., createObjectRequest: _Optional[_Union[CreateObjectRequest, _Mapping]] = ..., modifyObjectRequest: _Optional[_Union[ModifyObjectRequest, _Mapping]] = ..., deleteObjectRequest: _Optional[_Union[DeleteObjectRequest, _Mapping]] = ..., setMaterialRequest: _Optional[_Union[SetMaterialRequest, _Mapping]] = ...) -> None: ...

class CommandResponse(_message.Message):
    __slots__ = ("getSceneInfoResponse", "createObjectResponse", "modifyObjectResponse", "deleteObjectResponse", "setMaterialResponse")
    GETSCENEINFORESPONSE_FIELD_NUMBER: _ClassVar[int]
    CREATEOBJECTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    MODIFYOBJECTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    DELETEOBJECTRESPONSE_FIELD_NUMBER: _ClassVar[int]
    SETMATERIALRESPONSE_FIELD_NUMBER: _ClassVar[int]
    getSceneInfoResponse: GetSceneInfoResponse
    createObjectResponse: CreateObjectResponse
    modifyObjectResponse: ModifyObjectResponse
    deleteObjectResponse: DeleteObjectResponse
    setMaterialResponse: SetMaterialResponse
    def __init__(self, getSceneInfoResponse: _Optional[_Union[GetSceneInfoResponse, _Mapping]] = ..., createObjectResponse: _Optional[_Union[CreateObjectResponse, _Mapping]] = ..., modifyObjectResponse: _Optional[_Union[ModifyObjectResponse, _Mapping]] = ..., deleteObjectResponse: _Optional[_Union[DeleteObjectResponse, _Mapping]] = ..., setMaterialResponse: _Optional[_Union[SetMaterialResponse, _Mapping]] = ...) -> None: ...

class GetSceneInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SceneInfo(_message.Message):
    __slots__ = ("name", "materialCount", "objects")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MATERIALCOUNT_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    materialCount: int
    objects: _containers.RepeatedCompositeFieldContainer[ObjectInfo]
    def __init__(self, name: _Optional[str] = ..., materialCount: _Optional[int] = ..., objects: _Optional[_Iterable[_Union[ObjectInfo, _Mapping]]] = ...) -> None: ...

class ObjectInfo(_message.Message):
    __slots__ = ("objectId", "name", "Shape", "PositionsX", "PositionsY", "PositionsZ", "RotationX", "RotationY", "RotationZ", "RotationW", "ScaleX", "ScaleY", "ScaleZ", "Visible")
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    POSITIONSX_FIELD_NUMBER: _ClassVar[int]
    POSITIONSY_FIELD_NUMBER: _ClassVar[int]
    POSITIONSZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONX_FIELD_NUMBER: _ClassVar[int]
    ROTATIONY_FIELD_NUMBER: _ClassVar[int]
    ROTATIONZ_FIELD_NUMBER: _ClassVar[int]
    ROTATIONW_FIELD_NUMBER: _ClassVar[int]
    SCALEX_FIELD_NUMBER: _ClassVar[int]
    SCALEY_FIELD_NUMBER: _ClassVar[int]
    SCALEZ_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    name: str
    Shape: _sketch_common_pb2.BrushShape
    PositionsX: float
    PositionsY: float
    PositionsZ: float
    RotationX: float
    RotationY: float
    RotationZ: float
    RotationW: float
    ScaleX: float
    ScaleY: float
    ScaleZ: float
    Visible: bool
    def __init__(self, objectId: _Optional[str] = ..., name: _Optional[str] = ..., Shape: _Optional[_Union[_sketch_common_pb2.BrushShape, str]] = ..., PositionsX: _Optional[float] = ..., PositionsY: _Optional[float] = ..., PositionsZ: _Optional[float] = ..., RotationX: _Optional[float] = ..., RotationY: _Optional[float] = ..., RotationZ: _Optional[float] = ..., RotationW: _Optional[float] = ..., ScaleX: _Optional[float] = ..., ScaleY: _Optional[float] = ..., ScaleZ: _Optional[float] = ..., Visible: bool = ...) -> None: ...

class GetSceneInfoResponse(_message.Message):
    __slots__ = ("sceneInfo",)
    SCENEINFO_FIELD_NUMBER: _ClassVar[int]
    sceneInfo: SceneInfo
    def __init__(self, sceneInfo: _Optional[_Union[SceneInfo, _Mapping]] = ...) -> None: ...

class GetObjectInfoRequest(_message.Message):
    __slots__ = ("objectId",)
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    def __init__(self, objectId: _Optional[str] = ...) -> None: ...

class GetObjectInfoResponse(_message.Message):
    __slots__ = ("objectInfo",)
    OBJECTINFO_FIELD_NUMBER: _ClassVar[int]
    objectInfo: ObjectInfo
    def __init__(self, objectInfo: _Optional[_Union[ObjectInfo, _Mapping]] = ...) -> None: ...

class CreateObjectRequest(_message.Message):
    __slots__ = ("objectInfo", "torusParameters")
    OBJECTINFO_FIELD_NUMBER: _ClassVar[int]
    TORUSPARAMETERS_FIELD_NUMBER: _ClassVar[int]
    objectInfo: ObjectInfo
    torusParameters: TorusParameters
    def __init__(self, objectInfo: _Optional[_Union[ObjectInfo, _Mapping]] = ..., torusParameters: _Optional[_Union[TorusParameters, _Mapping]] = ...) -> None: ...

class TorusParameters(_message.Message):
    __slots__ = ("torusRadius", "coneRadius", "torusSegments", "coneSegments", "slice")
    TORUSRADIUS_FIELD_NUMBER: _ClassVar[int]
    CONERADIUS_FIELD_NUMBER: _ClassVar[int]
    TORUSSEGMENTS_FIELD_NUMBER: _ClassVar[int]
    CONESEGMENTS_FIELD_NUMBER: _ClassVar[int]
    SLICE_FIELD_NUMBER: _ClassVar[int]
    torusRadius: float
    coneRadius: float
    torusSegments: int
    coneSegments: int
    slice: float
    def __init__(self, torusRadius: _Optional[float] = ..., coneRadius: _Optional[float] = ..., torusSegments: _Optional[int] = ..., coneSegments: _Optional[int] = ..., slice: _Optional[float] = ...) -> None: ...

class CreateObjectResponse(_message.Message):
    __slots__ = ("objectId", "errorCode")
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    errorCode: CreateObjectResponseCode
    def __init__(self, objectId: _Optional[str] = ..., errorCode: _Optional[_Union[CreateObjectResponseCode, str]] = ...) -> None: ...

class ModifyObjectRequest(_message.Message):
    __slots__ = ("objectInfo",)
    OBJECTINFO_FIELD_NUMBER: _ClassVar[int]
    objectInfo: ObjectInfo
    def __init__(self, objectInfo: _Optional[_Union[ObjectInfo, _Mapping]] = ...) -> None: ...

class ModifyObjectResponse(_message.Message):
    __slots__ = ("objectId", "errorCode")
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    errorCode: ModifyObjectResponseCode
    def __init__(self, objectId: _Optional[str] = ..., errorCode: _Optional[_Union[ModifyObjectResponseCode, str]] = ...) -> None: ...

class DeleteObjectRequest(_message.Message):
    __slots__ = ("objectId",)
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    def __init__(self, objectId: _Optional[str] = ...) -> None: ...

class DeleteObjectResponse(_message.Message):
    __slots__ = ("objectId", "errorCode")
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    objectId: str
    errorCode: DeleteObjectResponseCode
    def __init__(self, objectId: _Optional[str] = ..., errorCode: _Optional[_Union[DeleteObjectResponseCode, str]] = ...) -> None: ...

class SetMaterialRequest(_message.Message):
    __slots__ = ("material",)
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    material: _sketch_common_pb2.DrawMaterial
    def __init__(self, material: _Optional[_Union[_sketch_common_pb2.DrawMaterial, _Mapping]] = ...) -> None: ...

class SetMaterialResponse(_message.Message):
    __slots__ = ("materialId",)
    MATERIALID_FIELD_NUMBER: _ClassVar[int]
    materialId: str
    def __init__(self, materialId: _Optional[str] = ...) -> None: ...
