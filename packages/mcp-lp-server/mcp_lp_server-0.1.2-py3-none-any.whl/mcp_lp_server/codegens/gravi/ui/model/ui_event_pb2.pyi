import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UIWidgetScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[UIWidgetScope]
    Global: _ClassVar[UIWidgetScope]
    Lobby: _ClassVar[UIWidgetScope]
    Sketch: _ClassVar[UIWidgetScope]
Unknown: UIWidgetScope
Global: UIWidgetScope
Lobby: UIWidgetScope
Sketch: UIWidgetScope

class UIWidgetSId(_message.Message):
    __slots__ = ("clientId", "widgetId")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    WIDGETID_FIELD_NUMBER: _ClassVar[int]
    clientId: int
    widgetId: str
    def __init__(self, clientId: _Optional[int] = ..., widgetId: _Optional[str] = ...) -> None: ...

class UIWidgetEventDef(_message.Message):
    __slots__ = ("widgetSId", "eventName")
    WIDGETSID_FIELD_NUMBER: _ClassVar[int]
    EVENTNAME_FIELD_NUMBER: _ClassVar[int]
    widgetSId: UIWidgetSId
    eventName: str
    def __init__(self, widgetSId: _Optional[_Union[UIWidgetSId, _Mapping]] = ..., eventName: _Optional[str] = ...) -> None: ...
