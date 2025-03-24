import gs_options_pb2 as _gs_options_pb2
from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.rpc.model.common import sketch_common_pb2 as _sketch_common_pb2
from gravi.rpc.model import sketch_model_pb2 as _sketch_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DocRevision(_message.Message):
    __slots__ = ("id", "name", "createdOn", "modifiedOn")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    MODIFIEDON_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    createdOn: int
    modifiedOn: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., createdOn: _Optional[int] = ..., modifiedOn: _Optional[int] = ...) -> None: ...

class ListDocRevisionsRequest(_message.Message):
    __slots__ = ("docId", "pageSize", "pageToken")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    docId: str
    pageSize: int
    pageToken: str
    def __init__(self, docId: _Optional[str] = ..., pageSize: _Optional[int] = ..., pageToken: _Optional[str] = ...) -> None: ...

class ListDocRevisionsResponse(_message.Message):
    __slots__ = ("revisions", "nextPageToken")
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    revisions: _containers.RepeatedCompositeFieldContainer[DocRevision]
    nextPageToken: str
    def __init__(self, revisions: _Optional[_Iterable[_Union[DocRevision, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...
