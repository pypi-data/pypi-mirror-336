import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AccountTypeUnknown: _ClassVar[AccountType]
    AccountTypeIndividual: _ClassVar[AccountType]
    AccountTypeOrg: _ClassVar[AccountType]
AccountTypeUnknown: AccountType
AccountTypeIndividual: AccountType
AccountTypeOrg: AccountType

class GetLoggedInUserRequestV2(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLoggedInUserResponseV2(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _gravi_model_pb2.UserTO
    def __init__(self, user: _Optional[_Union[_gravi_model_pb2.UserTO, _Mapping]] = ...) -> None: ...
