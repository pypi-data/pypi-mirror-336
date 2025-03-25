import gs_options_pb2 as _gs_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OptionalDouble(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: float
    set: bool
    def __init__(self, value: _Optional[float] = ..., set: bool = ...) -> None: ...

class OptionalFloat(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: float
    set: bool
    def __init__(self, value: _Optional[float] = ..., set: bool = ...) -> None: ...

class OptionalInt64(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: int
    set: bool
    def __init__(self, value: _Optional[int] = ..., set: bool = ...) -> None: ...

class OptionalUInt64(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: int
    set: bool
    def __init__(self, value: _Optional[int] = ..., set: bool = ...) -> None: ...

class OptionalInt32(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: int
    set: bool
    def __init__(self, value: _Optional[int] = ..., set: bool = ...) -> None: ...

class OptionalUInt32(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: int
    set: bool
    def __init__(self, value: _Optional[int] = ..., set: bool = ...) -> None: ...

class OptionalBool(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: bool
    set: bool
    def __init__(self, value: bool = ..., set: bool = ...) -> None: ...

class OptionalString(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: str
    set: bool
    def __init__(self, value: _Optional[str] = ..., set: bool = ...) -> None: ...

class OptionalBytes(_message.Message):
    __slots__ = ("value", "set")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    set: bool
    def __init__(self, value: _Optional[bytes] = ..., set: bool = ...) -> None: ...
