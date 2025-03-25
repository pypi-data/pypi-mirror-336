from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocalLang(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    English: _ClassVar[LocalLang]
    Chinese: _ClassVar[LocalLang]
    Spanish: _ClassVar[LocalLang]
    Japanese: _ClassVar[LocalLang]
    Korean: _ClassVar[LocalLang]
    German: _ClassVar[LocalLang]
    Italian: _ClassVar[LocalLang]
    French: _ClassVar[LocalLang]
English: LocalLang
Chinese: LocalLang
Spanish: LocalLang
Japanese: LocalLang
Korean: LocalLang
German: LocalLang
Italian: LocalLang
French: LocalLang

class Localization(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: LocalEntry
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[LocalEntry, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[str, LocalEntry]
    def __init__(self, entries: _Optional[_Mapping[str, LocalEntry]] = ...) -> None: ...

class LocalEntry(_message.Message):
    __slots__ = ("spacing", "colour", "sectionLabel", "langs")
    class LangsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: LangTranslation
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[LangTranslation, _Mapping]] = ...) -> None: ...
    SPACING_FIELD_NUMBER: _ClassVar[int]
    COLOUR_FIELD_NUMBER: _ClassVar[int]
    SECTIONLABEL_FIELD_NUMBER: _ClassVar[int]
    LANGS_FIELD_NUMBER: _ClassVar[int]
    spacing: float
    colour: str
    sectionLabel: str
    langs: _containers.MessageMap[int, LangTranslation]
    def __init__(self, spacing: _Optional[float] = ..., colour: _Optional[str] = ..., sectionLabel: _Optional[str] = ..., langs: _Optional[_Mapping[int, LangTranslation]] = ...) -> None: ...

class LangTranslation(_message.Message):
    __slots__ = ("lang", "font", "pt", "text")
    LANG_FIELD_NUMBER: _ClassVar[int]
    FONT_FIELD_NUMBER: _ClassVar[int]
    PT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    lang: LocalLang
    font: str
    pt: int
    text: str
    def __init__(self, lang: _Optional[_Union[LocalLang, str]] = ..., font: _Optional[str] = ..., pt: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...
