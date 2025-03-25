from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParquetEnumField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    None: _ClassVar[ParquetEnumField]
    Name: _ClassVar[ParquetEnumField]
    Value: _ClassVar[ParquetEnumField]
None: ParquetEnumField
Name: ParquetEnumField
Value: ParquetEnumField
STRUCT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
struct_message: _descriptor.FieldDescriptor
IMMUTABLE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
immutable_message: _descriptor.FieldDescriptor
IMMUTABLE_JAVA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
immutable_java_message: _descriptor.FieldDescriptor
DELTA_CODE_FIELD_NUMBER: _ClassVar[int]
delta_code: _descriptor.FieldDescriptor
PARQUET_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
parquet_table_name: _descriptor.FieldDescriptor
PARQUET_TABLE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
parquet_table_options: _descriptor.FieldDescriptor
MAP_KEY_FIELD_NUMBER: _ClassVar[int]
map_key: _descriptor.FieldDescriptor
READONLY_INTERFACE_FIELD_NUMBER: _ClassVar[int]
readonly_interface: _descriptor.FieldDescriptor
PROTO_ENCODING_FOR_DELTA_FIELD_NUMBER: _ClassVar[int]
proto_encoding_for_delta: _descriptor.FieldDescriptor
PARQUET_TYPE_FIELD_NUMBER: _ClassVar[int]
parquet_type: _descriptor.FieldDescriptor
STRING_RULES_FIELD_NUMBER: _ClassVar[int]
string_rules: _descriptor.FieldDescriptor
MESSAGE_RULES_FIELD_NUMBER: _ClassVar[int]
message_rules: _descriptor.FieldDescriptor
ENUM_RULES_FIELD_NUMBER: _ClassVar[int]
enum_rules: _descriptor.FieldDescriptor
BYTES_RULES_FIELD_NUMBER: _ClassVar[int]
bytes_rules: _descriptor.FieldDescriptor
TAGGED_MESSAGE_FIELD_FIELD_NUMBER: _ClassVar[int]
tagged_message_field: _descriptor.FieldDescriptor
TAGGED_MESSAGE_FIELD_NUMBER: _ClassVar[int]
tagged_message: _descriptor.FieldDescriptor

class ParquetFieldId(_message.Message):
    __slots__ = ("name", "enum_field")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_FIELD_NUMBER: _ClassVar[int]
    name: str
    enum_field: ParquetEnumField
    def __init__(self, name: _Optional[str] = ..., enum_field: _Optional[_Union[ParquetEnumField, str]] = ...) -> None: ...

class ParquetTableOptions(_message.Message):
    __slots__ = ("enable_parquet_table_nonstandard_naming_annotations", "parquet_table_synthetic_name_field_binding", "analytics_destination_table_name")
    ENABLE_PARQUET_TABLE_NONSTANDARD_NAMING_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    PARQUET_TABLE_SYNTHETIC_NAME_FIELD_BINDING_FIELD_NUMBER: _ClassVar[int]
    ANALYTICS_DESTINATION_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    enable_parquet_table_nonstandard_naming_annotations: bool
    parquet_table_synthetic_name_field_binding: ParquetFieldId
    analytics_destination_table_name: str
    def __init__(self, enable_parquet_table_nonstandard_naming_annotations: bool = ..., parquet_table_synthetic_name_field_binding: _Optional[_Union[ParquetFieldId, _Mapping]] = ..., analytics_destination_table_name: _Optional[str] = ...) -> None: ...

class ParquetType(_message.Message):
    __slots__ = ("ignore_field", "int64_timestamp_millis", "int32_encoded", "string_encoded", "int_encoded_enum_name", "int_encoded_enum_go_package", "parquet_name", "go_name", "enum_value_go_name", "enum_name_go_name", "tag_field", "tag_value", "field_annotations", "expect_field_overlap", "qualified_fallback_proto_field", "disable_system_encoding", "enum_value_parquet_name", "enum_name_parquet_name", "map_encoded_repeated")
    class FieldAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ParquetType
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ParquetType, _Mapping]] = ...) -> None: ...
    IGNORE_FIELD_FIELD_NUMBER: _ClassVar[int]
    INT64_TIMESTAMP_MILLIS_FIELD_NUMBER: _ClassVar[int]
    INT32_ENCODED_FIELD_NUMBER: _ClassVar[int]
    STRING_ENCODED_FIELD_NUMBER: _ClassVar[int]
    INT_ENCODED_ENUM_NAME_FIELD_NUMBER: _ClassVar[int]
    INT_ENCODED_ENUM_GO_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    PARQUET_NAME_FIELD_NUMBER: _ClassVar[int]
    GO_NAME_FIELD_NUMBER: _ClassVar[int]
    ENUM_VALUE_GO_NAME_FIELD_NUMBER: _ClassVar[int]
    ENUM_NAME_GO_NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_FIELD_NUMBER: _ClassVar[int]
    TAG_VALUE_FIELD_NUMBER: _ClassVar[int]
    FIELD_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    EXPECT_FIELD_OVERLAP_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_FALLBACK_PROTO_FIELD_FIELD_NUMBER: _ClassVar[int]
    DISABLE_SYSTEM_ENCODING_FIELD_NUMBER: _ClassVar[int]
    ENUM_VALUE_PARQUET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENUM_NAME_PARQUET_NAME_FIELD_NUMBER: _ClassVar[int]
    MAP_ENCODED_REPEATED_FIELD_NUMBER: _ClassVar[int]
    ignore_field: bool
    int64_timestamp_millis: bool
    int32_encoded: bool
    string_encoded: bool
    int_encoded_enum_name: str
    int_encoded_enum_go_package: str
    parquet_name: str
    go_name: str
    enum_value_go_name: str
    enum_name_go_name: str
    tag_field: str
    tag_value: str
    field_annotations: _containers.MessageMap[str, ParquetType]
    expect_field_overlap: bool
    qualified_fallback_proto_field: str
    disable_system_encoding: bool
    enum_value_parquet_name: str
    enum_name_parquet_name: str
    map_encoded_repeated: bool
    def __init__(self, ignore_field: bool = ..., int64_timestamp_millis: bool = ..., int32_encoded: bool = ..., string_encoded: bool = ..., int_encoded_enum_name: _Optional[str] = ..., int_encoded_enum_go_package: _Optional[str] = ..., parquet_name: _Optional[str] = ..., go_name: _Optional[str] = ..., enum_value_go_name: _Optional[str] = ..., enum_name_go_name: _Optional[str] = ..., tag_field: _Optional[str] = ..., tag_value: _Optional[str] = ..., field_annotations: _Optional[_Mapping[str, ParquetType]] = ..., expect_field_overlap: bool = ..., qualified_fallback_proto_field: _Optional[str] = ..., disable_system_encoding: bool = ..., enum_value_parquet_name: _Optional[str] = ..., enum_name_parquet_name: _Optional[str] = ..., map_encoded_repeated: bool = ...) -> None: ...

class StringRules(_message.Message):
    __slots__ = ("not_null_or_empty", "regex_pattern", "max_length", "is_valid_email")
    NOT_NULL_OR_EMPTY_FIELD_NUMBER: _ClassVar[int]
    REGEX_PATTERN_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_EMAIL_FIELD_NUMBER: _ClassVar[int]
    not_null_or_empty: bool
    regex_pattern: str
    max_length: int
    is_valid_email: bool
    def __init__(self, not_null_or_empty: bool = ..., regex_pattern: _Optional[str] = ..., max_length: _Optional[int] = ..., is_valid_email: bool = ...) -> None: ...

class MessageRules(_message.Message):
    __slots__ = ("not_null_or_default",)
    NOT_NULL_OR_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    not_null_or_default: bool
    def __init__(self, not_null_or_default: bool = ...) -> None: ...

class EnumRules(_message.Message):
    __slots__ = ("not_null_or_invalid", "not_null_or_default", "not_unrecognized")
    NOT_NULL_OR_INVALID_FIELD_NUMBER: _ClassVar[int]
    NOT_NULL_OR_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    NOT_UNRECOGNIZED_FIELD_NUMBER: _ClassVar[int]
    not_null_or_invalid: bool
    not_null_or_default: bool
    not_unrecognized: bool
    def __init__(self, not_null_or_invalid: bool = ..., not_null_or_default: bool = ..., not_unrecognized: bool = ...) -> None: ...

class BytesRules(_message.Message):
    __slots__ = ("not_null_or_empty",)
    NOT_NULL_OR_EMPTY_FIELD_NUMBER: _ClassVar[int]
    not_null_or_empty: bool
    def __init__(self, not_null_or_empty: bool = ...) -> None: ...

class TaggedMessageSpec(_message.Message):
    __slots__ = ("enum_tag", "tagged_rpc_field_number")
    ENUM_TAG_FIELD_NUMBER: _ClassVar[int]
    TAGGED_RPC_FIELD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    enum_tag: str
    tagged_rpc_field_number: int
    def __init__(self, enum_tag: _Optional[str] = ..., tagged_rpc_field_number: _Optional[int] = ...) -> None: ...

class TaggedMessageFieldSpec(_message.Message):
    __slots__ = ("tag",)
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: int
    def __init__(self, tag: _Optional[int] = ...) -> None: ...
