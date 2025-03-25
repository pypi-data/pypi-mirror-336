import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeneratePairDeviceCodeResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GeneratePairDeviceCodeResponseCodeUnknown: _ClassVar[GeneratePairDeviceCodeResponseCode]
    GeneratePairDeviceCodeResponseCodeSuccess: _ClassVar[GeneratePairDeviceCodeResponseCode]
    GeneratePairDeviceCodeResponseCodeUserAlreadyHasDevicePaired: _ClassVar[GeneratePairDeviceCodeResponseCode]

class GetPairedDeviceResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetPairedDeviceResponseCodeUnknown: _ClassVar[GetPairedDeviceResponseCode]
    GetPairedDeviceResponseCodeDevicePaired: _ClassVar[GetPairedDeviceResponseCode]
    GetPairedDeviceResponseCodeDeviceNotPaired: _ClassVar[GetPairedDeviceResponseCode]

class GetUserFromPairedDeviceIdResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GetUserFromPairedDeviceIdResponseCodeUnknown: _ClassVar[GetUserFromPairedDeviceIdResponseCode]
    GetUserFromPairedDeviceIdResponseCodeDevicePaired: _ClassVar[GetUserFromPairedDeviceIdResponseCode]
    GetUserFromPairedDeviceIdResponseCodeDeviceNotPaired: _ClassVar[GetUserFromPairedDeviceIdResponseCode]

class RevokeDevicePairingResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RevokeDevicePairingResponseCodeUnknown: _ClassVar[RevokeDevicePairingResponseCode]
    RevokeDevicePairingResponseCodeSuccess: _ClassVar[RevokeDevicePairingResponseCode]
    RevokeDevicePairingResponseCodeDeviceNotPaired: _ClassVar[RevokeDevicePairingResponseCode]
GeneratePairDeviceCodeResponseCodeUnknown: GeneratePairDeviceCodeResponseCode
GeneratePairDeviceCodeResponseCodeSuccess: GeneratePairDeviceCodeResponseCode
GeneratePairDeviceCodeResponseCodeUserAlreadyHasDevicePaired: GeneratePairDeviceCodeResponseCode
GetPairedDeviceResponseCodeUnknown: GetPairedDeviceResponseCode
GetPairedDeviceResponseCodeDevicePaired: GetPairedDeviceResponseCode
GetPairedDeviceResponseCodeDeviceNotPaired: GetPairedDeviceResponseCode
GetUserFromPairedDeviceIdResponseCodeUnknown: GetUserFromPairedDeviceIdResponseCode
GetUserFromPairedDeviceIdResponseCodeDevicePaired: GetUserFromPairedDeviceIdResponseCode
GetUserFromPairedDeviceIdResponseCodeDeviceNotPaired: GetUserFromPairedDeviceIdResponseCode
RevokeDevicePairingResponseCodeUnknown: RevokeDevicePairingResponseCode
RevokeDevicePairingResponseCodeSuccess: RevokeDevicePairingResponseCode
RevokeDevicePairingResponseCodeDeviceNotPaired: RevokeDevicePairingResponseCode

class GeneratePairDeviceCodeRequest(_message.Message):
    __slots__ = ("userId", "orgId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    orgId: str
    def __init__(self, userId: _Optional[str] = ..., orgId: _Optional[str] = ...) -> None: ...

class GeneratePairDeviceCodeResponse(_message.Message):
    __slots__ = ("pairingCode", "generatePairDeviceCodeResponseCode")
    PAIRINGCODE_FIELD_NUMBER: _ClassVar[int]
    GENERATEPAIRDEVICECODERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    pairingCode: str
    generatePairDeviceCodeResponseCode: GeneratePairDeviceCodeResponseCode
    def __init__(self, pairingCode: _Optional[str] = ..., generatePairDeviceCodeResponseCode: _Optional[_Union[GeneratePairDeviceCodeResponseCode, str]] = ...) -> None: ...

class PairDeviceRequest(_message.Message):
    __slots__ = ("pairingCode",)
    PAIRINGCODE_FIELD_NUMBER: _ClassVar[int]
    pairingCode: str
    def __init__(self, pairingCode: _Optional[str] = ...) -> None: ...

class GetPairedDeviceRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class GetPairedDeviceResponse(_message.Message):
    __slots__ = ("deviceId", "getPairedDeviceResponseCode")
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    GETPAIREDDEVICERESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    deviceId: str
    getPairedDeviceResponseCode: GetPairedDeviceResponseCode
    def __init__(self, deviceId: _Optional[str] = ..., getPairedDeviceResponseCode: _Optional[_Union[GetPairedDeviceResponseCode, str]] = ...) -> None: ...

class GetUserFromPairedDeviceIdRequest(_message.Message):
    __slots__ = ("deviceId",)
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    deviceId: str
    def __init__(self, deviceId: _Optional[str] = ...) -> None: ...

class GetUserFromPairedDeviceIdResponse(_message.Message):
    __slots__ = ("userEmail", "getUserFromPairedDeviceIdResponseCode")
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    GETUSERFROMPAIREDDEVICEIDRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    userEmail: str
    getUserFromPairedDeviceIdResponseCode: GetUserFromPairedDeviceIdResponseCode
    def __init__(self, userEmail: _Optional[str] = ..., getUserFromPairedDeviceIdResponseCode: _Optional[_Union[GetUserFromPairedDeviceIdResponseCode, str]] = ...) -> None: ...

class RevokeDevicePairingRequest(_message.Message):
    __slots__ = ("userId", "orgId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    orgId: str
    def __init__(self, userId: _Optional[str] = ..., orgId: _Optional[str] = ...) -> None: ...

class RevokeDevicePairingResponse(_message.Message):
    __slots__ = ("RevokeDevicePairingResponseCode",)
    REVOKEDEVICEPAIRINGRESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    RevokeDevicePairingResponseCode: RevokeDevicePairingResponseCode
    def __init__(self, RevokeDevicePairingResponseCode: _Optional[_Union[RevokeDevicePairingResponseCode, str]] = ...) -> None: ...
